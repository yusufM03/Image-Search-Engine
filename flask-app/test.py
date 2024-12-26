#-----------------1. Feature extraction from images
import pandas as pd
import os
import numpy as np
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Model
from elasticsearch import Elasticsearch
import ElasticManager as ELA
# Load the VGG16 model with ImageNet weights
base_model = VGG16(weights='imagenet')
# Use the `fc2` layer as the output for feature extraction
feat_extractor = Model(inputs=base_model.input, outputs=base_model.get_layer("fc1").output)

# Define the path to the folder containing images
main_folder = "test_image"  

def extract_features(img_path):
    # Load and preprocess the image
    img = load_img(img_path, target_size=(224, 224))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)  
    x = preprocess_input (x)
    x=x/255.
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
    es=ELA.elasticsearchManager()
    
    img_name = os.path.join(main_folder, "images.jpeg")  # Ensure this image exists in the folder

    # Extract features from the specified image
    feature_vector = extract_features(img_name)


    
    # Perform search for similar images
    desired_tag=""
    similar_images = es.search_similar_images_tags("image-index-combination",feature_vector,desired_tag,)
    print("Similar Images:")
    for sim_img in similar_images:
        print(sim_img)

  
    
