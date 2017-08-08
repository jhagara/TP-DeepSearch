import unittest
import os
import helper.rules_tester
from semantic import Semantic
from elasticsearch import Elasticsearch
import config


class TestRulesTester(unittest.TestCase):
    def test_all_issues(self):
        elastic_index = config.elastic_index()

        # establishment of connection
        es = Elasticsearch()
        path = os.path.dirname(os.path.abspath(__file__))
        json = path + '/../elastic_filler/slovak/1939/19390526/1939.json'
        dir = path + '/../elastic_filler/slovak/1939/19390526'
        journal_marc21 = path + '/../elastic_filler/slovak/journal_marc21.xml'
        xml = path + '/../elastic_filler/slovak/1939/19390526/XML/1336-4464_1939_19390526_00001.xml'
        file = {'json': json,
                'dir': dir,
                'journal_marc21': journal_marc21,
                'xml': xml}

        semantic = Semantic(xml=file['xml'], header_config=file['json'])
        issue_id = semantic.save_to_elastic("test_issue", file['dir'], file)
        es.update(index=elastic_index,
                  doc_type='issue',
                  id=issue_id,
                  body={
                      "script": {
                          "inline": "ctx._source.is_tested = params.is_tested",
                          "lang": "painless",
                          "params": {
                              "is_tested": True
                          }
                      }
                  })
        es.indices.refresh(index=elastic_index)
        helper.rules_tester.input = lambda: 'y'
        tester = helper.rules_tester.RulesTester()
        tester.test_all_test_issues('test_version', elastic_index)


if __name__ == '__main__':
    unittest.main()
