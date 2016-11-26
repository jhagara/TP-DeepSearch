import json
import re

from lxml import etree


class SourceHeader(object):

    @classmethod
    def get_source_header(cls, parsed_xml, header):
        # iterate through every item of list in marc21 key of input Dictionary
        for attr in header["marc21"]:
            attr['value'] = cls.__clean_and_join_list(parsed_xml.xpath(attr['path']))

        return parsed_xml, header

    # just list cleaner, join list of strings and clean string (remove all non-printable characters)
    @classmethod
    def __clean_and_join_list(cls, list):
        return re.sub('[^\040-\176]', '', ''.join(list)) if (len(list) != 0) else None

