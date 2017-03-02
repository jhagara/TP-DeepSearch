import unittest
import re
from lxml import etree
from parser.xml.cleaner import Cleaner
from parser.xml.discriminator._fulltext import _Fulltext
from parser.xml.discriminator.heading import _Heading
from parser.xml.discriminator.separatorsid import SeparatorId
from parser.xml.article.merger import Preprocessor


class TestPreprocess(unittest.TestCase):
    def test_preprocessing(self):
        original_xml = """
<document version="1.0" producer="FineReader 8.0" xmlns="http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml" pagesCount="28" mainLanguage="Slovak" languages="Slovak,Czech,EnglishUnitedStates">
<page width="3462" height="4986" resolution="400" originalCoords="true">
	<block blockType="Text" l="103" t="98" r="980" b="950">
		<par>
			<line baseline="250" l="103" t="98" r="980" b="258">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					A1
				</formatting>
			</line>
		</par>
		<par>
			<line baseline="670" l="103" t="253" r="980" b="671">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					A2
				</formatting>
			</line>
		</par>
		<par>
			<line baseline="110" l="103" t="678" r="980" b="950">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					A3
				</formatting>
			</line>
		</par>
	</block>
	<block blockType="Text" l="103" t="952" r="980" b="1870">
		<par>
			<line baseline="1198" l="103" t="952" r="980" b="1200">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					B1
				</formatting>
			</line>
		</par>
		<par>
			<line baseline="1674" l="103" t="1200" r="980" b="1678">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					B2
				</formatting>
			</line>
		</par>
		<par>
			<line baseline="1866" l="103" t="1679" r="980" b="1872">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					B3
				</formatting>
			</line>
		</par>
	</block>
	<block blockType="Text" l="103" t="1872" r="980" b="2568">
		<par>
			<line baseline="2307" l="103" t="1872" r="2388" b="2310">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					C1
				</formatting>
			</line>
		</par>
		<par>
			<line baseline="2567" l="103" t="2310" r="980" b="2568">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					C2
				</formatting>
			</line>
		</par>
	</block>
	<block blockType="Text" l="103" t="2570" r="980" b="4861">
		<par>
			<line baseline="2860" l="103" t="2570" r="980" b="2861">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					D1
				</formatting>
			</line>
		</par>
		<par>
			<line baseline="3500" l="103" t="2860" r="980" b="3501">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					D2
				</formatting>
			</line>
		</par>
		<par>
			<line baseline="4160" l="103" t="3501" r="980" b="4161">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					D3
				</formatting>
			</line>
		</par>
		<par>
			<line baseline="4460" l="103" t="4161" r="980" b="4461">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					D4
				</formatting>
			</line>
		</par>
		<par>
			<line baseline="4860" l="103" t="4461" r="980" b="4861">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					D5
				</formatting>
			</line>
		</par>
	</block>
	<block blockType="Text" l="1006" t="90" r="3420" b="512">
		<par>
			<line baseline="508" l="1006" t="90" r="3420" b="512">
				<formatting lang="Slovak" ff="Arial" fs="25." spacing="-14">
					E1
				</formatting>
			</line>
		</par>
	</block>
	<block blockType="Text" l="1006" t="513" r="2001" b="2012">
		<par>
			<line baseline="1680" l="1006" t="513" r="2001" b="1684">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					F1
				</formatting>
			</line>
		</par>
		<par>
			<line baseline="2010" l="1006" t="1684" r="2001" b="2012">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					F2
				</formatting>
			</line>
		</par>
	</block>
	<block blockType="Text" l="2006" t="513" r="2801" b="2012">
		<par>
			<line baseline="1740" l="2006" t="513" r="2801" b="1748">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					G1
				</formatting>
			</line>
		</par>
		<par>
			<line baseline="2008" l="2006" t="1748" r="2801" b="2012">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					G2
				</formatting>
			</line>
		</par>
	</block>
	<block blockType="Picture" l="1006" t="2014" r="2801" b="2400">
	</block>
	<block blockType="Text" l="1006" t="2401" r="2001" b="2968">
		<par>
			<line baseline="2767" l="1006" t="2401" r="2001" b="2768">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					I1
				</formatting>
			</line>
		</par>
		<par>
			<line baseline="2967" l="1006" t="2768" r="2001" b="2968">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					I2
				</formatting>
			</line>
		</par>
	</block>
	<block blockType="Text" l="2006" t="2401" r="2801" b="2968">
		<par>
			<line baseline="2667" l="2006" t="2401" r="2801" b="2668">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					J1
				</formatting>
			</line>
		</par>
		<par>
			<line baseline="2967" l="2006" t="2668" r="2801" b="2968">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					J2
				</formatting>
			</line>
		</par>
	</block>
	<block blockType="Text" l="1006" t="2974" r="2801" b="3500">
		<par>
			<line baseline="3500" l="1006" t="2974" r="2801" b="3500">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					K1
				</formatting>
			</line>
		</par>
	</block>
	<block blockType="Text" l="1006" t="3502" r="2001" b="4980">
		<par>
			<line baseline="4478" l="1006" t="3502" r="2001" b="4480">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					L1
				</formatting>
			</line>
		</par>
		<par>
			<line baseline="4975" l="1006" t="4480" r="2001" b="4980">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					L2
				</formatting>
			</line>
		</par>
	</block>
	<block blockType="Text" l="2006" t="3502" r="2801" b="4980">
		<par>
			<line baseline="4477" l="2006" t="3502" r="2801" b="4480">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					M1
				</formatting>
			</line>
		</par>
		<par>
			<line baseline="4977" l="2006" t="4480" r="2801" b="4980">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					M2
				</formatting>
			</line>
		</par>
	</block>
	<block blockType="Text" l="2804" t="514" r="3457" b="1840">
		<par>
			<line baseline="1437" l="2804" t="514" r="3457" b="1440">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					N1
				</formatting>
			</line>
		</par>
		<par>
			<line baseline="1833" l="2804" t="1440" r="3457" b="1840">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					N2
				</formatting>
			</line>
		</par>
	</block>
	<block blockType="Text" l="2804" t="1842" r="3457" b="2440">
		<par>
			<line baseline="2137" l="2804" t="1842" r="3457" b="2140">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					O1
				</formatting>
			</line>
		</par>
		<par>
			<line baseline="2437" l="2804" t="2142" r="3457" b="2440">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					O2
				</formatting>
			</line>
		</par>
	</block>
	<block blockType="Text" l="2804" t="2441" r="3457" b="3440">
		<par>
			<line baseline="2837" l="2804" t="2441" r="3457" b="2840">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					P1
				</formatting>
			</line>
		</par>
		<par>
			<line baseline="3437" l="2804" t="3841" r="3457" b="3440">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					P2
				</formatting>
			</line>
		</par>
	</block>
	<block blockType="Text" l="2804" t="3442" r="3457" b="4967">
		<par>
			<line baseline="4167" l="2804" t="3442" r="3457" b="4167">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					Q1
				</formatting>
			</line>
		</par>
		<par>
			<line baseline="4967" l="2804" t="4167" r="3457" b="4967">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					Q2
				</formatting>
			</line>
		</par>
	</block>
</page>
</document>"""
        desired_xml = """
<document version="1.0" producer="FineReader 8.0" xmlns="http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 pagesCount="28" mainLanguage="Slovak" languages="Slovak,Czech,EnglishUnitedStates">
	<page width="3462" height="4986" resolution="400">
		<group type="fulltexts" l="103" t="98" r="980" b="4861">
			<par l="103" t="98" r="980" b="258" type="fulltext">
				<line baseline="250" l="103" t="98" r="980" b="258">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						A1
					</formatting>
			</line>
			</par>
			<par l="103" t="253" r="980" b="671" type="fulltext">
				<line baseline="670" l="103" t="253" r="980" b="671">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						A2
					</formatting>
				</line>
			</par>
			<par l="103" t="678" r="980" b="950" type="fulltext">
				<line baseline="110" l="103" t="678" r="980" b="950">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						A3
					</formatting>
				</line>
			</par>
			<par l="103" t="952" r="980" b="1200" type="fulltext">
				<line baseline="1198" l="103" t="952" r="980" b="1200">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						B1
					</formatting>
				</line>
			</par>
			<par l="103" t="1200" r="980" b="1678" type="fulltext">
				<line baseline="1674" l="103" t="1200" r="980" b="1678">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						B2
					</formatting>
				</line>
			</par>
			<par l="103" t="1679" r="980" b="1872" type="fulltext">
				<line baseline="1866" l="103" t="1679" r="980" b="1872">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						B3
					</formatting>
				</line>
			</par>
			<par l="103" t="1872" r="2388" b="2310" type="fulltext">
				<line baseline="2307" l="103" t="1872" r="2388" b="2310">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						C1
					</formatting>
				</line>
			</par>
			<par l="103" t="2310" r="980" b="2568" type="fulltext">
				<line baseline="2567" l="103" t="2310" r="980" b="2568">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						C2
					</formatting>
				</line>
			</par>
			<par l="103" t="2570" r="980" b="2861" type="fulltext">
				<line baseline="2860" l="103" t="2570" r="980" b="2861">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						D1
					</formatting>
				</line>
			</par>
			<par l="103" t="2860" r="980" b="3501" type="fulltext">
				<line baseline="3500" l="103" t="2860" r="980" b="3501">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						D2
					</formatting>
				</line>
			</par>
			<par l="103" t="3501" r="980" b="4161" type="fulltext">
				<line baseline="4160" l="103" t="3501" r="980" b="4161">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						D3
					</formatting>
				</line>
			</par>
			<par l="103" t="4161" r="980" b="4461" type="fulltext">
				<line baseline="4460" l="103" t="4161" r="980" b="4461">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						D4
					</formatting>
				</line>
			</par>
			<par l="103" t="4461" r="980" b="4861" type="fulltext">
				<line baseline="4860" l="103" t="4461" r="980" b="4861">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						D5
					</formatting>
				</line>
			</par>
                </group>
		<group type="headings" l="1006" t="90" r="3420" b="512">
			<par l="1006" t="90" r="3420" b="512" type="heading">
				<line baseline="508" l="1006" t="90" r="3420" b="512">
					<formatting lang="Slovak" ff="Arial" fs="25." spacing="-14">
						E1
					</formatting>
				</line>
			</par>
		</group>
		<group type="fulltexts" l="1006" t="513" r="2001" b="2012">
			<par l="1006" t="513" r="2001" b="1684" type="fulltext">
				<line baseline="1680" l="1006" t="513" r="2001" b="1684">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						F1
					</formatting>
				</line>
			</par>
			<par l="1006" t="1684" r="2001" b="2012" type="fulltext">
				<line baseline="2010" l="1006" t="1684" r="2001" b="2012">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						F2
					</formatting>
				</line>
			</par>
		</group>
		<group type="fulltexts"  l="2006" t="513" r="2801" b="2012">
			<par l="2006" t="513" r="2801" b="1748" type="fulltext">
				<line baseline="1740" l="2006" t="513" r="2801" b="1748">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						G1
					</formatting>
				</line>
			</par>
			<par l="2006" t="1748" r="2801" b="2012" type="fulltext">
				<line baseline="2008" l="2006" t="1748" r="2801" b="2012">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						G2
					</formatting>
				</line>
			</par>
		</group>
		<group type="separators" l="1006" t="2014" r="2801" b="2400">
			<block blockType="Picture" l="1006" t="2014" r="2801" b="2400" type="separator">
			</block>
		</group>
		<group type="fulltexts" l="1006" t="2401" r="2001" b="4980">
			<par l="1006" t="2401" r="2001" b="2768" type="fulltext">
			<line baseline="2767" l="1006" t="2401" r="2001" b="2768">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					I1
				</formatting>
			</line>
			</par>
			<par l="1006" t="2768" r="2001" b="2968" type="fulltext">
				<line baseline="2967" l="1006" t="2768" r="2001" b="2968">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						I2
					</formatting>
				</line>
			</par>
			<par l="2006" t="2401" r="2801" b="2668" type="fulltext">
				<line baseline="2667" l="2006" t="2401" r="2801" b="2668">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						J1
					</formatting>
				</line>
			</par>
			<par l="2006" t="2668" r="2801" b="2968" type="fulltext">
				<line baseline="2967" l="2006" t="2668" r="2801" b="2968">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						J2
					</formatting>
				</line>
			</par>
			<par l="1006" t="2974" r="2801" b="3500" type="fulltext">
				<line baseline="3500" l="1006" t="2974" r="2801" b="3500">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						K1
					</formatting>
				</line>
			</par>
			<par l="1006" t="3502" r="2001" b="4480" type="fulltext">
				<line baseline="4478" l="1006" t="3502" r="2001" b="4480">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						L1
					</formatting>
				</line>
			</par>
			<par l="1006" t="4480" r="2001" b="4980" type="fulltext">
				<line baseline="4975" l="1006" t="4480" r="2001" b="4980">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						L2
					</formatting>
				</line>
			</par>
			<par l="2006" t="3502" r="2801" b="4480" type="fulltext">
				<line baseline="4477" l="2006" t="3502" r="2801" b="4480">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						M1
					</formatting>
				</line>
			</par>
			<par l="2006" t="4480" r="2801" b="4980" type="fulltext">
				<line baseline="4977" l="2006" t="4480" r="2801" b="4980">
					<formatting lang="Slovak" ff="Arial" fs="7.">
						M2
					</formatting>
				</line>
			</par>
		</group>
		<group type="fulltexts" l="2804" t="514" r="3457" b="4967">
			<par l="2804" t="514" r="3457" b="1440" type="fulltext">
			<line baseline="1437" l="2804" t="514" r="3457" b="1440">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					N1
				</formatting>
			</line>
		</par>
		<par l="2804" t="1440" r="3457" b="1840" type="fulltext">
			<line baseline="1833" l="2804" t="1440" r="3457" b="1840">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					N2
				</formatting>
			</line>
		</par>
		<par l="2804" t="1842" r="3457" b="2140" type="fulltext">
			<line baseline="2137" l="2804" t="1842" r="3457" b="2140">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					O1
				</formatting>
			</line>
		</par>
		<par l="2804" t="2142" r="3457" b="2440" type="fulltext">
			<line baseline="2437" l="2804" t="2142" r="3457" b="2440">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					O2
				</formatting>
			</line>
		</par>
		<par l="2804" t="2441" r="3457" b="2840" type="fulltext">
			<line baseline="2837" l="2804" t="2441" r="3457" b="2840">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					P1
				</formatting>
			</line>
		</par>
		<par l="2804" t="3841" r="3457" b="3440" type="fulltext">
			<line baseline="3437" l="2804" t="3841" r="3457" b="3440">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					P2
				</formatting>
			</line>
		</par>
		<par l="2804" t="3442" r="3457" b="4167" type="fulltext">
			<line baseline="4167" l="2804" t="3442" r="3457" b="4167">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					Q1
				</formatting>
			</line>
		</par>
		<par l="2804" t="4167" r="3457" b="4967" type="fulltext">
			<line baseline="4967" l="2804" t="4167" r="3457" b="4967">
				<formatting lang="Slovak" ff="Arial" fs="7.">
					Q2
				</formatting>
			</line>
		</par>
		</group>
	</page>
</document>"""
        desired_xml = etree.fromstring(desired_xml)
        actual_xml = Cleaner.clean(etree.fromstring(original_xml))
        actual_xml = _Heading.discriminate_headings(actual_xml)
        # set all missing par with attrib type = None to fulltexts
        for par in actual_xml.xpath('/document/page/block/par[not(@type)]'):
            par.attrib['type'] = 'fulltext'

        # set all block with attrib blockType 'text' to contain attrib type='text'
        for block in actual_xml.xpath('/document/page/block[@blockType=\'Text\']'):
            block.attrib['type'] = 'text'
        actual_xml = SeparatorId.discriminant_separators(actual_xml)
        actual_xml = Preprocessor.preprocess(actual_xml)
        print('1: ', re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(desired_xml).decode('utf-8')))
        print('2: ', re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(actual_xml).decode('utf-8')))
        self.assertEqual(
            re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(desired_xml).decode('utf-8')),
            re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(actual_xml).decode('utf-8')))
