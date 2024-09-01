import pandas as pd
import os
import shutil
import re
from datetime import datetime

# Function to sanitize folder or file names
def sanitize_name(name):
    # Replace invalid characters with underscores
    return re.sub(r'[\/:*?<>|]', '_', name).replace('"', "''").strip("[").strip("]")

# Function to ensure unique filenames in the destination folder
def get_unique_filename(destination_folder, filename, file_extension):
    base_name = filename
    count = 1
    while os.path.exists(os.path.join(destination_folder, f"{base_name}{file_extension}")):
        base_name = f"{filename}_{count}"
        count += 1
    return f"{base_name}{file_extension}"

def kosher_books(author):
    with open("koser.txt", "r", encoding = "utf-8") as list_books:
        list_books_2 = list_books.read().splitlines()
    if author in list_books_2:
        return True
    else:
        return False


def main():
    # Load the CSV file
    df = pd.read_csv(csv_file)

    # Specify the main folder where subfolders will be created
   
    # Add the main folder path to the relative paths in column A
    df['Full_Path'] = main_folder + df['path'] + file_type  # Replace 'YourPathColumnName'

    # Create a dictionary to store the author and title information for each file
    file_info = {}

    # Replace 'genre', 'authors', and 'title' with the actual column names from your CSV
    for index, row in df.iterrows():
        try:
            source_path = row['Full_Path']
            author = sanitize_name(row['authors'])  # Sanitize author name
            title = sanitize_name(row['title'])  # Sanitize title

            # Check if the source file exists
            if not os.path.exists(source_path):
                print(f"File not found: '{source_path}' - Skipping.")
                continue
            kosher = kosher_books(author)
            if kosher:
                # Create the destination folder for authors if it doesn't exist
                genre_folder = sanitize_name(row['genre'])  # Sanitize genre name
                author_folder = os.path.join("outpoot", genre_folder, author)
                os.makedirs(author_folder, exist_ok=True)

                # Generate the destination file path with a unique filename
                file_name, file_extension = os.path.splitext(os.path.basename(source_path))
                sanitized_title = sanitize_name(title)
                unique_filename = get_unique_filename(author_folder, sanitized_title, file_extension)
                destination_path = os.path.join(author_folder, unique_filename)

                # Try to move the file to the destination folder with the new name
                try:
                    shutil.move(source_path, destination_path)
                    print(f"Moved '{source_path}' to '{destination_path}'")
                except Exception as move_error:
                    print(f"Error moving file '{source_path}' to '{destination_path}': {str(move_error)}")

                # Store file information in the dictionary
                file_info[source_path] = (destination_path, author, sanitized_title, file_name, file_extension)
            else:
                print(author)
        except Exception as e:
            print(f"Error processing line {index + 1}: {str(e)}")

    print("Files moved and renamed successfully.")


csv_file = "pseudocatalogue.csv"  # Replace with the path to your CSV file
main_folder = 'html'  # Replace with the path to your main folder
file_type = '.html'
main()