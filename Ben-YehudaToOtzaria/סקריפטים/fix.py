from bs4 import BeautifulSoup
import re
import os
import html

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
    body_html = body_html.replace("\n", "")
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
            tag.unwrap()
    for tag in soup.find_all():
        if not tag.get_text(strip=True):  # If the tag has no text
            tag.decompose() 
        
    for tag in soup.find_all(recursive=False):
     	tag.insert_before('\n')
     	tag.insert_after('\n')

    text = str(soup).strip()

    return text

def main(book_file, target_file, file_name):
    with open(book_file, "r", encoding = "utf-8") as file:
        html_content = file.read()
    pattern = r'את הטקסט לעיל הפיקו מתנדבי <a href="https://benyehuda\.org/">פרויקט בן־יהודה באינטרנט</a>\.  הוא זמין תמיד בכתובת הבאה:<br /><a href="https://benyehuda\.org/read/\d*">https://benyehuda\.org/read/\d*</a>'
    html_content = re.sub(pattern, '', html_content)
    title, author, body = extract_html_info(html_content)
    processed_text = process_body_html(body).splitlines()
    output_text = [f"<h1>{title}</h1>" if title else f"<h1>{file_name}</h1>", author if author else ""] + [line.strip() for line in processed_text if line and line.strip() != "<!DOCTYPE html>"]
    if output_text[2] == title:
    	output_text.pop(2)
        
    join_lines = html.unescape("\n".join(output_text))
    with open(target_file, "w", encoding = "utf-8") as output:
        output.write(join_lines)


books_folder = "outpoot"
target_path = "output"
for root, dir, file in os.walk(books_folder):
    for file_name in file:
        if file_name.lower().endswith(".html"):
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(root, books_folder)
            destination_path = os.path.join(target_path, relative_path)
            os.makedirs(destination_path, exist_ok=True)
            target_file = os.path.join(destination_path, f"{file_name[:-4]}txt")
            main(file_path, target_file, file_name[:-5])
