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
