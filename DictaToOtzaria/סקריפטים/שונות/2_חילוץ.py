import os
import zipfile

# Function to extract ZIP files from a folder and delete them
def extract_and_delete_zip_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.zip'):
                zip_file_path = os.path.join(root, file)
                extract_folder = os.path.splitext(zip_file_path)[0]

                # Create the extraction folder if it doesn't exist
                if not os.path.exists(extract_folder):
                    os.makedirs(extract_folder)

                # Extract the ZIP file
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_folder)

                # Delete the ZIP file after extraction
                os.remove(zip_file_path)
                print(f"Extracted and deleted: {zip_file_path}")

# Specify the folder where you want to perform extraction and deletion
folder_to_process = r'./בעבודה'

# Call the function to extract and delete ZIP files
extract_and_delete_zip_files(folder_to_process)

