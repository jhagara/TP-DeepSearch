import unittest
from lxml import etree
from parser.xml.article.assembler import Assembler


class TestAssemblerHelperMethods(unittest.TestCase):
    def test_find_last_from_previous_page_success(self):
        original_xml = """
        <document>
            <page width="3455" height="4871" resolution="400">
                <group l="10" t="10" r="50" b="65" name="A" type='fulltexts' column_position='left'></group>
                <group l="10" t="70" r="49" b="95" name="B" type='headings' column_position='left'></group>
                <group l="10" t="100" r="52" b="220" name="C" type='fulltexts' column_position='left'></group>
                <group l="55" t="15" r="115" b="120" name="D" type='headings' column_position='middle'></group>
                <group l="55" t="125" r="120" b="215" name="E" type='fulltexts' column_position='middle'></group>
                <group l="120" t="12" r="220" b="115" name="F" type='fulltexts' column_position='right'></group>
                <group l="120" t="120" r="210" b="205" name="G" type='separators' column_position='right'></group>
            </page>
            <page width="3455" height="4871" resolution="400">
                <group l="10" t="10" r="50" b="65" name="A" type='fulltexts' column_position='left'></group>
                <group l="10" t="70" r="49" b="95" name="B" type='headings' column_position='left'></group>
                <group l="10" t="100" r="52" b="220" name="C" type='fulltexts' column_position='left'></group>
                <group l="55" t="15" r="115" b="120" name="D" type='headings' column_position='middle'></group>
                <group l="55" t="125" r="120" b="215" name="E" type='fulltexts' column_position='middle'></group>
                <group l="120" t="12" r="220" b="115" name="F" type='fulltexts' column_position='right'></group>
                <group l="120" t="120" r="210" b="205" name="G" type='fulltexts' column_position='right'></group>
            </page>
        </document>"""

        original_xml = etree.fromstring(original_xml)
        pages = original_xml.xpath("/document/page")
        previous_page = pages[0]
        groups = previous_page.xpath("group[@column_position = 'right']")
        max = 0

        if groups[0] is not None:
            result = groups[0]

            for group in groups:
                b = int(group.attrib['b'])
                if group.attrib['type'] != 'separators' and max < b:
                    max = b
                    result = group

        self.assertEqual('F', result.attrib['name'])


