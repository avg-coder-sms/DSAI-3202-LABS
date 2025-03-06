import numpy as np
import skimage.feature as feature
from multiprocessing import Pool

def compute_glcm_features(image, filter_name):
    """
    Computes GLCM (Gray Level Co-occurrence Matrix) features for an image.

    Parameters:
    - image: A 2D array representing the image. Should be in grayscale.
    - filter_name: A string representing the name of the filter applied to the image.

    Returns:
    - features: A dictionary containing the computed GLCM features.
    """
    image = (image * 255).astype(np.uint8)
    graycom = feature.graycomatrix(image, [1], [0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256, symmetric=True, normed=True)

    features = {}
    for prop in ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']:
        values = feature.graycoprops(graycom, prop).flatten()
        for i, value in enumerate(values):
            features[f'{filter_name}_{prop}_{i+1}'] = value
    return features

def process_image(image_data):
    """Helper function to process a single image"""
    filter_name, image, tumor_presence = image_data
    glcm_features = compute_glcm_features(image, filter_name)
    glcm_features['Tumor'] = tumor_presence
    return glcm_features

def process_images_parallel(images_list, tumor_presence):
    """
    Processes a list of images, applies filters, computes GLCM features in parallel, and adds a "Tumor" key.
    """
    image_data_list = [(key, image, tumor_presence) for filtered_images in images_list for key, image in filtered_images.items()]
    
    with Pool() as pool:
        glcm_features_list = pool.map(process_image, image_data_list)
    
    return glcm_features_list
