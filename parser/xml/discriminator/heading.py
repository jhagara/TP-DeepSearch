import re


# purpose of this class is to identify headings
class _Heading(object):
    # indentify all headings
    @classmethod
    def discriminate_headings(cls, parsed_xml):
        most_used = _Heading._most_used_fs(parsed_xml)
        for formatting \
                in parsed_xml.xpath('//*[local-name() = \'formatting\']'):
            fs = _Heading._get_fs(formatting)
            if fs > most_used:
                par = formatting.getparent().getparent()
                is_heading = True
                for line in par.getchildren():
                    for formatting in line.getchildren():
                        formatting_fs = _Heading._get_fs(formatting)
                        if formatting_fs <= most_used:
                            is_heading = False
                if is_heading:
                    par.set("type", "heading")
                    block = par.getparent()
                    block.set("type", "text")
        return parsed_xml

    # find tho most used font size
    @classmethod
    def _most_used_fs(cls, parsed_xml):
        number_fs = [0] * 1000
        for formatting \
                in parsed_xml.xpath('//*[local-name() = \'formatting\']'):
            fs = _Heading._get_fs(formatting)
            number_fs[fs] += 1

        most_used = 0
        for i in range(0, 999):
            if number_fs[i] > number_fs[most_used]:
                most_used = i
        return most_used

    # get font size from element formatting
    @classmethod
    def _get_fs(cls, formatting):
        fs_string = formatting.get("fs")
        fs = int(re.match("\d+", fs_string).group(0))
        return fs
