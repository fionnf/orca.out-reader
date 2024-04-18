import os

def find_energy_values(base_dir, subdirs):
    for subdir in subdirs:
        path = os.path.join(base_dir, subdir)
        energy_values = []
        frequencies = []
        status = "N/A"

        if os.path.exists(path):
            for filename in os.listdir(path):
                if filename.endswith("orca.out"):
                    full_path = os.path.join(path, filename)
                    final_energy = None
                    gibbs_energy = None
                    collecting_frequencies = False
                    frequencies_found = False

                    with open(full_path, 'r') as file:
                        lines = file.readlines()

                    # Reverse the list to find the last occurrence
                    for line in reversed(lines):
                        if "FINAL SINGLE POINT ENERGY" in line:
                            final_energy = line.strip().split()[-1]
                            break

                    for line in lines:
                        if "G-E(el)" in line:
                            gibbs_energy = line.strip().split()[-4]  # Ensure this index is correct
                            break
                        if "VIBRATIONAL FREQUENCIES" in line:
                            collecting_frequencies = True
                        elif "NORMAL MODES" in line and collecting_frequencies:
                            collecting_frequencies = False
                        elif collecting_frequencies:
                            parts = line.strip().split()
                            if parts and ':' in parts[0]:  # Check if the line starts with an index and colon
                                # Only process lines that can be converted to float
                                try:
                                    frequency_value = float(parts[-2])  # Frequency value is second last before "cm**-1"
                                    frequencies.append(frequency_value)
                                except ValueError:
                                    frequencies.append(None)  # Handle imaginary or incorrect formats

                    if frequencies:
                        if any(f is None or f < 0 for f in frequencies):  # Check for None or negative values
                            status = "FAIL"
                        else:
                            status = "PASS"
                    elif not frequencies and collecting_frequencies:
                        status = "N/A"

                    if final_energy or gibbs_energy:
                        energy_values.append((final_energy, gibbs_energy if gibbs_energy else "NONE", status))

        print(
            f"{subdir}\t{energy_values[0][0] if energy_values else 'No Data'}\t{energy_values[0][1] if energy_values else 'No Data'}\t{energy_values[0][2] if energy_values else 'No Data'}")

def generate_series(first_index, last_index):
    prefix = "FFc"
    series = [f"{prefix}{i:03}" for i in range(first_index, last_index + 1)]
    return series


# Example usage:
base_directory = r"G:\.shortcut-targets-by-id\1gpf-XKVVvMHbMGqpyQS5Amwp9fh8r96B\RUG shared\Master Project\Computations"
first = 132
last = 147


subdirectory_series = generate_series(first,last)
print(subdirectory_series)
find_energy_values(base_directory, subdirectory_series)

