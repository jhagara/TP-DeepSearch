import os
from elasticsearch import Elasticsearch


default_elastic_index = 'deep_search_dev'


def root_path():
    return os.path.dirname(os.path.abspath(__file__))


def get_full_path(*path):
    return os.path.join(root_path(), *path)


def elastic_index():
    env = Elasticsearch().search(
        index="deep_search", doc_type="settings",
        body={'query': {'match': {'_id': 'environment'}}})

    if env['hits']['total'] != 0:
        return env['hits']['hits'][0]['_source']['value']
    else:
        return default_elastic_index


def set_environment(environment):
    res = Elasticsearch().index(
        index="deep_search", doc_type="settings",
        id='environment', body={"value": environment},
        refresh=True)
