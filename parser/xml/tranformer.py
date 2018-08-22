from lxml import etree
import re

class Transformer(object):

    # transforms input alto pages into one abbyy xml
    def transform(cls, xml_pages, pages_info):
        abbyy_pages = []
        for alto_page in xml_pages:
            pages = cls.__transform_xml(alto_page)
            abbyy_pages.append(pages)
        parsed_xml = cls.__merge_pages(abbyy_pages, pages_info)

        return parsed_xml

    # merge alto pages
    @classmethod
    def __merge_pages(cls, xml_pages, pages_info):
        document = etree.Element("document")
        page_count = 0
        for pages in xml_pages:
            page_count += len(pages)
        document.set("pagesCount", str(page_count))
        ordered_pages = []
        for info in pages_info:
            pid = info.get("pid").split(':')[1]
            for pages in xml_pages:
                url = pages[0].docinfo.URL
                pid2 = url.split("uuid_")
                if pid == pid2:
                    page_number = re.findall('\d+', info.get("details").get("pagenumber"))[0]
                    ordered_pages[page_number] = pages
        for pages in ordered_pages:
            for page in pages:
                document.append(page.root)
        new_etree = etree.ElementTree(document)
        return new_etree

    # transform single alto xml
    # returns list of transformed pages
    @classmethod
    def __transform_xml(cls, alto_page):
        pages = []
        for page in alto_page.xpath('/alto/Layout/Page'):
            new_page = etree.Element("page")
            page_atrib = page.attrib
            new_page.set("width", page_atrib.get("WIDTH"))
            new_page.set("height", page_atrib.get("HEIGHT"))
            # transform all textblock on page
            for textblock in page.xpath('//TextBlock'):
                block = cls.__transform_textblock(textblock, alto_page)
                new_page.append(block)
            # transform all graphicalElements
            for graphicalElement in page.xpath('//GraphicalElement'):
                block = cls.__transform_graphicalelement(graphicalElement)
                new_page.append(block)
            # transform all illustrations
            for illustration in page.xpath('//Illustration'):
                block = cls.__transform_illustration(illustration)
                new_page.append(block)
            new_etree = etree.ElementTree(new_page)
            new_etree.docinfo.URL = alto_page.docinfo.URL
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
        for textline in textblock.xpath('./TextLine'):
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
        for string in textline.xpath('./String'):
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
        fontid = None
        if "StyleId" in styleref:
            fontid = styleref.split()[1]
        else:
            fontid = styleref
        textstyle = alto_page.xpath("/alto/Styles/TextStyle[@ID='" + fontid + "']")[0]
        new_formatting.set("ff", textstyle.get("FONTFAMILY"))
        new_formatting.set("fs", textstyle.get("FONTSIZE") + ".")
        # TODO pridat info do formatting zo STYLE atributu - zatial nie je potrabne
        # TODO su to: bold, italics, subscript, superscript, smallcaps, underline
        return new_formatting

    # transform GraphicalElement element into block element with type="picture"
    @classmethod
    def __transform_graphicalelement(cls, graphicalelement):
        new_block = etree.Element("block")
        new_block.set("blockType", "Picture")
        l = graphicalelement.get("HPOS")
        t = graphicalelement.get("VPOS")
        r = str(int(graphicalelement.get("HPOS")) + int(graphicalelement.get("WIDTH")))
        b = str(int(graphicalelement.get("VPOS")) + int(graphicalelement.get("HEIGHT")))
        new_block.set("l", l)
        new_block.set("t", t)
        new_block.set("r", r)
        new_block.set("b", b)
        return new_block

    # transform Illustration element into block element with type="picture"
    @classmethod
    def __transform_illustration(cls, illustration):
        new_block = etree.Element("block")
        new_block.set("blockType", "Picture")
        l = illustration.get("HPOS")
        t = illustration.get("VPOS")
        r = str(int(illustration.get("HPOS")) + int(illustration.get("WIDTH")))
        b = str(int(illustration.get("VPOS")) + int(illustration.get("HEIGHT")))
        new_block.set("l", l)
        new_block.set("t", t)
        new_block.set("r", r)
        new_block.set("b", b)
        return new_block
