import unittest
import os
import json
from semantic import Semantic
import re
from lxml import etree
from parser.xml.cleaner import Cleaner
from parser.xml.source_header import SourceHeader
from parser.xml.discriminator.heading import _Heading
from parser.xml.discriminator._fulltext import _Fulltext


class TestSemanticInit(unittest.TestCase):
    def test_basic_init_test(self):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        header_conf_path = abs_path + "/page_header_conf_1941_1.json"
        xml_path = abs_path + "/slovak_1941_1_strana_1.xml"
        semantic = Semantic(xml=xml_path, header_config=header_conf_path)
        i = 7

    def test_preprocess_xml(self):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        # just cleaned part
        with open(abs_path + '/slovak_1941_1_strana_just_cleaned.xml', 'r') as myfile:
            just_cleaned_part = re.sub("[\a\f\n\r\t\v ]", '', myfile.read())
        # cleaned anf after source header parsing
        cleaned_part = etree.parse(abs_path + '/slovak_1941_1_strana_cleaned.xml')
        with open(abs_path + '/slovak_1941_1_strana_cleaned.xml', 'r') as myfile:
            cleaned_part = re.sub("[\a\f\n\r\t\v ]", '', myfile.read())
        # load xml file to init stage
        xml = etree.parse(abs_path + '/slovak_1941_1_strana_1.xml')
        # load header config json file
        header_config = self.read_from_json(abs_path + '/page_header_conf_1941_1.json')

        # first clean whole file
        xml = Cleaner.clean(xml)

        # test just cleaned part
        self.assertEqual(just_cleaned_part,
                         re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(xml)
                                .decode('utf-8')))

        # parse header and remove used header blocks from cleaned xml
        xml, header = SourceHeader.get_source_header(xml, header_config)

        # now compare cleaned xml with xml as it should look like
        self.assertEqual(cleaned_part,
                         re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(xml)
                                .decode('utf-8')))

        # test correct types of header and fulltext
        with open(abs_path + '/slovak_1941_1_strana_header_and_fulltext.xml', 'r') as myfile:
            headed_and_fulltexted = re.sub("[\a\f\n\r\t\v ]", '', myfile.read())
        # discriminate headings
        xml = _Heading.discriminate_headings(xml)
        # discriminate fulltexts
        xml = _Fulltext.discriminate_fulltexts(xml)
        self.assertEqual(headed_and_fulltexted,
                         re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(xml)
                                .decode('utf-8')))

    # reading of JSON configuration file which defines paths
    @classmethod
    def read_from_json(cls, readfile):
        with open(readfile, 'r') as f:
            try:
                return json.load(f)
            except ValueError:
                print('Error! Unable to read file!')
                return {}


