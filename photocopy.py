import shutil
import os
import subprocess
csv_file_path = "Sakshee.csv"
base_dir = '/media/FPIBAK/'
photos_dir_path = 'photos'

def delete_directory_contents(output_path):
    try:
        shutil.rmtree(output_path)
        print(f"Deleted contents of directory: {output_path}")
    except FileNotFoundError:
        print(f"Directory not found: {output_path}")
    except OSError as e:
        print(f"Error occurred while deleting directory contents: {e}")

def copy_file(file_path, output_path):
    try:
        shutil.copy2(file_path, output_path)
        print(f"File copied successfully.")
    except FileNotFoundError:
        print(f"Source file '{file_path}' not found.")
    except IOError as e:
        print(f"Error occurred while copying the file: {e}")

# Prompt the user if they want to delete the data in the output directory
delete_data = input("Do you want to delete the data in the output directory? (yes/no): ")

if delete_data.lower() == "yes":
    # Delete the contents of the output directory
    delete_directory_contents(photos_dir_path)
    try:
        os.makedirs(photos_dir_path)
        print(f"Created new directory: {photos_dir_path}")
    except OSError as e:
        print(f"Error occurred while creating new directory: {e}")
    file_name = 'README.md'
    file_name_path = os.path.join(photos_dir_path, file_name)
    with open(file_name_path, 'w') as file:
        file.write('# My Readme File\n\nThis is my readme file.')

    breakpoint()
        
with open(csv_file_path, "r") as file_handler:
    next(file_handler)  # Skip the first line

    for line in file_handler:
        line_split = line.split(",")
        file_path = line_split[4]
        rel_path = file_path.replace(base_dir, "")
        output_path = os.path.join(photos_dir_path, rel_path)
        directory_name, filename = os.path.split(output_path)
        if os.path.exists(directory_name) == False:
            command = f"mkdir -p {directory_name}"
            subprocess.run(command, shell=True)
        if os.path.exists(output_path) == False:
            copy_file(file_path, output_path)
