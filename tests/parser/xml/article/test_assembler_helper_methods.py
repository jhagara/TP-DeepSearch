import unittest
from lxml import etree
from parser.xml.article.assembler import Assembler


class TestAssemblerHelperMethods(unittest.TestCase):
    def test_find_nearest_left_success(self):
        original_xml = """
        <document>
            <page width="3455" height="4871" resolution="400">
                <group l="55" t="0" r="100" b="50" name="A" type='fulltexts'></group>
                <group l="0" t="80" r="50" b="135" name="B" type='headings'></group>
                <group l="55" t="80" r="105" b="120" name="C" type='fulltexts'></group>
                <group l="55" t="125" r="100" b="200" name="D" type='fulltexts'></group>
                <group l="120" t="100" r="180" b="135" name="E" type='fulltexts'></group>
                <group l="200" t="150" r="250" b="200" name="F" type='separators'></group>
            </page>
        </document>"""

        original_xml = etree.fromstring(original_xml)
        group_E = original_xml.xpath("/document/page/group[@name='E'][1]")[0]
        current_page = original_xml.xpath("/document/page[1]")[0]

        assembler = Assembler(None, current_page=current_page, ERROR=3)
        found_group = assembler._Assembler__find_nearest_left(group_E)
        self.assertIsNotNone(found_group)
        self.assertEqual('C', found_group.attrib['name'])

    def test__success(self):
        original_xml = """
        <document>
            <page width="3455" height="4871" resolution="400">
                <group l="55" t="0" r="100" b="50" name="A" type='fulltexts'></group>
                <group l="0" t="80" r="50" b="135" name="B" type='headings'></group>
                <group l="55" t="80" r="105" b="120" name="C" type='fulltexts'></group>
                <group l="55" t="125" r="100" b="200" name="D" type='fulltexts'></group>
                <group l="120" t="100" r="180" b="135" name="E" type='fulltexts'></group>
                <group l="200" t="150" r="250" b="200" name="F" type='fulltexts'></group>
                <group l="195" t="80" r="250" b="110" name="G" type='headings'></group>
            </page>
        </document>"""

        original_xml = etree.fromstring(original_xml)
        group_E = original_xml.xpath("/document/page/group[@name='E'][1]")[0]
        current_page = original_xml.xpath("/document/page[1]")[0]

        assembler = Assembler(None, current_page=current_page, ERROR=3)
        found_group = assembler._Assembler__find_nearest_right(group_E)
        self.assertIsNotNone(found_group)
        self.assertEqual('G', found_group.attrib['name'])

    def test_find_column_position_success(self):
        original_xml = """
        <document>
            <page width="3455" height="4871" resolution="400">
                <group l="55" t="0" r="100" b="50" name="A" type='fulltexts'></group>
                <group l="0" t="80" r="50" b="135" name="B" type='headings'></group>
                <group l="55" t="80" r="105" b="120" name="C" type='fulltexts'></group>
                <group l="55" t="125" r="100" b="200" name="D" type='fulltexts'></group>
                <group l="120" t="100" r="180" b="135" name="E" type='fulltexts'></group>
                <group l="200" t="150" r="300" b="200" name="F" type='fulltexts'></group>
                <group l="195" t="80" r="250" b="110" name="G" type='headings'></group>
                <group l="55" t="300" r="100" b="300" name="M" type='fulltexts'></group>
                <group l="120" t="350" r="200" b="400" name="N" type='headings'></group>
            </page>
        </document>"""

        original_xml = etree.fromstring(original_xml)
        current_page = original_xml.xpath("/document/page[1]")[0]
        assembler = Assembler(None, current_page=current_page, ERROR=3)

        # left group
        group_B = original_xml.xpath("/document/page/group[@name='B'][1]")[0]
        self.assertEqual('left', assembler._Assembler__find_column_position(group_B))

        # middle group
        group_D = original_xml.xpath("/document/page/group[@name='D'][1]")[0]
        self.assertEqual('middle', assembler._Assembler__find_column_position(group_D))

        # middle group
        group_E = original_xml.xpath("/document/page/group[@name='E'][1]")[0]
        self.assertEqual('middle', assembler._Assembler__find_column_position(group_E))

        # middle group
        group_M = original_xml.xpath("/document/page/group[@name='M'][1]")[0]
        self.assertEqual('middle', assembler._Assembler__find_column_position(group_M))

        # middle group
        group_N = original_xml.xpath("/document/page/group[@name='N'][1]")[0]
        self.assertEqual('middle', assembler._Assembler__find_column_position(group_N))

        # right group
        group_G = original_xml.xpath("/document/page/group[@name='G'][1]")[0]
        self.assertEqual('right', assembler._Assembler__find_column_position(group_G))

    def test_find_middle_alone_success(self):
        original_xml = """
        <document>
            <page width="3455" height="4871" resolution="400">
                <group l="55" t="0" r="100" b="50" name="A" type='fulltexts' column_position='middle' chained='true'></group>
                <group l="0" t="80" r="50" b="135" name="B" type='headings' column_position='left' chained='true'></group>
                <group l="55" t="80" r="105" b="120" name="C" type='fulltexts' column_position='middle' chained='true'></group>
                <group l="55" t="125" r="100" b="200" name="D" type='fulltexts' column_position='middle'></group>
                <group l="120" t="100" r="180" b="135" name="E" type='fulltexts' column_position='middle'></group>
                <group l="200" t="150" r="250" b="200" name="F" type='fulltexts' column_position='right' chained='true'></group>
                <group l="195" t="80" r="250" b="110" name="G" type='headings' column_position='right' chained='true'></group>
            </page>
        </document>"""

        original_xml = etree.fromstring(original_xml)
        current_page = original_xml.xpath("/document/page[1]")[0]
        assembler = Assembler(None, current_page=current_page, ERROR=3)
        found_group = assembler._Assembler__find_middle_alone()

        # should return alone middle group, do not care if D or E
        self.assertIsNotNone(found_group)
        self.assert_(found_group.attrib['name'] in ['D', 'E'])

    def test_find_last_middle_success(self):
        original_xml = """
        <document>
            <page width="3455" height="4871" resolution="400">
                <group l="55" t="0" r="100" b="50" name="A" type='fulltexts' column_position='middle' chained='true'></group>
                <group l="0" t="80" r="50" b="135" name="B" type='headings' column_position='left' chained='true'></group>
                <group l="55" t="80" r="105" b="120" name="C" type='fulltexts' column_position='middle' chained='true'></group>
                <group l="55" t="125" r="100" b="200" name="D" type='fulltexts' column_position='middle'></group>
                <group l="120" t="100" r="180" b="135" name="E" type='fulltexts' column_position='middle'></group>
                <group l="200" t="150" r="250" b="200" name="F" type='fulltexts' column_position='right' chained='true'></group>
                <group l="195" t="80" r="250" b="110" name="G" type='headings' column_position='right' chained='true'></group>
                <group l="115" t="150" r="178" b="230" name="H" type='headings' column_position='middle' chained='true'></group>
            </page>
        </document>"""
        original_xml = etree.fromstring(original_xml)
        current_page = original_xml.xpath("/document/page[1]")[0]
        assembler = Assembler(None, current_page=current_page, ERROR=3)
        found_group = assembler._Assembler__find_last_middle()

        # find last element in middle column, should return element with name H
        self.assertIsNotNone(found_group)
        self.assertEqual('H', found_group.attrib['name'])

    def test_chain_groups_success(self):
        original_xml = """
        <document>
            <page width="3455" height="4871" resolution="400">
                <group l="55" t="0" r="100" b="50" name="A" type='fulltexts'></group>
                <group l="0" t="80" r="50" b="135" name="B" type='headings'></group>
                <group l="55" t="80" r="105" b="120" name="C" type='fulltexts'></group>
                <group l="55" t="125" r="100" b="200" name="D" type='fulltexts'></group>
                <group l="120" t="100" r="180" b="135" name="E" type='fulltexts'></group>
                <group l="200" t="150" r="250" b="200" name="F" type='separators'></group>
            </page>
        </document>"""
        original_xml = etree.fromstring(original_xml)
        assembler = Assembler(None, current_page_num=1, chains={1: {}})

        # chain not exists yet
        group_A = original_xml.xpath("/document/page/group[@name='A'][1]")[0]
        group_C = original_xml.xpath("/document/page/group[@name='C'][1]")[0]
        assembler._Assembler__chain_groups(group_A, group_C)

        # chain exist first group1
        group_D = original_xml.xpath("/document/page/group[@name='D'][1]")[0]
        assembler._Assembler__chain_groups(group_C, group_D)

        # new chain not exsits yet
        group_E = original_xml.xpath("/document/page/group[@name='E'][1]")[0]
        group_F = original_xml.xpath("/document/page/group[@name='F'][1]")[0]
        assembler._Assembler__chain_groups(group_E, group_F)

        # chain exist for second group 2
        group_B = original_xml.xpath("/document/page/group[@name='B'][1]")[0]
        assembler._Assembler__chain_groups(group_B, group_E)

        # should create 2 chains
        # 1 chain with elements A, C, D
        self.assertCountEqual([group_A, group_C, group_D], assembler.chains[1][1])
        # 2 chain with elements B, E, F
        self.assertCountEqual([group_B, group_E, group_F], assembler.chains[1][2])