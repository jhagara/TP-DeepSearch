import config

from elasticsearch import Elasticsearch
from parser.xml.xml_parser import XmlParser


class RulesTester(object):

    # make testing on all test issues set as test_issue
    def test_all_test_issues(self):
        test_issues = self.__find_all_test_issues()

        for issue in test_issues:

            # parse issue with new rules
            xml_path = issue['_source']['source_dirname']
            config_path = self.__find_config_path(xml_path)
            parser = XmlParser()
            xml, header, parsed_articles = parser.parse(config_path, xml_path)

            elastic_index = config.elastic_index()

            # establishment of connection
            es = Elasticsearch()

            test_articles = es.search(index=elastic_index, doc_type="article",
                                      body={'query': {'bool': {'must': {'nested': {'path': 'issue',
                                            'query': {'match': {'issue.id': issue['_id']}}}}}},
                                            'size': 1000})['hits']['hits']

            for test_article in test_articles:

                # find article in newly parsed issue
                parsed_article = self.__find_parsed_article(test_article, parsed_articles)
                if parsed_article is None:
                    # TODO zapocitat vsetky bloky ako nespravne urcene
                # compare articles
                statistics = self.__compare_articles(test_article, parsed_article) # TODO zmenit podla toho ake statistiky sa budu pocitat
                # TODO pripocitat do celkovych statistik pre issue

            # save statistics
            self.__save_statistics(statistics)

    # find all test issues set as test_issue
    def __find_all_test_issues(self):
        return

    # find header config for xml
    def __find_config_path(self, xml_path):
        return

    # find same article in newly parsed issue
    def __find_parsed_article(self, test_article, parsed_articles):
        return

    # compare test article and newly parsed article and compute statistics for article
    def __compare_articles(self, test_article, parsed_article):
        return

    # sace statistics
    def __save_statistics(self, statistics):
        return
