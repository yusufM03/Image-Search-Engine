import pandas as pd
from elasticsearch import Elasticsearch, helpers
import os

class elasticsearchManager ():
    def __init__(self) :
        self.connect= Elasticsearch(["http://localhost:9200"])
    def create_index_combination(self,index_name):
      # Create the new index with mappings
      try:
          resp = self.connect.indices.create(
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
                      "tags": {  # Add the tags field
                           "type": "text"
                      }
                  }
              },
          )
          print(f"Index '{index_name}' created.")
      except Exception as e:
          print(f"Failed to create index: {e}")

    
    def create_index(self,index_name):
      # Create the new index with mappings
      try:
          resp = self.connect.indices.create(
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
      except Exception as e:
          print(f"Failed to create index: {e}")

    def delete_index(self,index_name):
          
      # Check if the index already exists and delete it if it does
      if self.connect.indices.exists(index=index_name):
          self.connect.indices.delete(index=index_name)
          print(f"Index '{index_name}' deleted.")

      
    def injection(self,index,csv_path):
      try:
          df = pd.read_csv(csv_path)  # Load your CSV file
          print(f"Data CSV: {csv_path}")
          print(f"Number of rows in the CSV: {len(df)}")
          
          # Convert 'image_vector' column from string to list of floats
          df['image_vector'] = df['image_vector'].apply(lambda x: list(map(float, x.split(','))))
          print("Processed image vectors:")
          print(df['image_vector'].head())

          def load_tags(title):
            tags_file_path=os.path.join("4",title[:-4]+".txt")
            with open(tags_file_path,'r',encoding='utf-8', errors='replace') as f:
                tags=f.read().splitlines()
            return tags 
            
            
                

          # Prepare the data for bulk indexing
          actions = []
          def generate_data():
            for idx, row in df.iterrows():
                yield {
                    "_op_type": "update",  # Use update for upsert behavior
                    "_index": index,
                    "_id": str(idx),  # Unique document ID (based on row index)
                    "doc": {
                        "image-vector": row['image_vector'],  # Elasticsearch expects this field name
                        "title": row['image_name'],
                        "tags" :  load_tags(row['image_name'])
                    },
                    "doc_as_upsert": True  # If the document doesn't exist, create it
              }
            

          # Perform bulk indexing
          es=self.connect
          res = helpers.bulk(es,generate_data(), chunk_size=500)
          print("Indexing successful:", res)

      except Exception as e:
          print(f"Indexing failed: {e}")
          if isinstance(e, helpers.BulkIndexError):
              for failed in e.errors:
                  print("Failed to index:", failed)
          else:
              print("An unexpected error occurred during injection.")
    def count_doc(self,index_name):
      try:
          doc_count = self.connect.cat.count(index=index_name, format='json')
          print("Documents in index:", doc_count)
      except Exception as e:
          print(f"Failed to retrieve document count: {e}")
    


    def search_similar_images(self,index,feature_vector, top_n=40):
      
      response = self.connect.search(
      index=index,
      knn={
          "field": "image-vector",
          "query_vector":feature_vector,
          "k": 30,
          "num_candidates": 150
      },
      size=top_n,
      fields=[
          "title"
          ],
      )
    def search_similar_images_tags(self, index, feature_vector,desired_tag=None, top_n=40):
      query={
              "bool": {
                  "must": {
                      "knn": {
                          "field": "image-vector",
                          "query_vector": feature_vector,
                          "k": 30,
                          "num_candidates": 150
                      }
                  },
                  "filter": []
              }
          }
      if desired_tag :
         query["bool"]["filter"].append({
                          "fuzzy": {
                              "tags": {
                                  "value": desired_tag,  # Replace with the desired tag
                                  "fuzziness": "AUTO"  # Enables fuzzy matching
                              }
                          }
                      })
      response = self.connect.search(
          index=index,
          size=top_n,
          query=query,
          _source=["title"]  # Retrieve only the title field in results
      )
    

      # Retrieve and print the results
      similar_images = []
      for hit in response['hits']['hits']:
          print(hit["_index"])
          print(hit["_score"])
          print(hit["_source"]["title"])
          path = os.path.join("4", str(hit["_source"]["title"]))
          similar_images.append(path)

          print("################")

      return similar_images






def main ():
    es=elasticsearchManager()

    #es.delete_index("image-index")
    es.create_index_combination("image-index-combination")
       
    es.injection("image-index-combination","data_csv/image_features_withoutpca_4.csv")
    es.count_doc("image-index-combination")


if __name__=="__main__":
    main()



          
      

                

                
              
              
