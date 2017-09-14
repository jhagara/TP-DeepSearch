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
    # if es.indices.exists(index=index):
    es.indices.delete(index=index, ignore=[400, 404])

    # create index
    es.indices.create(
        index=index,
        body={
            "mappings": {
                "issue": {
                    "properties": {
                        "journal_name": {"type": "keyword"},
                        "name": {"type": "text"},
                        "content": {"type": "text"},
                        "publisher": {"type": "text"},
                        "release_from": {"type": "text"},
                        "release_date": {"type": "text"},
                        "number": {"type": "text"},
                        "pages_count": {"type": "short"},
                        "year": {"type": "text"},
                        "source_dirname": {"type": "keyword"},
                        "journal_marc21_path": {"type": "text"},
                        "issue_marc21_path": {"type": "text"},
                        "page_height": {"type": "short"},
                        "page_width": {"type": "short"},
                        "created_at": {"type": "date", 'format': "yyyy-MM-dd HH:mm:ss"},
                        "is_tested": {"type": "boolean"},
                        "was_exported": {"type": "boolean"}
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
                        "article_marc21_path": {"type": "text"},
                        "source_dirname": {"type": "keyword"},
                        "issue": {
                            "type": "nested",
                            "properties": {
                                "id": {"type": "keyword"}
                            }
                        },
                        "is_ignored": {"type": "boolean"}
                    }
                },
                "history": {
                    "properties": {
                        "client": {"type": "string"},
                        "target_type": {'type': 'keyword'},
                        "target_id": {'type': 'keyword'},
                        "updated_at": {"type": "date", 'format': "yyyy-MM-dd HH:mm:ss"},
                        "action": {'type': "keyword"},
                        "old_value": {'type': 'text'}
                    }
                },
                "test": {
                    "properties": {
                        "journal_name": {"type": "keyword"},
                        "tested_at": {"type": "date", 'format': "yyyy-MM-dd HH:mm:ss"},
                        "version": {"type": "keyword"},
                        "correct_blocks": {"type": "short"},
                        "all_blocks": {"type": "short"},
                        "correct_articles": {"type": "short"},
                        "all_articles": {"type": "short"},
                        "test_issues": {
                            "type": "nested",
                            "properties": {
                                "id": {"type": "keyword"},
                                "name": {"type": "text"},
                                "correct_blocks": {"type": "short"},
                                "all_blocks": {"type": "short"},
                                "correct_articles": {"type": "short"},
                                "all_articles": {"type": "short"},
                                "incorrect_articles": {
                                    "type": "nested",
                                    "properties": {
                                        "id": {"type": "keyword"},
                                        "correct_blocks": {"type": "short"},
                                        "all_blocks": {"type": "short"},
                                        "page": {"type": "short"},
                                        "title": {"type": "text"}
                                    }
                                }
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
