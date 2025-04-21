import numpy as np
import os
import sys
import json

def parse_pdb(file_path):
    """
    Reads a PDB file and extracts atomic positions and residue data.

    Args:
    file_path (str): Path to the PDB file.

    Returns:
    atoms (list): List of atoms with (x, y, z) coordinates.
    residues (dict): Dictionary of residues {res_id: res_type}.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    atoms = []
    residues = {}

    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM'):
                try:
                    # Extract atomic coordinates
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    atom_name = line[12:16].strip()  # Atom name (optional for future use)

                    # Append atom information
                    atoms.append((atom_name, x, y, z))

                    # Extract residue data
                    res_id = int(line[22:26].strip())
                    res_type = line[17:20].strip()

                    # Store residue info uniquely (avoids duplicates)
                    if res_id not in residues:
                        residues[res_id] = res_type

                except ValueError as e:
                    print(f"Warning: Could not parse line: {line.strip()} - {e}")

    # Debugging print statements
    print(f"Parsed {len(atoms)} atoms.")
    print(f"Extracted {len(residues)} unique residues.")

    return atoms, residues

def compute_accessibility(atoms, cutoff=8.0, use_surface_approach=True, scale_factor=10.0, normalize=True):
    """
    Estimates solvent accessibility for residues using a distance-based approach.

    Args:
    atoms (list): List of atoms with (x, y, z) coordinates.
    cutoff (float): Distance threshold for considering neighbor atoms.
    use_surface_approach (bool): Whether to use a simple surface-exposure check.
    scale_factor (float): Scaling factor to adjust the accessibility values.
    normalize (bool): Whether to normalize the accessibility values.

    Returns:
    accessibility (dict): Estimated solvent accessibility per atom index.
    """
    accessibility = {}

    for i, (atom_name, x1, y1, z1) in enumerate(atoms):
        count = 0  # Count neighboring atoms
        for j, (atom_name2, x2, y2, z2) in enumerate(atoms):
            if i != j:
                dist = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
                if dist < cutoff:
                    count += 1

        # Surface-based approach (simple heuristic for surface atoms)
        if use_surface_approach:
            if count <= 2:
                # Surface atoms have higher accessibility
                accessibility[i] = scale_factor / (count + 1)
            else:
                # Interior atoms have lower accessibility
                accessibility[i] = scale_factor / (count + 1)
        else:
            # Standard approach (no surface-exposure check)
            accessibility[i] = scale_factor / (count + 1)

    # Normalize accessibility values to a range of 0-1 if desired
    if normalize:
        max_access = max(accessibility.values())
        min_access = min(accessibility.values())
        range_access = max_access - min_access

        # Avoid division by zero
        if range_access > 0:
            for i in accessibility:
                accessibility[i] = (accessibility[i] - min_access) / range_access

    print("Computed solvent accessibility for all atoms.")
    return accessibility


def save_data_to_file(atoms, residues, accessibility, output_file):
    """
    Saves parsed PDB data and solvent accessibility to a JSON file.

    Args:
    atoms (list): List of atoms with (atom_name, x, y, z) coordinates.
    residues (dict): Dictionary of residues {res_id: res_type}.
    accessibility (dict): Solvent accessibility per atom index.
    output_file (str): Path to the output JSON file.
    """
    # Prepare the data to be saved
    data = {
        'atoms': [{'atom_name': atom[0], 'coordinates': atom[1:]} for atom in atoms],
        'residues': residues,
        'accessibility': accessibility
    }

    # Write the data to the JSON file
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Data saved to {output_file}")

def main():
    """
    Main function to parse a PDB file, compute solvent accessibility, and save data to a file.
    """
    if len(sys.argv) < 3:
        print("Usage: python PDBparser.py <PDB_FILE> <OUTPUT_FILE>")
        sys.exit(1)

    file_path = sys.argv[1]
    output_file = sys.argv[2]

    # Parse PDB file
    atoms, residues = parse_pdb(file_path)

    # Compute solvent accessibility
    accessibility = compute_accessibility(atoms)

    # Save the data to a file
    save_data_to_file(atoms, residues, accessibility, output_file)

if __name__ == '__main__':
    main()