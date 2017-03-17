import re
from lxml import etree

HEADER_PER = 5  # percentage for calculating where is page header


# purpose of this class is simply in cleaning the input xml, then this cleaned
# xml is used in further steps of collecting and assembling articles
# from headings, fulltexts and separators
class Cleaner(object):
    DOC_ATTRS = ['producer', 'version', 'pagesCount',
                 'mainLanguage', 'languages']
    PAGE_ATTRS = ['resolution', 'width', 'height']
    BLOCK_ATTRS = ['blockType', 'l', 't', 'r', 'b']
    LINE_ATTRS = ['baseline', 'l', 't', 'r', 'b']
    FORMATTING_ATTRS = ['lang', 'ff', 'fs', 'spacing']

    # main function for cleaning original input xml
    @classmethod
    def clean(cls, parsed_xml):
        for node in parsed_xml.iter():
            # remove namespaces
            node = cls.__strip_ns_prefix(node)
            # keep only desired attributes
            node = cls.__remove_unwanted_attrs(node)

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
            cls.__set_par_coordinates(par)

        cls.__remove_page_header(parsed_xml)

        return parsed_xml

    # PRIVATE methods

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
    def __remove_unwanted_attrs(cls, node):
        if node.tag == 'document':
            node = cls.__clear_attrs(node, Cleaner.DOC_ATTRS)
        elif node.tag == 'page':
            node = cls.__clear_attrs(node, Cleaner.PAGE_ATTRS)
        elif node.tag == 'block':
            node = cls.__clear_attrs(node, Cleaner.BLOCK_ATTRS)
        elif node.tag == 'line':
            node = cls.__clear_attrs(node, Cleaner.LINE_ATTRS)
        elif node.tag == 'formatting':
            node = cls.__clear_attrs(node, Cleaner.FORMATTING_ATTRS)

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

    # add coordinates to par element, get most left, right,
    # top and bottom from all lines in par element
    @classmethod
    def __set_par_coordinates(cls, par):
        par.attrib['l'] = cls.__get_min_coord(par, 'l')
        par.attrib['t'] = cls.__get_min_coord(par, 't')
        par.attrib['r'] = cls.__get_max_coord(par, 'r')
        par.attrib['b'] = cls.__get_max_coord(par, 'b')

    # get attribute - coordinate, biggest from line
    @classmethod
    def __get_max_coord(cls, par, attr):
        maximum = -1
        for line in par.xpath("line"):
            val = int(line.attrib[attr])
            if val > maximum:
                maximum = val

        return str(maximum)

    # get attribute - coordinate, smallest or smallest from line
    @classmethod
    def __get_min_coord(cls, par, attr):
        min = 100000
        for line in par.xpath("line"):
            val = int(line.attrib[attr])
            if val < min:
                min = val

        return str(min)

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
                if par1.getchildren()[0].getchildren()[0].text.lower() == \
                        par2.getchildren()[0].getchildren()[0].text.lower():
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



