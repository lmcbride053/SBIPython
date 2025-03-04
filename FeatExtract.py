"""
Extracts numerical features from detected binding pockets to be used as input 
for the Random Forest model.

Functions:
- extract_features(pockets): Converts pocket data into feature vectors.
- save_features_to_csv(features, output_file): Saves extracted features in CSV format.

Input:
- List of detected pockets from `pocket_detection.py`.

Output:
- CSV file containing feature vectors for ML training.
"""
import json
import csv
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def extract_features(pockets: List[Dict[str, Any]]) -> List[Dict[str, float]]:
    """
    Generates a feature vector for each detected pocket, including a binding site label.
    
    Args:
        pockets (List[Dict[str, Any]]): List of detected binding pockets with attributes.
    
    Returns:
        List[Dict[str, float]]: List of feature vectors as dictionaries.
    """
    feature_vectors = []
    
    for pocket in pockets:
        try:
            # Example feature extraction (replace with actual logic)
            features = {
                "pocket_id": pocket.get("pocket_id", 0),
                "num_points": pocket.get("num_points", 0),
                "depth_mean": pocket.get("depth_mean", 0.0),
                "center_x": pocket.get("center", [0, 0, 0])[0],
                "center_y": pocket.get("center", [0, 0, 0])[1],
                "center_z": pocket.get("center", [0, 0, 0])[2],
                "binding_site_label": 1 if pocket.get("depth_mean", 0.0) > 0.8 else 0  # Labeling rule
            }
            feature_vectors.append(features)
        except Exception as e:
            logging.error(f"Error processing pocket: {e}")

    logging.info(f"Extracted {len(feature_vectors)} feature vectors.")
    return feature_vectors


def save_features_to_csv(features: List[Dict[str, float]], output_file: str) -> None:
    """
    Saves feature vectors to a CSV file.
    
    Args:
        features (List[Dict[str, float]]): List of feature vectors.
        output_file (str): Path to the output CSV file.
    """
    if not features:
        logging.warning("No features to save.")
        return
    
    fieldnames = features[0].keys()

    try:
        with open(output_file, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(features)

        logging.info(f"Features saved to {output_file}")
    except Exception as e:
        logging.error(f"Failed to save CSV: {e}")


if __name__ == "__main__":
    # Example pocket data (Replace this with actual data from pocket_detection.py)
    with open("outputfile3.json", "r") as f:
        pockets = json.load(f)  # Assuming this is how the pockets data is loaded

    # Extract features
    features = extract_features(pockets)

    # Save to CSV
    output_file = "pocket_features.csv"
    save_features_to_csv(features, output_file)

    print(f"Feature extraction complete. Check '{output_file}'.")
