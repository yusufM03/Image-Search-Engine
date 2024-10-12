#-------------- 3. Define the Index Mapping:---------------------------------#
from elasticsearch import Elasticsearch, helpers
import pandas as pd
import json

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")  

# Define the index mapping for k-NN
index = 'similarity'

# Define the settings for the index
settings = {
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "elastiknn": True  # Ensure the elastiknn plugin is enabled
  }
}

# Define the mapping for the index
mapping = {
  "mappings": {  # Corrected to include "mappings"
    "dynamic": False,
    "properties": {
      "imageId": { "type": "keyword" },
      "featureVec": {
        "type": "elastiknn_dense_float_vector",
        "elastiknn": {
          "dims": 4096,
          "model": "lsh",
          "similarity": "l2",
          "L": 60,
          "k": 3,
          "w": 2
        }
      }
    }
  }
}

# Create the index if it doesn't exist
if not es.indices.exists(index):
    es.indices.create(index=index, body=settings)  # Use body parameter to create index
    es.indices.put_mapping(index=index, body=mapping)  # Use body parameter for mapping
#else:
    #es.indices.put_mapping(index=index, body=mapping)  # Update mapping if index exists

# Retrieve and print the mapping for verification
mapping_info = es.indices.get_mapping(index=index)  # Use keyword arguments
print(mapping_info)
def injection(index, es, helpers):
    df = pd.read_csv('image_features.csv')  # Load your CSV file

    # Prepare the data for bulk indexing
    actions = []
    for idx, row in df.iterrows():
        request = {
            "_index": index,
            "_id": str(row.iloc[0]),  
            "_source": {
                "imageId": row.iloc[0],  
                "featureVec": row.iloc[1:].tolist()  
            }
        }
        actions.append(request)

    try:
        # Perform bulk indexing
        res = helpers.bulk(es, actions)  # No need for 'index' parameter here, actions contain the index
        print("Indexing successful:", res)
    except Exception as e:
        print("Indexing failed:", e)
        if isinstance(e, helpers.BulkIndexError):
            for failed in e.errors:  # Extract detailed failure messages
                print("Failed to index:", failed)
        else:
            print("An unexpected error occurred.")

# Call the injection function
#injection(index, es, helpers)
