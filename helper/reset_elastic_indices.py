"""
     Resets/create certain indexes with mapping of types and properties
     -  if none arguments is given, then all indices are reseted/created
     -  if some arguments are given, then theese arguments - indices - strings
        are reseted/created
"""

import sys
from elasticsearch import Elasticsearch

all_indices = ['deep_search_test', 'deep_search_dev',
               'deep_search_prod', 'deep_search_test_python']
es = Elasticsearch()

if len(sys.argv) == 1:
    indices = all_indices
else:
    indices = sys.argv[1:]

for index in indices:
    print("indexing: " + index)

    # destroy index if already exists
    if es.indices.exists(index=index):
        es.indices.delete(index=index)

    # create index
    es.indices.create(
        index=index,
        body={
            "mappings": {
                "issue": {
                    "properties": {
                        "name": { "type": "text" },
                        "content": {"type": "text"},
                        "publisher": {"type": "text"},
                        "release_from": {"type": "text"},
                        "release_date": {"type": "text"},
                        "number": {"type": "text"},
                        "source_dirname": {"type": "text"},
                        "journal_marc21_path": {"type": "text"},
                        "page_height": {"type": "short"},
                        "page_width": {"type": "short"}
                    }
                },
                "article": {
                    "properties": {
                        "groups": {
                            "type": "nested",
                            "properties": {
                                "page": {"type": "short"},
                                "type": {"type": "keyword"},
                                "text": {"type": "text"},
                                "l": {"type": "short"},
                                "r": {"type": "short"},
                                "t": {"type": "short"},
                                "b": {"type": "short"}
                            }
                        },
                        "authors": {"type": "string"},
                        "keywords": {"type": "keyword"},
                        "issue": {
                            "type": "nested",
                            "properties": {
                                "id": {"type": "keyword"}
                            }
                        }
                    }
                }
            }
        }
    )

# create other indices if not exist
if not es.indices.exists(index='deep_search'):
    es.indices.create(index='deep_search')
