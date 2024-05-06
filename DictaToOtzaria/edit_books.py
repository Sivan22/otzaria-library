import os
import csv

def process_in_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            print(file_name)
            delite_blank_line(os.path.join(root, file_name), file_name)

def delite_blank_line(file, file_name):
    with open (file, "r", encoding = "utf-8") as f:
        content = f.read().splitlines()
    meta_data = search_csv("books.csv", file_name, 0)
    if meta_data != None:
        prossesd_lines = [f'<h1>{meta_data[0]}</h1>',meta_data[2]]
    else:
        prossesd_lines = [f'<h1>{file}</h1>']
    for line in content:
        if line != "":
            prossesd_lines.append(line)
    data = "\n".join(prossesd_lines)
    with open (file , "w", encoding = "utf-8") as autpoot:
        autpoot.write(data)

def search_csv(filename, search_text, column_index):
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            # Strip quotes from the CSV column value
            csv_text = row[column_index].replace('"',"")
            if csv_text == search_text:
                return row
    return None
        
folder_path = r'./dicta'
process_in_folder(folder_path)
    
