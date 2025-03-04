"""
visualization.py

Generates visualization files for PyMOL or Chimera to display predicted ligand-binding sites.

Functions:
- generate_pymol_script(predicted_sites, pdb_file, output_script): Generates a PyMOL script.
- generate_chimera_script(predicted_sites, pdb_file, output_script): Generates a Chimera script.

Input:
- Predicted binding sites from `model_prediction.py`.
- Original PDB file.

Output:
- PyMOL and Chimera visualization scripts.
"""

import pandas as pd

def generate_pymol_script(predicted_sites, pdb_file, output_script):
    """Creates a PyMOL script to highlight predicted binding sites."""
    try:
        with open(output_script, 'w') as file:
            # Write the PDB file into the script
            file.write(f"load {pdb_file}\n")
            
            # Add commands for each predicted binding site (assuming the predictions are indices)
            for i, prediction in enumerate(predicted_sites):
                if prediction == 1:  # If the prediction is 1 (binding site)
                    # Highlight binding site by creating a sphere at the predicted location
                    file.write(f"create binding_site_{i}, (resi {i+1})\n")  # Adjust depending on your prediction format
                    file.write(f"show spheres, binding_site_{i}\n")
                    file.write(f"set sphere_scale, 0.5, binding_site_{i}\n")
                    file.write(f"color red, binding_site_{i}\n")
            
            file.write("show sticks\n")  # Show protein sticks
            file.write("set stick_radius, 0.2\n")
            file.write("set stick_color, gray\n")
            
            print(f"PyMOL script generated: {output_script}")
    except Exception as e:
        print(f"Error generating PyMOL script: {e}")

def generate_chimera_script(predicted_sites, pdb_file, output_script):
    """Creates a Chimera script for visualization."""
    try:
        with open(output_script, 'w') as file:
            # Write the PDB file into the script
            file.write(f"open {pdb_file}\n")
            
            # Add commands for each predicted binding site
            for i, prediction in enumerate(predicted_sites):
                if prediction == 1:  # If the prediction is 1 (binding site)
                    # Highlight binding site by creating a sphere at the predicted location
                    file.write(f"show sphere radius 1.0 at {i+1}\n")
                    file.write(f"color red #{i+1}\n")
            
            file.write("color gray #0\n")  # Default color for the protein
            file.write("show sticks\n")  # Show protein as sticks
            
            print(f"Chimera script generated: {output_script}")
    except Exception as e:
        print(f"Error generating Chimera script: {e}")

def main(predictions_file, pdb_file, output_script, tool="pymol"):
    """Load predictions and generate visualization script."""
    # Load predictions
    try:
        predictions_df = pd.read_csv(predictions_file)
        predicted_sites = predictions_df['binding_site_prediction'].tolist()
        print(f"Loaded predictions: {predicted_sites}")
    except Exception as e:
        print(f"Error loading predictions: {e}")
        return
    
    # Generate the visualization script for the chosen tool
    if tool.lower() == "pymol":
        generate_pymol_script(predicted_sites, pdb_file, output_script)
    elif tool.lower() == "chimera":
        generate_chimera_script(predicted_sites, pdb_file, output_script)
    else:
        print("Unsupported tool specified. Please choose either 'pymol' or 'chimera'.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate PyMOL/Chimera scripts for predicted binding sites.")
    parser.add_argument("predictions_file", type=str, help="Path to the CSV file containing the predicted binding sites.")
    parser.add_argument("pdb_file", type=str, help="Path to the original PDB file.")
    parser.add_argument("output_script", type=str, help="Path to the output visualization script.")
    parser.add_argument("--tool", type=str, default="pymol", choices=["pymol", "chimera"], help="Visualization tool to generate the script for (default is PyMOL).")

    args = parser.parse_args()

    main(args.predictions_file, args.pdb_file, args.output_script, args.tool)
    