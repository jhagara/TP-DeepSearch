from lxml import etree
import re

# purpose of this class is to identify separators (pictures, adds, horizontal
# lines etc.) and rename blockTypes to "separator"
class SeparatorId(object):

    #main method for identifing separators
    @classmethod
    def discriminant_separators(cls, parsed_xml):

        prev_block_bottom = -1

        for node in parsed_xml.xpath('//*[local-name() = \'block\']'):
            if prev_block_bottom == -1:
                prev_block_bottom = int(node.attrib['b'])
            if node.attrib['blockType'] != 'Text':
                node = cls.__change_blocktype(node)
                prev_block_bottom = -1
            else:
                current_block_top = int(node.attrib['t'])

                if 'type' not in node.attrib or node.attrib['type'] != 'Headline':

                    if current_block_top - prev_block_bottom > 10:

                        node.getparent().append(
                        cls.__create_new_horizontal_line(node,
                        prev_block_bottom + 1,
                        current_block_top - 1))
                        prev_block_bottom = int(node.attrib['b'])
                    else:
                        prev_block_bottom = int(node.attrib['b'])
                else:
                    prev_block_bottom = -1


        return parsed_xml

    #rename type attribute to Separator
    @classmethod
    def __change_blocktype(cls, node):
        node.attrib['type'] = 'Separator'

        return node

    @classmethod
    def __create_new_horizontal_line(cls,node,top,bottom):
        new_hr = etree.Element('block')
        new_hr.text = ""
        new_hr.attrib['blockType'] = 'Picture'
        new_hr.attrib['l'] = node.attrib['l']
        new_hr.attrib['t'] = str(top)
        new_hr.attrib['r'] = node.attrib['r']
        new_hr.attrib['b'] = str(bottom)
        new_hr.attrib['type'] = 'Separator'

        return new_hr
