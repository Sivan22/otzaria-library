from bs4 import BeautifulSoup
import os
import json

def print_all_tags(html_content, tag_list, attr_list, file_path):
    soup = BeautifulSoup(html_content, "lxml")
    for tag in soup.find_all():
        if tag.name not in tag_list:
            tag_list[tag.name] = [file_path]
        elif file_path not in tag_list[tag.name]:
           tag_list[tag.name] += [file_path] 

        if not attr_list.get(tag.name):
            attr_list[tag.name] = {}
        for key in tag.attrs.keys():
            if not attr_list[tag.name].get(key):
                attr_list[tag.name][key] = {}
            if attr_list[tag.name][key].get(str(tag.attrs[key])):
                if file_path not in attr_list[tag.name][key][str(tag.attrs[key])]:
                    attr_list[tag.name][key][str(tag.attrs[key])] += [file_path]
            else:
                attr_list[tag.name][key][str(tag.attrs[key])] = [file_path]

    return tag_list, attr_list

main_folder = "ספרים ובלכתך בדרך"
tag_list = {}
attr_list = {}
for root, dir, file in os.walk(main_folder):
    for file_name in file:
        if file_name.lower().endswith(".txt"):
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    html_content = file.read()
                print(file_path)
            except UnicodeDecodeError:
                with open(file_path, "r", encoding="windows-1255") as file:
                    html_content = file.read()
                print("windows-1255")
            tag_list, attr_list = print_all_tags(html_content, tag_list, attr_list, file_path)
with open("list_tag_3.json", "w", encoding = "utf-8") as file_tag:
    json.dump(tag_list, file_tag, ensure_ascii=False, indent=4)
with open("attr_list_5.json", "w", encoding="utf-8") as file_attr:
    json.dump(attr_list, file_attr, ensure_ascii=False, indent=4)
list_all_tags = "\n".join([i for i in tag_list])
with open("list_tag_3.txt", "w", encoding="utf-8") as file_attr:
    file_attr.write(list_all_tags)
list_all_tags = "\n".join([i for i in attr_list])
with open("attr_tag_3.txt", "w", encoding="utf-8") as file_attr:
    file_attr.write(list_all_tags)
