import unittest
from lxml import etree
from parser.xml.article.assembler import Assembler


class TestAssemblerHelperMethods(unittest.TestCase):
    def test_find_all_nearest_below(self):
        original_xml = """
        <document>
            <page width="3455" height="4871" resolution="400">
                <group l="10" t="10" r="100" b="30" name="A" type='fulltexts'
                column_position='left'></group>
                <group l="10" t="40" r="25" b="80" name="B" type='headings'
                column_position='left'></group>
                <group l="30" t="42" r="58" b="80" name="C"
                type='fulltexts' column_position='left'></group>
                <group l="60" t="43" r="100" b="800" name="D"
                type='headings' column_position='middle'></group>
                <group l="10" t="90" r="100" b="150" name="E"
                type='fulltexts' column_position='middle'></group>
                <group l="10" t="152" r="100" b="199" name="F"
                type='fulltexts' column_position='right'></group>
            </page>
        </document>"""
        original_xml = etree.fromstring(original_xml)
        group_A = original_xml.xpath("/document/page/group[@name='A'][1]")[0]
        current_page = original_xml.xpath("/document/page[1]")[0]

        assembler = Assembler(None, current_page=current_page, ERROR=3)
        found_group = assembler._Assembler__find_all_nearest_below(group_A)
        list = []
        self.assertIsNotNone(found_group)
        for x in found_group:
            list.append(x.attrib['name'])
        self.assertEqual(['B', 'C', 'D'], list)

    def test_find_nearest_above(self):
        original_xml = """
        <document>
            <page width="3455" height="4871" resolution="400">
                <group l="10" t="10" r="100" b="30" name="A" type='fulltexts'
                column_position='left'></group>
                <group l="10" t="40" r="25" b="80" name="B" type='headings'
                column_position='left'></group>
                <group l="30" t="42" r="58" b="80" name="C"
                type='fulltexts' column_position='left'></group>
                <group l="60" t="43" r="100" b="800" name="D"
                type='headings' column_position='middle'></group>
                <group l="10" t="90" r="100" b="150" name="E"
                type='fulltexts' column_position='middle'></group>
                <group l="10" t="152" r="100" b="199" name="F"
                type='fulltexts' column_position='right'></group>
            </page>
        </document>"""

        original_xml = etree.fromstring(original_xml)
        group_F = original_xml.xpath("/document/page/group[@name='F'][1]")[0]
        current_page = original_xml.xpath("/document/page[1]")[0]

        assembler = Assembler(None, current_page=current_page, ERROR=3)
        found_group = assembler._Assembler__find_nearest_above(group_F)
        self.assertIsNotNone(found_group)
        self.assertEqual('E', found_group.attrib['name'])
