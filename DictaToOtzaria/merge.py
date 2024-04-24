import os
import re
import datetime

def extract_numerical_part(filename):
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
    return float('inf')  # Put files without numbers at the end

def merge_and_rename_subfolders(parent_folder, log_file):
    for root, dirs, files in os.walk(parent_folder):
        text_files = [file for file in files if file.lower().endswith('.html')]
        
        if text_files:
            merge_and_rename(root, text_files, log_file)

def merge_and_rename(folder_path, text_files, log_file):
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
                merged_content += ''

    # Create a new merged file
    subfolder_name = os.path.basename(folder_path)
    merged_file_path = os.path.join(folder_path, f'{subfolder_name}')
    with open(merged_file_path, 'w', encoding="utf-8") as merged_file:
        merged_file.write(merged_content)

    # Delete the original text files
    for text_file in text_files:
        file_path = os.path.join(folder_path, text_file)
        os.remove(file_path)

    # Log the merge and rename operation
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp}: Merged and renamed '{subfolder_name}'\n"
    with open(log_file, 'a',encoding="utf-8") as log:
        log.write(log_entry)

if __name__ == '__main__':
    parent_folder = r"./dicta"
    log_file = os.path.join(parent_folder, 'merge_log.txt')
    
    with open(log_file, 'w', encoding="utf-8") as log:
        log.write("Merge Log\n")
    
    merge_and_rename_subfolders(parent_folder, log_file)
    print("Merging and renaming complete for eligible subfolders. Log written to 'merge_log.txt'.")

