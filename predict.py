import joblib
import sys
from Bio import PDB  

def load_model(model_path):
    """Loads a trained model from the specified path."""
    return joblib.load(model_path)

def parse_protein_structure(pdb_file):
    """Parses a PDB file and extracts relevant features for prediction."""
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure("protein", pdb_file)
    return structure

def extract_features(protein_structure):
    """Extracts features from the protein structure for the model."""
    features = []
    for model in protein_structure:
        for chain in model:
            for residue in chain:
                features.append(residue.get_resname())  
    return features 

def output_binding_sites(binding_sites, output_file):
    """Outputs a list of residues in predicted binding sites to a file."""
    with open(output_file, 'w') as f:
        for site in binding_sites:
            f.write(f"{site}\n")

def predict_binding_sites(model, protein_structure):
    """Predicts binding sites on new protein structures."""
    features = extract_features(protein_structure)
    return model.predict([features])  # Ensure the model can handle this input

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python predict.py <model_path> <protein_structure> <output_file>")
        sys.exit(1)

    model_path = sys.argv[1]
    protein_structure_path = sys.argv[2]
    output_file = sys.argv[3]

    model = load_model(model_path)
    protein_structure = parse_protein_structure(protein_structure_path)  # Load and parse PDB file
    binding_sites = predict_binding_sites(model, protein_structure)
    output_binding_sites(binding_sites, output_file)
