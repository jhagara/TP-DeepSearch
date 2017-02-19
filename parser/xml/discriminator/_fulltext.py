import array


# class identifying which paragraphs are fulltexts
class _Fulltext(object):
    @classmethod
    def discriminate_fulltexts(cls, parsed_xml):
        median = _Fulltext._get_median(parsed_xml)
        for block in parsed_xml.xpath('//*[local-name() = \'block\']'):
            # checking only Text blocks
            if block.get("blockType") == 'Text':
                for paragraph in block.getchildren():
                    fs = 0
                    for line in paragraph.getchildren():
                        for element in line.getchildren():
                            fs = float(element.get("fs"))
                        break
                    if fs <= median:
                        paragraph.set("type", "fulltext")
        return parsed_xml

    # find median font size
    @classmethod
    def _get_median(cls, parsed_xml):
        counter = 0
        font_sizes = array.array('f')
        for block in parsed_xml.xpath('//*[local-name() = \'block\']'):
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
