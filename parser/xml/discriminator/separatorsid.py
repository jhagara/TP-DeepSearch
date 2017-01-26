from lxml import etree

# purpose of this class is to identify separators (pictures, adds, horizontal
# lines etc.) and rename blockTypes to "separator"
ERROR = 3
gap = 5


class SeparatorId(object):

    # main method for identifing separators
    @classmethod
    def discriminant_separators(cls, parsed_xml):

        # add attribute type to all blocks of BlockType ='Picture'/'Table/et.'
        # set type to "Separator"
        for node in parsed_xml.xpath('//*[local-name() = \'block\']'):
            if node.attrib['blockType'] != 'Text':
                node = cls.__change_blocktype(node)

        # iterate through all par elements in pages
        # find all nearest elements according to actual par element
        # nearest_many is RESULT - list of all nearest found elements
        for page in parsed_xml.xpath("/document/page"):
            for par in page.xpath("block/par"):
                os = int(int(par.attrib['l'])
                         + (int(par.attrib['r'])
                         - int(par.attrib['l']))
                         / 2)
                l = int(par.attrib['l'])
                if l >= ERROR:
                    l -= ERROR
                r = int(par.attrib['r']) + ERROR
                t = int(par.attrib['t']) + ERROR

                # De Morgan's law - check intersection - (StartA <= EndB)  and  (EndA >= StartB) # NOQA
                query = "block/par[@l <= " + str(r) + " and @r >= " + str(
                    l) + " and @b <= " + str(t) + "]"

                results = page.xpath(query)
                if len(results) != 0:
                    nearest = cls.get_nearest(results)

                    # nearest_many is RESULT
                    nearest_many = cls.get_relative_nearest(nearest, results)

                    # check if horizontal line is needed
                    for near in nearest_many:
                        new_line = cls.__check_if_line_needed(
                                par,
                                near,
                                parsed_xml)
                        if new_line is not None:
                            page.append(new_line)

        return parsed_xml

    # rename type attribute to Separator
    @classmethod
    def __change_blocktype(cls, node):
        node.attrib['type'] = 'separator'

        return node

    # create new block for horizontal line
    @classmethod
    def __create_new_horizontal_line(cls, top, right, bottom, left):
        new_hr = etree.Element('block')
        new_hr.text = ""
        new_hr.attrib['blockType'] = 'Picture'
        new_hr.attrib['l'] = left
        new_hr.attrib['t'] = top
        new_hr.attrib['r'] = right
        new_hr.attrib['b'] = bottom
        new_hr.attrib['type'] = 'separator'

        return new_hr

    # get one nearest element
    @classmethod
    def get_nearest(cls, results):
        maximum = -1
        for result in results:
            val = int(result.attrib['b'])
            if val > maximum:
                maximum = val
                max_elem = result

        return max_elem

    # get all nearest elements with usage of ERROR value
    @classmethod
    def get_relative_nearest(cls, nearest, results):
        b_max = int(nearest.attrib['b'])
        b_min = b_max - ERROR
        relative = []
        for result in results:
            b = int(result.attrib['b'])
            if b >= b_min and b <= b_max:
                    relative.append(result)

        return relative

    # check if horizontal line needs to be added between two paragraphs
    @classmethod
    def __check_if_line_needed(cls, current, upper, parsed_xml):
        new_line = None
        if upper.attrib.get('type') == 'fulltext':
            if int(current.attrib['t']) - int(upper.attrib['b']) > gap:
                new_line = cls.__create_new_horizontal_line(
                        str(int(upper.attrib['b']) + 1),
                        upper.attrib['r'],
                        str(int(current.attrib['t'])-1),
                        upper.attrib['l'])
        return new_line
