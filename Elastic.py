import pandas as pd
from elasticsearch import Elasticsearch, helpers

# Connect to Elasticsearch with options
es = Elasticsearch("http://localhost:9200").options(ignore_status=[400, 404])

# Define the index name
index_name = "image-index"

# Check if the index already exists and delete it if it does
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
    print(f"Index '{index_name}' deleted.")

# Create the new index
resp = es.indices.create(
    index=index_name,
    mappings={
        "properties": {
            "image-vector": {
                "type": "dense_vector",
                "dims": 4096,
                "similarity": "cosine"
            },
            "title": {
                "type": "text"
            },
        }
    },
)
print(f"Index '{index_name}' created.")

# Function to inject data into Elasticsearch
def injection(index, es):
    df = pd.read_csv('image_features.csv')  # Load your CSV file
    print("Dataframe loaded. Here are the first few rows:")
    print(df.head())  # Check the first few rows
    
    # Process the image vectors from string to list of floats
    df['image_vector'] = df['image_vector'].apply(lambda x: list(map(float, x.split(','))))
    print("Processed image vectors:")
    print(df['image_vector'].head())

    # Prepare the data for bulk indexing
    actions = []
    for idx, row in df.iterrows():
        request = {
            "_index": index,
            "_id": str(idx), 
            "_source": {
                "image-vector": row['image_vector'],  
                "title": row['image_name']  # Ensure this matches your CSV column name
            }
        }
        actions.append(request)

    try:
        # Perform bulk indexing
        res = helpers.bulk(es, actions)
        print("Indexing successful:", res)
    except Exception as e:
        print("Indexing failed:", e)
        if isinstance(e, helpers.BulkIndexError):
            for failed in e.errors:
                print("Failed to index:", failed)
        else:
            print("An unexpected error occurred.")

# Call the injection function
injection(index_name, es)

# Check the number of documents in the index after injection
doc_count = es.cat.count(index=index_name, format='json')
print("Documents in index:", doc_count)
