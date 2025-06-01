from elasticsearch import Elasticsearch
import os
import json

PROCESSED_DIR = 'data/processed'

# Connect to ES (disable auth for now or set credentials)
es = Elasticsearch("http://localhost:9200")

INDEX_NAME = "smartsearch-index"

# Optional: Delete index if exists (dev use)
if es.indices.exists(index=INDEX_NAME):
    es.indices.delete(index=INDEX_NAME)

# Create index with analyzer
es.indices.create(index=INDEX_NAME, body={
    "settings": {
        "analysis": {
            "analyzer": {
                "default": {
                    "type": "standard"
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "filename": {"type": "keyword"},
            "content": {"type": "text"}
        }
    }
})

# Index documents
for filename in os.listdir(PROCESSED_DIR):
    file_path = os.path.join(PROCESSED_DIR, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    doc = {
        "filename": filename,
        "content": content
    }
    es.index(index=INDEX_NAME, document=doc)

    print(f"[✓] Indexed {filename}")