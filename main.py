import os

def find_energy_values(base_dir, subdirs):
    for subdir in subdirs:
        path = os.path.join(base_dir, subdir)
        energy_values = []

        if os.path.exists(path):
            for filename in os.listdir(path):
                if filename.endswith("orca.out"):
                    full_path = os.path.join(path, filename)
                    final_energy = None
                    gibbs_energy = None

                    with open(full_path, 'r') as file:
                        lines = file.readlines()

                    # Reverse the list to find the last occurrence
                    for line in reversed(lines):
                        if "FINAL SINGLE POINT ENERGY" in line:
                            final_energy = line.strip().split()[-1]
                            break

                    for line in lines:
                        if "G-E(el)" in line:
                            gibbs_energy = line.strip().split()[-4]  # Assumes the value is the second last element
                            break

                    if final_energy or gibbs_energy:
                        energy_values.append((final_energy, gibbs_energy if gibbs_energy else "NONE"))

        print(
            f"{subdir}\t{energy_values[0][0] if energy_values else 'No Data'}\t{energy_values[0][1] if energy_values else 'No Data'}")

def generate_series(first_index, last_index):
    prefix = "FFc"
    series = [f"{prefix}{i:03}" for i in range(first_index, last_index + 1)]
    return series


# Example usage:
base_directory = r"G:\.shortcut-targets-by-id\1gpf-XKVVvMHbMGqpyQS5Amwp9fh8r96B\RUG shared\Master Project\Computations"
first = 58
last = 107


subdirectory_series = generate_series(first,last)
print(subdirectory_series)
find_energy_values(base_directory, subdirectory_series)

