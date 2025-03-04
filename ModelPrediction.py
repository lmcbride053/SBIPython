"""
model_prediction.py

Uses a trained Random Forest model to predict ligand binding sites on new proteins.

Functions:
- load_model(model_path): Loads a trained model.
- predict_binding_sites(model, test_data): Predicts binding sites using extracted pocket features.

Input:
- A trained model and extracted features from `feature_extraction.py`.

Output:
- Predicted binding site locations.
"""
import joblib
import pandas as pd
import logging
import argparse
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_model(model_path):
    """Loads a pre-trained Random Forest model."""
    try:
        model = joblib.load(model_path)
        logging.info(f"Model loaded from {model_path}")
        return model
    except Exception as e:
        logging.error(f"Failed to load model: {e}")
        return None

def predict_binding_sites(model, test_data):
    """Predicts binding sites based on pocket features."""
    try:
        # Drop the 'pocket_id' and 'binding_site_label' columns (only features should be passed)
        if 'pocket_id' in test_data.columns:
            test_data = test_data.drop(columns=["pocket_id"])

        if 'binding_site_label' in test_data.columns:
            test_data = test_data.drop(columns=["binding_site_label"])

        # Extract features from test data (ensure we have only the feature columns)
        X_test = test_data
        
        # Make predictions
        predictions = model.predict(X_test)
        
        logging.info(f"Predictions made on {len(test_data)} samples.")
        return predictions
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        return None

def main(model_path, test_data_path, output_predictions_path):
    """Main function to load model, predict binding sites, and output predictions."""
    # Load model
    model = load_model(model_path)
    if model is None:
        return
    
    # Load test data (features)
    try:
        test_data = pd.read_csv(test_data_path)
        logging.info(f"Test data loaded from {test_data_path} with {len(test_data)} samples.")
    except Exception as e:
        logging.error(f"Failed to load test data: {e}")
        return

    # Predict binding sites
    predictions = predict_binding_sites(model, test_data)

    if predictions is not None and predictions.size > 0:
        logging.info(f"Predictions: {predictions}")
        # Save predictions to CSV for visualization script
        predictions_df = pd.DataFrame(predictions, columns=["binding_site_prediction"])
        predictions_df.to_csv(output_predictions_path, index=False)
        logging.info(f"Predictions saved to {output_predictions_path}")
    else:
        logging.error("No predictions made.")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict binding sites using a trained Random Forest model.")
    parser.add_argument("model_path", type=str, help="Path to the trained Random Forest model.")
    parser.add_argument("test_data_path", type=str, help="Path to the test data CSV file containing pocket features.")
    parser.add_argument("output_predictions_path", type=str, help="Path to save the predicted binding sites.")

    args = parser.parse_args()

    main(args.model_path, args.test_data_path, args.output_predictions_path)

