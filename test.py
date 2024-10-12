#-----------------1. Feature extraction from images
import pandas as pd
import os
import numpy as np
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Model
from elasticsearch import Elasticsearch

# Load the VGG16 model with ImageNet weights
base_model = VGG16(weights='imagenet')
# Use the `fc2` layer as the output for feature extraction
feat_extractor = Model(inputs=base_model.input, outputs=base_model.get_layer("fc2").output)

# Define the path to the folder containing images
main_folder = "test_image"  

def extract_features(img_path):
    # Load and preprocess the image
    img = load_img(img_path, target_size=(224, 224))
    #img_array = img_to_array(img)
    #img_array = np.expand_dims(img_array, axis=0)
    #img_array = preprocess_input(img_array)  # Preprocess the image
    #img = load_img(img_path, target_size=(224, 224))  # Resize to VGG16 expected input
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)  # Add batch dimension
    x = x / 255.0  # Normalize if needed
    features = feat_extractor.predict(x)  # Extract features
    return features.flatten().tolist()  # Flatten the features and convert to list

# Function to search for similar images

def search_similar_images(es,feature_vector, top_n=5):
  

    
    response = es.search(
    index="image-index",
    knn={
        "field": "image-vector",
        "query_vector":feature_vector,
        "k": 30,
        "num_candidates": 150
    },
    fields=[
        "title"
        ],
    )
    
    
    # Retrieve and print the results
    similar_images = []
    for hit in response['hits']['hits']:
        print(hit["_index"])
        print(hit["_score"])
        print(hit["_source"]["title"])

        
      
        
        print("################")
        
    return similar_images

# Example usage
if __name__ == "__main__":
    es = Elasticsearch("http://localhost:9200")
    
    img_name = os.path.join(main_folder, "images.jpg")  # Ensure this image exists in the folder

    # Extract features from the specified image
    feature_vector = extract_features(img_name)


    
    # Perform search for similar images
    similar_images = search_similar_images(es,feature_vector, 5)
    print("Similar Images:")
    for sim_img in similar_images:
        print(sim_img)

  
    
