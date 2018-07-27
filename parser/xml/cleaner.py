import re
from lxml import etree
from parser.xml.position_helper import PositionHelper

HEADER_PER = 5  # percentage for calculating where is page header


# purpose of this class is simply in cleaning the input xml, then this cleaned
# xml is used in further steps of collecting and assembling articles
# from headings, fulltexts and separators
class Cleaner(object):
    ABBYY_DOC_ATTRS = ['producer', 'version', 'pagesCount',
                 'mainLanguage', 'languages']
    ABBYY_PAGE_ATTRS = ['resolution', 'width', 'height']
    ABBYY_BLOCK_ATTRS = ['blockType', 'l', 't', 'r', 'b']
    ABBYY_LINE_ATTRS = ['baseline', 'l', 't', 'r', 'b']
    ABBYY_FORMATTING_ATTRS = ['lang', 'ff', 'fs', 'spacing']
    ALTO_TEXTBLOCK = ['HEIGHT', 'WIDTH', 'VPOS', 'HPOS', 'language', 'STYLEREFS', 'STYLE']
    ALTO_TEXTLINE = ['BASELINE', 'HEIGHT', 'WIDTH', 'VPOS', 'HPOS', 'STYLEREFS', 'STYLE']
    ALTO_STRING = ['STYLE', 'CONTENT']

    # main function for cleaning original input xml
    @classmethod
    def clean(cls, parsed_xml):
        root_tag = parsed_xml.getroot().tag
        if "abbyy".lower() in root_tag.lower():
            return cls.__clean_abbyy(parsed_xml)
        elif "alto".lower() in root_tag.lower():
            return cls.__clean_alto(parsed_xml)
        else:
            return -1

    # PRIVATE methods

    @classmethod
    # function for cleaning abbyy input xml
    def __clean_abbyy(cls, parsed_xml):
        for node in parsed_xml.iter():
            # remove namespaces
            node = cls.__strip_ns_prefix(node)
            # keep only desired attributes
            node = cls.__abbyy_remove_unwanted_attrs(node)

        # put text from charParams into text of formatting
        # remove all charParams from formatting
        for formatting in parsed_xml.xpath('//formatting'):
            formatting = cls.__get_text_from_char_params(formatting)

        # replace hierarchy: block -> text -> par -> line,
        # with new one: block -> par -> line
        for text in parsed_xml.xpath('//text'):
            parent = text.getparent()
            for child in text.getchildren():
                parent.append(child)
            parent.remove(text)

        # remove unnecessary element region from block
        for region in parsed_xml.xpath('//region'):
            region.getparent().remove(region)

        # add coordinates to param
        for par in parsed_xml.xpath('//par'):
            PositionHelper.add_coordinates_from_child(par)

        cls.__remove_page_header(parsed_xml)
        return parsed_xml

    @classmethod
    # function for cleaning alto input xml
    def __clean_alto(cls, parsed_xml):
        for node in parsed_xml.iter():
            # remove namespaces
            node = cls.__strip_ns_prefix(node)
            # keep only desired attributes
            node = cls.__alto_remove_unwanted_attrs(node)

        for textline in parsed_xml.xpath('//TextLine'):
            textline = cls.__merge_string_elements(textline)

        return parsed_xml

    # remove namespaces from node
    @classmethod
    def __strip_ns_prefix(cls, node):
        try:
            has_namespace = node.tag.startswith('{')
        except AttributeError:
            return node
        if has_namespace:
            node.tag = node.tag.split('}', 1)[1]

        return node

    # depending on node tag name, use corresponding desired attributes
    # and push them into method for removing unwanted attributes
    @classmethod
    def __abbyy_remove_unwanted_attrs(cls, node):
        if node.tag == 'document':
            node = cls.__clear_attrs(node, Cleaner.ABBYY_DOC_ATTRS)
        elif node.tag == 'page':
            node = cls.__clear_attrs(node, Cleaner.ABBYY_PAGE_ATTRS)
        elif node.tag == 'block':
            node = cls.__clear_attrs(node, Cleaner.ABBYY_BLOCK_ATTRS)
        elif node.tag == 'line':
            node = cls.__clear_attrs(node, Cleaner.ABBYY_LINE_ATTRS)
        elif node.tag == 'formatting':
            node = cls.__clear_attrs(node, Cleaner.ABBYY_FORMATTING_ATTRS)

        return node

    # depending on node tag name, use corresponding desired attributes
    # and push them into method for removing unwanted attributes
    @classmethod
    def __alto_remove_unwanted_attrs(cls, node):
        if node.tag == 'TextBlock':
            node = cls.__clear_attrs(node, Cleaner.ALTO_TEXTBLOCK)
        elif node.tag == 'TextLine':
            node = cls.__clear_attrs(node, Cleaner.ALTO_TEXTLINE)
        elif node.tag == 'String':
            node = cls.__clear_attrs(node, Cleaner.ALTO_STRING)

        return node

    # remove all unwanted attributes from node
    @classmethod
    def __clear_attrs(cls, node, wanted_attrs):
        for unwanted_attr in list(set(node.attrib.keys()) - set(wanted_attrs)):
            node.attrib.pop(unwanted_attr)

        return node

    # strip text of all children charParams in formatting elements
    # remove all non-printable characters from formatting text
    @classmethod
    def __get_text_from_char_params(cls, formatting):
        etree.strip_tags(formatting, 'charParams')
        formatting.text = re.sub("[\a\f\n\r\t\v]", '', formatting.text)

        return formatting

    @classmethod
    def __merge_string_elements(cls, textline):
        act_string = None
        for child in textline.getchildren():
            if child.tag == 'String':
                if act_string is None:
                    child.text = child.get('CONTENT')
                    child.pop('CONTENT')
                    act_string = child
                    continue
                act_style = act_string.get('STYLE')
                child_style = child.get('STYLE')
                if act_style == child_style:
                    act_string.text = act_string.text + child.get('CONTENT')
                    textline.remove(child)
                else:
                    act_string = child
            elif child.tag == 'SP' and act_string is not None:
                act_string.text = act_string.text + ' '

        return textline


    # remove page header
    # first it calculates height where page header should be
    # then try find text that is same and removes it
    # in page_nubmer are strings that are always removed
    @classmethod
    def __remove_page_header(cls, parsed_xml):
        found = []
        page_number = ["page", "strana"]  # add strings if needed
        for page in parsed_xml.xpath('.//page'):
            page_height = page.attrib['height']
            height = int(page_height) / 100 * HEADER_PER
            query = ".//par[@b <= " + str(int(height)) + "]"
            result = page.xpath(query)
            found.extend(result)
        to_remove = []
        for i, par1 in enumerate(found):
            line1 = par1.getchildren()
            if len(line1) == 0 or len(line1[0].getchildren()) == 0:
                continue
            for par2 in found[i+1:]:
                line2 = par2.getchildren()
                if len(line2) == 0 or len(line2[0].getchildren()) == 0:
                    continue
                if par1.getchildren()[0].getchildren()[0].text.lower().replace(",", ".") == \
                        par2.getchildren()[0].getchildren()[0].text.lower().replace(",", "."):
                    to_remove.append(par1)
                    to_remove.append(par2)
                    continue
            for word in page_number:
                if word in par1.getchildren()[0].getchildren()[0].text.lower():
                    to_remove.append(par1)

        for par in to_remove:
            if par is not None and par.getparent() is not None:
                block = par.getparent()
                block.remove(par)
                if len(block.getchildren()) == 0:
                    page = block.getparent()
                    page.remove(block)



