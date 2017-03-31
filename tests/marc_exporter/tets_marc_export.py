import unittest
import os
from pathlib import Path

from tests.helper.helper_test_methods import HelperTestMethods
import marc_exporter
import config
import shutil
from pymarc import Record, Field
from time import gmtime, strftime


class TestMarcExport(unittest.TestCase):
    def create_journal_marc(self):
        journal_record = Record(leader='     nas  22     uic4500', force_utf8=True)

        # leader
        # journal_record.add_field(Field(tag='leader', data='     nas  22     uic4500'))

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
        path = os.path.dirname(os.path.abspath(__file__)) + "/slovak/journal_marc21.txt"
        with open(path, 'wb') as f:
            f.write(journal_record.as_marc())
        return path

    def test_export(self):

        path = self.create_journal_marc()

        path_issue = os.path.dirname(os.path.abspath(__file__)) + "/slovak/19400102"

        issue = {'name': 'Slovak19400102', 'content': 'CustomContent',
                 'publisher': 'CustomPublisher', 'release_from': 'CustomRelease',
                 'release_date': '19400202', 'number': '10',
                 'source_dirname': path_issue, 'page_height': 4000,
                 'page_width': 6000, 'year': 'XX', 'page_count': 10, 'journal_marc21_path': path}

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
            "keywords": ['word1', 'anothorword1'],
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
            "keywords": ['word2'],
            "issue": {
                "id": 0
            }
        }

        # export marc
        issue, articles = HelperTestMethods.create_custom_issue(issue, [article1, article2])
        marc_exporter.main(issue['_id'], config.default_elastic_index)

        #  check if files exists
        marc_issue = Path(path_issue + "/issue_marc21.txt")
        self.assertEqual(True, marc_issue.is_file(), "No file " + path_issue + "/issue_marc21.txt")
        marc1 = Path(path_issue + "/articles/1/1_marc21.txt")
        self.assertEqual(True, marc1.is_file(), "No file " + path_issue + "/articles/1/1_marc21.txt")
        marc2 = Path(path_issue + "/articles/2/2_marc21.txt")
        self.assertEqual(True, marc2.is_file(), "No file " + path_issue + "/articles/2/2_marc21.txt")

        #  delete files
        # os.remove(path_issue + "/issue.txt")
        # shutil.rmtree(path_issue + "/articles")
        # TODO delete journal marc
        # TODO kontrola ci je cesta v elasticu, try, catch ayb sa vymazali subory


if __name__ == '__main__':
    unittest.main()
