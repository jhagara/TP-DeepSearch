import re
import array
from parser.xml.position_helper import PositionHelper

ERROR = 3

# purpose of this class is to identify headings


class _Heading(object):
    # indentify all headings
    @classmethod
    def discriminate_headings(cls, parsed_xml):
        for page in parsed_xml.xpath('//*[local-name() = \'page\']'):
            limit = _Heading._most_used_fs(page) + ERROR
            for par in page.xpath('.//*[local-name() = \'par\']'):
                is_heading = True
                for formatting \
                        in par.xpath('.//*[local-name() = \'formatting\']'):
                    fs = PositionHelper.get_fs(formatting)
                    if fs <= limit:
                        is_heading = False
                        break
                if is_heading:
                    par.set("type", "heading")
        return parsed_xml

    # find the most used font size
    @classmethod
    def _most_used_fs(cls, parsed_xml):
        number_fs = [0] * 1000
        for formatting \
                in parsed_xml.xpath('.//*[local-name() = \'formatting\']'):
            fs = PositionHelper.get_fs(formatting)
            number_fs[fs] += 1

        most_used = 0
        for i in range(0, 999):
            if number_fs[i] > number_fs[most_used]:
                most_used = i
        return most_used

