import os
import subprocess
import getpass

def run_command_with_sudo(command):
    """ Function to run a shell command with sudo privileges, assumes password is cached or not needed """
    try:
        result = subprocess.run(f'sudo {command}', shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)

def convert_files_in_subdirectories(parent_directory, subdirectories):
    """ Converts files in specified subdirectories using dos2unix with sudo, skips .xyz files """
    file_paths = []
    for subdir in subdirectories:
        full_path = os.path.join(parent_directory, subdir)
        for root, dirs, files in os.walk(full_path):
            for file in files:
                if not file.endswith('.xyz'):
                    file_paths.append(os.path.join(root, file))

    if file_paths:
        files_string = ' '.join(f'"{path}"' for path in file_paths)  # Create a single string of file paths
        command = f"dos2unix {files_string}"  # Modify to batch process files
        print(f"Converting files...")
        run_command_with_sudo(command)

if __name__ == "__main__":
    parent_dir = r"G:\.shortcut-targets-by-id\1gpf-XKVVvMHbMGqpyQS5Amwp9fh8r96B\RUG shared\Master Project\Computations"
    subdirs = ['FFc132']  # List your subdirectories here
    convert_files_in_subdirectories(parent_dir, subdirs)
