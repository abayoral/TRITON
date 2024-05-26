import os
import glob

def update_labels_in_file(file_path):
    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Process each line
    updated_lines = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) > 0:
            label = int(parts[0])
            # Update the label if necessary
            if label == 2:
                parts[0] = '0'
            elif label == 3:
                parts[0] = '1'
            updated_line = ' '.join(parts)
            updated_lines.append(updated_line)
    
    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write('\n'.join(updated_lines) + '\n')

def update_labels_in_folder(folder_path):
    # Find all files in the folder that match the naming pattern
    pattern = os.path.join(folder_path, '*.txt')
    files = glob.glob(pattern)

    for file_path in files:
        update_labels_in_file(file_path)

# Define the path to the folder containing your files
folder_path = 'train/labels'

# Update the labels in all files in the folder
update_labels_in_folder(folder_path)
