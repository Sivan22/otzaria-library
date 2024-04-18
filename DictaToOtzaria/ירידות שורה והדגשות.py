from bs4 import BeautifulSoup
import os

def process_in_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            print(file_name)
            process_html(os.path.join(root, file_name))

def process_html(file):
    with open(file, 'r', encoding="utf-8") as f:
        html_content = f.read().replace("\n"," ")

    soup = BeautifulSoup(html_content, 'html.parser')
    for i, tag in enumerate(soup.find_all()):
        previous_tag = soup.find_all()[i - 1] if i > 0 else None
        if "bold" in tag.get('class', []) or "marked-paragraph" in tag.get('class', []):
            if not (previous_tag and ("bold" in previous_tag.get('class', []) or "marked-paragraph" in previous_tag.get('class', []))):
                tag.insert_before("\n")
    for tag in soup.find_all(class_="heading"):
        if tag.parent.name != 'big':
            new_tag_big = soup.new_tag("big")
            if tag.has_attr('class') and 'bold' in tag['class']:
                new_tag_b = soup.new_tag("b")
                new_tag_b.string = tag.get_text()
                new_tag_big.append(new_tag_b)
            else:
                new_tag_big.string = tag.get_text()
            tag.replace_with(new_tag_big)
    for tag in soup.find_all(class_="bold"):
        if tag.parent.name != 'b':
            new_tag = soup.new_tag("b")
            new_tag.string = tag.get_text()
            tag.replace_with(new_tag)
    for tag in soup.find_all():
        if tag.name not in ['b','big']:
            tag.unwrap()
    with open(file, 'w', encoding="utf-8") as f:
        f.write(str(soup))

folder_path = r'./null'
process_in_folder(folder_path)

