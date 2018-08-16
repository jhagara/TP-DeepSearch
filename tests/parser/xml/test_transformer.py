import unittest
import json
import os
from lxml import etree
from parser.xml.tranformer import Transformer
from parser.xml.cleaner import Cleaner


class TestTransformer(unittest.TestCase):
    def test_transformer(self):
        dir = os.path.dirname(os.path.abspath(__file__)) + "/../../lidove_noviny/1943/19430203/XML/"
        xml_pages = []
        cleaner = Cleaner()
        for file in os.listdir(dir):
            if file.endswith(".xml"):
                path = os.path.join(dir, file)
                xml = etree.parse(path)
                xml = cleaner.clean(xml)
                xml_pages.append(xml)
        pages_info = self.read_from_json(os.path.dirname(os.path.abspath(__file__)) +
                                         "/../../lidove_noviny/1943/19430203/children.json")
        transformer = Transformer()
        parsed_xml = transformer.transform(xml_pages, pages_info)

    # reading of JSON configuration file which defines paths
    def read_from_json(self, readfile):
        with open(readfile, 'r') as f:
            try:
                return json.load(f)
            except ValueError:
                print('Error! Unable to read file!')
                return {}