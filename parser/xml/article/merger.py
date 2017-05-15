from lxml import etree
import copy
from parser.xml.position_helper import PositionHelper

ERROR = 3

# purpose of this class is to merge blocks of equal type
# to groups of that type and set coordinates to the group


class Preprocessor(object):
    # main method for preprocessing elements for assembling
    # joins vertical affined elements and removes unused
    @classmethod
    def preprocess(cls, parsed_xml):
        for page in parsed_xml.xpath("/document/page"):
            for node in page.xpath("block"):
                if node.attrib.get('type') == "separator":
                    results = cls.__search_blocks_below_separator(page, node)
                    cls.__manage_group(page, node, results)
                else:
                    for par in node.xpath("par"):
                        results = cls.__search_blocks_and_pars_below_non_separator(page, par)
                        cls.__manage_group(page, par, results)

        cls.__detele_unused_blocks_and_groups(parsed_xml)

        return parsed_xml

    # search blocks in area below separator
    # using De Morgan's law
    @classmethod
    def __search_blocks_below_separator(cls, page, node):
        l = int(node.attrib['l'])
        if l >= ERROR:
            l -= ERROR
        r = int(node.attrib['r']) + ERROR
        t = int(node.attrib['t'])

        query = "block[@l <= " + str(r) + \
                " and @r >= " + str(l) + \
                " and @b <= " + str(t) + "]"

        return page.xpath(query)

    # search blocks and paragraphs in area below fulltexts
    # and headings using De Morgan's law
    @classmethod
    def __search_blocks_and_pars_below_non_separator(cls, page, par):
        l = int(par.attrib['l'])
        if l >= ERROR:
            l -= ERROR
        r = int(par.attrib['r']) + ERROR
        t = int(par.attrib['t'])

        query = "block[@type ='separator' and @l <= " + \
                str(r) + " and @r >= " + \
                str(l) + " and @b <= " + \
                str(t) + "] | block/par[@l <= " + \
                str(r) + " and @r >= " + \
                str(l) + " and @b <= " + \
                str(t) + "]"

        return page.xpath(query)

    # delete all unused blocks and groups
    # set coordinates for used groups
    @classmethod
    def __detele_unused_blocks_and_groups(cls, parsed_xml):
        for block in parsed_xml.xpath("/document/page/block"):
            block.getparent().remove(block)
        for group in parsed_xml.xpath("/document/page/group"):
            if not group.getchildren():
                group.getparent().remove(group)
            else:
                PositionHelper.add_coordinates_from_child(group)

    # method to manage grouping
    # based on number of results and type of result
    # and whether the node is already in group
    @classmethod
    def __manage_group(cls, page, node, results):
        # if results exist
        if len(results) != 0:
            nearest = PositionHelper.get_nearest(results)
            nearest_many = PositionHelper.get_relative_nearest(nearest, results)

            # if type matches
            if cls.__get_type(node, nearest_many):
                result = cls.__in_group(page, node)
                if not result:
                    page.append(cls.__set_group(page, node, nearest_many))
                else:
                    cls.__join_group(page, result[0], nearest_many)
            else:
                # if node is not assigned to group
                if not cls.__in_group(page, node):
                    page.append(cls.__create_group(node))
        else:
            # if node is not assigned to group
            if not cls.__in_group(page, node):
                page.append(cls.__create_group(node))

    # method for determining type of group of elements
    @classmethod
    def __get_type(cls, node, nearest):

        t = node.attrib.get('type')
        for n in nearest:
            if t != n.attrib['type']:
                return False
        return True

    # method for joining elements from existing groups to one
    @classmethod
    def __join_group(cls, page, node, nearest):

        has_group = 0
        for n in nearest:
            if cls.__in_group(page, n):
                has_group = 1
                break
        if has_group:
            for n in nearest:
                result = cls.__in_group(page, n)
                if result:
                    for child in result[0].getparent().getchildren():
                        node.getparent().append(child)
                else:
                    node.getparent().append(copy.deepcopy(n))
        else:
            for n in nearest:
                node.getparent().append(copy.deepcopy(n))

    # method for joining elements in new group
    @classmethod
    def __set_group(cls, page, node, nearest):

        has_group = 0
        for n in nearest:
            if cls.__in_group(page, n):
                has_group = 1
                break
        new_group = cls.__create_group(node)
        if has_group:
            for n in nearest:
                result = cls.__in_group(page, n)
                if result:
                    for child in result[0].getparent().getchildren():
                        new_group.append(child)
                else:
                    new_group.append(copy.deepcopy(n))
        else:
            for n in nearest:
                new_group.append(copy.deepcopy(n))

        return new_group

    # method for creating new group
    # with initializing node
    @classmethod
    def __create_group(cls, node):

        new_group = etree.Element('group')
        new_group.attrib['type'] = node.attrib['type'] + 's'
        new_group.append(copy.deepcopy(node))

        return new_group

    # method for determining whether node is part of existing group
    @classmethod
    def __in_group(cls, page, node):
        type = node.attrib.get('type') if node.attrib.get('type') is not None else '' # NOQA

        query = "group/" + node.tag + "[@type = '" + type +\
                "' and @r = " + node.attrib['r'] + " and @b = " + \
                node.attrib['b'] + " and @l = " + node.attrib['l'] +\
                " and @t = " + node.attrib['t'] + "]"
        result = page.xpath(query)

        return result

    # method to calculate axis of element
    @classmethod
    def __axis(cls, node):
        return (int(node.attrib['l'])+int(node.attrib['r']))/2
