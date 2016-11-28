import re
from lxml import etree


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
        formatting.text = re.sub('[^\040-\176]', '', formatting.text)

        return formatting

    # add coordinates to par element, get most left, right, top and bottom from all lines in par element
    @classmethod
    def __set_par_coordinates(self, par):
        par.attrib['l'] = par.xpath('(./line/@l[not(. > //@l)])[1]')[0]
        par.attrib['t'] = par.xpath('(./line/@t[not(. > //@t)])[1]')[0]
        par.attrib['r'] = par.xpath('(./line/@r[not(. < //@r)])[1]')[0]
        par.attrib['b'] = par.xpath('(./line/@b[not(. < //@b)])[1]')[0]



