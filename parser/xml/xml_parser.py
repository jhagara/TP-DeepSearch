import json
from lxml import etree
from parser.xml.cleaner import Cleaner
from parser.xml.source_header import SourceHeader
from parser.xml.discriminator.heading import _Heading
from parser.xml.discriminator._fulltext import _Fulltext
from parser.xml.discriminator.separatorsid import SeparatorId
from parser.xml.article.merger import Preprocessor
from parser.xml.article.assembler import Assembler


class XmlParser(object):
    @classmethod
    def parse(cls, header_config_path, xml_path):
        # load xml file to init stage
        xml = etree.parse(xml_path)
        # load header config json file
        header_config = cls.read_from_json(header_config_path)

        # first clean whole file
        xml = Cleaner.clean(xml)

        # parse header and remove used header blocks from cleaned xml
        xml, header = SourceHeader.get_source_header(xml, header_config)

        # discriminate headings
        xml = _Heading.discriminate_headings(xml)

        # discriminate fulltexts
        xml = _Fulltext.discriminate_fulltexts(xml)

        # temporary set all missing par with attrib type = None to fulltexts
        for par in xml.xpath('/document/page/block/par[not(@type)]'):
            par.attrib['type'] = 'fulltext'

        # discriminate separators
        xml = SeparatorId.discriminant_separators(xml)

        # preprocess xml, merge into bigger groups
        xml = Preprocessor.preprocess(xml)

        # assemble article block
        assembler = Assembler(xml)
        assembler.assembly_articles()

        # return parsed header and articles (arrays of groups)
        return header, assembler.articles

    # reading of JSON configuration file which defines paths
    @classmethod
    def read_from_json(cls, readfile):
        with open(readfile, 'r') as f:
            try:
                return json.load(f)
            except ValueError:
                print('Error! Unable to read file!')
                return {}
