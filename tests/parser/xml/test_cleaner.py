import re
import unittest
from lxml import etree
from parser.xml.cleaner import Cleaner


class TestCleaner(unittest.TestCase):
    def test_clean_abbyy_success(self):
        original_xml = """
            <document version="1.0" producer="FineReader 8.0"
                    xmlns="http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xsi:schemaLocation="http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml
                    http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml"
                    pagesCount="8" mainLanguage="Slovak" languages="Slovak,Czech,EnglishUnitedStates">
                <page width="3455" height="4871" resolution="400" originalCoords="true">
                    <block blockType="Text" l="180" t="10" r="566" b="100">
                        <region>
                            <rect l="180" t="10" r="566" b="100">
                            </rect>
                        </region>
                        <text>
                            <par>
                                <line baseline="156" l="30" t="10" r="549" b="100">
                                    <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">
                                        <charParams l="195" t="10" r="229" b="100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">P</charParams>
                                        <charParams l="195" t="10" r="229" b="100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">H</charParams>
                                    </formatting>
                                </line>
                            </par>
                        </text>
                    </block>
                    <block blockType="Text" l="180" t="10" r="566" b="100">
                        <region>
                            <rect l="180" t="10" r="566" b="100">
                            </rect>
                        </region>
                        <text>
                            <par>
                                <line baseline="156" l="30" t="10" r="549" b="100">
                                    <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">
                                        <charParams l="195" t="10" r="229" b="100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">A</charParams>
                                        <charParams l="195" t="10" r="229" b="100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">.</charParams>
                                    </formatting>
                                </line>
                            </par>
                        </text>
                    </block>
                    <block blockType="Text" l="180" t="10" r="566" b="100">
                        <region>
                            <rect l="180" t="10" r="566" b="100">
                            </rect>
                        </region>
                        <text>
                            <par>
                                <line baseline="156" l="30" t="10" r="549" b="100">
                                    <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">
                                        <charParams l="195" t="10" r="229" b="100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">P</charParams>
                                        <charParams l="195" t="10" r="229" b="100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">H</charParams>
                                    </formatting>
                                </line>
                            </par>
                        </text>
                    </block>
                    <block blockType="Text" l="180" t="2000" r="566" b="2100">
                        <region>
                            <rect l="180" t="2000" r="566" b="2300">
                            </rect>
                        </region>
                        <text>
                            <par>
                                <line baseline="156" l="30" t="2000" r="549" b="2100">
                                    <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">
                                        <charParams l="195" t="2000" r="229" b="2100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">O</charParams>
                                        <charParams l="195" t="2000" r="229" b="2100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">K</charParams>
                                    </formatting>
                                </line>
                                <line baseline="156" l="195" t="2000" r="549" b="2100">
                                    <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">
                                        <charParams l="195" t="2000" r="229" b="2100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">B</charParams>
                                        <charParams l="195" t="2000" r="229" b="2100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">B</charParams>
                                    </formatting>
                                </line>
                                <line baseline="156" l="195" t="2000" r="700" b="2100">
                                    <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">
                                        <charParams l="195" t="2000" r="229" b="2100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">C</charParams>
                                        <charParams l="195" t="2000" r="229" b="2100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">C</charParams>
                                    </formatting>
                                </line>
                                <line baseline="156" l="195" t="2000" r="549" b="2100">
                                    <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">
                                        <charParams l="195" t="2000" r="229" b="2100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">D</charParams>
                                        <charParams l="195" t="2000" r="229" b="2100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">D</charParams>
                                    </formatting>
                                </line>
                            </par>
                        </text>
                    </block>
                    <block blockType="Text" l="180" t="2000" r="566" b="2300">
                        <region>
                            <rect l="180" t="2000" r="566" b="2300">
                            </rect>
                        </region>
                        <text>
                            <par>
                                <line baseline="156" l="30" t="2000" r="549" b="2300">
                                    <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">
                                        <charParams l="195" t="2000" r="229" b="2300" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">O</charParams>
                                        <charParams l="195" t="2000" r="229" b="2300" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">K</charParams>
                                    </formatting>
                                </line>
                            </par>
                        </text>
                    </block>
                </page>
                <page width="3455" height="4871" resolution="400" originalCoords="true">
                    <block blockType="Text" l="180" t="10" r="566" b="100">
                        <region>
                            <rect l="180" t="10" r="566" b="100">
                            </rect>
                        </region>
                        <text>
                            <par>
                                <line baseline="156" l="30" t="10" r="549" b="100">
                                    <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">
                                        <charParams l="195" t="10" r="229" b="100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">P</charParams>
                                        <charParams l="195" t="10" r="229" b="100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">H</charParams>
                                    </formatting>
                                </line>
                            </par>
                        </text>
                    </block>
                    <block blockType="Text" l="180" t="10" r="566" b="100">
                        <region>
                            <rect l="180" t="10" r="566" b="100">
                            </rect>
                        </region>
                        <text>
                            <par>
                                <line baseline="156" l="30" t="10" r="549" b="100">
                                    <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">
                                        <charParams l="195" t="10" r="229" b="100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">A</charParams>
                                        <charParams l="195" t="10" r="229" b="100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">,</charParams>
                                    </formatting>
                                </line>
                            </par>
                        </text>
                    </block>
                    <block blockType="Text" l="180" t="2000" r="566" b="2100">
                        <region>
                            <rect l="180" t="2000" r="566" b="2300">
                            </rect>
                        </region>
                        <text>
                            <par>
                                <line baseline="156" l="30" t="2000" r="549" b="2100">
                                    <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">
                                        <charParams l="195" t="2000" r="229" b="2100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">O</charParams>
                                        <charParams l="195" t="2000" r="229" b="2100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">K</charParams>
                                    </formatting>
                                </line>
                                <line baseline="156" l="195" t="2000" r="549" b="2100">
                                    <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">
                                        <charParams l="195" t="2000" r="229" b="2100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">B</charParams>
                                        <charParams l="195" t="2000" r="229" b="2100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">B</charParams>
                                    </formatting>
                                </line>
                                <line baseline="156" l="195" t="2000" r="700" b="2100">
                                    <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">
                                        <charParams l="195" t="2000" r="229" b="2100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">C</charParams>
                                        <charParams l="195" t="2000" r="229" b="2100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">C</charParams>
                                    </formatting>
                                </line>
                                <line baseline="156" l="195" t="2000" r="549" b="2100">
                                    <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">
                                        <charParams l="195" t="2000" r="229" b="2100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">D</charParams>
                                        <charParams l="195" t="2000" r="229" b="2100" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">D</charParams>
                                    </formatting>
                                </line>
                            </par>
                        </text>
                    </block>
                    <block blockType="Text" l="180" t="2000" r="566" b="2300">
                        <region>
                            <rect l="180" t="2000" r="566" b="2300">
                            </rect>
                        </region>
                        <text>
                            <par>
                                <line baseline="156" l="30" t="2000" r="549" b="2300">
                                    <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">
                                        <charParams l="195" t="2000" r="229" b="2300" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">O</charParams>
                                        <charParams l="195" t="2000" r="229" b="2300" wordStart="true"
                                                wordFromDictionary="true" wordNormal="true" wordNumeric="false"
                                                wordIdentifier="false" wordPenalty="1" meanStrokeWidth="96"
                                                charConfidence="38" serifProbability="26">K</charParams>
                                    </formatting>
                                </line>
                            </par>
                        </text>
                    </block>
                </page>
            </document>""" # NOQA

        desired_xml = """
            <document version="1.0" producer="FineReader 8.0"
                    xmlns="http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    pagesCount="8" mainLanguage="Slovak" languages="Slovak,Czech,EnglishUnitedStates">
                <page width="3455" height="4871" resolution="400">
                    <block blockType="Text" l="180" t="2000" r="566" b="2100">
                        <par l="30" t="2000" r="700" b="2100">
                            <line baseline="156" l="30" t="2000" r="549" b="2100">
                                <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">OK</formatting>
                            </line>
                            <line baseline="156" l="195" t="2000" r="549" b="2100">
                                <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">BB</formatting>
                            </line>
                            <line baseline="156" l="195" t="2000" r="700" b="2100">
                                <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">CC</formatting>
                            </line>
                            <line baseline="156" l="195" t="2000" r="549" b="2100">
                                <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">DD</formatting>
                            </line>
                        </par>
                    </block>
                    <block blockType="Text" l="180" t="2000" r="566" b="2300">
                        <par l="30" t="2000" r="549" b="2300">
                            <line baseline="156" l="30" t="2000" r="549" b="2300">
                                <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">OK</formatting>
                            </line>
                        </par>
                    </block>
                </page>
                <page width="3455" height="4871" resolution="400">
                    <block blockType="Text" l="180" t="2000" r="566" b="2100">
                        <par l="30" t="2000" r="700" b="2100">
                            <line baseline="156" l="30" t="2000" r="549" b="2100">
                                <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">OK</formatting>
                            </line>
                            <line baseline="156" l="195" t="2000" r="549" b="2100">
                                <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">BB</formatting>
                            </line>
                            <line baseline="156" l="195" t="2000" r="700" b="2100">
                                <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">CC</formatting>
                            </line>
                            <line baseline="156" l="195" t="2000" r="549" b="2100">
                                <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">DD</formatting>
                            </line>
                        </par>
                    </block>
                    <block blockType="Text" l="180" t="2000" r="566" b="2300">
                        <par l="30" t="2000" r="549" b="2300">
                            <line baseline="156" l="30" t="2000" r="549" b="2300">
                                <formatting lang="Czech" ff="Arial" fs="10." spacing="-2">OK</formatting>
                            </line>
                        </par>
                    </block>
                </page>
            </document>""" # NOQA

        root = etree.XML(original_xml)
        actual_xml = Cleaner.clean(etree.ElementTree(root))

        desired_xml = etree.fromstring(desired_xml)
        self.assertEqual(
                re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(desired_xml)
                       .decode('utf-8')),
                re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(actual_xml)
                       .decode('utf-8')))

    def test_clean_alto_success(self):
        original_xml = """
                    <alto xmlns="http://www.loc.gov/standards/alto/ns-v2#" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.loc.gov/standards/alto/ns-v2# http://www.loc.gov/standards/alto/alto-v2.0.xsd">
                    <Description>
                    <MeasurementUnit>pixel</MeasurementUnit>
                    <OCRProcessing ID="IdOcr"><ocrProcessingStep><processingDateTime>2015-09-15</processingDateTime><processingSoftware><softwareCreator>ABBYY</softwareCreator><softwareName>ABBYY Recognition Server</softwareName><softwareVersion>4.0</softwareVersion></processingSoftware></ocrProcessingStep></OCRProcessing>
                    </Description>
                    <Styles><TextStyle ID="font3" FONTFAMILY="Times New Roman" FONTSIZE="7"/>
                    <ParagraphStyle ID="StyleId-52FA022A-701E-44A2-B344-54320DB8388F-" ALIGN="Left" LEFT="0." RIGHT="0." FIRSTLINE="0."/>
                    </Styles>
                    <Layout>
                    <Page ID="Page1" PHYSICAL_IMG_NR="1" HEIGHT="6159" WIDTH="3924">
                    <TopMargin HEIGHT="357" WIDTH="3924" VPOS="0" HPOS="0">
                    <ComposedBlock ID="Page1_Block1" HEIGHT="66" WIDTH="3495" VPOS="277" HPOS="293" TYPE="container">
                    <TextBlock ID="Page1_Block2" HEIGHT="47" WIDTH="190" VPOS="277" HPOS="293" language="sk" STYLEREFS="StyleId-52FA022A-701E-44A2-B344-54320DB8388F- font3">
                    <TextLine BASELINE="316" HEIGHT="35" WIDTH="178" VPOS="283" HPOS="299"><String STYLE="bold" CONTENT="Strana" HEIGHT="33" WIDTH="128" VPOS="283" HPOS="299"/><SP WIDTH="18" VPOS="287" HPOS="428"/><String STYLE="bold" CONTENT="?" HEIGHT="31" WIDTH="30" VPOS="287" HPOS="447"/></TextLine>
                    </TextBlock>
                    </ComposedBlock>
                    <GraphicalElement ID="Page1_Block5" HEIGHT="48" WIDTH="2111" VPOS="0" HPOS="0"/>
                    </TopMargin>
                    <LeftMargin HEIGHT="5724" WIDTH="239" VPOS="357" HPOS="0">
                    </LeftMargin>
                    <RightMargin HEIGHT="5724" WIDTH="87" VPOS="357" HPOS="3837">
                    </RightMargin>
                    <BottomMargin HEIGHT="78" WIDTH="3924" VPOS="6081" HPOS="0">
                    </BottomMargin>
                    <PrintSpace HEIGHT="5724" WIDTH="3598" VPOS="357" HPOS="239">
                    <TextBlock ID="Page1_Block8" HEIGHT="5461" WIDTH="905" VPOS="357" HPOS="239" STYLEREFS="StyleId-52FA022A-701E-44A2-B344-54320DB8388F- font3">
                    <TextLine BASELINE="398" HEIGHT="42" WIDTH="860" VPOS="363" HPOS="277" STYLEREFS="StyleId-1E99D8DA-7651-4BFA-A8F9-829F83281F28- font3"><String CONTENT="AA" HEIGHT="33" WIDTH="122" VPOS="363" HPOS="277"/><SP WIDTH="13" VPOS="365" HPOS="400"/><String CONTENT="BB" HEIGHT="9" WIDTH="6" VPOS="375" HPOS="414"/></TextLine>
                    <TextLine BASELINE="831" HEIGHT="39" WIDTH="819" VPOS="799" HPOS="316"><String CONTENT="CC" HEIGHT="33" WIDTH="146" VPOS="799" HPOS="316"/><SP WIDTH="26" VPOS="805" HPOS="463"/><String CONTENT="DD" HEIGHT="24" WIDTH="35" VPOS="805" HPOS="490"/></TextLine>
                    </TextBlock>
                    </PrintSpace>
                    </Page>
                    </Layout>
                    </alto>
                    """  # NOQA

        desired_xml = """
                    <alto xmlns="http://www.loc.gov/standards/alto/ns-v2#" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.loc.gov/standards/alto/ns-v2# http://www.loc.gov/standards/alto/alto-v2.0.xsd">
                    <Description>
                    <MeasurementUnit>pixel</MeasurementUnit>
                    <OCRProcessing ID="IdOcr"><ocrProcessingStep><processingDateTime>2015-09-15</processingDateTime><processingSoftware><softwareCreator>ABBYY</softwareCreator><softwareName>ABBYY Recognition Server</softwareName><softwareVersion>4.0</softwareVersion></processingSoftware></ocrProcessingStep></OCRProcessing>
                    </Description>
                    <Styles><TextStyle ID="font3" FONTFAMILY="Times New Roman" FONTSIZE="7"/>
                    <ParagraphStyle ID="StyleId-52FA022A-701E-44A2-B344-54320DB8388F-" ALIGN="Left" LEFT="0." RIGHT="0." FIRSTLINE="0."/>
                    </Styles>
                    <Layout>
                    <Page ID="Page1" PHYSICAL_IMG_NR="1" HEIGHT="6159" WIDTH="3924">
                    <TopMargin HEIGHT="357" WIDTH="3924" VPOS="0" HPOS="0">
                    <ComposedBlock ID="Page1_Block1" HEIGHT="66" WIDTH="3495" VPOS="277" HPOS="293" TYPE="container">
                    <TextBlock HEIGHT="47" WIDTH="190" VPOS="277" HPOS="293" language="sk" STYLEREFS="StyleId-52FA022A-701E-44A2-B344-54320DB8388F- font3">
                    <TextLine BASELINE="316" HEIGHT="35" WIDTH="178" VPOS="283" HPOS="299"><String STYLE="bold">Strana ?</String></TextLine>
                    </TextBlock>
                    </ComposedBlock>
                    <GraphicalElement ID="Page1_Block5" HEIGHT="48" WIDTH="2111" VPOS="0" HPOS="0"/>
                    </TopMargin>
                    <LeftMargin HEIGHT="5724" WIDTH="239" VPOS="357" HPOS="0">
                    </LeftMargin>
                    <RightMargin HEIGHT="5724" WIDTH="87" VPOS="357" HPOS="3837">
                    </RightMargin>
                    <BottomMargin HEIGHT="78" WIDTH="3924" VPOS="6081" HPOS="0">
                    </BottomMargin>
                    <PrintSpace HEIGHT="5724" WIDTH="3598" VPOS="357" HPOS="239">
                    <TextBlock HEIGHT="5461" WIDTH="905" VPOS="357" HPOS="239" STYLEREFS="StyleId-52FA022A-701E-44A2-B344-54320DB8388F- font3">
                    <TextLine BASELINE="398" HEIGHT="42" WIDTH="860" VPOS="363" HPOS="277" STYLEREFS="StyleId-1E99D8DA-7651-4BFA-A8F9-829F83281F28- font3"><String>AA BB</String></TextLine>
                    <TextLine BASELINE="831" HEIGHT="39" WIDTH="819" VPOS="799" HPOS="316"><String>CC DD</String></TextLine>
                    </TextBlock>
                    </PrintSpace>
                    </Page>
                    </Layout>
                    </alto>
                    """  # NOQA  # NOQA

        root = etree.XML(original_xml)
        tree = etree.ElementTree(root)
        actual_xml = Cleaner.clean(etree.ElementTree(root))

        desired_xml = etree.fromstring(desired_xml)
        self.assertEqual(
            re.sub("[\a\f\n\r\t\v ]", ' ', etree.tostring(desired_xml)
                   .decode('utf-8')),
            re.sub("[\a\f\n\r\t\v ]", ' ', etree.tostring(actual_xml)
                   .decode('utf-8')))