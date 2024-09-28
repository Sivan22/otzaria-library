import csv
import requests
from bs4 import BeautifulSoup
import re
import os
import html

def sanitize_filename(filename):
    sanitized_filename = re.sub(r'[\/:*?<>|]', '', filename).replace('"', "''").replace('_', ' ')
    return sanitized_filename

def adjust_html_tag_spaces(html):
    start_pattern = r'(<[^/<>]+?>)([ ]+)' 
    end_pattern = r'([ ]+)(</[^<>]+?>)' 
    # Move spaces from inside the closing tag to after the tag
    while re.findall(end_pattern , html):
        html = re.sub(end_pattern, r'\2\1', html)

    # Move spaces from the beginning of tags to before the tags
    while re.findall(start_pattern, html):
        html = re.sub(start_pattern , r'\2\1', html)
    # Clean up any double spaces created by the previous step
    html = re.sub(r'[ ]{2,}', ' ', html)

    return html
    
def extract_html_info(html):
    # Parse the HTML content
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract the title text
    title = soup.title.string if soup.title else None
    
    # Extract the author from the meta tag
    author = None
    author_meta = soup.find('meta', attrs={'name': 'author'})
    if author_meta:
        author = author_meta.get('content')
    
    # Extract the body HTML
    body = str(soup.body) if soup.body else None
    
    return title, author, body

def process_body_html(body_html):
    body_html = body_html.replace("\n", " ")
    supported_tags = {
    "a", "abbr", "acronym", "address", "article", "aside", "audio", "b", "bdi", "bdo", "big",
    "blockquote", "br", "caption", "cite", "code", "data", "dd", "del", "details", "dfn", "dl", "dt", "em", "figcaption", "figure", "footer", "font", "h1", "h2", "h3", "h4",
    "h5", "h6", "header", "hr", "i", "iframe", "img", "ins", "kbd", "li", "main", "mark", "nav",
    "noscript", "ol", "p", "pre", "q", "rp", "rt", "ruby", "s", "samp", "section", "small", "span",
    "strike", "strong", "sub", "sup", "summary", "svg", "table", "tbody", "td", "template", "tfoot",
    "th", "thead", "time", "tr", "tt", "u", "ul", "var", "video", "math", "mrow", "msup", "msub",
    "mover", "munder", "msubsup", "moverunder", "mfrac", "mlongdiv", "msqrt", "mroot", "mi", "mn", "mo"
}
    soup = BeautifulSoup(body_html, 'html.parser')

    # Check if there is an <h1> tag in the document
    has_h1 = soup.find('h1') is not None

    # Decrease heading levels and remove id attributes
    for heading in soup.find_all(re.compile('^h[1-6]$')):
        if has_h1:
            current_level = int(heading.name[1])
            new_level = min(current_level + 1, 6)  # Ensure the level doesn't go beyond h6
            heading.name = f'h{new_level}'
    for tag in soup.find_all():
        if tag.name not in supported_tags:
            tag.unwrap() #צריך לסדר את span וdiv
        elif tag.name.lower() in ("section", "span", "tr", "div", "a"):
            tag_class = tag.attrs.get("class")
            if tag_class:
                class_replace = ""
                if tag_class == ["footnotes"]:
                    class_replace += "border-top: 1px solid lightgray; margin: 20px 0;"
                elif tag_class == ["header"]:
                    pass
                elif tag_class == ["anchor"]:
                    pass
                elif tag_class == ["odd"]:
                    pass
                elif tag_class == ["underline"]:
                    pass
                elif tag_class == ["even"]:
                    pass
                elif tag_class == ["math"]:
                    pass
                if tag.attrs.get("style"):
                    tag.attrs["style"] += class_replace
                elif class_replace:
                    tag.attrs["style"] = class_replace
                del tag.attrs["class"]

    for tag in soup.find_all():
        if not tag.get_text(strip=True) and tag.name != "br":  # If the tag has no text
            tag.decompose() 
        
    for tag in soup.find_all(recursive=False):
        tag.insert_before('\n')
        tag.insert_after('\n')

    text = str(soup).strip()

    return text

def get_updated_csv(url):
    content = requests.get(url)
    if content.status_code == 200:
        content = content.text.splitlines()
        csv_format = csv.reader(content)
        return list(csv_format)

def read_old_csv_file(csv_path):
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8") as csv_content:
            return list(csv.reader(csv_content))
    else:
        return []


def author_list(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            list_all = file.read().splitlines()
        return list_all
    else:
        return []

def write_to_csv(csv_path, data):
    with open(csv_path, "a", newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(data)

def get_book(book_path, base_url):
    full_url = f"{base_url}/{book_path}.html"
    content = requests.get(full_url)
    if content.status_code == 200:
        content = content.text
        return content
    else:
        print(full_url)

def main(url, koser_file, base_url, not_koser_file, need_to_check_file, csv_path, destination_path):
    updated_csv = get_updated_csv(url)
    old_csv = read_old_csv_file(csv_path)
    kosher_list = author_list(koser_file)
    not_koser_list = author_list(not_koser_file)
    need_to_check_list = author_list(need_to_check_file)
    for line in updated_csv[1:]:
        if line not in old_csv:
            author = line[3]
            if author not in not_koser_file:
                if author in kosher_list:
                    html_content = get_book(line[1], base_url)
                    if html_content:
                        pattern = r'את הטקסט לעיל הפיקו מתנדבי <a href="https://benyehuda\.org/">פרויקט בן־יהודה באינטרנט</a>\.  הוא זמין תמיד בכתובת הבאה:<br /><a href="https://benyehuda\.org/read/\d*">https://benyehuda\.org/read/\d*</a>'
                        html_content = re.sub(pattern, '', html_content)
                        title, author, body = extract_html_info(html_content)
                        processed_text = process_body_html(body).splitlines()
                        output_text = [f"<h1>{title}</h1>" if title else f"<h1>{line[2]}</h1>", author if author else (line[3] if line[3] else "")] + [adjust_html_tag_spaces(line).strip() for line in processed_text if line.strip() and line.strip() != "<!DOCTYPE html>"]
                        if output_text[2] == title:
                            output_text.pop(2)
                        join_lines = html.unescape("\n".join(output_text))
                        target_path = os.path.join(destination_path, sanitize_filename(line[8]), sanitize_filename(line[3]))
                        os.makedirs(target_path, exist_ok=True)
                        target_file = os.path.join(target_path, f"{sanitize_filename(line[2])}.txt")
                        num = 1
                        while os.path.exists(target_file):
                            num += 1
                            target_file = os.path.join(target_path, f"{sanitize_filename(line[2])}_{num}.txt")
                        with open(target_file, "w", encoding = "utf-8") as output:
                            output.write(join_lines)
                        write_to_csv(csv_path, line)
                elif author not in need_to_check_list and author not in not_koser_list:
                    need_to_check_list.append(author)
                    with open(need_to_check_file, "w", encoding = "utf-8") as need_to_check_new:
                        need_to_check_new.write("\n".join(need_to_check_list))

url = "https://raw.githubusercontent.com/projectbenyehuda/public_domain_dump/refs/heads/master/pseudocatalogue.csv"
koser_file = "koser_file.txt"
not_koser_file = "not_koser_file.txt"
need_to_check_file = "need_to_check.txt"
base_url = "https://raw.githubusercontent.com/projectbenyehuda/public_domain_dump/refs/heads/master/html"
csv_path = "list.csv"
destination_path = os.path.join("..", "ספרים")
main(url, koser_file, base_url, not_koser_file, need_to_check_file, csv_path, destination_path)