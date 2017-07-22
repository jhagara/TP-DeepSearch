import unittest
import os
from pathlib import Path

from tests.helper.helper_test_methods import HelperTestMethods
import config
import shutil
from pymarc import Record, Field, XMLWriter
from time import gmtime, strftime
from elasticsearch import Elasticsearch
from semantic import Semantic


class TestMarcExport(unittest.TestCase):
    def create_journal_marc(self):
        journal_record = Record(leader='     nas  22     uic4500', force_utf8=True)

        # 001
        journal_record.add_field(Field(tag='001', data='0123456'))

        # 003 VRT = organization code for UKB
        journal_record.add_field(Field(tag='003', data='VRT'))

        # 005
        time = strftime("%Y%m%d%H%M%S", gmtime())
        time += ".0"
        journal_record.add_field(Field(tag='005', data=time))

        # 008
        journal_record.add_field(Field(tag='008', data="040701d19191945xo wr|p|||||||0|||a0slo|d"))

        # 007
        journal_record.add_field(Field(tag='007', data="ta"))

        # 022
        journal_record.add_field(Field(tag='022', indicators=[' ', ' '], subfields=['a', '1336-4464']))

        # 245
        journal_record.add_field(
            Field(
                tag='245',
                indicators=[' ', ' '],
                subfields=['a', 'Slovak']
            )
        )

        # 264
        journal_record.add_field(
            Field(
                tag='264',
                indicators=['', ''],
                subfields=['a', 'Bratislava',
                           'b', 'Účastinná spoločnosť Slováka ',
                           'c', '1919-1945']
            )
        )
        path = os.path.dirname(os.path.abspath(__file__)) + "/slovak/journal_marc21.xml"
        writer = XMLWriter(open(path, 'wb'))
        writer.write(journal_record)
        writer.close()
        return path

    def test_export(self):

        # create marc for journal
        # path = self.create_journal_marc()

        path = os.path.dirname(os.path.abspath(__file__)) + "/slovak/journal_marc21.xml"

        path_issue = os.path.dirname(os.path.abspath(__file__)) + "/slovak/19400102"

        issue = {'name': 'Slovak19400102', 'content': 'CustomContent',
                 'publisher': 'CustomPublisher', 'release_from': 'CustomRelease',
                 'release_date': '19400202', 'number': '10',
                 'source_dirname': path_issue, 'page_height': 4000,
                 'page_width': 6000, 'year': 'XX', 'pages_count': 10, 'journal_marc21_path': path}

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

        article1 = {
            'groups': [
                {'page': 1, 'type': 'headings', 'text': 'Some Heading', 'l': 45, 'r': 100, 't': 10, 'b': 100},
                {'page': 1, 'type': 'fulltexts', 'text': text1, 'l': 45, 'r': 100, 't': 120,
                 'b': 200}
            ],
            "authors": ['Miro', 'Jano', 'Prdo'],
            "keywords": ['word1', 'anothorword1'],
            "is_ignored": True,
            "issue": {
                "id": 0
            }
        }

        try:
            # export marc
            issue, articles = HelperTestMethods.create_custom_issue(issue, [article1])
            semantic = Semantic()
            semantic.export_marc_for_issue(issue['_id'])


            #  check if files does not exist for ignored article
            marc1 = Path(path_issue + "/articles/1/1_marc21.xml")
            self.assertNotEqual(True, marc1.is_file(), "No file " + path_issue + "/articles/1/1_marc21.xml")

        finally:
            #  delete files
            marc_issue = Path(path_issue + "/issue_marc21.xml")
            if marc_issue.is_file():
                os.remove(path_issue + "/issue_marc21.xml")
            marc1 = Path(path_issue + "/articles/1/1_marc21.xml")
            if marc1.is_file():
                shutil.rmtree(path_issue + "/articles")


if __name__ == '__main__':
    unittest.main()