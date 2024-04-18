import os
import shutil

# Function to move a file out of its current folder to the folder containing its current folder
def move_file_to_parent_folder(file_path):
    current_folder = os.path.dirname(file_path)
    parent_folder = os.path.dirname(current_folder)
    filename = os.path.basename(file_path)

    # Check if there are subdirectories in the current folder
    if any(os.path.isdir(os.path.join(current_folder, subfolder)) for subfolder in os.listdir(current_folder)):
        print(f"Skipping '{filename}' in '{current_folder}' because it has subdirectories.")
        return

    # Determine the new path for the file in the parent folder
    new_file_path = os.path.join(parent_folder, filename)

    # Check if a file with the same name already exists in the parent folder
    if os.path.exists(new_file_path):
        # If a conflict exists, add a number to the filename
        base_filename, file_extension = os.path.splitext(filename)
        count = 1
        while os.path.exists(new_file_path):
            new_filename = f"{base_filename}_{count}{file_extension}"
            new_file_path = os.path.join(parent_folder, new_filename)
            count += 1

    # Move the file to the parent folder
    shutil.move(file_path, new_file_path)
    print(f"Moved '{filename}' to '{parent_folder}' as '{os.path.basename(new_file_path)}'")

    # Delete the empty folder
    os.rmdir(current_folder)
    print(f"Deleted empty folder '{current_folder}'")

# Define the root directory where you want to start the search
root_directory = "/media/zevi/My Passport/דיקטה סופי/test"

# Recursively search for folders with a single file in subdirectories
for foldername, subfolders, filenames in os.walk(root_directory):
    if len(filenames) == 1:
        file_path = os.path.join(foldername, filenames[0])
        move_file_to_parent_folder(file_path)

print("File movement and empty folder deletion complete.")

