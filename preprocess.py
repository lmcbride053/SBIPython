"""
preprocess.py - PDB File Preprocessing Module

This script handles preprocessing of protein structure files (.pdb) to prepare them 
for machine learning-based ligand binding site prediction.

Functions:
1. **PDB Parsing**: Extracts atomic and residue-level data using Biopython.
2. **Data Cleaning**: Removes missing residues, alternative conformations, or non-standard residues.
3. **Surface Accessibility Calculation**: Identifies exposed residues.
4. **Secondary Structure Extraction**: Uses DSSP to determine α-helices, β-sheets, and loops.
5. **Data Structuring**: Converts extracted information into an organized format (e.g., Pandas DataFrame, JSON, or NumPy array).

Expected Input:
- A PDB file containing the 3D structure of a protein.

Expected Output:
- A cleaned and structured representation of the protein (e.g., residue lists, atomic coordinates).
- A file or in-memory object ready for feature extraction (e.g., CSV, JSON, or pickle file).

Dependencies:
- Biopython (for PDB parsing)
- DSSP (for secondary structure analysis)
"""

# Import necessary libraries
import os
import numpy as np
import pandas as pd
from Bio.PDB import PDBParser, DSSP
from Bio.PDB.DSSP import make_dssp_dict
from Bio.PDB.Polypeptide import PPBuilder
from Bio.PDB.ResidueDepth import ResidueDepth
from Bio.PDB.Polypeptide import three_to_one
from Bio.PDB.Polypeptide import is_aa
from Bio.PDB.Polypeptide import is_aa_residue
from Bio.PDB.Polypeptide import aa1
from Bio.PDB.Polypeptide import aa3

# Define the preprocess function
def preprocess_pdb(pdb_file, output_dir=None):
    """
    Preprocess a PDB file to extract atomic and residue-level information.
    
    Parameters:
    - pdb_file (str): Path to the input PDB file.
    - output_dir (str): Directory to save the preprocessed data (default: None).
    
    Returns:
    - dict: A dictionary containing the preprocessed data.
    """
    # Initialize the parser
    parser = PDBParser(QUIET=True)
    
    # Load the structure
    structure = parser.get_structure('protein', pdb_file)
    
    # Extract the chain ID
    chain_id = list(structure.get_chains())[0].id
    
    # Extract the sequence
    ppb = PPBuilder()
    sequence = ''
    for pp in ppb.build_peptides(structure[0][chain_id]):
        sequence += str(pp.get_sequence())
    
    # Extract the secondary structure
    dssp = DSSP(structure[0], pdb_file)
    dssp_dict = make_dssp_dict(dssp)
    ss = [dssp_dict[aa][2] for aa in dssp_dict]
    
    # Extract the residue depth
    rd = ResidueDepth(structure[0])
    residue_depth = [rd[residue_id] for residue_id in rd]
    
    # Extract the residue information
    residues = []
    for residue in structure[0][chain_id]:
        if is_aa_residue(residue):
            res_id = residue.get_id()[1]
            res_name = three_to_one(residue.get_resname())
            res_depth = residue_depth[res_id - 1]
            res_ss = ss[res_id - 1]
            res_coords = residue["CA"].get_coord()
            residues.append((res_id, res_name, res_depth, res_ss, res_coords))
    
    # Create a DataFrame from the extracted data
    columns = ['residue_id', 'residue_name', 'residue_depth', 'secondary_structure', 'coordinates']
    df = pd.DataFrame(residues, columns=columns)
    
    # Save the preprocessed data
    if output_dir:
        output_file = os.path.join(output_dir, f'{os.path.basename(pdb_file).split(".")[0]}_preprocessed.csv')
        df.to_csv(output_file, index=False)
    
    return df

# Define the main function
def main():
    # Define the input PDB file
    pdb_file = 'data/1AK4.pdb'
    
    # Preprocess the PDB file
    preprocessed_data = preprocess_pdb(pdb_file, output_dir='output')
    
    # Display the preprocessed data
    print(preprocessed_data)

# Execute the main function
if __name__ == '__main__':
    main()

# End of preprocess.py