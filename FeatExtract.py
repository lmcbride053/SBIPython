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


def load_json_file(input_file: str) -> List[Dict[str, Any]]:
    """
    Loads the JSON file containing detected pockets.

    Args:
        input_file (str): Path to the JSON file.

    Returns:
        List[Dict[str, Any]]: List of pockets with attributes.
    """
    try:
        with open(input_file, "r") as file:
            pockets = json.load(file)
        logging.info(f"Loaded {len(pockets)} pockets from {input_file}")
        return pockets
    except Exception as e:
        logging.error(f"Failed to load JSON file: {e}")
        return []


def extract_features(pockets: List[Dict[str, Any]]) -> List[Dict[str, float]]:
    """
    Generates a feature vector for each detected pocket.

    Args:
        pockets (List[Dict[str, Any]]): List of detected binding pockets with attributes.

    Returns:
        List[Dict[str, float]]: List of feature vectors as dictionaries.
    """
    feature_vectors = []
    
    for pocket in pockets:
        try:
            features = {
                "pocket_id": pocket.get("pocket_id", 0),
                "num_points": pocket.get("num_points", 0),
                "depth_mean": pocket.get("depth_mean", 0.0),
                "center_x": pocket["center"][0] if "center" in pocket else 0.0,
                "center_y": pocket["center"][1] if "center" in pocket else 0.0,
                "center_z": pocket["center"][2] if "center" in pocket else 0.0,
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
    # Load detected pockets from JSON
    input_json_file = "outputfile3.json" 
    pockets = load_json_file(input_json_file)

    # Extract features
    features = extract_features(pockets)

    # Save to CSV
    output_csv_file = "pocket_features.csv"
    save_features_to_csv(features, output_csv_file)

    print(f"Feature extraction complete. Check '{output_csv_file}'.")
