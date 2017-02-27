import re
import unittest
from lxml import etree
from parser.xml.article.merger import Preprocessor


class TestMerger(unittest.TestCase):

    def test_easy_merge_output_format_success(self):

        original_xml = """<document version="1.0" producer="FineReader 8.0"
        pagesCount="8" mainLanguage="Slovak" languages="Slovak,Czech,EnglishUnitedStates">
        <page width="3455" height="4871" resolution="400">
                <block blockType="Text" l="10" t="25" r="220" b="780" type="text">
                        <par type="heading" l="10" t="25" r="220" b="256">
                        </par>
                        <par type="heading" l="10" t="257" r="220" b="780">
                        </par>
                </block>
                <block blockType="Text" l="10" t="783" r="220" b="1260" type="text">
                        <par type="heading" l="10" t="783" r="220" b="1012">
                        </par>
                        <par type="fulltext" l="10" t="1013" r="220" b="1260" >
                        </par>
                </block>
                <block blockType="Text" l="11" t="1262" r="221" b="1484" type="text">
                        <par type="fulltext" l="11" t="1262" r="221" b="1316">
                        </par>
                        <par type="fulltext" l="11" t="1317" r="221" b="1395">
                        </par>
                        <par type="fulltext" l="11" t="1396" r="221" b="1484">
                        </par>
                </block>
                <block blockType="Picture" l="240" t="25" r="280" b="65" type="separator">
                </block>
                <block blockType="Picture" l="240" t="75" r="280" b="106" type="separator">
                </block>
                <block blockType="Picture" l="240" t="109"  r="280" b="144" type="separator">
                </block>
        </page>
        <page width="3455" height="4871" resolution="400">
                <block blockType="Text" l="10" t="25" r="220" b="780" type="text">
                        <par type="heading" l="10" t="25" r="220" b="480">
                        </par>
                        <par type="heading" l="10" t="481" r="220" b="780">
                        </par>
                </block>
                <block blockType="Text" l="10" t="783" r="220" b="1260" type="text">
                        <par type="heading" l="10" t="783" r="220" b="1110">
                        </par>
                        <par type="fulltext" l="10" t="1111" r="220" b="1260">
                        </par>
                </block>
                <block blockType="Text" l="11" t="1262" r="221" b="1484" type="text">
                        <par type="fulltext" l="11" t="1262" r="221" b="1299">
                        </par>
                        <par type="fulltext" l="11" t="1300" r="221" b="1401">
                        </par>
                        <par type="fulltext" l="11" t="1402" r="221" b="1484">
                        </par>
                </block>
        </page>
        </document>""" # NOQA

        desired_xml = """<document version="1.0" producer="FineReader 8.0" pagesCount="8" mainLanguage="Slovak"
        languages="Slovak,Czech,EnglishUnitedStates">
        <page width="3455" height="4871" resolution="400">
                <group type="headings" t="25" b="1012" r="220" l="10"><par type="heading" l="10" t="783" r="220"
                 b="1012">
                        </par>
                        <par type="heading" l="10" t="257" r="220" b="780">
                        </par>
                <par type="heading" l="10" t="25" r="220" b="256">
                        </par>
                        </group><group type="fulltexts" t="1013" b="1484" r="221" l="10"><par type="fulltext" l="11"
                         t="1396" r="221" b="1484">
                        </par>
                <par type="fulltext" l="11" t="1317" r="221" b="1395">
                        </par>
                        <par type="fulltext" l="11" t="1262" r="221" b="1316">
                        </par>
                        <par type="fulltext" l="10" t="1013" r="220" b="1260">
                        </par>
                </group><group type="separators" t="25" b="144" r="280" l="240"><block blockType="Picture" l="240"
                t="109" r="280" b="144" type="separator">
                </block>
        <block blockType="Picture" l="240" t="75" r="280" b="106" type="separator">
                </block>
                <block blockType="Picture" l="240" t="25" r="280" b="65" type="separator">
                </block>
                </group></page>
        <page width="3455" height="4871" resolution="400">
                <group type="headings" t="25" b="1110" r="220" l="10"><par type="heading" l="10" t="783" r="220"
                b="1110">
                        </par>
                        <par type="heading" l="10" t="481" r="220" b="780">
                        </par>
                <par type="heading" l="10" t="25" r="220" b="480">
                        </par>
                        </group><group type="fulltexts" t="1111" b="1484" r="221" l="10"><par type="fulltext" l="11"
                        t="1402" r="221" b="1484">
                        </par>
                <par type="fulltext" l="11" t="1300" r="221" b="1401">
                        </par>
                        <par type="fulltext" l="11" t="1262" r="221" b="1299">
                        </par>
                        <par type="fulltext" l="10" t="1111" r="220" b="1260">
                        </par>
                </group></page>
        </document>""" # NOQA

        actual_xml = Preprocessor.preprocess(etree.fromstring(original_xml))
        desired_xml = etree.fromstring(desired_xml)
        self.assertEqual(
                re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(desired_xml)
                       .decode('utf-8')),
                re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(actual_xml)
                       .decode('utf-8')))

    def test_medium_merge_output_format_success(self):

        original_xml = """<document version="1.0" producer="FineReader 8.0"
        pagesCount="8" mainLanguage="Slovak" languages="Slovak,Czech,EnglishUnitedStates">
        <page width="3455" height="4871" resolution="400">
                <block blockType="Text" l="0" t="0" r="200" b="40" type="Text">
                        <par type="heading" l="0" t="0" r="200" b="40">
                        </par>
                </block>
                <block blockType="Text" l="0" t="45" r="200" b="100" type="Text">
                        <par type="fulltext" l="0" t="45" r="95" b="100">
                        </par>
                        <par type="fulltext" l="105" t="45" r="200" b="100">
                        </par>
                </block>
                <block blockType="Text" l="0" t="165" r="200" b="250" type="Text">
                        <par type="fulltext" l="0" t="165" r="95" b="250">
                        </par>
                        <par type="fulltext" l="105" t="165" r="200" b="250">
                        </par>
                </block>
                <block blockType="Text" l="0" t="105" r="200" b="160" type="Text">
                        <par type="fulltext" l="0" t="105" r="200" b="160">
                        </par>
                </block>
        </page>
        </document>""" # NOQA

        desired_xml = """<document version="1.0" producer="FineReader 8.0" pagesCount="8" mainLanguage="Slovak" languages="Slovak,Czech,EnglishUnitedStates">
        <page width="3455" height="4871" resolution="400">
                <group type="headings" t="0" b="40" r="200" l="0"><par type="heading" l="0" t="0" r="200" b="40">
                        </par>
                </group><group type="fulltexts" t="45" b="250" r="200" l="0"><par type="fulltext" l="105" t="165" r="200" b="250">
                        </par>
                <par type="fulltext" l="0" t="165" r="95" b="250">
                        </par>
                        <par type="fulltext" l="0" t="105" r="200" b="160">
                        </par>
                <par type="fulltext" l="0" t="45" r="95" b="100">
                        </par>
                        <par type="fulltext" l="105" t="45" r="200" b="100">
                        </par>
                </group></page>
        </document>""" # NOQA

        actual_xml = Preprocessor.preprocess(etree.fromstring(original_xml))
        desired_xml = etree.fromstring(desired_xml)
        self.assertEqual(
                re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(desired_xml)
                       .decode('utf-8')),
                re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(actual_xml)
                       .decode('utf-8')))
