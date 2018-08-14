from lxml import etree

class Transformer(object):

    # transforms input alto pages into one abbyy xml
    def transform(cls, xml_pages, pages_info):
        for alto_page in xml_pages:
            pages = cls.__transform_xml(alto_page)
        parsed_xml = cls.__merge_pages(xml_pages, pages_info)

        return parsed_xml

    # merge alto pages
    @classmethod
    def __merge_pages(cls, xml_pages, pages_info):
        parsed_xml = None
        return parsed_xml

    # transform single alto page
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

    # transform textblock into block
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
        act_styleref = None
        new_par = None
        # connect textlines with same styleref into par element
        for textline in textblock.xpath('//TextLine'):
            line = cls.__transform_textline(textline, textblock.get("STYLEREFS"), alto_page)
            if act_styleref == textblock.get("STYLEREFS"):
                if new_par is None:
                    new_par = etree.Element("par")
                new_par.append(line)
            else:
                if new_par is not None:
                    new_block.append(new_par)
                new_par = etree.Element("par")
                new_par.append(line)
        new_block.append(new_par)
        return new_block

    # transform textline element into line element
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

    # transform string element into formatting element
    @classmethod
    def __transform_string(cls, string, styleref, alto_page):
        new_formatting = etree.Element("formatting")
        new_formatting.text = string.text
        fontid = styleref.split()[1]
        textstyle = alto_page.xpath("/alto/Styles/TextStyle[@ID='" + fontid + "']")
        new_formatting.set("ff", textstyle.get("FONTFAMILY"))
        new_formatting.set("fs", textstyle.get("FONTSIZE") + ".")
        return new_formatting