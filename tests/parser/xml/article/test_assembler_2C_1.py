import unittest
from lxml import etree
from parser.xml.article.assembler import Assembler
import re

def test_scenario_2C_separator_bigger(self):
        original_xml = """
        <document>
            <page width="950" height="510" resolution="400">
                <group l="10" t="10" r="940" b="210" name="N" 
                type='headings' column_position='left'></group>
                <group l="20" t="220" r="320" b="500" name="FT"
                type='fulltexts' column_position='left'></group>
                <group l="330" t="220" r="930" b="500" name="S"
                type='separators' column_position='left'></group>
            </page>
        </document>"""

        original_xml = etree.fromstring(original_xml)
        group_fulltext = original_xml.xpath("/document/page/group[@name='FT'][1]")[0]
        current_page = original_xml.xpath("/document/page[1]")[0]

        assembler = Assembler(None, current_page=current_page, ERROR=3)
        found_group = assembler._Assembler__chainable_major_ratio_heading(group_fulltext)
        list = []
        self.assertIsNotNone(found_group)
        for x in found_group:
            list.append(x.attrib['name'])
        self.assertEqual(['FT'], list)

def test_scenario_2C_fulltext_bigger(self):
        original_xml = """
        <document>
            <page width="950" height="510" resolution="400">
                <group l="10" t="10" r="940" b="210" name="N" 
                type='headings' column_position='left'></group>
                <group l="20" t="220" r="320" b="500" name="S"
                type='separators' column_position='left'></group>
                <group l="330" t="220" r="930" b="500" name="FT"
                type='fulltexts' column_position='left'></group>
            </page>
        </document>"""

        original_xml = etree.fromstring(original_xml)
        group_fulltext = original_xml.xpath("/document/page/group[@name='FT'][1]")[0]
        current_page = original_xml.xpath("/document/page[1]")[0]

        assembler = Assembler(None, current_page=current_page, ERROR=3)
        found_group = assembler._Assembler__chainable_major_ratio_heading(group_fulltext)
        list = []
        self.assertIsNotNone(found_group)
        for x in found_group:
            list.append(x.attrib['name'])
        self.assertEqual(['FT'], list)
