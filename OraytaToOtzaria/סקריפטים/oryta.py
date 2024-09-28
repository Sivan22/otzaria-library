from bs4 import BeautifulSoup
import os
import zipfile
import re
import html as html_module
import csv

"""
to do:
סוגריים כפולים וכו'
"""

def sanitize_filename(filename):
    sanitized_filename = re.sub(r'[\/:*?<>|]', '', filename).replace('"', "''")
    return sanitized_filename

def adjust_html_tag_spaces(html):
    #replacement_dict = {"{{":"{", }
    start_pattern = r'(<[^/<>]+?>)([ ]+)' 
    end_pattern = r'([ ]+)(</[^<>]+?>)' 
    while re.findall(end_pattern , html):
        html = re.sub(end_pattern, r'\2\1', html)
    while re.findall(start_pattern, html):
        html = re.sub(start_pattern , r'\2\1', html)
    html = re.sub(r'[ ]{2,}', ' ', html)
    #for fined, replace in replacement_dict.items():
    #   html = html.replace(fined, replace)
    return html

def main(books_dir, target_dir, csv_file):
    for root, _, files in os.walk(books_dir):
        for file_name in files:
            if file_name.lower().endswith(".obk"):
                title = None
                file_path = os.path.join(root, file_name)
                content = read_zip(file_path)
                archive_comment = get_comment(file_path)
                if archive_comment:
                    archive_comment = archive_comment.splitlines()
                    dict_comment = {}
                    dict_comment_2 = {}
                    for line in archive_comment:
                        try:
                            name_key, name_value = line.split("=")
                            dict_comment[name_key.strip()] = name_value.strip()
                        except ValueError:
                            continue
                    title = dict_comment.get("DisplayName")
                    if not title:
                        title = dict_comment.get("ForcedBookName")
                    list_all_data = ("ForcedBookName", "SearchInTitles", "LastLevelIndex", "CosmeticsType", "PasukIndMode", "HiddenFromIndex", "FilesGotFrom",
                                "PutNewLinesAsIs", "DisplayName", "UniqueId", "MixedSources", "WeaveLevel", "SpecialTitle", "MixedDisplay", "TextSource",
                                "GroupId", "BranchName", "Comments", "RavMechaber", "ChainFolderName")
                    for i in list_all_data:
                        dict_comment_2[i] = dict_comment.get(i) if dict_comment.get(i) else ""

                content = read_zip(file_path)
                if not content:
                    continue
                content = re.sub(r"<!--[^א-ת]+?-->","", content)
                content = content.splitlines()
                fix_content, title_from_file = proses_file(content)
                fix_spaces = adjust_html_tag_spaces(fix_content).splitlines()
                output_text = [line.strip() for line in fix_spaces if line.strip()]
                join_lines = html_module.unescape("\n".join(output_text))
                target_dir_heb = get_path(file_path, books_dir, target_dir)
                os.makedirs(target_dir_heb, exist_ok=True)
                if not title:
                    title = title_from_file
                title = sanitize_filename(title)
                target_file_path = os.path.join(target_dir_heb, f"{title}.txt")
                num = 1
                while os.path.exists(target_file_path):
                    num += 1
                    target_file_path = os.path.join(target_dir_heb, f"{title}_{num}.txt")
                with open(target_file_path, "w", encoding = "utf-8") as output:
                    output.write(join_lines)
                with open(csv_file, "a", newline = '', encoding="utf-8") as csv_list:
                    writer = csv.writer(csv_list)
                    if csv_list.tell() == 0:
                        writer.writerow(["original path", "target path", "ForcedBookName", "SearchInTitles", "LastLevelIndex", "CosmeticsType", "PasukIndMode", "HiddenFromIndex", "FilesGotFrom",
                                "PutNewLinesAsIs", "DisplayName", "UniqueId", "MixedSources", "WeaveLevel", "SpecialTitle", "MixedDisplay", "TextSource",
                                "GroupId", "BranchName", "Comments", "RavMechaber", "ChainFolderName"])
                    values = [os.path.relpath(file_path, books_dir), os.path.relpath(target_file_path, target_dir)] + list(dict_comment_2.values())
                    writer.writerow((values)) 
                    

def read_zip(file_path):
    with zipfile.ZipFile(file_path, 'r') as archive:
        content = archive.read("BookText")
    try:
        content = content.decode()
    except UnicodeDecodeError:
        try:
            content = content.decode(encoding='windows-1255')
        except UnicodeDecodeError:
            return False
    return content

def get_comment(file_path):
    with zipfile.ZipFile(file_path, 'r') as archive:
        archive_comment = archive.comment
    try:
        archive_comment = archive_comment.decode('utf-8')
    except UnicodeDecodeError:
        try:
            archive_comment = archive_comment.decode('windows-1255')
        except UnicodeDecodeError:
            return False
        
    return archive_comment

def get_path(file_path, books_dir, target_dir):
    rel_path = os.path.relpath(file_path, books_dir)
    split_path = rel_path.split(os.sep)
    path_now = books_dir
    for i in split_path[:-1]:
        folder_name_file = os.path.join(path_now, f"{i}.folder")
        try:
            with open(folder_name_file, "r", encoding = "utf-8") as folder_name:
                new_name_from_file = sanitize_filename(folder_name.read().split("=")[1].strip("\n"))
        except FileNotFoundError:
            new_name_from_file = i
            print(i)

        target_dir = os.path.join(target_dir, new_name_from_file)
        path_now = os.path.join(path_now, i)
    return target_dir

        
def proses_file(text):
    proses_file = []
    start = False
    title = None
    for line in text:
        if line.startswith("$") and not proses_file:
            line = line.strip("$").strip()
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
            elif line.startswith("**INDEX_WRITE"):
                continue
            else:
                proses_file.append(line)

    join_lines = "\n".join(proses_file)

    soup = BeautifulSoup(join_lines, 'lxml')
    for tag in soup.find_all():
        if tag.name:
            if tag.name.lower() in ('html', "body", "amats", "iri", "nsobr", "qm", "r", "ra", "rb", "sp", "trim", "x", "y", "yesh"):
                tag.unwrap()
            elif tag.name.lower() == "center":
                tag.name = "span"
                if tag.attrs.get("style"):
                    tag.attrs["style"] += "text-align: center;"
                else:
                    tag.attrs["style"] = "text-align: center;"
            elif tag.name.lower() in ("div", "span"):
                tag_class = tag.attrs.get("class")
                if tag_class:
                    class_replace = ""
                    if tag_class == ["MsoNormal"]:
                        pass
                    elif tag_class == ["breadcrumbs"]:
                        pass
                    elif tag_class == ["pageno"]:
                        pass
                    elif tag_class == ["pirush"]:
                        class_replace += "color:#2828AC;"
                    elif tag_class == ["ref"]:
                        class_replace += "font-size:80%;"
                    elif tag_class == ["pasuk"]:
                        class_replace += "font-family: SBL Hebrew;"
                    elif tag_class == ["editor"]:
                        class_replace += "color:#008A00;"
                    elif tag_class == ["Aliyah"]:
                        class_replace += "font-size:80%;"
                    elif tag_class == ["S0"]:
                        class_replace += "font-size:95%;  font-weight:bold;"
                    elif tag_class == ["pasuk", "small"]:
                        class_replace += f"font-size:70%; font-family: SBL Hebrew;"
                    if tag.attrs.get("style"):
                        tag.attrs["style"] += class_replace
                    elif class_replace:
                        tag.attrs["style"] = class_replace
                    del tag.attrs["class"]
    for tag in soup.find_all():
        if not tag.get_text(strip=True) and tag.name != "br":  # If the tag has no text
            tag.decompose() 

    for tag in soup.find_all(recursive=False):
        tag_str = str(tag)
        re.sub(r"([^>])(\n)(\s*[^<\s])", r"\1<br>\3", tag_str)
        tag_str = tag_str.replace("\n", " ")
        new_tag = BeautifulSoup(tag_str, "html.parser").find()
        tag.replace_with(new_tag)

    return str(soup), title
    

books_dir = "books"
target_dir = os.path.join("..", "ספרים")
csv_file = "list.csv"
main(books_dir, target_dir, csv_file)