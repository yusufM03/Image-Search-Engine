import pandas as pd
import os
import numpy as np
import json
import matplotlib.pyplot as plt
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model



#-----------------1.Feature extraction from images
base_model = VGG16(weights='imagenet')
# Use the `fc2` layer as the output for feature extraction
feat_extractor = Model(inputs=base_model.input, outputs=base_model.get_layer("fc2").output)

# Step 2: Define Image Processing Function
import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from concurrent.futures import ThreadPoolExecutor

# Define the path to the folder containing images
main_folder = "images/0"
all_features = {}

# Load and preprocess the image
def load_and_preprocess_image(img_path):
    try:
        img = load_img(img_path, target_size=(224, 224))  # Resize to VGG16 expected input
        x = img_to_array(img)
        x = np.expand_dims(x, axis=0)  # Add batch dimension
        x = x / 255.0  # Normalize if needed
        return x
    except Exception as e:
        print(f"Error loading {img_path}: {e}")
        return None

# Function to extract features from an image
def extract_features(img_name):
    img_path = os.path.join(main_folder, img_name)
    x = load_and_preprocess_image(img_path)
    if x is not None:
        features = feat_extractor.predict(x)[0]  # Get the feature vector for the image
        return img_name, features
    return None

# Use ThreadPoolExecutor for concurrent processing
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(extract_features, img_name) for img_name in os.listdir(main_folder)]

    for future in futures:
        result = future.result()
        if result is not None:
            img_name, features = result
            all_features[img_name] = features
            print(f"Processed: {img_name}")

print("Feature extraction completed.")

# Step 4: Convert Extracted Features into a DataFrame for CSV Export
# Prepare a list to hold image data for the DataFrame
image_data = []

# Loop through each image and its corresponding features
for img_name, features in all_features.items():
    image_data.append({
        "image_name": img_name,
        "image_vector": features
    })

# Create a DataFrame
df = pd.DataFrame(image_data)

# Convert the `image_vector` list into a comma-separated string for CSV storage
df['image_vector'] = df['image_vector'].apply(lambda x: ','.join(map(str, x)))

# Step 5: Save DataFrame to CSV
output_csv_path = 'image_features.csv'
df.to_csv(output_csv_path, index=False)

print(f"Features successfully extracted and saved to {output_csv_path}")