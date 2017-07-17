import unittest
from semantic import Semantic
from textblob import TextBlob as tB
import issue_facade
import config
from tests.helper.helper_test_methods import HelperTestMethods
from elasticsearch import Elasticsearch


class TestKeyWords(unittest.TestCase):
    def test_key_words(self):

        document1 = tB("""Python is a 2000 made-for-TV horror movie directed by Richard
        Clabaugh. The film features several cult favorite actors, including William
        Zabka of The Karate Kid fame, Wil Wheaton, Casper Van Dien, Jenny McCarthy,
        Keith Coogan, Robert Englund (best known for his role as Freddy Krueger in the
        A Nightmare on Elm Street series of films), Dana Barron, David Bowe, and Sean
        Whalen. The film concerns a genetically engineered snake, a python, that
        escapes and unleashes itself on a small town. It includes the classic final
        girl scenario evident in films like Friday the 13th. It was filmed in Los Angeles,
         California and Malibu, California. Python was followed by two sequels: Python
         II (2002) and Boa vs. Python (2004), both also made-for-TV films.""")

        document2 = tB("""Python, from the Greek word (πύθων/πύθωνας), is a genus of
        nonvenomous pythons[2] found in Africa and Asia. Currently, 7 species are
        recognised.[2] A member of this genus, P. reticulatus, is among the longest
        snakes known.""")

        document3 = tB("""The Colt Python is a .357 Magnum caliber revolver formerly
        manufactured by Colt's Manufacturing Company of Hartford, Connecticut.
        It is sometimes referred to as a "Combat Magnum".[1] It was first introduced
        in 1955, the same year as Smith & Wesson's M29 .44 Magnum. The now discontinued
        Colt Python targeted the premium revolver market segment. Some firearm
        collectors and writers such as Jeff Cooper, Ian V. Hogg, Chuck Hawks, Leroy
        Thompson, Renee Smeets and Martin Dougherty have described the Python as the
        finest production revolver ever made.""")
        
        list_of_starts = ["Python, The, The, It, It, Python",
                  "Python, A",
                  "The, It, It, The, Some"]
        
        bloblist = [document1, document2, document3]
        sem = Semantic()
        key_words_art = sem.key_words(bloblist,list_of_starts)
        self.assertEqual(key_words_art is None, False)
        for i, key_words in enumerate(key_words_art):
            self.assertEqual(len(key_words) > 0, True)
            # print("Top words in document {}".format(i + 1))
            # for word in key_words:
            #     print("Word: {}".format(word))

    def test_elastic_updater_script_call(self):

        text1 = """Python is a 2000 made-for-TV horror movie directed by Richard
        Clabaugh. The film features several cult favorite actors, including William
        Zabka of The Karate Kid fame, Wil Wheaton, Casper Van Dien, Jenny McCarthy,
        Keith Coogan, Robert Englund (best known for his role as Freddy Krueger in the
        A Nightmare on Elm Street series of films), Dana Barron, David Bowe, and Sean
        Whalen. The film concerns a genetically engineered snake, a python, that
        escapes and unleashes itself on a small town. It includes the classic final
        girl scenario evident in films like Friday the 13th. It was filmed in Los Angeles,
         California and Malibu, California. Python was followed by two sequels: Python
         II (2002) and Boa vs. Python (2004), both also made-for-TV films."""

        text2 = """The Colt Python is a .357 Magnum caliber revolver formerly
        manufactured by Colt's Manufacturing Company of Hartford, Connecticut.
        It is sometimes referred to as a "Combat Magnum".[1] It was first introduced
        in 1955, the same year as Smith & Wesson's M29 .44 Magnum. The now discontinued
        Colt Python targeted the premium revolver market segment. Some firearm
        collectors and writers such as Jeff Cooper, Ian V. Hogg, Chuck Hawks, Leroy
        Thompson, Renee Smeets and Martin Dougherty have described the Python as the
        finest production revolver ever made."""

        article1 = {
            'groups': [
                {'page': 1, 'type': 'headings', 'text': 'Some Heading', 'l': 45, 'r': 100, 't': 10, 'b': 100},
                {'page': 1, 'type': 'fulltexts', 'text': text1, 'l': 45, 'r': 100, 't': 120,
                 'b': 200}
            ],
            "authors": ['Miro', 'Jano', 'Prdo'],
            "keywords": [],
            "issue": {
                "id": 0
            }
        }

        article2 = {
            'groups': [
                {'page': 1, 'type': 'headings', 'text': 'Some Heading', 'l': 45, 'r': 100, 't': 10, 'b': 100},
                {'page': 1, 'type': 'fulltexts', 'text': text2, 'l': 45, 'r': 100, 't': 120,
                 'b': 200}
            ],
            "authors": ['Miro', 'Jano', 'Prdo'],
            "keywords": [],
            "issue": {
                "id": 0
            }
        }
        issue, articles = HelperTestMethods.create_custom_issue(articles=[article1, article2])
        issue_facade.main('update_issue', config.default_elastic_index, issue['_id'])
        es = Elasticsearch()
        articles = es.search(index='deep_search_test_python', doc_type="article",
                             body={'query': {'bool': {'must': {
                                 'nested': {'path': 'issue', 'query': {'match': {'issue.id': issue['_id']}}}}}},
                                   'size': 1000})['hits']['hits']
        for article in articles:
            self.assertGreater(len(article['_source']['keywords']), 0)
        self.assert_

if __name__ == '__main__':
    unittest.main()