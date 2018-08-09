from lxml import etree

class Transformer(object):
    def tranform(cls, xml_pages, pages_info):
        for alto_page in xml_pages:
            pages = self.__transform_xml(alto_page)
        parsed_xml = self.__merge_pages(xml_pages, pages_info)

        return parsed_xml

    @classmethod
    def __merge_pages(cls, xml_pages, pages_info):
        parsed_xml = None
        return parsed_xml

    @classmethod
    def __transform_xml(cls, alto_page):
        pages = []
        for page in alto_page.xpath('//Page'):
            new_page = etree.Element("page")
            page_atrib = page.attrib
            new_page.set("width", page_atrib.get("WIDTH"))
            new_page.set("height", page_atrib.get("HEIGHT"))
            print_space = page.xpath('//PrintSpace')
            for textblock in print_space.xpath('//TextBlock'):
                block = cls.__transform_textblock(textblock, alto_page)
                new_page.append(block)
            new_etree = etree.ElementTree(new_page)
            new_etree.docinfo.URL = alto_page.docinfo.get("URL")
            pages.append(new_etree)
        return pages

    @classmethod
    def __transform_textblock(cls, textblock, alto_page):
        new_block = etree.Element("block")
        new_block.set("blockType", "Text")
        l = textblock.get("HPOS")
        t = textblock.get("VPOS")
        r = str(int(textblock.get("HPOS")) + int(textblock.get("WIDTH")))
        b = str(int(textblock.get("VPOS")) + int(textblock.get("HEIGHT")))
        new_block.set("l", l)
        new_block.set("t", t)
        new_block.set("r", r)
        new_block.set("b", b)
        for textline in textblock.xpath('//TextLine'):
            # TODO spajat textlines s rovnakym styleref za sabou do jedneho par
            par = cls.__transform_textline(textline, textblock.get("STYLEREFS"), alto_page)
            new_block.append(par)
        return new_block


    @classmethod
    def __transform_textline(cls, textline, styleref, alto_page):
        new_line = etree.Element("par")
        new_line.set("baseline", textline.get("BASELINE"))
        l = textline.get("HPOS")
        t = textline.get("VPOS")
        r = str(int(textline.get("HPOS")) + int(textline.get("WIDTH")))
        b = str(int(textline.get("VPOS")) + int(textline.get("HEIGHT")))
        new_line.set("l", l)
        new_line.set("t", t)
        new_line.set("r", r)
        new_line.set("b", b)
        for string in textline.xpath('//String'):
            string_styleref = styleref
            if string.get("STYLEREFS") is not None:
                string_styleref = string.get("STYLEREFS")
            formatting = cls.__transform_string(string, string_styleref, alto_page)
            new_line.append(formatting)
        return new_line

    @classmethod
    def __transform_string(cls, string, styleref, alto_page):
        new_formatting = etree.Element("formatting")
        return new_formatting