from lxml import etree
from parser.xml.position_helper import PositionHelper

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
                    nearest = PositionHelper.get_nearest(results)

                    # nearest_many is RESULT
                    nearest_many = PositionHelper.get_relative_nearest(nearest, results)

                    # check if horizontal line is needed
                    for near in nearest_many:
                        new_line = cls.__check_if_line_needed(
                                par,
                                near,
                                parsed_xml)
                        if new_line is not None:

                            # before adding horizontal line check font sizes of paragraphs
                            fs1 = 0
                            fs2 = 0
                            for element in par.iter():
                                if element.tag=='formatting':
                                    fs1 = element.attrib['fs']
                                    break

                            for element in near.iter():
                                if element.tag=='formatting':
                                    fs2 = element.attrib['fs']
                                    break
                            if (fs1 >= fs2):
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

    # check if horizontal line needs to be added between two paragraphs
    @classmethod
    def __check_if_line_needed(cls, current, upper, parsed_xml):
        new_line = None

        if upper.attrib.get('type') == 'fulltext' and current.attrib.get('type') == 'fulltext':
            first_line = current.xpath("line[1]")
            if len(first_line) > 0:
                first_line = first_line[0]
                first_line_height = (int(first_line.attrib.get('b')) - int(first_line.attrib.get('t'))) * 2
            else:
                first_line_height = gap

            if int(current.attrib['t']) - int(upper.attrib['b']) > first_line_height:
                new_line = cls.__create_new_horizontal_line(
                        str(int(upper.attrib['b']) + 1),
                        upper.attrib['r'],
                        str(int(current.attrib['t'])-1),
                        upper.attrib['l'])
        return new_line
