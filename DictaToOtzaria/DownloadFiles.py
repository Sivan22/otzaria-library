import os
import requests
from urllib.parse import urlparse
 
# Read the lines from the text file
with open('books.json', 'r', encoding='utf-8') as file:
    lines = file.readlines()
 
# Initialize variables to store display name, category, and file URLs
display_name = None
category = None
OCRDataURL = None
 
# Define a function to clean and sanitize folder and file names
def clean_name(name):
    # Replace _, ", \, and / characters with space
    name = name.replace('_', ' ').replace('"', '').replace('\\', '').replace('/', '')
    return name
 
# Iterate through the lines
for line in lines:
    line = line.strip()
    if line.startswith('"displayName":'):
        display_name = line.split('"displayName": ')[1].strip().strip('",')
    elif line.startswith('"category":'):
        category = line.split('"category": ')[1].strip().strip('",')
    elif line.startswith('"OCRDataURL":'):
        OCRDataURL = line.split('"OCRDataURL": ')[1].strip().strip('",')
 
        if display_name and category:
            # Clean and sanitize folder and file names
            display_name = clean_name(display_name)
            category = clean_name(category)
 
            # Parse the URLs to extract the filenames
            text_parsed_url = urlparse(OCRDataURL)
            text_filename = os.path.basename(text_parsed_url.path)
 
            # Create a folder if it doesn't exist
            folder_name = category
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
 
            # Download and rename text file
            text_response = requests.get(OCRDataURL)
            if text_response.status_code == 200:
                text_new_filename = os.path.join(folder_name, f"{display_name}.zip")
                with open(text_new_filename, "wb") as file:
                    file.write(text_response.content)
                print(f"Downloaded and renamed {text_filename} to {text_new_filename}")
            else:
                print(f"Failed to download {nikud_filename}")
 
            # Reset variables for the next entry
            display_name = None
            category = None
            OCRDataURL = None
 
 
print("All files downloaded and organized.")
