FROM docker.elastic.co/elasticsearch/elasticsearch:8.15.2

# Disable security and configure ElasticSearch as a single node
ENV discovery.type=single-node
ENV xpack.security.enabled=false

# Install k-NN plugin
RUN bin/elasticsearch-plugin install --batch https://github.com/alexklibisz/elastiknn/releases/download/8.15.2.0/elastiknn-8.15.2.0.zip
