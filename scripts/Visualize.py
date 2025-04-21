"""
visualization.py

Generates a PyMOL script to visualize predicted binding pockets from a scored JSON file.

Each pocket is represented as a colored sphere at its center, with color indicating rank.

Usage:
    python visualization.py <POCKET_JSON> <OUTPUT_PYMOL_SCRIPT>

Inputs:
    - POCKET_JSON: JSON file containing scored pockets with "center" coordinates.
    - OUTPUT_PYMOL_SCRIPT: File path to save the generated PyMOL script.
"""

import json
import sys

# Define a list of PyMOL colors for ranked pockets (can expand if needed)
RANK_COLORS = [
    "red",       # rank 1
    "orange",    # rank 2
    "yellow",    # rank 3
    "green",     # rank 4
    "cyan",      # rank 5
    "blue",      # rank 6
    "purple",    # rank 7
    "magenta",   # rank 8
    "gray70",    # rank 9
    "gray50"     # rank 10+
]

def generate_pymol_script(pockets, output_script):
    with open(output_script, 'w') as f:
        f.write("# PyMOL visualization script for predicted binding pockets\n")
        f.write("bg_color white\n")
        f.write("hide everything\n")
        f.write("show cartoon\n")
        f.write("color gray80\n")

        for i, pocket in enumerate(pockets):
            x, y, z = pocket['center']
            color = RANK_COLORS[i] if i < len(RANK_COLORS) else "gray50"
            f.write(f"pseudoatom pocket_{i}, pos=[{x:.3f}, {y:.3f}, {z:.3f}], color={color}\n")
            f.write(f"show spheres, pocket_{i}\n")
            f.write(f"set sphere_scale, 1.0, pocket_{i}\n")

        f.write("zoom\n")

    print(f"[✔] PyMOL script saved to: {output_script}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python Visualize.py <POCKET_JSON> <OUTPUT_PYMOL_SCRIPT>")
        sys.exit(1)

    pocket_json = sys.argv[1]
    output_script = sys.argv[2]

    with open(pocket_json, 'r') as f:
        pockets = json.load(f)

    generate_pymol_script(pockets, output_script)


if __name__ == "__main__":
    main()
