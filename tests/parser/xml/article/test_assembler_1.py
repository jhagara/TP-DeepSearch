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
                        N1
                    </group>
                    <group type="fulltext" t="285" b="2250" l="0" r="1500">
                        FN1
                    </group>
                    <group type="fulltext" t="285" b="2250" l="1570" r="3455">
                        FN1
                    </group>
                    <group type="separator" t="2251" b="2270" l="0" r="1500">
                    </group>
                    <group type="separator" t="2251" b="2270" l="1570" r="3455">
                    </group>
                    <group type="heading" t="2271" b="2280" l="0" r="2000">
                        N2
                    </group>
                    <group type="fulltext" t="2281" b="3400" l="0" r="1000">
                        FN2
                    </group>
                    <group type="fulltext" t="2281" b="4800" l="1020" r="2000">
                        FN2
                    </group>
                    <group type="fulltext" t="2271" b=4800" l="2020" r="3450">
                        FN2
                    </group>
                    <group type="heading" t="2905" b="3000" l="2200" r="3440">
                        N3
                    </group>
                    <group type="fulltext" t="3002" b="4800" l="2020" r="3450">
                        FN3
                    </group>
                </page>
                <page width="3455" height="4871" resolution="400">
                    <group type="fulltext" t="0" b="3450" l="0" r="1500">
                        FN3
                    </group>
                    <group type="heading" t="0" b="1580" l="1550" r="3450">
                        N4
                    </group>
                    <group type="fulltext" t="2281" b="3400" l="1520" r="2000">
                        FN4
                    </group>
                    <group type="separator" t="2281" b="2800" l="2020" r="3450">
                    </group>
                    <group type="fulltext" t="2820" b="3400" l="2020" r="3450">
                        FN4
                    </group>
                    <group type="separator" t="3401" b="3440" l="1520" r="2800">
                    </group>
                    <group type="separator" t="3401" b="3440" l="2820" r="3450">
                    </group>
                    <group type="fulltext" t="3441" b="4800" l="1520" r="2450">
                        FN3
                    </group>
                    <group type="fulltext" t="3441" b="4800" l="2450" r="3450">
                        FN3
                    </group>
                </page>
                <page width="3455" height="4871" resolution="400">
                    <group type="heading" t="0" b="800" l="0" r="1700">
                        N5
                    </group>
                    <group type="fulltext" t="1000" b="1700" l="0" r="1700">
                        FN5
                    </group>
                    <group type="separator" t="2251" b="1700" l="0" r="1500">
                    </group>
                    <group type="heading" t="1720" b="2000" l="500" r="2000">
                        N6
                    </group>
                    <group type="fulltext" t="2281" b="3400" l="0" r="1000">
                        FN6
                    </group>
                    <group type="fulltext" t="2281" b="4800" l="1020" r="2000">
                        FN6
                    </group>
                    <group type="fulltext" t="1720" b=4800" l="2020" r="3450">
                        FN6
                    </group>
                    <group type="heading" t="0" b="500" l="2000" r="3450">
                        N7
                    </group>
                    <group type="fulltext" t="520" b="1700" l="2000" r="2483">
                        FN7
                    </group>
                    <group type="fulltext" t="520" b="1700" l="2486" r="2969">
                        FN7
                    </group>
                    <group type="fulltext" t="520" b="1700" l="2972" r="3455">
                        FN7
                    </group>
                </page>
                <page width="3455" height="4871" resolution="400">
                    <group type="heading" t="0" b="1000" l="200" r="3200">
                        N8
                    </group>
                    <group type="fulltext" t="1100" b="2500" l="0" r="1152">
                        FN8
                    </group>
                    <group type="fulltext" t="1100" b="2500" l="1157" r="2308">
                        FN8
                    </group>
                    <group type="fulltext" t="1100" b="2500" l="2309" r="3455">
                        FN8
                    </group>
                    <group type="heading" t="2521 b="2540" l="0" r="2000">
                        N9
                    </group>
                    <group type="fulltext" t="2545" b="4871" l="0" r="1000">
                        FN9
                    </group>
                    <group type="fulltext" t="2545" b="4871" l="1010" r="2000">
                        FN9
                    </group>
                    <group type="heading" t="2521" b="2561" l="2020" r="3400">
                        N10
                    </group>
                    <group type="fulltext" t="2565" b="4800" l="1520" r="2450">
                        FN10
                    </group>
                    <group type="separators" t="3441" b="4800" l="2500" r="3450">
                    </group>
                </page>
                <page width="3455" height="4871" resolution="400">
                    <group type="heading" t="0" b="540" l="100" r="600">
                        N11
                    </group>
                    <group type="fulltext" t="550" b="4871" l="0" r="700">
                        FN11
                    </group>
                    <group type="heading" t="0" b="545" l="900" r="2200">
                        N12
                    </group>
                    <group type="fulltext" t="550" b="2500" l="800" r="1608">
                        FN12
                    </group>
                    <group type="separator" t="2501" b="2520" l="800" r="1608">
                    </group>
                    <group type="separator" t="550" b="2500" l="1640" r="2200">
                    </group>
                    <group type="heading" t="2521" b="2550" l="900" r="2200">
                        N13
                    </group>
                    <group type="fulltext" t="2700" b="4870" l="800" r="1607">
                        FN13
                    </group>
                    <group type="fulltext" t="2700" b="4870" l="1640" r="2200">
                        FN13
                    </group>
                    <group type="fulltext" t="0" b="4871" l="2400" r="3450">
                        FN13
                    </group>
                </page>
                <page width="3455" height="4871" resolution="400">
                    <group type="heading" t="0" b="540" l="500" r="3000">
                        N14
                    </group>
                    <group type="fulltext" t="550" b="4871" l="0" r="1100">
                        FN14
                    </group>
                    <group type="fulltext" t="550" b="1800" l="1120" r="2250">
                        FN14
                    </group>
                    <group type="fulltext" t="550" b="4871" l="2300" r="3450">
                        FN14
                    </group>
                    <group type="separator" t="2000" b="2520" l="1150" r="2200">
                    </group>
                    <group type="fulltext" t="2600" b="4870" l="1120" r="2250">
                        FN14
                    </group>
                </page>
                <page width="3455" height="4871" resolution="400">
                    <group type="heading" t="0" b="540" l="100" r="600">
                        N15
                    </group>
                    <group type="fulltext" t="550" b="2000" l="0" r="3400">
                        FN15
                    </group>
                    <group type="separator" t="2001" b="2080" l="0" r="3400">
                    </group>
                    <group type="fulltext" t="2081" b="4871" l="0" r="1100">
                        FN14
                    </group>
                    <group type="fulltext" t="2081" b="4871" l="1120" r="2200">
                        FN14
                    </group>
                    <group type="fulltext" t="2081" b="4871" l="2220" r="3400">
                        FN14
                    </group>
                </page>
                <page width="3455" height="4871" resolution="400">
                    <group type="separator" t="0" b="540" l="0" r="600">
                    </group>
                    <group type="fulltext" t="550" b="4871" l="0" r="700">
                        FN15
                    </group>
                    <group type="heading" t="0" b="545" l="900" r="2200">
                        N16
                    </group>
                    <group type="fulltext" t="550" b="2500" l="800" r="1608">
                        FN16
                    </group>
                    <group type="separator" t="2501" b="2520" l="800" r="1608">
                    </group>
                    <group type="heading" t="2521" b="2550" l="900" r="2200">
                        N17
                    </group>
                    <group type="fulltext" t="2700" b="3200" l="800" r="2200">
                        FN17
                    </group>
                    <group type="heading" t="3220" b="3300" l="900" r="2020">
                        N18
                    </group>
                    <group type="fulltext" t="3370" b="4871" l="800" r="2200">
                        FN18
                    </group>
                    <group type="fulltext" t="0" b="4870" l="2300" r="3455">
                        FN18
                    </group>
                </page>
               </document>""" # NOQA
