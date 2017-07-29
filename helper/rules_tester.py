import config
import os
import re

from elasticsearch import Elasticsearch
from parser.xml.xml_parser import XmlParser


class RulesTester(object):

    # make testing on all test issues set as test_issue
    def test_all_test_issues(self):
        elastic_index = config.elastic_index()

        # establishment of connection
        es = Elasticsearch()

        test_issues = self.__find_all_test_issues(es, elastic_index)

        for issue in test_issues:

            # parse issue with new rules
            source_path = issue['_source']['source_dirname']
            xml_path = self.__find_xml(source_path)
            config_path = self.__find_config(source_path)
            if xml_path == '' or config_path == '':
                print("Missing config file or xml file in dir and parent dirs:" + source_path)
                return -1
            parser = XmlParser()
            xml, header, parsed_articles = parser.parse(config_path, xml_path)

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
            self.__save_statistics(correct_articles, all_articles, correct_blocks, all_blocks, issue)

    # find all test issues set as test_issue
    def __find_all_test_issues(self, elastic, index):
        test_issues = elastic.search(index=index, doc_type="issue",
                                     body={'query': {'term': {'is_tested': 'true'}}, 'size': 1000})['hits']['hits']
        return test_issues

    # find xml path
    def __find_xml(self, source_dir):
        xml_dir = source_dir + "/XML"
        path = os.popen("find " + xml_dir + " -maxdepth 1 -type f -name '*.xml'").read()
        path = re.sub("[\n]", '', path)

        return path

    # find header config for xml
    def __find_config(self, source_dir):
        current_dir = source_dir
        while True:
            path = os.popen("find " + current_dir + " -maxdepth 1 -type f -name '*.json'").read()
            path = re.sub("[\n]", '', path)

            if path != '' or current_dir == '/':
                break
            else:
                current_dir = re.sub("[\n]", '', os.popen("dirname '" + current_dir + "'").read())

        return path

    # find same article in newly parsed issue
    def __find_parsed_article(self, test_article, parsed_articles):
        # find heading in article
        heading = next((group for group in test_article['_source']['groups'] if group['type'] == "headings"), None)

        if heading is None:
            return None

        l = str(heading['l'])
        r = str(heading['r'])
        t = str(heading['t'])
        b = str(heading['b'])
        page = int(heading['page'])
        for article in parsed_articles[page - 1]:
            for group in article:
                found = group.xpath("par[@l = " + l + " and @r = " + r + " and @t = " + t + " and @b = " + b + "]")
                if found is not None and len(found) != 0:
                    return article
        return None

    # compare test article and newly parsed article and compute statistics for article
    def __compare_articles(self, test_article, parsed_article):
        correct_blocks = 0
        for test_group in test_article['_source']['groups']:
            l = str(test_group['l'])
            r = str(test_group['r'])
            t = str(test_group['t'])
            b = str(test_group['b'])
            for parsed_group in parsed_article:
                found = parsed_group.xpath("par[@l = " + l + " and @r = " + r + " and @t = " + t + " and @b = " +
                                           b + "]")
                if found is not None and len(found) != 0:
                    correct_blocks += 1
                    break

        correct_article = False
        if correct_blocks == len(test_article['_source']['groups']):
            correct_article = True
        return correct_article, correct_blocks

    # sace statistics
    def __save_statistics(self, correct_articles, all_articles, correct_blocks, all_blocks, issue):
        return
