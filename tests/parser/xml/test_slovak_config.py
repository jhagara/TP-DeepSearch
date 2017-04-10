import json
import unittest
import os
import re
from lxml import etree
from parser.xml.source_header import SourceHeader
from parser.xml.cleaner import Cleaner


class TestSlovakConfig(unittest.TestCase):
    def test_slovak_output_config_success(self):
        path = os.path.dirname(
                    os.path.abspath(
                        __file__)) + "/slovak_config.json"
        config = self.read_from_json(path)
        original_xml = etree.parse(
                os.path.dirname(
                    os.path.abspath(
                        __file__)) + "/page_header_example.xml")
        original_xml = Cleaner.clean(original_xml)
        # print(etree.tostring(original_xml).decode('utf-8'))

        actual_xml, header = SourceHeader.get_source_header(original_xml, config)
        self.assertEqual('XXIII.', header['marc21'][0]['value'])
        self.assertEqual('149', header['marc21'][1]['value'])

    # reading of JSON configuration file which defines paths
    def read_from_json(self, readfile):
        with open(readfile, 'r') as f:
            try:
                return json.load(f)
            except ValueError:
                print('Error! Unable to read file!')
                return {}


if __name__ == '__main__':
    unittest.main()
