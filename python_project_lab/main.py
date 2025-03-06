import time
import pandas as pd
from src.image_processing import process_images_parallel
from src.machine_learning import train_and_evaluate_models_parallel
from src.utils import load_images

def main():
    # Load and preprocess images
    yes_inputs, no_inputs = load_images()
    
    # Process the images to compute GLCM features in parallel
    yes_glcm_features = process_images_parallel(yes_inputs, 1)
    no_glcm_features = process_images_parallel(no_inputs, 0)
    
    # Combine all features into a single DataFrame
    all_glcm_features = yes_glcm_features + no_glcm_features
    dataframe = pd.DataFrame(all_glcm_features)

    # Shuffle the DataFrame
    shuffled_dataframe = dataframe.sample(frac=1).reset_index(drop=True)

    # Split data into X (features) and y (target)
    X = shuffled_dataframe.drop(columns=["Tumor"])
    y = shuffled_dataframe["Tumor"]
    
    # Train and evaluate models in parallel
    results = train_and_evaluate_models_parallel(X, y)
    
    # Print results
    print(results)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"Execution Time: {time.time() - start_time} seconds")
