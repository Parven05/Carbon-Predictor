import os
import shutil
import zipfile

def find_and_cut_exe(src_dir):
    dist_path = os.path.join(src_dir, 'dist')
    if os.path.exists(dist_path):
        # Find and move .exe files
        for file_name in os.listdir(dist_path):
            if file_name.endswith('.exe'):
                exe_path = os.path.join(dist_path, file_name)
                shutil.move(exe_path, os.path.join(src_dir, file_name))
                print(f"Moved: {exe_path} to {os.path.join(src_dir, file_name)}")
    else:
        print(f"'dist' directory not found in {src_dir}")

def zip_folders_and_files(folder_names, src_dir, zip_file_name, specific_py_files):
    # Create the /release directory if it does not exist
    release_dir = os.path.join(src_dir, 'release')
    os.makedirs(release_dir, exist_ok=True)

    # Create or replace the ZIP file in the /release directory
    zip_path = os.path.join(release_dir, zip_file_name)
    if os.path.exists(zip_path):
        os.remove(zip_path)
        print(f"Removed existing ZIP file: {zip_path}")
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        # Add specified folders and their contents
        for folder_name in folder_names:
            folder_path = os.path.join(src_dir, folder_name)
            if os.path.exists(folder_path):
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, src_dir)
                        zipf.write(file_path, arcname)
                        print(f"Added {file_path} to {zip_file_name}")
            else:
                print(f"Folder '{folder_name}' not found")
        
        # Add .py, .qss files, and .exe files in the specified directory
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                if file.endswith('.qss') or file.endswith('.exe') or file in specific_py_files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, src_dir)
                    zipf.write(file_path, arcname)
                    print(f"Added {file_path} to {zip_file_name}")
                
    print(f"Created ZIP file: {zip_path}")

if __name__ == "__main__":
    # Current directory (where the script is located)
    src_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Find and move .exe files from 'dist' to the parent directory
    find_and_cut_exe(src_directory)

    # List of folders to include in the ZIP file
    folder_names_to_zip = ['resources', 'models', 'scripts']  # Replace with your folder names
    zip_file_name = 'Carbon Predictor.zip'  # Replace with your desired ZIP file name

    # List of specific .py files to include
    specific_py_files = ['main.py']  # Replace with your specific .py files

    # Create the ZIP file including the specified folders, .py/.qss/.exe files
    zip_folders_and_files(folder_names_to_zip, src_directory, zip_file_name, specific_py_files)
