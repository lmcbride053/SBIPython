"""
main.py

Master script to run the full ligand binding site prediction pipeline using a purely geometric approach.

Steps:
1. Parse protein PDB file to extract atomic coordinates.
2. Run surface analysis to compute geometric features.
3. Detect and filter potential ligand-binding pockets.
4. Score pockets using geometric heuristics.
5. Generate a PyMOL visualization script for ranked pockets.

Usage:
    python main.py <INPUT_PDB> <OUTPUT_PREFIX>

Project Structure:
    ├── scripts/
    │   ├── PDBParser.py
    │   ├── SurfAnal.py
    │   ├── PockDet.py
    │   ├── Scoring.py
    │   └── Visualize.py
    └── results/
        └── <OUTPUT_PREFIX>/
"""

import os
import sys
import subprocess

SCRIPT_DIR = os.path.join(os.path.dirname(__file__), 'scripts')
RESULTS_DIR = os.path.join(os.path.dirname(__file__), 'results')

def run_step(script_name, args=[]):
    """Run a Python script in the 'scripts' folder with the provided arguments."""
    script_path = os.path.join(SCRIPT_DIR, script_name)
    print(f"🔹 Running {script_name} with args: {' '.join(args)}")
    result = subprocess.run(['python', script_path] + args)
    if result.returncode != 0:
        print(f"❌ Error while running {script_name}")
        sys.exit(result.returncode)
    print(f"✅ {script_name} completed.\n")

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <INPUT_PDB> <OUTPUT_PREFIX>")
        sys.exit(1)

    pdb_file = sys.argv[1]
    prefix = sys.argv[2]

    # Create results/<prefix>/ directory
    output_dir = os.path.join(RESULTS_DIR, prefix)
    os.makedirs(output_dir, exist_ok=True)

    # Output file paths
    parsed_json   = os.path.join(output_dir, "parsed.json")
    surface_json  = os.path.join(output_dir, "surface.json")
    surface_plot  = os.path.join(output_dir, "surface.png")
    pockets_json  = os.path.join(output_dir, "pockets.json")
    scored_json   = os.path.join(output_dir, "scored.json")
    pymol_script  = os.path.join(output_dir, "pockets.pml")

    # Run the pipeline steps
    run_step("PDBParser.py", [pdb_file, parsed_json])
    run_step("SurfAnal.py", [parsed_json, surface_json, surface_plot])
    run_step("PockDet.py", [surface_json, pockets_json])
    run_step("Scoring.py", [pockets_json, scored_json])
    run_step("Visualize.py", [scored_json, pymol_script])

    print(f"🎉 All results saved to: {output_dir}/")

if __name__ == "__main__":
    main()
