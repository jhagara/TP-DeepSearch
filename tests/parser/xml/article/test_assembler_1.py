import re
import unittest
from lxml import etree
from parser.xml.article.merger import Preprocessor

#test for usage of 2B,2C, 2A,2Di,2Dii,2Diii
class TestMerger(unittest.TestCase):
    def test_clean_output_format_success(self):
        original_xml = """<document version="1.0" producer="FineReader 8.0" pagesCount="8" mainLanguage="Slovak" languages="Slovak,Czech,EnglishUnitedStates">
               <page width="3455" height="4871" resolution="400">
                       <group type="heading" t="0" b="280" l="0" r="3400">
                       </group>
                       <group type="fulltext" t="285" b="2250" l="0" r="1500">
                       </group>
                       <group type="fulltext" t="285" b="2250" l="1570" r="3455">
                       </group>
                       <group type="separator" t="2251" b="2270" l="0" r="1500">
                       </group>
                       <group type="separator" t="2251" b="2270" l="1570" r="3455">
                       </group>
                       <group type="heading" t="2271" b="2280" l="0" r="2000">
                       </group>
                       <group type="fulltext" t="2281" b="3400" l="0" r="1000">
                       </group>
                       <group type="fulltext" t="2281" b="4800" l="1020" r="2000">
                       </group>
                       <group type="fulltext" t="2271" b=4800" l="2020" r="3450">
                       </group>
                       <group type="heading" t="2905" b="3000" l="2200" r="3440">
                       </group>
                       <group type="fulltext" t="3002" b="4800" l="2020" r="3450">
                       </group>
                    </page>
                    <page width="3455" height="4871" resolution="400">
                       <group type="fulltext" t="0" b="3450" l="0" r="1500">
                       </group>
                       <group type="heading" t="0" b="1580" l="1550" r="3450">
                       </group>
                       <group type="fulltext" t="2281" b="3400" l="1520" r="2000">
                       </group>
                       <group type="separator" t="2281" b="2800" l="2020" r="3450">
                       </group>
                       <group type="fulltext" t="2820" b="3400" l="2020" r="3450">
                       </group>
                       <group type="separator" t="3401" b="3440" l="1520" r="2800">
                       </group>
                       <group type="separator" t="3401" b="3440" l="2820" r="3450">
                       </group>
                       <group type="fulltext" t="3441" b="4800" l="1520" r="2450">
                       </group>
                       <group type="fulltext" t="3441" b="4800" l="2450" r="3450">
                       </group>
                    </page>
               </document>"""

        actual_xml = SeparatorId.discriminant_separators(etree.fromstring(original_xml))
        desired_xml = etree.fromstring(desired_xml)

        print (etree.tostring(actual_xml).decode('utf-8'))
        self.assertEqual(re.sub('[^\040-\176]| ', '', etree.tostring(desired_xml).decode('utf-8')),
                         re.sub('[^\040-\176]| ', '', etree.tostring(actual_xml).decode('utf-8')))



        self.assertEqual(re.sub('[^\040-\176]| ', '', etree.tostring(desired_xml).decode('utf-8')),
                         re.sub('[^\040-\176]| ', '', etree.tostring(actual_xml).decode('utf-8')))


