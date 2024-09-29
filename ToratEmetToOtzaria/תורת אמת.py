import os
import re
import csv
import html as html_module
from bs4 import BeautifulSoup

def adjust_html_tag_spaces(html):
    start_pattern = r'(<[^/<>]+?>)([ ]+)' 
    end_pattern = r'([ ]+)(</[^<>]+?>)' 
    while re.findall(end_pattern , html):
        html = re.sub(end_pattern, r'\2\1', html)
    while re.findall(start_pattern, html):
        html = re.sub(start_pattern , r'\2\1', html)
    html = re.sub(r'[ ]{2,}', ' ', html)
    return html


def sanitize_filename(filename):
    # Remove invalid characters
    sanitized_filename = re.sub(r'[\\/:*?<>|]', '', filename).replace('"', "''")
    return sanitized_filename

def process_body_html(content):
    supported_tags = {
    "a", "abbr", "acronym", "address", "article", "aside", "audio", "b", "bdi", "bdo", "big",
    "blockquote", "br", "caption", "cite", "code", "data", "dd", "del", "details", "dfn", "dl", "dt", "em", "figcaption", "figure", "footer", "font", "h1", "h2", "h3", "h4",
    "h5", "h6", "header", "hr", "i", "iframe", "img", "ins", "kbd", "li", "main", "mark", "nav",
    "noscript", "ol", "p", "pre", "q", "rp", "rt", "ruby", "s", "samp", "section", "small", "span",
    "strike", "strong", "sub", "sup", "summary", "svg", "table", "tbody", "td", "template", "tfoot",
    "th", "thead", "time", "tr", "tt", "u", "ul", "var", "video", "math", "mrow", "msup", "msub",
    "mover", "munder", "msubsup", "moverunder", "mfrac", "mlongdiv", "msqrt", "mroot", "mi", "mn", "mo", "span", "div"
}
    proses_file = []
    content = content.splitlines()
    TextSource = content[0].split("&")
    start = False
    for i in TextSource:
        if "TextSource" in i:
            license = i.replace("TextSource=", "")
        elif "SpecialTitle" in i:
            license = i.replace("SpecialTitle=","")
        title = i.replace("ForcedBookName=","") if "ForcedBookName" in i else None
    for line in content[1:]:
        if line:
            if line.startswith("$") and not proses_file:
                line = line.strip("$").strip()
                if not title:
                    title = line
                proses_file.append(f"<h1>{line}</h1>")
                start = True
            elif start:
                if line.startswith("^"):
                    line = line.strip("^").strip()
                    proses_file.append(f"<h2>{line}</h2>")
                elif line.startswith("~"):
                    line = line.strip("~").strip()
                    proses_file.append(f"<h3>{line}</h3>")
                elif line.startswith("@"):
                    line = line.strip("@").strip()
                    proses_file.append(f"<h2>{line}</h2>")
                elif line.startswith("#"):
                    line = line.strip("#").strip()
                    proses_file.append(f"<h2>{line}</h2>")
                elif line.startswith("!"):
                    line = line.strip("!").strip()
                    proses_file.append(f"<h4>{line}</h4>")
                elif line.startswith("**INDEX_WRITE="):
                    continue
                else:
                    proses_file.append(line.strip())
    proses_file = "\n".join(proses_file)
    soup = BeautifulSoup(proses_file, 'lxml')
    for tag in soup.find_all():
        if tag.name.lower() not in supported_tags:
            tag.unwrap()
    for tag in soup.find_all():
        if not tag.get_text(strip=True) and tag.name != "br":
            tag.decompose() 

    for tag in soup.find_all(recursive=False):
        tag_str = str(tag)
        re.sub(r"([^>])(\n)(\s*[^<\s])", r"\1<br>\3", tag_str)
        tag_str = tag_str.replace("\n", " ")
        new_tag = BeautifulSoup(tag_str, "html.parser").find()
        tag.replace_with(new_tag)
    proses_file = adjust_html_tag_spaces(str(soup))
    proses_file = re.sub(r"[\n]{2,}", "\n", proses_file)
    proses_file = re.sub(r"<!--[^א-ת]+?-->","", proses_file)
    return proses_file, title, license

def main(books_dir, target_dir):
    for root, _, files in os.walk(books_dir):
        for file_name in files:
            if file_name.lower().endswith(".txt"):
                old_path = os.path.join(root, file_name)
                try:
                    with open(old_path, "r", encoding = "windows-1255") as file:
                        content = file.read()
                except UnicodeDecodeError:
                    try:
                        with open(old_path, "r", encoding = "utf-8") as file:
                            content = file.read()
                    except UnicodeDecodeError:
                        continue
                content, title, license = process_body_html(content)
                rel_path = os.path.relpath(old_path, books_dir).split("\\")[:-1]
                rel_path = "\\".join(rel_path)
                target_path = os.path.join(target_dir, rel_path)
                os.makedirs(target_path, exist_ok=True)
                target_file_path = os.path.join(target_path, f"{sanitize_filename(title)}.txt")
                with open(target_file_path, "w", encoding="utf-8") as output:
                    output.write(html_module.unescape(content))
                with open(csv_file, "a", newline = '', encoding="utf-8") as csv_list:
                    writer = csv.writer(csv_list)
                    if csv_list.tell() == 0:
                        writer.writerow(["original path", "target_file_path", "LICENSE"])
                    writer.writerow((old_path, target_file_path, license)) 

books_dir = "מתורת אמת שלא קיים באוצריא"
target_dir = "test"
csv_file = "test.csv"
main(books_dir, target_dir) 