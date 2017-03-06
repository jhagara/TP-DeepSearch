import unittest
import os
import re
from lxml import etree
from parser.xml.cleaner import Cleaner
from parser.xml.discriminator.heading import _Heading


class TestAssembler3(unittest.TestCase):

   def test_assembler_all3_success(self):

        abs_path = os.path.dirname(os.path.abspath(__file__))
        actual_xml = etree.parse(abs_path + '/test_assembler_cleaned.xml')
        actual_xml = Cleaner.clean(actual_xml)
        actual_xml = _Heading.discriminate_headings(actual_xml)
        for par in actual_xml.xpath('/document/page/block/par[not(@type)]'):
            par.attrib['type'] = 'fulltext'
        for block in actual_xml.xpath('/document/page/block[@blockType=\'Text\']'):
            block.attrib['type'] = 'text'
        desired_xml = etree.parse(abs_path + '/test_assembler_fulltext.xml')
        self.assertEqual(
            re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(desired_xml)
                  .decode('utf-8')),
            re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(actual_xml)
                  .decode('utf-8')))
