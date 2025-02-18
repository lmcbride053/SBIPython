import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import preprocess
    import features
    import train_model
    import predict
    import visualize
except ImportError as e:
    print(f"Error to import modules: {e}")
    sys.exit(1)

from Bio.Data.IUPACData import protein_letters_3to1

def three_to_one(residue):
    return protein_letters_3to1.get(residue.upper(), "X")  

def main(pdb_file):
    if not os.path.exists(pdb_file):
        print(f"Error: File {pdb_file} does not exist")
        sys.exit(1)

    try:
        # Step1: Preprocess
        preprocessed_data = preprocess.parse_pdb(pdb_file)
        features_data = preprocess.extract_features(preprocessed_data)
        formatted_data = preprocess.convert_structure_data(features_data)

        # Step2: Extraction
        physicochemical_features = features.compute_physicochemical(formatted_data)
        geometric_features = features.compute_geometric(formatted_data)
        evolutionary_features = features.compute_evolutionary(formatted_data)

        # Step3: Training
        training_data = train_model.load_training_data()
        model = train_model.train_classifier(training_data)
        train_model.save_model(model)

        # Step 4: Prediction
        trained_model = predict.load_model()
        binding_sites = predict.predict_binding_sites(trained_model, formatted_data)

        # Step 5: Visualization
        visualize.generate_output(binding_sites, output_format='pdb')
        visualize.highlight_predicted_sites(binding_sites)

        print("Pipeline executed with sucess.")
    except Exception as e:
        print(f"Error during the execution of pipeline: {e}")
        sys.exit(1)

if __name__ == "__main__":
    pdb_file = "path_to_your_pdb_file.pdb"  
    main(pdb_file)
