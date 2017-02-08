import unittest
from lxml import etree
from parser.xml.discriminator.heading import _Heading
import re


class HeadingTest(unittest.TestCase):
    def test_heading_success(self):
        original_xml = """
<document version="1.0" producer="FineReader 8.0"
xmlns="http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
pagesCount="1" mainLanguage="Slovak"
languages="Slovak,Czech,EnglishUnitedStates">
<page width="3485" height="4887" resolution="400">
<block blockType="Text" l="212" t="130" r="540" b="190">
<par>
    <line baseline="185" l="227" t="139" r="536" b="186">
        <formatting lang="Czech" ff="Arial" fs="11." spacing="-9">
            Nadpis 1
        </formatting>
    </line>
</par>
<par>
    <line baseline="270" l="205" t="247" r="570" b="271">
            <formatting lang="Czech" ff="Times New Roman" fs="6.">
            Text 1
            </formatting>
    </line>
</par>
<par>
    <line baseline="369" l="204" t="348" r="564" b="370">
            <formatting lang="Czech" ff="Times New Roman" fs="6.">
            Text 1
            </formatting>
    </line>
</par>
</block>
<block blockType="Text" l="186" t="242" r="730" b="578">
<par>
    <line baseline="270" l="205" t="247" r="570" b="271">
            <formatting lang="Czech" ff="Arial" fs="11." spacing="-9">
            Nadpis 2
            </formatting>
    </line>
</par>
<par>
    <line baseline="302" l="204" t="278" r="729" b="307">
            <formatting lang="Czech" ff="Times New Roman" fs="6.">
            Text 3
            </formatting>
    </line>
    <line baseline="302" l="204" t="278" r="729" b="307">
            <formatting lang="Czech" ff="Times New Roman" fs="6.">
            Text 3
            </formatting>
    </line>
    <line baseline="302" l="204" t="278" r="729" b="307">
            <formatting lang="Czech" ff="Times New Roman" fs="6.">
            Text 3
            </formatting>
    </line>
    <line baseline="302" l="204" t="278" r="729" b="307">
            <formatting lang="Czech" ff="Times New Roman" fs="6.">
            Text 3
            </formatting>
    </line>
</par>
<par>
    <line baseline="336" l="202" t="314" r="570" b="337">
            <formatting lang="Czech" ff="Times New Roman" fs="6.">
            Text 4
            </formatting>
    </line>
</par>
</block>

<block blockType="Text" l="198" t="632" r="1038" b="686">
<par>
    <line baseline="676" l="214" t="641" r="1022" b="681">
            <formatting lang="Czech" ff="Arial" fs="24." spacing="-9">
            Nadpis 3
            </formatting>
    </line>
</par>
</block>
<block blockType="Text" l="198" t="632" r="1038" b="686">
<par>
    <line baseline="676" l="214" t="641" r="1022" b="681">
            <formatting lang="Czech" ff="Arial" fs="24." spacing="-9">
            NIENadpis 3
            </formatting>
    </line>
    <line baseline="336" l="202" t="314" r="570" b="337">
            <formatting lang="Czech" ff="Times New Roman" fs="6.">
            Text 4
            </formatting>
    </line>
</par>
</block>
<block blockType="Text" l="198" t="632" r="1038" b="686">
<par>
    <line baseline="676" l="214" t="641" r="1022" b="681">
            <formatting lang="Czech" ff="Arial" fs="24." spacing="-9">
            Nadpis 3
            </formatting>
    </line>
    <line baseline="336" l="202" t="314" r="570" b="337">
            <formatting lang="Czech" ff="Times New Roman" fs="7.">
            Podnadpis
            </formatting>
    </line>
</par>
</block>
</page>
</document>"""

        desired_xml = """
<document version="1.0" producer="FineReader 8.0"
xmlns="http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
pagesCount="1" mainLanguage="Slovak"
languages="Slovak,Czech,EnglishUnitedStates">
<page width="3485" height="4887" resolution="400">
<block blockType="Text" l="212" t="130" r="540" b="190" type="text">
<par type="heading">
    <line baseline="185" l="227" t="139" r="536" b="186">
            <formatting lang="Czech" ff="Arial" fs="11." spacing="-9">
            Nadpis 1
            </formatting>
    </line>
</par>
<par>
    <line baseline="270" l="205" t="247" r="570" b="271">
            <formatting lang="Czech" ff="Times New Roman" fs="6.">
            Text 1
            </formatting>
    </line>
</par>
<par>
    <line baseline="369" l="204" t="348" r="564" b="370">
            <formatting lang="Czech" ff="Times New Roman" fs="6.">
            Text 1
            </formatting>
    </line>
</par>
</block>
<block blockType="Text" l="186" t="242" r="730" b="578" type="text">
<par type="heading">
    <line baseline="270" l="205" t="247" r="570" b="271">
            <formatting lang="Czech" ff="Arial" fs="11." spacing="-9">
            Nadpis 2
            </formatting>
    </line>
</par>
<par>
    <line baseline="302" l="204" t="278" r="729" b="307">
            <formatting lang="Czech" ff="Times New Roman" fs="6.">
            Text 3
            </formatting>
    </line>
    <line baseline="302" l="204" t="278" r="729" b="307">
            <formatting lang="Czech" ff="Times New Roman" fs="6.">
            Text 3
            </formatting>
    </line>
    <line baseline="302" l="204" t="278" r="729" b="307">
            <formatting lang="Czech" ff="Times New Roman" fs="6.">
            Text 3
            </formatting>
    </line>
    <line baseline="302" l="204" t="278" r="729" b="307">
            <formatting lang="Czech" ff="Times New Roman" fs="6.">
            Text 3
            </formatting>
    </line>
</par>
<par>
    <line baseline="336" l="202" t="314" r="570" b="337">
            <formatting lang="Czech" ff="Times New Roman" fs="6.">
            Text 4
            </formatting>
    </line>
</par>
</block>

<block blockType="Text" l="198" t="632" r="1038" b="686" type="text">
<par type="heading">
    <line baseline="676" l="214" t="641" r="1022" b="681">
            <formatting lang="Czech" ff="Arial" fs="24." spacing="-9">
            Nadpis 3
            </formatting>
    </line>
</par>
</block>
<block blockType="Text" l="198" t="632" r="1038" b="686">
<par>
    <line baseline="676" l="214" t="641" r="1022" b="681">
            <formatting lang="Czech" ff="Arial" fs="24." spacing="-9">
            NIENadpis 3
            </formatting>
    </line>
    <line baseline="336" l="202" t="314" r="570" b="337">
            <formatting lang="Czech" ff="Times New Roman" fs="6.">
            Text 4
            </formatting>
    </line>
</par>
</block>
<block blockType="Text" l="198" t="632" r="1038" b="686" type="text">
<par type="heading">
    <line baseline="676" l="214" t="641" r="1022" b="681">
            <formatting lang="Czech" ff="Arial" fs="24." spacing="-9">
            Nadpis 3
            </formatting>
    </line>
    <line baseline="336" l="202" t="314" r="570" b="337">
            <formatting lang="Czech" ff="Times New Roman" fs="7.">
            Podnadpis
            </formatting>
    </line>
</par>
</block>
</page>
</document>"""

        actual_xml = \
            _Heading.discriminate_headings(etree.fromstring(original_xml))
        desired_xml = \
            etree.fromstring(desired_xml)
        self.assertEqual(re.sub("[\a\f\n\r\t\v ]", '',
                                etree.tostring(desired_xml).decode('utf-8')),
                         re.sub("[\a\f\n\r\t\v ]", '',
                                etree.tostring(actual_xml).decode('utf-8')))
