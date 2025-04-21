# Protein Ligand Binding Predictor

## Ligand Binding Predictor using Geometry 

This program visualize potential ligand binding sites on protein structures using a geometry-driven approach. It identifies and ranks potential ligand binding pockets directly from protein PDB files by leveraging purely geometric features, such as surface depth and curvature. The final visualization is rendered in PyMOL, providing an intuitive representation of the predicted pockets on the protein surface.

## Features
* Geometry Approach: Focused on surface depth and density-based clustering.
* Educational Focus: Lightweight dependencies and a clear, modular design.
* Visualization: Output easily rendered in PyMOL for 3D exploration.


## Requirements
<pre>Python 3.x 
mkdssp version 3.0.0 
Required Python packages:
– spicy.spatial (spatial, Delaunay and QhullError) 
– sklearn.decomposition (PCA)
– sklearn.manifold (TSNE)
– matplotlib.pyplot (plt)
– json 
- sys   </pre>

## Installation
To use the program, follow these next steps:

1. Clone this repository:
<pre> git clone https://github.com/lmcbride053/SBIPython.git </pre>

2. Install the required Python packages using pip
<pre> pip install biopython scipy scikit-learn matplotlib </pre>

3. Run the program with the following command-line arguments:
<pre>python main.py [PATH to PDB FILE] [PDB Code] 
example: examples/pdb_examples/4q21.pdb 4Q21 </pre>


# Output 
The program will generate the following outputs:

* output_atoms.json: pre process file and extracts relevant atomic coordinates for surface analysis.

* output_pockets.pdb: Filters surface points by depth and clusters them using DBSCAN

* output_surface.json: Calculates point-wise geometric properties: depth from convex hull, curvature, and surface coordinates.

* output_pockets.json: Applies heuristics such as mean/max depth, cluster size, and compactness.

* output_pockets_pymol.pml and output_surface.png: Converts the top-ranked pockets into PyMOL-compatible scripts using color-coded spheres.


# Model Generator with PyMol

This script generates a geometry-based pipeline for predicting and visualizing ligand binding sites on protein structures. By relying solely on structural features such as surface depth, curvature, and enclosure without the need for ligand-bound complexes, this method offers an interpretable, and visually rich approach for pocket detection. The integration with PyMOL enables intuitive 3D inspection, making the pipeline a valuable educational tool and a practical framework for early stage drug discovery, and a comparative structural analysis.

## Requirements

<pre>Required Program:
- PyMol </pre>

## Usage
<pre>pymol
load protein.pdb
@output_pockets_pymol.pml </pre>


# Example of the Analysis 
In the following example, the adf.pdb file was used, which represents



