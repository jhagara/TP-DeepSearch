from elasticsearch import Elasticsearch
import config
from pymarc import MARCReader


class Marc(object):
    #  export issue into marc
    def __export_issue(self, issue, journal_marc, source_dirname):
        print()

    #  export article into marc
    def __export_article(self, article, issue_marc, source_dirname):
        print()

    #  save marc on path
    def __save_marc(self, marc, path):
        print()

    def export_marc_for_issue(self, issue_id):

        elastic_index = config.elastic_index()

        #  get issue and article from elastic
        es = es = Elasticsearch()
        issue = es.get(index=elastic_index, doc_type='issue', id=issue_id)
        articles = es.search(index=elastic_index, doc_type="article",
                             body={'query': {'bool': {'must': {
                                 'nested': {'path': 'issue', 'query': {'match': {'issue.id': issue_id}}}}}},
                                 'size': 1000})['hits']['hits']

        journal_path = issue['journal_marc21']  # TODO skontrolovat v elasticu
        source_dirname = issue['source_dirname']

        #  get marc21 for jurnal

        with open(journal_path, 'rb') as fh:
            reader = MARCReader(fh)
            journal_marc = next(reader)

        issue_marc = self.__export_issue(issue, journal_marc, source_dirname)

        for article in articles:
            self.__export_article(article, issue_marc, source_dirname)


