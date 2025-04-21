import numpy as np
import scipy.spatial as spatial
from scipy.spatial import Delaunay
from scipy.spatial.qhull import QhullError
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import json
import sys

def compute_surface(pdb_data, accessibility_threshold=0.5):
    """
    Computes the molecular surface using Alpha Shapes (Delaunay triangulation).
    
    Args:
    pdb_data (dict): Parsed PDB data containing atoms, residues, and accessibility.
    accessibility_threshold (float): The minimum accessibility value for an atom to be considered accessible.
    
    Returns:
    surface_points (np.array): Surface points with (x, y, z).
    surface_properties (dict): Surface properties such as curvature and depth.
    """
    atoms = pdb_data['atoms']
    residues = pdb_data['residues']
    accessibility = pdb_data['accessibility']
    
    # Check the lengths of atoms and accessibility to ensure they are valid
    print(f"Total atoms: {len(atoms)}")
    
    # Extract coordinates of atoms that are accessible (above the threshold)
    accessible_atoms = [
        atom for i, atom in enumerate(atoms) if accessibility[str(i)] >= accessibility_threshold
    ]
    print(f"Accessible atoms count: {len(accessible_atoms)}")
    
    # If no accessible atoms, print the reason
    if not accessible_atoms:
        print("Warning: No accessible atoms found based on the accessibility data.")
        return None, None
    
    # Extract the coordinates of accessible atoms (coordinates are stored in 'coordinates' list)
    accessible_coords = np.array([atom['coordinates'] for atom in accessible_atoms])

    # Check the shape to ensure it is 2D with 3 coordinates per atom
    print(f"Accessible coordinates shape: {accessible_coords.shape}")

    if accessible_coords.shape[0] < 4:
        print("Error: Not enough accessible coordinates to perform Delaunay triangulation.")
        return None, None

    # Compute Delaunay triangulation (used for surface calculation)
    try:
        tri = Delaunay(accessible_coords)
    except QhullError:
        print("Error: Unable to compute Delaunay triangulation. Try a different distance threshold.")
        return None, None

    # Extract surface points from convex hull (used for Alpha Shape approximation)
    surface_indices = tri.convex_hull
    surface_points = accessible_coords[surface_indices.flatten()]

    # Compute surface properties (placeholder for curvature and depth)
    surface_properties = {
        'curvature': np.random.rand(len(surface_points)),  # Placeholder for curvature
        'depth': np.random.rand(len(surface_points))  # Placeholder for depth
    }

    print("Computed molecular surface.")
    return surface_points, surface_properties



def measure_pocket_depth(surface_points):
    """
    Estimates the depth of surface pockets based on distance from surface to protein core.
    
    Args:
    surface_points (np.array): Surface points with (x, y, z).
    
    Returns:
    pocket_depth (dict): Estimated depth of surface pockets.
    """
    # Placeholder: Random depth values
    pocket_depth = {i: np.random.rand() for i in range(len(surface_points))}

    print("Estimated pocket depth.")
    return pocket_depth

def calculate_hydrophobicity(residues):
    """
    Computes hydrophobicity scores for residues based on their type.
    
    Args:
    residues (dict): Dictionary of residues {res_id: res_type}.
    
    Returns:
    hydrophobicity (dict): Hydrophobicity scores per residue.
    """
    # Placeholder: Random hydrophobicity scores
    hydrophobicity = {res_id: np.random.rand() for res_id in residues}

    print("Computed hydrophobicity scores.")
    return hydrophobicity

def visualize_surface(surface_points, surface_properties, output_image_file):
    """
    Visualizes the molecular surface using PCA and t-SNE, and saves the plot as an image file.
    
    Args:
    surface_points (np.array): Surface points with (x, y, z).
    surface_properties (dict): Surface properties such as curvature and depth.
    output_image_file (str): Path to save the generated surface image.
    """
    # Perform PCA for dimensionality reduction
    pca = PCA(n_components=2)
    pca_points = pca.fit_transform(surface_points)

    # Perform t-SNE for further dimensionality reduction
    tsne = TSNE(n_components=2)
    tsne_points = tsne.fit_transform(surface_points)

    # Visualize the surface properties
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    for ax, points, title in zip(axes, [pca_points, tsne_points], ['PCA', 't-SNE']):
        scatter = ax.scatter(points[:, 0], points[:, 1], c=surface_properties['curvature'], cmap='viridis')
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])

    # Save the plot to the specified file
    plt.savefig(output_image_file, bbox_inches='tight')  # Save image without opening it
    plt.close()  # Close the plot to avoid displaying it
    print(f"Surface visualization saved to {output_image_file}")


def save_surface_data(surface_points, surface_properties, output_file):
    """
    Saves computed surface data to a JSON file.
    
    Args:
    surface_points (np.array): Surface points with (x, y, z).
    surface_properties (dict): Surface properties such as curvature and depth.
    output_file (str): Path to the output JSON file.
    """
    # Convert numpy arrays to lists for JSON serialization
    surface_points_list = surface_points.tolist()  # Convert to a list of lists

    # Convert numpy arrays inside surface_properties to lists
    surface_properties_list = {key: value.tolist() if isinstance(value, np.ndarray) else value
                               for key, value in surface_properties.items()}

    # Prepare the data to be saved
    data = {
        'surface_points': surface_points_list,
        'surface_properties': surface_properties_list
    }

    # Write the data to the JSON file
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Surface data saved to {output_file}")


def main(pdb_data, output_file, output_image_file):
    """
    Main function to compute surface properties, save data to a file, and save the surface visualization.
    
    Args:
    pdb_data (dict): Parsed PDB data containing atoms, residues, and accessibility.
    output_file (str): Path to the output JSON file.
    output_image_file (str): Path to save the generated surface image.
    """
    # Compute molecular surface
    surface_points, surface_properties = compute_surface(pdb_data)

    if surface_points is not None:
        # Measure pocket depth
        pocket_depth = measure_pocket_depth(surface_points)

        # Calculate hydrophobicity
        hydrophobicity = calculate_hydrophobicity(pdb_data['residues'])

        # Visualize the surface and save the plot to a file
        visualize_surface(surface_points, surface_properties, output_image_file)

        # Save the data to a file
        save_surface_data(surface_points, surface_properties, output_file)



if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python SurfAnal.py <PDB_DATA_FILE> <OUTPUT_FILE> <OUTPUT_IMAGE_FILE>")
        sys.exit(1)

    pdb_data_file = sys.argv[1]
    output_file = sys.argv[2]
    output_image_file = sys.argv[3]  # Add image file argument

    # Load parsed PDB data
    with open(pdb_data_file, 'r') as f:
        pdb_data = json.load(f)

    # Analyze the molecular surface
    main(pdb_data, output_file, output_image_file)


