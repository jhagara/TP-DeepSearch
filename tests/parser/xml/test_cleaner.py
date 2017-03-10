import re
import unittest
from lxml import etree
from parser.xml.cleaner import Cleaner


class TestCleaner(unittest.TestCase):
    def test_clean_output_format_success(self):
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

        actual_xml = Cleaner.clean(etree.fromstring(original_xml))
        desired_xml = etree.fromstring(desired_xml)
        self.assertEqual(
                re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(desired_xml)
                       .decode('utf-8')),
                re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(actual_xml)
                       .decode('utf-8')))
