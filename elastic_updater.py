import os
import sys
from semantic import Semantic
import re
import config
from elasticsearch import Elasticsearch


def main(issue_id, environment):
    # set environment to new value
    config.set_environment(environment)

    es = Elasticsearch()
    articles = es.search(index='deep_search_test_python', doc_type="article",
                         body={'query': {'bool': {'must': {
                             'nested': {'path': 'issue', 'query': {'match': {'issue.id': issue_id}}}}}},
                             'size': 10000})['hits']['hits']

    # update articles key_words
    semantic = Semantic()
    semantic.insert_key_words(issue_id)

    # set environment to default
    config.set_environment(config.default_elastic_index)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
    sys.exit()



