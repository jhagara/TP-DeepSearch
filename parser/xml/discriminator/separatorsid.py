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

                            # before adding horizontal line check font sizes of paragraphs
                            for element in par.iter():
                                if element.tag=='formatting':
                                    fs1 = element.attrib['fs']
                                    break

                            for element in near.iter():
                                if element.tag=='formatting':
                                    fs2 = element.attrib['fs']
                                    break
                            print(fs1)
                            print(fs2)
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

        if upper.attrib.get('type') == 'fulltext' and current.attrib.get('type') == 'fulltext':
            current_first_line = current.xpath("line[1]")
            current_second_line = current.xpath("line[2]")
            upper_last_line = upper.xpath("line[last()]")
            upper_belast_line = upper.xpath("line[last()-1]")

            if len(upper_last_line) > 0:
                upper_last_line = upper_last_line[0]
                if len(upper_belast_line) > 0:
                    upper_belast_line = upper_belast_line[0]
                    upper_line_h = int(upper_last_line.attrib.get('t')) - int(upper_belast_line.attrib.get('t'))
                else:
                    upper_line_h = int(upper_last_line.attrib.get('b')) - int(upper_last_line.attrib.get('t'))
            else:
                upper_line_h = gap

            if len(current_first_line) > 0:
                current_first_line = current_first_line[0]
                if len(current_second_line) > 0:
                    current_second_line = current_second_line[0]
                    current_line_h = int(current_second_line.attrib.get('t')) - int(current_first_line.attrib.get('t'))

                else:
                    current_line_h = int(current_first_line.attrib.get('b')) - int(current_first_line.attrib.get('t'))
            else:
                current_line_h = gap

            if current_line_h>upper_line_h:
                height_threshold = upper_line_h*1.5
            else:
                height_threshold = current_line_h*1.5

            if int(current.attrib['t']) - int(upper.attrib['b']) > height_threshold:
                new_line = cls.__create_new_horizontal_line(
                        str(int(upper.attrib['b']) + 1),
                        upper.attrib['r'],
                        str(int(current.attrib['t'])-1),
                        upper.attrib['l'])
        return new_line
