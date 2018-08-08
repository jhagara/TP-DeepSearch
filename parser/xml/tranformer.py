from lxml import etree

class Transformer(object):
    def tranform(self, xml_pages, pages_info):
        parsed_xml = self.__merge_pages(xml_pages, pages_info)

        return parsed_xml

    @classmethod
    def __merge_pages(self, xml_pages, pages_info):
        parsed_xml = None
        return parsed_xml