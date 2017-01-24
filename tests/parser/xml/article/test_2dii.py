import unittest
from lxml import etree
from parser.xml.article.assembler import Assembler


class Test2Dii(unittest.TestCase):
    def test_2dii_success(self):
        original_xml = """
<document version="1.0" producer="FineReader 8.0" xmlns="http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml" pagesCount="1" mainLanguage="Slovak" languages="Slovak,Czech,EnglishUnitedStates">>
        <page width="3485" height="4887" resolution="400">
                <group type='headings' l="294" t="800" r="824" b="1018">
					<block blockType="Text" l="294" t="800" r="824" b="1018" type='text'>
						<par type='heading'>
							<line baseline="905" l="359" t="820" r="755" b="907">
								<formatting lang="Slovak" ff="Times New Roman" fs="19.">
									Nadpis1
								</formatting>
							</line>
							<line baseline="1013" l="309" t="933" r="808" b="1015">
								<formatting lang="Slovak" ff="Times New Roman" fs="19.">
									Nadpis2
								</formatting>
							</line>
						</par>
					</block>
				</group>
				<group type='fulltext' l="142" t="1056" r="930" b="4766">
					<block blockType="Text" l="142" t="1056" r="930" b="4766" type='text'>
						<par type='fulltext'>
							<line baseline="1086" l="441" t="1062" r="924" b="1092">
								<formatting lang="Slovak" ff="Times New Roman" fs="6.">
									Text1
								</formatting>
							</line>
						</par>
					</block>
				</group>
				<group type='text' l="950" t="3648" r="1712" b="4764">
					<block blockType="Text" l="950" t="3648" r="1712" b="4764" type="text">
						<par type='fulltext'>
							<line baseline="3681" l="958" t="3653" r="1694" b="3687">
								<formatting lang="Slovak" ff="Times New Roman" fs="6.">
									Text v strede
								</formatting>
							</line>
						</par>
					</block>
				</group>
				<group type='text' l="1726" t="3650" r="2490" b="4766">
					<block blockType="Text" l="1726" t="3650" r="2490" b="4766" type="text">
						<par type='fulltext'>
							<line baseline="3682" l="1742" t="3655" r="2478" b="3687">
								<formatting lang="Slovak" ff="Times New Roman" fs="6.">
									Text vpravo
								</formatting>
							</line>
						</par>
					</block>
				</group>
        </page>
</document>""" # NOQA

        desired_output = """
<group xmlns="http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" type="headings" l="294" t="800" r="824" b="1018" chained="true">
					<block blockType="Text" l="294" t="800" r="824" b="1018" type="text">
						<par type="heading">
							<line baseline="905" l="359" t="820" r="755" b="907">
								<formatting lang="Slovak" ff="Times New Roman" fs="19.">
									Nadpis1
								</formatting>
							</line>
							<line baseline="1013" l="309" t="933" r="808" b="1015">
								<formatting lang="Slovak" ff="Times New Roman" fs="19.">
									Nadpis2
								</formatting>
							</line>
						</par>
					</block>
				</group>
				<group xmlns="http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" type="fulltext" l="142" t="1056" r="930" b="4766" chained="true">
					<block blockType="Text" l="142" t="1056" r="930" b="4766" type="text">
						<par type="fulltext">
							<line baseline="1086" l="441" t="1062" r="924" b="1092">
								<formatting lang="Slovak" ff="Times New Roman" fs="6.">
									Text1
								</formatting>
							</line>
						</par>
					</block>
				</group>
				<group xmlns="http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" type="text" l="950" t="3648" r="1712" b="4764" chained="true">
					<block blockType="Text" l="950" t="3648" r="1712" b="4764" type="text">
						<par type="fulltext">
							<line baseline="3681" l="958" t="3653" r="1694" b="3687">
								<formatting lang="Slovak" ff="Times New Roman" fs="6.">
									Text v strede
								</formatting>
							</line>
						</par>
					</block>
				</group>
				<group xmlns="http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" type="text" l="1726" t="3650" r="2490" b="4766" chained="true">
					<block blockType="Text" l="1726" t="3650" r="2490" b="4766" type="text">
						<par type="fulltext">
							<line baseline="3682" l="1742" t="3655" r="2478" b="3687">
								<formatting lang="Slovak" ff="Times New Roman" fs="6.">
									Text vpravo
								</formatting>
							</line>
						</par>
					</block>
				</group>""" # NOQA

        assembler = Assembler(etree.fromstring(original_xml))
        Assembler.assembly_articles
        chains = assembler.chains
        for i, page in enumerate(chains):
            print("page" + i)
            for j, chain in enumerate(page):
                print("chain" + j)
                for group in chain:
                    print(group.xpath('.//formatting').text)
