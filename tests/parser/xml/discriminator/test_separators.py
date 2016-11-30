import re
import unittest
from lxml import etree
from parser.xml.discriminator.separatorsid import SeparatorId

#test for identifying separators when fulltexts and headlines  identified
class TestSeparator(unittest.TestCase):
    def test_clean_output_format_success(self):
        original_xml = """
            <document version="1.0" producer="FineReader 8.0"
                    xmlns="http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    pagesCount="8" mainLanguage="Slovak" languages="Slovak,Czech,EnglishUnitedStates">
                <page width="3455" height="4871" resolution="400">
                    <block blockType="Text" l="180" t="98" r="566" b="100" type="text">
                        <par l="180" t="98" r="566" b="100" type="Fulltext">
                        </par>
                        <par l="180" t="101" r="566" b="104" type="Fulltext">
                        </par>
                    </block>
                    <block blockType="Picture" l="180" t="105" r="566" b="164">
                    </block>
                    <block blockType="Text" l="180" t="165" r="566" b="299" type="text">
                        <par l="180" t="165" r="566" b="171" type="Fulltext">
                        </par>
                        <par l="180" t="172" r="566" b="180" type="Heading">
                        </par>
                        <par l="180" t="181" r="566" b="199" type="Fulltext">
                        </par>
                        <par l="180" t="230" r="566" b="240" type="Fulltext">
                        </par>
                        <par l="180" t="260" r="566" b="299" type="Heading">
                        </par>
                    </block>
                </page>
            </document>
            """

        desired_xml = """
                <document version="1.0" producer="FineReader 8.0"
                        xmlns="http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml"
                        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                        pagesCount="8" mainLanguage="Slovak" languages="Slovak,Czech,EnglishUnitedStates">
                    <page width="3455" height="4871" resolution="400">
                        <block blockType="Text" l="180" t="98" r="566" b="100" type="text">
                            <par l="180" t="98" r="566" b="100" type="Fulltext">
                            </par>
                            <par l="180" t="101" r="566" b="104" type="Fulltext">
                            </par>
                        </block>
                        <block blockType="Picture" l="180" t="105" r="566" b="164" type="Separator">
                        </block>
                        <block blockType="Text" l="180" t="165" r="566" b="299" type="text">
                            <par l="180" t="165" r="566" b="171" type="Fulltext">
                            </par>
                            <par l="180" t="172" r="566" b="180" type="Heading">
                            </par>
                            <par l="180" t="181" r="566" b="199" type="Fulltext">
                            </par>
                            <par l="180" t="230" r="566" b="240" type="Fulltext">
                            </par>
                            <par l="180" t="260" r="566" b="299" type="Heading">
                            </par>
                        </block>
                    <block blockType="Picture" l="180" t="200" r="566" b="229" type="Separator"> </block></page>
                </document>
                """

        actual_xml = SeparatorId.discriminant_separators(etree.fromstring(original_xml))
        desired_xml = etree.fromstring(desired_xml)

        print (etree.tostring(actual_xml).decode('utf-8'))
        self.assertEqual(re.sub('[^\040-\176]| ', '', etree.tostring(desired_xml).decode('utf-8')),
                         re.sub('[^\040-\176]| ', '', etree.tostring(actual_xml).decode('utf-8')))


