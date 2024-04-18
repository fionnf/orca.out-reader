import os
import shutil
import sys

def main(source, target, charge, multiplicity):
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
    if len(sys.argv) != 5:
        print("Usage: python script.py <source_subdir> <target_subdir> <charge> <multiplicity>")
    else:
        source_subdir = sys.argv[1]
        target_subdir = sys.argv[2]
        charge = int(sys.argv[3])
        multiplicity = int(sys.argv[4])
        main(source_subdir, target_subdir, charge, multiplicity)
