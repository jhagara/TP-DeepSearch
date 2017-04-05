import json
import unittest
import os
import re
from lxml import etree
from parser.xml.source_header import SourceHeader
from parser.xml.cleaner import Cleaner


class TestSourceHeader(unittest.TestCase):
    def test_clean_output_format_success(self):
        data = self.read_from_json(
                os.path.dirname(
                    os.path.abspath(
                        __file__)) + "/page_header_conf_example.json")
        original_xml = etree.parse(
                os.path.dirname(
                    os.path.abspath(
                        __file__)) + "/page_header_example.xml")
        desired_xml = etree.parse(
                os.path.dirname(
                    os.path.abspath(
                        __file__)) + "/page_header_after_parse_example.xml")
        original_xml = Cleaner.clean(original_xml)
        desired_xml = Cleaner.clean(desired_xml)

        actual_xml, header = SourceHeader.get_source_header(original_xml, data)
        self.assertEqual('Cena 80 h?l.', header['marc21'][0]['value'])

    # reading of JSON configuration file which defines paths
    def read_from_json(self, readfile):
        with open(readfile, 'r') as f:
            try:
                return json.load(f)
            except ValueError:
                print('Error! Unable to read file!')
                return {}
