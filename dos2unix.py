import os
import subprocess
import getpass


def run_command_with_sudo(command, password):
    """ Function to run a shell command with sudo privileges """
    command = f'echo {password} | sudo -S {command}'
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
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
        files_string = ' '.join(file_paths)  # Create a single string of file paths
        command = f"dos2unix {files_string}"  # Modify to batch process files
        print(f"Converting files...")
        sudo_password = getpass.getpass("Enter sudo password: ")  # Get password once
        run_command_with_sudo(command, sudo_password)

if __name__ == "__main__":
    parent_dir = r"G:\.shortcut-targets-by-id\1gpf-XKVVvMHbMGqpyQS5Amwp9fh8r96B\RUG shared\Master Project\Computations"  # Modify this to your parent directory path
    subdirs = ['FFc132', 'FFc133', 'FFc134', 'FFc135', 'FFc136', 'FFc137', 'FFc138', 'FFc139', 'FFc140', 'FFc141', 'FFc142', 'FFc143', 'FFc144', 'FFc145', 'FFc146']  # List your subdirectories here
    convert_files_in_subdirectories(parent_dir, subdirs)
