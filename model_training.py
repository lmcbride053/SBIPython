"""
Trains a Random Forest classifier using extracted pocket features and known binding site labels.

Functions:
- train_model(training_data, target_column, **rf_params): Trains a Random Forest model.
- save_model(model, output_path): Saves the trained model.

Input:
- A CSV file with pocket features and binding site labels.

Output:
- A trained Random Forest model saved as a `.pkl` file.
"""

import pandas as pd
import joblib
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def train_model(training_data, target_column, test_size=0.2, random_state=42, **rf_params):
    """Trains a Random Forest classifier on extracted pocket features."""
    logging.info("Loading data...")
    if isinstance(training_data, str):
        df = pd.read_csv(training_data)
    else:
        df = training_data  # Assume it's already a DataFrame

    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset.")

    X = df.drop(columns=[target_column])
    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    logging.info("Training Random Forest model...")
    model = RandomForestClassifier(**rf_params)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    logging.info(f"Model training complete. Accuracy: {accuracy:.4f}")

    return model

def save_model(model, output_path):
    """Saves the trained model to disk."""
    logging.info(f"Saving model to {output_path}...")
    joblib.dump(model, output_path)
    logging.info("Model saved successfully.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train a Random Forest model on pocket features.")
    parser.add_argument("input_csv", type=str, help="Path to input CSV file.")
    parser.add_argument("output_model", type=str, help="Path to save the trained model.")
    parser.add_argument("target_column", type=str, help="Name of the target column.")

    args = parser.parse_args()

    trained_model = train_model(args.input_csv, args.target_column, n_estimators=100)
    save_model(trained_model, args.output_model)
