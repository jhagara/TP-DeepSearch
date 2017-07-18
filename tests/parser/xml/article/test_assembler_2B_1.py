import unittest
from lxml import etree
from parser.xml.article.assembler import Assembler
from parser.xml.article.chainable_equal_ratio_heading import ChainableEqualRatioHeading


class Test2B(unittest.TestCase):
    def test_scenario_2B_2_of_same_size_success(self):
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
            </document>""" # NOQA

            original_xml = etree.fromstring(original_xml)
            current_page = original_xml.xpath(
                    "/document/page[1]")[0]
            assembler = Assembler(None, current_page=current_page, ERROR=3)
            group_A = original_xml.xpath(
                    "/document/page/group[@name='A'][1]")[0]

            chainable = ChainableEqualRatioHeading(assembler)

            found_group = chainable.is_valid(group_A)
            self.assertIsNotNone(found_group)
            self.assertEqual(found_group.attrib['name'], 'N')

            group_B = original_xml.xpath(
                    "/document/page/group[@name='B'][1]")[0]

            found_group = chainable.is_valid(group_B)
            self.assertIsNotNone(found_group)
            self.assertEqual(found_group.attrib['name'], 'N')

    def test_scenario_2B_3_of_same_size_failure(self):
            original_xml = """
            <document>
                <page width="960" height="510" resolution="400">
                    <group l="10" t="10" r="950" b="210" name="N" 
                    type='headings' column_position='left'></group>
                    <group l="20" t="220" r="320" b="500" name="A"
                    type='fulltexts' column_position='left'></group>
                    <group l="330" t="220" r="430" b="500" name="B"
                    type='fulltexts' column_position='left'></group>
                </page>
            </document>"""

            original_xml = etree.fromstring(original_xml)
            group_A = original_xml.xpath(
                    "/document/page/group[@name='A'][1]")[0]
            current_page = original_xml.xpath(
                    "/document/page[1]")[0]
            assembler = Assembler(None, current_page=current_page, ERROR=3)
            chainable = ChainableEqualRatioHeading(assembler)

            found_group = chainable.is_valid(group_A)
            self.assertIsNone(found_group)
