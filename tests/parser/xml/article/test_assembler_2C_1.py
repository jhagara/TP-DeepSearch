import unittest
from lxml import etree
from parser.xml.article.assembler import Assembler
from parser.xml.article.chainable_major_ratio_heading import ChainableMajorRatioHeading


class Test2C(unittest.TestCase):
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
            </document>""" # NOQA

            original_xml = etree.fromstring(original_xml)
            group_fulltext = original_xml.xpath(
                    "/document/page/group[@name='FT'][1]")[0]
            current_page = original_xml.xpath(
                    "/document/page[1]")[0]
            assembler = Assembler(None, current_page=current_page, ERROR=3)
            chainable = ChainableMajorRatioHeading(assembler)

            found_group = chainable.is_valid(group_fulltext)
            self.assertIsNotNone(found_group)
            self.assertEqual(found_group.attrib['name'], 'N')

    def test_scenario_2C_fulltext_bigger(self):
            original_xml = """
            <document>
                <page width="950" height="510" resolution="400">
                    <group l="10" t="10" r="940" b="210" name="N" 
                    type='headings' column_position='left'></group>
                    <group l="20" t="220" r="320" b="500" name="FT_smaller"
                    type='fulltexts' column_position='left'></group>
                    <group l="330" t="220" r="930" b="500" name="FT_bigger"
                    type='fulltexts' column_position='left'></group>
                </page>
            </document>"""

            original_xml = etree.fromstring(original_xml)
            current_page = original_xml.xpath(
                    "/document/page[1]")[0]
            assembler = Assembler(None, current_page=current_page, ERROR=3)
            chainable = ChainableMajorRatioHeading(assembler)
            group_fulltext_bigger = original_xml.xpath(
                    "/document/page/group[@name='FT_bigger'][1]")[0]

            # bigger success
            found_group = chainable.is_valid(group_fulltext_bigger)
            self.assertIsNotNone(found_group)
            self.assertEqual(found_group.attrib['name'], 'N')

            # smaller failure
            group_smaller_bigger = original_xml.xpath(
                    "/document/page/group[@name='FT_smaller'][1]")[0]

            found_group = chainable.is_valid(group_smaller_bigger)
            self.assertIsNone(found_group)
