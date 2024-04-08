import os
import shutil

def split_folder(source_folder, num_folders):
    # Create destination folders
    for i in range(num_folders):
        folder_name = f"{source_folder}/parse_{i+1}"
        os.makedirs(folder_name, exist_ok=True)
    
    # Get list of files in the source folder
    files = os.listdir(source_folder)
    num_files = len(files)
    
    # Calculate number of files per folder
    files_per_folder = num_files // num_folders
    
    # Distribute files to destination folders
    for i in range(num_folders):
        folder_name = f"{source_folder}/parse_{i+1}"
        start_index = i * files_per_folder
        end_index = start_index + files_per_folder if i < num_folders - 1 else num_files
        
        for file_name in files[start_index:end_index]:
            source_path = os.path.join(source_folder, file_name)
            dest_path = os.path.join(folder_name, file_name)
            shutil.move(source_path, dest_path)

source_folder = "Triplet_Extraction/Test_data"  # Change this to your source folder
num_folders = 5

split_folder(source_folder, num_folders)
