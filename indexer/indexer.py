import json
from elasticsearch import Elasticsearch
from config import ELASTICSEARCH_URL, INDEX_NAME

# Connect to Elasticsearch
es = Elasticsearch(ELASTICSEARCH_URL)

# Load your cleaned data (e.g., JSON file)
with open("data/cleaned_data.json", "r") as f:
    documents = json.load(f)

# Create index if not exists
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME)

# Index each document
for i, doc in enumerate(documents):
    es.index(index=INDEX_NAME, id=i, document=doc)

print(f"✅ Indexed {len(documents)} documents into '{INDEX_NAME}'")