from lxml import etree

# purpose of this class is to identify separators (pictures, adds, horizontal
# lines etc.) and rename blockTypes to "separator"
class SeparatorId(object):

    #main method for identifing separators
    @classmethod
    def discriminant_separators(cls, parsed_xml):

        prev_block_bottom = -1

        for node in parsed_xml.iter():

            if node.tag == 'block':
                if prev_block_bottom == -1:
                    prev_block_bottom = int(node.attrib['t'])
                if node.attrib['blockType'] != 'Text':
                    node = cls.__change_blocktype(node)
                    prev_block_bottom = -1
                else:
                    current_block_top = int(node.attrib['t'])
                    if hasattr(node,'type') and node.attrib['type'] != 'Separator':
                        if current_block_top - prev_block_bottom > 10:
                            new_hr = etree.Element('block')
                            new_hr.text = ""
                            new_hr.attrib['blockType'] = 'Text'
                            new_hr.attrib['l'] = node.attrib['l']
                            new_hr.attrib['t'] = str(prev_block_bottom + 1)
                            new_hr.attrib['r'] = node.attrib['r']
                            new_hr.attrib['b'] = str(current_block_top - 1)
                            new_hr.attrib['type'] = 'Separator'

                            node.getparent().append(new_hr)

                    elif hasattr(node,'type') == False:
                        if current_block_top - prev_block_bottom > 10:
                            print(current_block_top)
                            print(prev_block_bottom)

                            new_hr = etree.Element('block')
                            new_hr.text = ""
                            new_hr.attrib['blockType'] = 'Text'
                            new_hr.attrib['l'] = node.attrib['l']
                            new_hr.attrib['t'] = str(prev_block_bottom + 1)
                            new_hr.attrib['r'] = node.attrib['r']
                            new_hr.attrib['b'] = str(current_block_top - 1)
                            new_hr.attrib['type'] = 'Separator'

                            node.getparent().append(new_hr)

                        prev_block_bottom = int(node.attrib['b'])
                    else:
                         prev_block_bottom = -1


        return parsed_xml

    #rename BlockType attribute to separator
    @classmethod
    def __change_blocktype(cls, node):

        node.attrib['type'] = 'Separator'

        return node

