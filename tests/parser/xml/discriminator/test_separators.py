import re
import unittest
from lxml import etree
from parser.xml.discriminator.separatorsid import SeparatorId


# test for identifying separators when fulltexts and headlines  identified
class TestSeparator(unittest.TestCase):
    def test_clean_output_format_success(self):
        original_xml = """
            <document>
                <page width="3455" height="4871" resolution="400">
                    <block blockType="Text" l="180" t="98" r="566" b="164">
                        <par l="0" t="0" r="100" b="100" type="fulltext">
                        </par>
                        <par l="101" t="0" r="200" b="100" type="heading">
                        </par>
                        <par l="201" t="0" r="300" b="100" type="fulltext">
                        </par>
                    </block>
                    <block blockType="Picture" l="0" t="120" r="300" b="147">
                    </block>
                    <block blockType="Text" l="0" t="150" r="300" b="200">
                        <par l="0" t="150" r="300" b="200" type="fulltext">
                        </par>
                    </block>
                </page>
                <page width="3455" height="4871" resolution="400">
                    <block blockType="Text" l="180" t="98" r="566" b="164">
                        <par l="0" t="0" r="100" b="100" type="fulltext">
                        </par>
                        <par l="101" t="0" r="200" b="100" type="heading">
                        </par>
                        <par l="201" t="0" r="300" b="100" type="fulltext">
                        </par>
                    </block>
                    <block blockType="Picture" l="0" t="120" r="300" b="147">
                    </block>
                    <block blockType="Text" l="0" t="150" r="300" b="200">
                        <par l="0" t="150" r="300" b="200" type="fulltext">
                        </par>
                    </block>
                </page>
            </document>
            """ # NOQA

        desired_xml = """
            <document>
                <page width="3455" height="4871" resolution="400">
                    <block blockType="Text" l="180" t="98" r="566" b="164">
                        <par l="0" t="0" r="100" b="100" type="fulltext">
                        </par>
                        <par l="101" t="0" r="200" b="100" type="heading">
                        </par>
                        <par l="201" t="0" r="300" b="100" type="fulltext">
                        </par>
                    </block>
                    <block blockType="Picture" l="0" t="120" r="300" b="147" type="separator">
                    </block>
                    <block blockType="Text" l="0" t="150" r="300" b="200">
                        <par l="0" t="150" r="300" b="200" type="fulltext">
                        </par>
                    </block>
                    <block blockType="Picture" l="0" t="101" r="100" b="149" type="separator"> </block>
                    <block blockType="Picture" l="201" t="101" r="300" b="149" type="separator"> </block></page>
                <page width="3455" height="4871" resolution="400">
                    <block blockType="Text" l="180" t="98" r="566" b="164">
                        <par l="0" t="0" r="100" b="100" type="fulltext">
                        </par>
                        <par l="101" t="0" r="200" b="100" type="heading">
                        </par>
                        <par l="201" t="0" r="300" b="100" type="fulltext">
                        </par>
                    </block>
                    <block blockType="Picture" l="0" t="120" r="300" b="147" type="separator">
                    </block>
                    <block blockType="Text" l="0" t="150" r="300" b="200">
                        <par l="0" t="150" r="300" b="200" type="fulltext">
                        </par>
                    </block>
                    <block blockType="Picture" l="0" t="101" r="100" b="149" type="separator"> </block>
                    <block blockType="Picture" l="201" t="101" r="300" b="149" type="separator"> </block></page>
            </document>
                        """ # NOQA

        actual_xml = SeparatorId.discriminant_separators(
                etree.fromstring(original_xml))
        desired_xml = etree.fromstring(desired_xml)
        print(etree.tostring(actual_xml).decode('utf-8'))
        self.assertEqual(
                re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(desired_xml)
                       .decode('utf-8')),
                re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(actual_xml)
                       .decode('utf-8')))

        self.assertEqual(
                re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(desired_xml)
                       .decode('utf-8')),
                re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(actual_xml)
                       .decode('utf-8')))
