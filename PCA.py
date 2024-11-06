import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import joblib
df=pd.read_csv("image_features_withoutpca.csv")

features=df['image_vector'].apply(lambda x: list(map(float, x.split(','))))

features=np.array(features.to_list())

def reduce_Dimension(features):
  
  
    
    pca=PCA(n_components=300)
    pca.fit(features)
    pca_features=pca.transform(features)
    print(pca_features.shape)
    joblib.dump(pca,"pca_model.joblib")
    return pca_features

print(len(df))
pca_features=reduce_Dimension(features)


image_data = []


for img_name,image_vector  in zip(df["image_name"].to_list(),pca_features):
    
    image_data.append({
        "image_name": img_name,
        "image_vector": image_vector
    })
  



# Create a DataFrame
df_pca = pd.DataFrame(image_data)
print(len(df_pca))
# Convert the `image_vector` list into a comma-separated string for CSV storage
df_pca['image_vector'] = df_pca['image_vector'].apply(lambda x: ','.join(map(str, x)))

# Step 5: Save DataFrame to CSV
output_csv_path = 'image_features_pca.csv'
df.to_csv(output_csv_path, index=False)

print(f"Features successfully extracted and saved to {output_csv_path}")