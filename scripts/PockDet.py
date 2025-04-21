"""
pocket_detection.py

Identifies potential binding pockets by clustering surface depressions 
and filtering based on volume and depth.

Functions:
- detect_pockets(surface_data): Uses a geometric method to detect potential ligand-binding pockets.
- filter_pockets(pockets): Filters pockets based on size and depth.

Input:
- Geometric features computed in `surface_analysis.py`.

Output:
- List of detected pockets with their properties, formatted for scoring.
"""

import json
import numpy as np
from sklearn.cluster import DBSCAN

def detect_pockets(surface_data, eps=2.0, min_samples=3):
    surface_points = np.array(surface_data['surface_points'])
    depth_values = np.array(surface_data['surface_properties']['depth'])

    print(f"Depth Min: {depth_values.min()}, Max: {depth_values.max()}, Mean: {depth_values.mean()}")

    depth_threshold = np.percentile(depth_values, 50)
    pocket_indices = np.where(depth_values >= depth_threshold)[0]
    pocket_points = surface_points[pocket_indices]

    print(f"Total surface points: {len(surface_points)}")
    print(f"Points above depth threshold: {len(pocket_points)}")

    if len(pocket_points) == 0:
        print("No points meet the depth threshold. Adjust thresholding.")
        return []

    for eps_test in [1.0, 1.5, 2.0, 2.5]:
        clustering_test = DBSCAN(eps=eps_test, min_samples=min_samples).fit(pocket_points)
        print(f"Eps: {eps_test}, Detected Clusters: {len(set(clustering_test.labels_)) - 1}")

    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(pocket_points)

    pockets = []
    for cluster_id in set(clustering.labels_):
        if cluster_id == -1:
            continue

        cluster_indices = np.where(clustering.labels_ == cluster_id)[0]
        cluster_points = pocket_points[cluster_indices]

        depth = float(depth_values[pocket_indices][cluster_indices].mean())
        volume = len(cluster_points)
        enclosure = min(1.0, len(cluster_points) / 500)  # Normalized placeholder
        curvature = -0.2  # Placeholder

        pocket = {
            'pocket_id': int(cluster_id),
            'num_points': len(cluster_points),
            'center': cluster_points.mean(axis=0).tolist(),
            'depth_mean': depth,
            'volume': volume,
            'depth': depth,
            'enclosure': enclosure,
            'curvature': curvature
        }
        pockets.append(pocket)

    print(f"Detected {len(pockets)} potential pockets.")
    return pockets

def filter_pockets(pockets, min_size=5, min_depth=0.3):
    filtered_pockets = [
        p for p in pockets
        if p['num_points'] >= min_size and p['depth_mean'] >= min_depth
    ]
    print(f"Filtered to {len(filtered_pockets)} pockets after applying constraints.")
    return filtered_pockets

def save_pockets_as_pdb(pockets, output_pdb):
    """
    Saves pocket centers as a PDB file for visualization.
    
    Args:
    - pockets (list): List of detected pockets with their center coordinates.
    - output_pdb (str): Output PDB file path.
    """
    with open(output_pdb, 'w') as f:
        for i, pocket in enumerate(pockets):
            x, y, z = pocket['center']
            f.write(f"HETATM{i:5d}  O   POCK    1    {x:8.3f}{y:8.3f}{z:8.3f}  1.00 20.00           O\n")

    print(f"Pockets saved to {output_pdb} for visualization.")

def main(input_json, output_json):
    with open(input_json, 'r') as f:
        surface_data = json.load(f)
    
    pockets = detect_pockets(surface_data)
    filtered_pockets = filter_pockets(pockets)

    with open(output_json, 'w') as f:
        json.dump(filtered_pockets, f, indent=4)

    output_pdb_file = output_json.replace(".json", ".pdb")
    save_pockets_as_pdb(filtered_pockets, output_pdb_file)
    
    print(f"Pockets saved to {output_json}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python PockDet.py <INPUT_JSON> <OUTPUT_JSON>")
        sys.exit(1)
    
    input_json = sys.argv[1]
    output_json = sys.argv[2]
    
    main(input_json, output_json)
