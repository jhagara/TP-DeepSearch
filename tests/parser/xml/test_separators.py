import re
import unittest
from lxml import etree
from parser.xml.separatorsid import SeparatorId


class TestSeparator(unittest.TestCase):
    def test_clean_output_format_success(self):
        original_xml = """
            <document version="1.0" producer="FineReader 8.0"
                    pagesCount="8" mainLanguage="Slovak" languages="Slovak,Czech,EnglishUnitedStates">
                <page width="3455" height="4871" resolution="400">
                    <block blockType="Text" l="180" t="98" r="566" b="100">
                    </block>
                    <block blockType="Picture" l="180" t="102" r="566" b="164">
                    </block>
                    <block blockType="Text" l="180" t="165" r="566" b="170">
                    </block>
                    <block blockType="Text" l="180" t="200" r="566" b="250">
                    </block>
                    <block blockType="Text" l="180" t="300" r="566" b="400">
                    </block>
                </page>
            </document>
            """

        desired_xml = """
                <document version="1.0" producer="FineReader 8.0"
                        pagesCount="8" mainLanguage="Slovak" languages="Slovak,Czech,EnglishUnitedStates">
                    <page width="3455" height="4871" resolution="400">
                        <block blockType="Text" l="180" t="98" r="566" b="100">
                        </block>
                        <block blockType="Picture" l="180" t="102" r="566" b="164" type="Separator">
                        </block>
                        <block blockType="Text" l="180" t="165" r="566" b="170">
                        </block>
                        <block blockType="Text" l="180" t="200" r="566" b="250">
                        </block>
                        <block blockType="Text" l="180" t="300" r="566" b="400">
                        </block>
                     <block blockType="Hr" l="180" t="171" r="566" b="199" type="Separator"> </block><block blockType="Hr" l="180" t="251" r="566" b="299" type="Separator"> </block></page>
                </document>
                """

        actual_xml = SeparatorId.discriminant_separators(etree.fromstring(original_xml))
        desired_xml = etree.fromstring(desired_xml)

        print (etree.tostring(actual_xml).decode('utf-8'))
        self.assertEqual(re.sub('[^\040-\176]| ', '', etree.tostring(desired_xml).decode('utf-8')),
                         re.sub('[^\040-\176]| ', '', etree.tostring(actual_xml).decode('utf-8')))


