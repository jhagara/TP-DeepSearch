import unittest
import os
import re
from lxml import etree
from parser.xml.article.merger import Preprocessor


class TestAssembler3Preprocess(unittest.TestCase):

    def test_assembler_all3_preprocess_success(self):

        abs_path = os.path.dirname(os.path.abspath(__file__))
        actual_xml = etree.parse(abs_path + '/test_assembler_separators.xml')
        actual_xml = Preprocessor.preprocess(actual_xml)
        desired_xml = etree.parse(abs_path + '/test_assembler_preprocess.xml')
        self.assertEqual(
            re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(desired_xml)
                .decode('utf-8')),
            re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(actual_xml)
                .decode('utf-8')))

