import pytest
from elasticsearch import Elasticsearch


def pytest_sessionstart(session):
    """ before session.main() is called. """
    es = Elasticsearch()

    # delete all test items
    for hit in es.search(index='deep_search_test_python', size=9000)['hits']['hits']:
        es.delete(index=hit['_index'], doc_type=hit['_type'], id=hit['_id'])

    es.indices.refresh(index='deep_search_test_python')

    pass

def pytest_sessionfinish(session, exitstatus):
    """ whole test run finishes. """

    pass