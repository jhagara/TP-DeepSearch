import os
import getopt
import re
import sys
from time import gmtime, strftime
from operator import itemgetter
import itertools

from elasticsearch import Elasticsearch
from parser.xml.xml_parser import XmlParser


class RulesTester(object):
    def __init__(self, index):
        # establishment of connection
        self.elastic = Elasticsearch()
        self.index = index

    # make testing on all test issues set as test_issue
    def test_test_issues(self, journal_name, version, old_version):

        test_issues = self.__find_test_issues(journal_name)

        results = []
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

            test_articles = self.elastic.search(index=self.index, doc_type="article",
                                                body={'query': {'bool': {'must': {'nested': {'path': 'issue',
                                                      'query': {'match': {'issue.id': issue['_id']}}}}}},
                                                      'size': 1000})['hits']['hits']

            correct_articles = 0
            all_articles = 0
            correct_blocks = 0
            all_blocks = 0
            incorrect_articles = []
            for test_article in test_articles:
                if test_article['_source']['is_ignored']:
                    continue

                # find heading in test article
                test_heading = next(
                        (group for group in test_article['_source']['groups'] if group['type'] == "headings"), None)
                if test_heading is None:
                    continue

                all_blocks += len(test_article['_source']['groups'])
                all_articles += 1

                # find article in newly parsed issue
                parsed_article = self.__find_parsed_article(test_heading, parsed_articles)
                if parsed_article is None:
                    incorrect_article = self.__get_incorrect_article(test_article, 0)
                    incorrect_articles.append(incorrect_article)
                    continue

                # compare articles
                ca, cb = self.__compare_articles(test_article, parsed_article)
                if ca:
                    correct_articles += 1
                else:
                    incorrect_article = self.__get_incorrect_article(test_article, cb)
                    incorrect_articles.append(incorrect_article)
                correct_blocks += cb

            result_issue = {'correct_articles': correct_articles, 'all_articles': all_articles,
                            'correct_blocks': correct_blocks, 'all_blocks': all_blocks,
                            'incorrect_articles': incorrect_articles, 'issue': issue,
                            'journal_name': issue['_source']['journal_name']}

            results.append(result_issue)

        # save statistics
        self.__save_statistics(results, journal_name, version, old_version)

    # find test issues set as test_issue
    def __find_test_issues(self, journal_name):
        if journal_name is None or journal_name == 'all':
            test_issues = self.elastic.search(index=self.index, doc_type="issue",
                                              body={'query': {'term': {'is_tested': {'value': True}}},
                                                    'size': 1000})['hits']['hits']
        else:
            test_issues = self.elastic.search(index=self.index, doc_type="issue",
                                              body={'query': {'bool': {'must': [
                                                  {'match': {'journal_name': journal_name}},
                                                  {'term': {'is_tested': {'value': 'true'}}}]}},
                                                  'size': 1000})['hits']['hits']
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
        path = None
        while True:
            path = os.popen("find " + current_dir + " -maxdepth 1 -type f -name '*.json'").read()
            path = re.sub("[\n]", '', path)

            if path != '' or current_dir == '/':
                break
            else:
                current_dir = re.sub("[\n]", '', os.popen("dirname '" + current_dir + "'").read())

        return path

    # find same article in newly parsed issue
    def __find_parsed_article(self, heading, parsed_articles):
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
            page = str(test_group['page'])
            for parsed_group in parsed_article:
                if page != parsed_group.attrib['page']:
                    continue
                found = parsed_group.xpath("par[@l = " + l + " and @r = " + r + " and @t = " + t + " and @b = " +
                                           b + "]")
                if found is not None and len(found) != 0:
                    correct_blocks += 1
                    break

        correct_article = False
        if correct_blocks == len(test_article['_source']['groups']):
            correct_article = True
        return correct_article, correct_blocks

    def __get_latest_test(self, journal_name, old_version):
        if old_version is None:
            result = self.elastic.search(index=self.index, doc_type="test",
                                         body={'query': {"match": {"journal_name": journal_name}}, 'size': 1,
                                               'sort': [{'tested_at': {'order': 'desc'}}]})['hits']['hits']
        else:
            result = self.elastic.search(index=self.index, doc_type="test",
                                         body={'query': {'bool': {'must': [
                                             {'match': {'journal_name': journal_name}},
                                             {'match': {'version': old_version}}]}}, 'size': 1,
                                              'sort': [{'tested_at': {'order': 'desc'}}]})['hits']['hits']
        if result is not None and len(result) > 0:
            return result[0]
        else:
            return None

    # get percentage
    # if y is 0 return 0%
    def __safe_per(self, x, y):
        if y == 0:
            return "0%"
        return "{0:.2f}%".format(x / y * 100)

    # print results
    def __print_results(self, results, old_version):

        all_blocks = 0
        all_cor_blocks = 0
        all_articles = 0
        all_cor_articles = 0
        old_all_blocks = 0
        old_all_cor_blocks = 0
        old_all_articles = 0
        old_all_cor_articles = 0
        for key, group in itertools.groupby(results, lambda r: r["journal_name"]):
            latest_test = self.__get_latest_test(key, old_version)
            if latest_test is not None:
                v = latest_test['_source']['version']
            else:
                v = "Not tested"
            print("Journal: " + key + " old version: " + v)
            print("{:<20} {:<12} {:<12} {:<10} {:<10}".format('Issue', 'Old Articles', 'New Articles', 'Old Blocks',
                                                              'New Blocks'))
            journal_all_blocks = 0
            journal_cor_blocks = 0
            journal_all_articles = 0
            journal_cor_articles = 0
            for result in group:
                if latest_test is not None:
                    old_result = next((issue for issue in latest_test['_source']['test_issues']
                                       if issue['id'] == result['issue']['_id']), None)
                all_blocks += result['all_blocks']
                all_cor_blocks += result['correct_blocks']
                all_articles += result['all_articles']
                all_cor_articles += result['correct_articles']
                journal_all_blocks += result['all_blocks']
                journal_cor_blocks += result['correct_blocks']
                journal_all_articles += result['all_articles']
                journal_cor_articles += result['correct_articles']
                per_blocks = self.__safe_per(result['correct_blocks'], result['all_blocks'])
                per_articles = self.__safe_per(result['correct_articles'], result['all_articles'])
                if latest_test is not None:
                    old_per_blocks = self.__safe_per(old_result['correct_blocks'], old_result['all_blocks'])
                    old_per_articles = self.__safe_per(old_result['correct_articles'], old_result['all_articles'])
                else:
                    old_per_blocks = "Not tested"
                    old_per_articles = "Not tested"
                print("{:<20} {:<12} {:<12} {:<10} {:<10}".format(result['issue']['_source']['name'], old_per_articles,
                                                                  per_articles, old_per_blocks, per_blocks))
            per_articles = self.__safe_per(journal_cor_articles, journal_all_articles)
            per_blocks = self.__safe_per(journal_cor_blocks, journal_all_blocks)
            if latest_test is not None:
                old_all_blocks += latest_test['_source']['all_blocks']
                old_all_cor_blocks += latest_test['_source']['correct_blocks']
                old_all_articles += latest_test['_source']['all_articles']
                old_all_cor_articles += latest_test['_source']['correct_articles']
                old_per_articles = self.__safe_per(latest_test['_source']['correct_articles'],
                                                   latest_test['_source']['all_articles'])
                old_per_blocks = self.__safe_per(latest_test['_source']['correct_blocks'],
                                                 latest_test['_source']['all_blocks'])
            else:
                old_per_blocks = "Not tested"
                old_per_articles = "Not tested"
            print("{:<20} {:<12} {:<12} {:<10} {:<10}".format('TOTAL', old_per_articles, per_articles, old_per_blocks,
                                                              per_blocks))
            print()
        print("For all journals")
        per_articles = self.__safe_per(all_cor_articles, all_articles)
        per_blocks = self.__safe_per(all_cor_blocks, all_blocks)
        if old_all_articles > 0:
            old_per_articles = self.__safe_per(old_all_cor_articles, old_all_articles)
        else:
            old_per_articles = "Not tested"
        if old_all_blocks > 0:
            old_per_blocks = self.__safe_per(old_all_cor_blocks, old_all_blocks)
        else:
            old_per_blocks = "Not tested"
        print("{:<20} {:<12} {:<12} {:<10} {:<10}".format('All', 'Old Articles', 'New Articles', 'Old Blocks',
                                                          'New Blocks'))
        print("{:<20} {:<12} {:<12} {:<10} {:<10}".format('ALL', old_per_articles, per_articles, old_per_blocks,
                                                          per_blocks))

    # save test
    def __save_test(self, results, version, journal_name):
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        correct_blocks = 0
        all_blocks = 0
        correct_articles = 0
        all_articles = 0
        test_issues = []
        for result in results:
            correct_blocks += result['correct_blocks']
            all_blocks += result['all_blocks']
            correct_articles += result['correct_articles']
            all_articles += result['all_articles']
            test_issue = {'id': result['issue']['_id'], 'correct_blocks': result['correct_blocks'],
                          'all_blocks': result['all_blocks'], 'correct_articles': result['correct_articles'],
                          'all_articles': result['all_articles'], 'incorrect_articles': result['incorrect_articles']}
            test_issues.append(test_issue)

        test = {'journal_name': journal_name, 'tested_at': time, 'version': version, 'correct_blocks': correct_blocks,
                'all_blocks': all_blocks, 'correct_articles': correct_articles, 'all_articles': all_articles,
                'test_issues': test_issues}

        self.elastic.index(index=self.index, doc_type='test', body=test)

    def __query_yes_no(self, question, default="yes"):
        """Ask a yes/no question via input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        The "answer" return value is True for "yes" or False for "no".
        """
        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                                 "(or 'y' or 'n').\n")

    # create dictionry for incorrect article
    def __get_incorrect_article(self, test_article, correct_blocks):
        all_blocks = len(test_article['_source']['groups'])

        # find heading
        heading = next((group for group in test_article['_source']['groups'] if group['type'] == "headings"), None)

        title = ''
        page = None
        if heading is not None:
            title = heading['text']
            page = heading['page']

        # if article don't have heading get page for first block - all blocks should be on one page
        if page is None and len(test_article['_source']['groups']) > 0:
            page = test_article['_source']['groups'][0]['page']

        incorrect_article = {"id": test_article['_id'], "correct_blocks": correct_blocks,
                             "all_blocks": all_blocks, "page": page, "title": title}

        return incorrect_article

    def __find_latest_version(self):
        latest_test = self.elastic.search(index=self.index, doc_type="test",
                                          body={'query': {"match_all": {}}, 'size': 1,
                                                'sort': [{'tested_at': {'order': 'desc'}}]})['hits']['hits']
        if latest_test is None or len(latest_test) == 0:
            print("No existing tests")
        else:
            print("Latest version is: " + latest_test[0]['_source']['version'])

        sys.stdout.write("Enter current version: ")
        version = input()
        return version

    # save statistics
    def __save_statistics(self, results, journal_name, version, old_version):

        results.sort(key=itemgetter("journal_name"))
        self.__print_results(results, old_version)

        respond = self.__query_yes_no("Do you want to save results to elastic?")
        if respond is False:
            return

        if version is None:
            version = self.__find_latest_version()

        # save for all
        if journal_name is None or journal_name == 'all':
            self.__save_test(results, version, 'all')

        # save for each journal
        for key, group in itertools.groupby(results, lambda result: result["journal_name"]):
            self.__save_test(group, version, key)

        self.elastic.indices.refresh(index=self.index)


def usage():
    print("Name")
    print("rules_tester.py - test issues that are marked as tested")
    print()
    print("Usage")
    print("rules_tester.py -v [version] -o [old version] -i [elastic index] -n [journal name] -h")
    print("-v [version]: save statistics with specified version")
    print("-o [old version]: compare resutls with specific version")
    print("-i [elastic index]: use [elastic index] for elasticsearch")
    print("-n [journal name]: test for issues with journal name = [journal name]")
    print("-h: usage of script")
    print()
    es = Elasticsearch()
    indices = es.indices.get_alias().keys()
    print("Existing elasticsearch indecies:")
    for index in indices:
        print(index)
    return


def main():
    version = None
    index = None
    name = None
    old_version = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'v:i:n:o:h', ['version=', 'index=', 'name=', 'old=', 'help'])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-v', '--version'):
            version = arg
        elif opt in ('-i', '--index'):
            index = arg
        elif opt in ('-n', '--name'):
            name = arg
        elif opt in ('-o', '--old'):
            old_version = arg
        else:
            usage()
            sys.exit(2)

    if index is None:
        print("NO ELASTIC INDEX")
        usage()
        sys.exit(2)

    tester = RulesTester(index)
    tester.test_test_issues(name, version, old_version)

if __name__ == "__main__":
    main()
