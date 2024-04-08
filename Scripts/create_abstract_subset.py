import os
import shutil

# Function to count words in a file
def count_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = file.read().split()
        return len(words)

# Source and destination folders
source_folder = ''
destination_folder = ''

# Create destination folder if it doesn't exist
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Iterate through files in source folder
file_count = 0
for filename in os.listdir(source_folder):
    if file_count >= 2500:
        break

    file_path = os.path.join(source_folder, filename)
    
    # Check if it's a file
    if os.path.isfile(file_path):
        word_count = count_words(file_path)
        
        # Check if word count is within the specified range
        if 250 <= word_count <= 750:
            # Copy file to destination folder
            shutil.copy(file_path, destination_folder)
            file_count += 1

print("Files copied successfully.")
