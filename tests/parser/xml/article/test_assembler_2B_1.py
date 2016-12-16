import unittest
from lxml import etree
from parser.xml.article.assembler import Assembler
import re

def test_scenario_2B_2_of_same_size(self):
        original_xml = """
        <document>
            <page width="1020" height="510" resolution="400">
                <group l="10" t="10" r="1010" b="210" name="N" 
                type='headings' column_position='left'></group>
                <group l="20" t="220" r="505" b="500" name="A"
                type='fulltexts' column_position='left'></group>
                <group l="515" t="220" r="1000" b="500" name="B"
                type='fulltexts' column_position='left'></group>
            </page>
        </document>"""

        original_xml = etree.fromstring(original_xml)
        group_A = original_xml.xpath("/document/page/group[@name='A'][1]")[0]
        current_page = original_xml.xpath("/document/page[1]")[0]

        assembler = Assembler(None, current_page=current_page, ERROR=3)
        found_group = assembler._Assembler__chainable_equal_ratio_heading(group_A)
        list = []
        self.assertIsNotNone(found_group)
        for x in found_group:
            list.append(x.attrib['name'])
        self.assertEqual(['A', 'B'], list)

def test_scenario_2B_3_of_same_size(self):
        original_xml = """
        <document>
            <page width="960" height="510" resolution="400">
                <group l="10" t="10" r="950" b="210" name="N" 
                type='headings' column_position='left'></group>
                <group l="20" t="220" r="320" b="500" name="A"
                type='fulltexts' column_position='left'></group>
                <group l="330" t="220" r="630" b="500" name="B"
                type='fulltexts' column_position='left'></group>
                <group l="640" t="220" r="940" b="500" name="C"
                type='fulltexts' column_position='left'></group>
            </page>
        </document>"""

        original_xml = etree.fromstring(original_xml)
        group_A = original_xml.xpath("/document/page/group[@name='A'][1]")[0]
        current_page = original_xml.xpath("/document/page[1]")[0]

        assembler = Assembler(None, current_page=current_page, ERROR=3)
        found_group = assembler._Assembler__chainable_equal_ratio_heading(group_A)
        list = []
        self.assertIsNotNone(found_group)
        for x in found_group:
            list.append(x.attrib['name'])
        self.assertEqual(['A', 'B', 'C'], list)
