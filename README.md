Protein Ligand Binding Predictor

Final Project for SBI and Python Liam McBride and Regina Rodríguez Durant Reyes

This script, a Python-based pipeline was developed to visualize potential ligand binding sites on protein structures using a geometry-driven approach. The final visualization was rendered in PyMOL, providing an intuitive representation of the predicted pockets on the protein surface.

Requirements
<pre>Python 3.x 
mkdssp version 3.0.0 
Required Python packages:
– spicy.spatial (spatial, Delauanay and QhullError) 
– sklearn.decomposition (PCA)
– sklearn.manifold (TSNE)
– matplotlib.pyplot (plt)
– json 
- sys   </pre>

Usage
To use the program, follow these steps:

1. Clone this repository:
<pre> git clone https://github.com/lmcbride053/SBIPython.git </pre>

2. Install the required Python packages using pip
<pre> pip install biopython scipy scikit-learn matplotlib </pre>

3. Run the program with the following command-line arguments:
<pre>python main.py PDB_FILE OUTPUT_JSON SURFACE_JSON IMAGE_FILE POCKET_JSON </pre>


