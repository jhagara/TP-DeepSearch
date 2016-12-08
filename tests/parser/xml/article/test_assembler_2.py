import re
import unittest
from lxml import etree
from parser.xml.article.merger import Preprocessor


# test for usage of 2B,2C, 2A,2Di,2Dii,2Diii
class TestMerger(unittest.TestCase):
    def test_clean_output_format_success(self):
        original_xml = """<document version="1.0" producer="FineReader 8.0" pagesCount="8" mainLanguage="Slovak" languages="Slovak,Czech,EnglishUnitedStates">
               <page width="3455" height="4871" resolution="400">
                       <group type="heading" t="0" b="800" l="0" r="1700">
                       </group>
                       <group type="fulltext" t="1000" b="1700" l="0" r="1700">
                       </group>
                       <group type="separator" t="2251" b="1700" l="0" r="1500">
                       </group>
                       <group type="heading" t="1720" b="2000" l="500" r="2000">
                       </group>
                       <group type="fulltext" t="2281" b="3400" l="0" r="1000">
                       </group>
                       <group type="fulltext" t="2281" b="4800" l="1020" r="2000">
                       </group>
                       <group type="fulltext" t="1720" b=4800" l="2020" r="3450">
                       </group>
                       <group type="heading" t="0" b="500" l="2000" r="3450">
                       </group>
                       <group type="fulltext" t="520" b="1700" l="2000" r="2483">
                       </group>
                        <group type="fulltext" t="520" b="1700" l="2486" r="2969">
                       </group>
                        <group type="fulltext" t="520" b="1700" l="2972" r="3455">
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

        actual_xml = SeparatorId.discriminant_separators(
            etree.fromstring(original_xml))
        desired_xml = etree.fromstring(desired_xml)

        print(etree.tostring(actual_xml).decode('utf-8'))
        self.assertEqual(re.sub('[^\040-\176]| ', '',
                                etree.tostring(desired_xml).decode('utf-8')),
                         re.sub('[^\040-\176]| ', '',
                                etree.tostring(actual_xml).decode('utf-8')))

        self.assertEqual(re.sub('[^\040-\176]| ', '',
                                etree.tostring(desired_xml).decode('utf-8')),
                         re.sub('[^\040-\176]| ', '',
                                etree.tostring(actual_xml).decode('utf-8')))


