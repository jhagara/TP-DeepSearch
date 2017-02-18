import re
import array

ERROR = 2

# purpose of this class is to identify headings
class _Heading(object):
    # indentify all headings
    @classmethod
    def discriminate_headings(cls, parsed_xml):
        for page in parsed_xml.xpath('//*[local-name() = \'page\']'):
            limit = _Heading._most_used_fs(page) + ERROR
            for par in page.xpath('.//*[local-name() = \'par\']'):
                is_heading = True
                for formatting in par.xpath('.//*[local-name() = \'formatting\']'):
                    fs = _Heading._get_fs(formatting)
                    if fs <= limit:
                        is_heading = False
                        break
                if is_heading:
                    par.set("type", "heading")
                    block = par.getparent()
                    block.set("type", "text")
        return parsed_xml

    # find the most used font size
    @classmethod
    def _most_used_fs(cls, parsed_xml):
        number_fs = [0] * 1000
        for formatting \
                in parsed_xml.xpath('.//*[local-name() = \'formatting\']'):
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

    # find median font size
    @classmethod
    def _get_median(cls, parsed_xml):
        counter = 0
        font_sizes = array.array('f')
        for block in parsed_xml.xpath('.//*[local-name() = \'block\']'):
            # checking only font sizes of paragraphs of Text blocks
            if block.get("blockType") == 'Text':
                for paragraph in block.getchildren():
                    for line in paragraph.getchildren():
                        for element in line.getchildren():
                            counter += 1
                            font_sizes.append(float(element.get("fs")))

        font_sizes = font_sizes.tolist()
        font_sizes.sort()
        median = 0
        # calculating median
        if counter != 0:
            if counter % 2 == 0:
                a = font_sizes[int(counter / 2)]
                b = font_sizes[int(counter / 2) - 1]
                median = (a + b) / 2
            else:
                median = font_sizes[int(counter / 2)]
        return median
