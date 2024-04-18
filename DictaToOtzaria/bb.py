from bs4 import BeautifulSoup

def process_html(input_file, output_file):
    with open(input_file, 'r') as f:
        html_content = f.read().replace("\n","")

    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove all tags except <b> and <highlight>

    # Insert line break before the first occurrence of "bold" or "marked-paragraph" class
    inserted_break = False
    for i, tag in enumerate(soup.find_all()):
        if not inserted_break:
            previous_tag = soup.find_all()[i - 1] if i > 0 else None
            if "bold" in tag.get('class', []) or "marked-paragraph" in tag.get('class', []):
                if not (previous_tag and ("bold" in previous_tag.get('class', []) or "marked-paragraph" in previous_tag.get('class', []))):
                    tag.insert_before("\n")


    # Wrap text inside the BOLD class with the <b> tags
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

    # Wrap text inside the heading class with the <big> tags


    with open(output_file, 'w') as f:
        f.write(str(soup))

# Replace 'input_file.html' with the path to your input HTML file
# Replace 'output_file.html' with the path to the output HTML file
process_html('input_file.html', 'output_file.html')

