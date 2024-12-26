import pandas as pd
import os
import numpy as np
import json
import matplotlib.pyplot as plt
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from sklearn.decomposition import PCA
import joblib

#-----------------1.Feature extraction from images


# Step 2: Define Image Processing Function
import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from concurrent.futures import ThreadPoolExecutor



class Feature_Extractor():
    def __init__(self,last_layer) :
        base_model = VGG16(weights='imagenet')
        self.feat_extractor=Model(inputs=base_model.input, outputs=base_model.get_layer(last_layer).output)
    
    def load_and_preprocess_image(self,img_path):
      try:
          img = load_img(img_path, target_size=(224, 224))  # Resize to VGG16 expected input
          x = img_to_array(img)
          x = np.expand_dims(x, axis=0)  
          x = preprocess_input (x)
          x=x/255.   
          return x
      except Exception as e:
          print(f"Error loading {img_path}: {e}")
          return None
    # Function to extract features from an image
    def extract_features(self,img_path):
        x = self.load_and_preprocess_image(img_path)
        
        features = self.feat_extractor.predict(x)
        
        return  os.path.basename(img_path),features.flatten().tolist()  
        
    

    def reduce_Dimension(self,features):
        features=np.array(features)
        pca=PCA(n_components=300)
        pca.fit(features)
        pca_features=pca.transform(features)
        joblib.dump(pca,"pca.joblib")
        return pca_features





def main():
    
    Feature_Extractor_model=Feature_Extractor("fc1")
    # Define the path to the folder containing images
    main_folder = "static/Data/4"
    all_features = {}

    # Use ThreadPoolExecutor for concurrent processing
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(Feature_Extractor_model.extract_features, os.path.join(main_folder,img_name)) for img_name in os.listdir(main_folder)]

        for future in futures:
            result = future.result()
            if result is not None:
                img_name, features = result
                all_features[img_name] = features
                print(f"Processed: {img_name}")

    print("Feature extraction completed.")
    

  

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
    output_csv_path = 'image_features_4.csv'
    df.to_csv(output_csv_path, index=False)

    print(f"Features successfully extracted and saved to {output_csv_path}")


if __name__== "__main__":
  main()
