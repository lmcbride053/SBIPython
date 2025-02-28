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

import csv
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


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
            # Example feature extraction (replace with actual logic)
            features = {
                "volume": pocket.get("volume", 0.0),
                "surface_area": pocket.get("surface_area", 0.0),
                "hydrophobicity": pocket.get("hydrophobicity", 0.0),
                "polarity": pocket.get("polarity", 0.0),
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
    pockets = [
        {"volume": 150.5, "surface_area": 80.2, "hydrophobicity": 0.75, "polarity": 0.25},
        {"volume": 200.0, "surface_area": 95.0, "hydrophobicity": 0.80, "polarity": 0.20},
    ]

    # Extract features
    features = extract_features(pockets)

    # Save to CSV
    output_file = "pocket_features.csv"
    save_features_to_csv(features, output_file)

    print(f"Feature extraction complete. Check '{output_file}'.")
