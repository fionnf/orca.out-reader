import os
import shutil
import sys

def extract_charge_multiplicity(file_path):
    charge, multiplicity = None, None
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip().startswith('*xyz'):
                parts = line.split()
                try:
                    charge = int(parts[1])
                    multiplicity = int(parts[2])
                    break
                except (IndexError, ValueError):
                    print("Charge and multiplicity not found or incorrect format in orca.inp")
                    break
    return charge, multiplicity

def main(source, target):
    # Hardcoded base directory
    base_dir = r"G:\.shortcut-targets-by-id\1gpf-XKVVvMHbMGqpyQS5Amwp9fh8r96B\RUG shared\Master Project\Computations"

    source_dir = os.path.join(base_dir, source)
    target_dir = os.path.join(base_dir, target)

    # Create the target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)

    # Copy and rename the orca.xyz file
    src_file = os.path.join(source_dir, 'orca.xyz')
    dest_file = os.path.join(target_dir, 'inp.xyz')
    shutil.copy(src_file, dest_file)

    # Extract charge and multiplicity from source orca.inp
    source_inp = os.path.join(source_dir, 'orca.inp')
    charge, multiplicity = extract_charge_multiplicity(source_inp)
    if charge is None or multiplicity is None:
        print("Failed to extract charge or multiplicity from source orca.inp.")
        return

    # Create orca.inp file
    inp_content = f"""%pal nprocs 32 end
%maxcore 5000

%scf
   MaxIter 2500
end

! B3LYP D3BJ 6-311++G** NoTrah Normalprint PrintMOs
! CPCM
%cpcm
   smd true
   SMDsolvent "Acetonitrile"
end

!xyzfile
*xyz {charge} {multiplicity} inp.xyz

!NMR

%eprnmr 
   maxiter 124
   gtensor true printlevel 3  # this computes the g-tensor
   nuclei = all H {{aiso, adip}} # this compute the hyperfine coupling for all hydrogens.
   nuclei = all F {{aiso, adip}}
   nuclei = all N {{aiso, adip}}
end
"""
    with open(os.path.join(target_dir, 'orca.inp'), 'w') as f:
        f.write(inp_content)

    # Create orca.pbs file
    pbs_content = """#!/bin/bash
#SBATCH --job-name=orca
#SBATCH --time=00-08:00:00
#SBATCH --partition=regular
#SBATCH --ntasks=32
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=5500mb
#SBATCH --nodes=1

module load ORCA

/apps/versions/2023.01/rocky8/x86_64/generic/software/ORCA/5.0.4-gompi-2022a/bin/orca orca.inp > orca.out
orca_2mkl orca -molden
exit
"""
    with open(os.path.join(target_dir, 'orca.pbs'), 'w') as f:
        f.write(pbs_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <source_subdir> <target_subdir>")
    else:
        source_subdir = sys.argv[1]
        target_subdir = sys.argv[2]
        main(source_subdir, target_subdir)
