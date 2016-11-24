from lxml import etree
import re

# purpose of this class is to identify separators (pictures, adds, horizontal
# lines etc.) and rename blockTypes to "separator"
class SeparatorId(object):

    #main method for identifing separators
    @classmethod
    def discriminant_separators(cls, parsed_xml):
        gap = 10
        prev_par_bottom = -1
        i = 0

        for node in parsed_xml.xpath('//*[local-name() = \'block\']'):
            if node.attrib['blockType'] != 'Text':
                node = cls.__change_blocktype(node)
                prev_par_bottom = -1
            else:
                paragraphs = node.xpath('.//*[local-name() = \'par\']')
                for parag in paragraphs:

                    if prev_par_bottom == -1:
                        prev_par_bottom = int(parag.attrib['b'])
                    current_par_top = int(parag.attrib['t'])

                    if parag.attrib['type'] != 'Heading':

                        if current_par_top - prev_par_bottom > gap:

                            node.getparent().append(cls.__create_new_horizontal_line(parag, prev_par_bottom + 1,current_par_top - 1))
                            prev_par_bottom = int(parag.attrib['b'])

                        else:
                            prev_par_bottom = int(parag.attrib['b'])
                    else:
                        prev_par_bottom = -1


        return parsed_xml

    #rename type attribute to Separator
    @classmethod
    def __change_blocktype(cls, node):
        node.attrib['type'] = 'Separator'

        return node

    #create new block for horizontal line
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
