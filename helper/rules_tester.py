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

            correct_articles = 0
            all_articles = len(test_articles)
            correct_blocks = 0
            all_blocks = 0
            for test_article in test_articles:
                all_blocks += len(test_article['_source']['groups'])
                # find article in newly parsed issue
                parsed_article = self.__find_parsed_article(test_article, parsed_articles)
                if parsed_article is None:
                    continue
                # compare articles
                ca, cb = self.__compare_articles(test_article, parsed_article)
                if ca:
                    correct_articles += 1
                correct_blocks += cb

            # save statistics
            self.__save_statistics(correct_articles, all_articles, correct_blocks, all_blocks)

    # find all test issues set as test_issue
    def __find_all_test_issues(self):
        return

    # find header config for xml
    def __find_config_path(self, xml_path):
        return

    # find same article in newly parsed issue
    def __find_parsed_article(self, test_article, parsed_articles):
        heading = None
        for group in test_article['_source']['groups']:
            if group['type'] == "headings":
                heading = group
                break

        # heading = next((x for x in test_article['_source']['groups'] if x['type'] == "headings"), None)

        if heading is None:
            return None

        l = str(heading['l'])
        r = str(heading['r'])
        t = str(heading['t'])
        b = str(heading['b'])
        found = None
        for article in parsed_articles[heading['page'] - 1]:
            for group in article:
                found = group.xpath("par[@l = " + l + " and @r = " + r + " and @t = " + t + " and @b = " + b + "]")
            if found is not None:
                return article
        return None

    # compare test article and newly parsed article and compute statistics for article
    def __compare_articles(self, test_article, parsed_article):
        return

    # sace statistics
    def __save_statistics(self, correct_articles, all_articles, correct_blocks, all_blocks):
        return
