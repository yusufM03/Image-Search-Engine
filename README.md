# Elastic_Search_image_VGG16

**Status**: In Progress

## First Steps

1. **Feature Extraction from Images**
2. **Set Up ElasticSearch and k-NN Plugin**
3. **Define the Index Mapping: Create an index with the proper mapping to support k-NN**
4. **Load CSV Data into ElasticSearch**
5. **Perform k-NN Search**


5. **Different methods of KNN plugin**:
   Approximate KNN  : + Low latency
                      - less accuracy

      * It's recommended to reduce the vector dimentinality using **PCA**
      * For memory saving : We can use quantization . It converts float vectors into byte vectors
      * We can add filter option ( tags for examples) to reduce the number of images to seach .
      * Semantic Search: Using a previously deployed text embedding model, it retrieves results based on the intent and the contextual meaning of a search query.
   
1. ElasticSearch Connection
  `docker run --name elasticsearch --net elas -e "discovery.type=single-node" -e "xpack.security.enabled=false" -p 9200:9200 -p 9300:9300 docker.elastic.co/elasticsearch/elasticsearch:8.15.2`

2. `python app.py`


## References

- [ElasticSearch Docker Guide](https://www.elastic.co/guide/en/elasticsearch/reference/8.15/docker.html)
- [Machine Learning NLP Text Embedding Vector Search Example](https://www.elastic.co/guide/en/machine-learning/8.15/ml-nlp-text-emb-vector-search-example.html)
- [k-NN Search Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/8.15/knn-search.html)
