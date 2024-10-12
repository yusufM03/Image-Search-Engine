# Elastic_Search_image_VGG16
(In Progress)
**First Steps**:

 * 1.Feature extraction from images **
 * 2.Set Up ElasticSearch and k-NN Plugin
   `./bin/elasticsearch-plugin install https://github.com/opendistro-for-elasticsearch/k-NN/releases/download/v1.11.0.0/opendistro-knn-1.11.0.0.zip`
 * 3.Define the Index Mapping: Create an index with the proper mapping to support k-NN.
 * 4.Load CSV Data into ElasticSearch
 * 5.Perform k-NN Search


Reference:
 . Guide
https://www.elastic.co/guide/en/elasticsearch/reference/8.15/docker.html
https://www.elastic.co/guide/en/machine-learning/8.15/ml-nlp-text-emb-vector-search-example.html
https://www.elastic.co/guide/en/elasticsearch/reference/8.15/knn-search.html


