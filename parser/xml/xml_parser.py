# -*- coding: utf-8 -*-

import json
import os
import re
from lxml import etree
from parser.xml.cleaner import Cleaner
from parser.xml.source_header import SourceHeader
from parser.xml.discriminator.heading import _Heading
from parser.xml.discriminator.separatorsid import SeparatorId
from parser.xml.article.merger import Preprocessor
from parser.xml.article.assembler import Assembler
from parser.xml.schema_validator import SchemaValidator
from parser.xml.tranformer import Transformer


class XmlParser(object):
    @classmethod
    def parse(cls, header_config_path, xml_path):

        parsed_xml = etree.parse(xml_path)

        root_tag = parsed_xml.getroot().tag
        if "document".lower() in root_tag.lower():
            return cls.__parse_abbyy(header_config_path, xml_path)
        elif "alto".lower() in root_tag.lower():
            return cls.__parse_alto(header_config_path, xml_path)
        else:
            return -1

    @classmethod
    def __parse_abbyy(cls, header_config_path, xml_path):
        # load xml file to init stage
        xml = etree.parse(xml_path)

        # validate xml
        schemavalidator = SchemaValidator()
        schemavalidator.validate_inputxml(xml)

        # load header config json file
        header_config = cls.read_from_json(header_config_path)

        # first clean whole file
        xml = Cleaner.clean(xml)

        # parse header and remove used header blocks from cleaned xml
        xml, header = SourceHeader.get_source_header(xml, header_config)

        # discriminate headings
        xml = _Heading.discriminate_headings(xml)

        # set all missing par with attrib type = None to fulltexts
        for par in xml.xpath('/document/page/block/par[not(@type)]'):
            par.attrib['type'] = 'fulltext'

        # set all block with attrib blockType 'text' to contain attrib type='text'
        for block in xml.xpath('/document/page/block[@blockType=\'Text\']'):
            block.attrib['type'] = 'text'

        # discriminate separators
        xml = SeparatorId.discriminant_separators(xml)

        # preprocess xml, merge into bigger groups
        xml = Preprocessor.preprocess(xml)

        # assemble article block
        assembler = Assembler(xml)
        assembler.assembly_articles()

        # return parsed header and articles (arrays of groups)
        return xml, header, assembler.articles

    @classmethod
    def __parse_alto(cls, header_config_path, xml_path):
        # find all xmls
        dir = os.path.dirname(xml_path)
        xml_pages = []
        for file in os.listdir(dir):
            if file.endswith(".xml"):
                path = os.path.join(dir, file)
                xml = etree.parse(path)
                xml_pages.append(xml)

        # validate xml files
        schemavalidator = SchemaValidator()
        for xml in xml_pages:
            schemavalidator.validate_inputxml(xml)

        # load header config json file
        header_config = cls.read_from_json(header_config_path)

        # first clean whole file
        for xml in xml_pages:
            xml = Cleaner.clean(xml)

        # parse header and remove used header blocks from cleaned xml
        header = None
        for xml in xml_pages:
            url = xml.docinfo.URL
            file_name = url.split('/')[-1]
            page_number = int(file_name.split('_')[0])
            if page_number == 1:
                xml, header = SourceHeader.get_source_header(xml, header_config)

        # delete top marging from all pages
        for xml in xml_pages:
            for topmarging in xml.xpath('/alto/Layout/Page/TopMargin'):
                parent = topmarging.getparent()
                parent.remove(topmarging)

        # transform alto pages into abbyy xml
        transformer = Transformer()

        xml = transformer.transform(xml_pages)

        # discriminate headings
        xml = _Heading.discriminate_headings(xml)

        # set all missing par with attrib type = None to fulltexts
        for par in xml.xpath('/document/page/block/par[not(@type)]'):
            par.attrib['type'] = 'fulltext'

        # set all block with attrib blockType 'text' to contain attrib type='text'
        for block in xml.xpath('/document/page/block[@blockType=\'Text\']'):
            block.attrib['type'] = 'text'

        # discriminate separators
        xml = SeparatorId.discriminant_separators(xml)

        # preprocess xml, merge into bigger groups
        xml = Preprocessor.preprocess(xml)

        # assemble article block
        assembler = Assembler(xml)
        assembler.assembly_articles()

        # return parsed header and articles (arrays of groups)
        return xml, header, assembler.articles

    # reading of JSON configuration file which defines paths
    @classmethod
    def read_from_json(cls, readfile):
        with open(readfile, encoding='utf8') as f:
            cnfg = json.load(f)
            return cnfg

