import os
import re
import csv

def extract_numerical_part(filename):
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
    return float('inf')  # Put files without numbers at the end

def merge_and_rename_subfolders(parent_folder):
    for root,  files in os.walk(parent_folder):
        text_files = [file for file in files if file.lower().endswith('.html')]
        
        if text_files:
            merge_and_rename(root, text_files)

def fix_content(file_name, content):
    content = content.splitlines()
    meta_data = search_csv("books.csv", file_name, 0)
    
    if meta_data != None:
        prossesd_lines = [f'<h1>{meta_data[0]}</h1>',meta_data[2]]
    else:
        prossesd_lines = [f'<h1>{file_name}</h1>']
   
    for line in content:
        if line != "":
    
            prossesd_lines.append(line)
    data = "\n".join(prossesd_lines)
    replace_data = data.replace("\n ", "\n").replace("<b> </b>", " ").replace("<big> </big>", " ").replace(" </b>", "</b> ").replace(" </big>", "</big> ").replace("<b></b>", "").replace("<big></big>", "").replace("</b> <b>", " ").replace("</big> <big>", " ")
    
    while "  " in replace_data:
        replace_data = replace_data.replace("  ", " ")

    return replace_data

def search_csv(filename, search_text, column_index):
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            # Strip quotes from the CSV column value
            csv_text = row[column_index].replace('"',"")
            if csv_text == search_text:
                return row
    return None

def merge_and_rename(folder_path, text_files):
    # Sort the text files based on the embedded numerical parts
    text_files.sort(key=extract_numerical_part)

    # Initialize the merged content
    merged_content = ''

    for index, text_file in enumerate(text_files):
        file_path = os.path.join(folder_path, text_file)
        with open(file_path, 'r', encoding="utf-8") as file:
            file_content = file.read()

            # Append file content and add a line break unless it's the last file
            merged_content += file_content
            if index < len(text_files) - 1:
                merged_content += ' '
                #צריך עדיין לתקן שבירידות שורה זה לא יתווסף

    # Create a new merged file
    subfolder_name = os.path.basename(folder_path)
    fix_merged = fix_content(subfolder_name, merged_content)
    merged_file_path = os.path.join(folder_path, f'{subfolder_name}.txt')
    with open(merged_file_path, 'w', encoding="utf-8") as merged_file:
        merged_file.write(fix_merged)

    # Delete the original text files
    for text_file in text_files:
        file_path = os.path.join(folder_path, text_file)
        os.remove(file_path)


if __name__ == '__main__':
    parent_folder = r"./dicta"
    merge_and_rename_subfolders(parent_folder)
    print("Merging and renaming complete for eligible subfolders.")

