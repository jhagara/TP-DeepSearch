import unittest
import config
import issue_facade
from elasticsearch import Elasticsearch


class TestElasticFiller(unittest.TestCase):
    def test_basic_filler_script_call(self):
        path = config.get_full_path('tests/elastic_filler/slovak')
        parser_dir = config.get_full_path('tests', 'elastic_filler')
        issue_facade.main('bulk_insert', config.default_elastic_index, parser_dir, path, 'slovak')
        self.assert_

    def test_extend_filler_script_call(self):
        path = config.get_full_path('tests/elastic_filler/slovak/1939/19390526')
        parser_dir = config.get_full_path('tests', 'elastic_filler')
        issue_facade.main('bulk_insert', config.default_elastic_index, parser_dir, path, 'slovak/1939/19390526')
        self.assert_

        es = Elasticsearch()
        res = es.search(index=config.elastic_index(), doc_type="issue",
                        body={"query": {"match": {'name': 'slovak/1939/19390526'}}})

        issue_id = res['hits']['hits'][0]['_id']
        articles = es.search(index=config.elastic_index(), doc_type="article",
                             body={'query': {'bool': {'must': {
                                 'nested': {'path': 'issue', 'query': {'match': {'issue.id': issue_id}}}}}},
                                 'size': 1000})['hits']['hits']

        for article in articles:
            self.assertIsNotNone(article['_source'].get('keywords'))




