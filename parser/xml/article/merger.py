from lxml import etree
import copy

# purpose of this class is to merge blocks of equal type
# to groups of that type and set coordinates to the group

ERROR = 3


class Preprocessor(object):

    # main method for preprocessing elements for assembling

    @classmethod
    def preprocess(cls, parsed_xml):

        # search document for pages
        for page in parsed_xml.xpath("/document/page"):
            # search every page for blocks
            for node in page.xpath("block"):
                # if block type is separator
                if node.attrib.get('type') == "separator":
                    l = int(node.attrib['l'])
                    if l >= ERROR:
                        l -= ERROR
                    r = int(node.attrib['r']) + ERROR
                    t = int(node.attrib['t'])

                    # De Morgan's law - check intersection
                    # (StartA <= EndB)  and  (EndA >= StartB)
                    # find all matching blocks
                    query = "block[@l <= " + str(r) + \
                            " and @r >= " + str(l) + \
                            " and @b <= " + str(t) + "]"
                    results = page.xpath(query)
                    cls.__manage_group(page, node, results)
                else:
                    for par in node.xpath("par"):
                        l = int(par.attrib['l'])
                        if l >= ERROR:
                            l -= ERROR
                        r = int(par.attrib['r']) + ERROR
                        t = int(par.attrib['t'])

                        # De Morgan's law - check intersection
                        # (StartA <= EndB)  and  (EndA >= StartB)
                        # find all matching blocks and paragraphs
                        query = "block[@type ='separator' and @l <= " +\
                                str(r) + " and @r >= " +\
                                str(l) + " and @b <= " +\
                                str(t) + "] | block/par[@l <= " +\
                                str(r) + " and @r >= " +\
                                str(l) + " and @b <= " +\
                                str(t) + "]"
                        results = page.xpath(query)
                        cls.__manage_group(page, par, results)
        # delete all unused block
        for block in parsed_xml.xpath("/document/page/block"):
            block.getparent().remove(block)
        for group in parsed_xml.xpath("/document/page/group"):
            # delete all unused groups
            if not group.getchildren():
                group.getparent().remove(group)
            # set coordinates for groups
            else:
                cls.__add_coordinates(group)

        return parsed_xml

    # PRIVATE METHODS

    # method to manage grouping
    # based on number of results and type of result
    # and whether the node is already in group
    @classmethod
    def __manage_group(cls, page, node, results):
        # if results exist
        if len(results) != 0:
            nearest = cls.__get_nearest(results)
            nearest_many = cls.__get_relative_nearest(nearest, results)

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

    # method to calculate and set coordinates to established groups
    @classmethod
    def __add_coordinates(cls, node):
        group_t = -1
        group_b = -1
        group_r = -1
        group_l = -1
        for child in node.getchildren():
            if int(child.attrib['t']) < group_t or group_t == -1:
                group_t = int(child.attrib['t'])
            if int(child.attrib['b']) > group_b:
                group_b = int(child.attrib['b'])
            if int(child.attrib['r']) > group_r:
                group_r = int(child.attrib['r'])
            if int(child.attrib['l']) < group_l or group_l == -1:
                group_l = int(child.attrib['l'])

        node.attrib['t'] = str(group_t)
        node.attrib['b'] = str(group_b)
        node.attrib['r'] = str(group_r)
        node.attrib['l'] = str(group_l)

    # method to  get one nearest element
    @classmethod
    def __get_nearest(cls, results):
        maximum = -1
        max_elem = results[0]
        for result in results:
            val = int(result.attrib['b'])
            if val > maximum:
                maximum = val
                max_elem = result

        return max_elem

    # method to get all nearest elements with usage of ERROR value
    @classmethod
    def __get_relative_nearest(cls, nearest, results):
        b_max = int(nearest.attrib['b'])
        b_min = b_max - ERROR
        relative = []
        for result in results:
            b = int(result.attrib['b'])
            if b_min <= b <= b_max:
                relative.append(result)

        return relative

    # method to calculate axis of element
    @classmethod
    def __axis(cls, node):
        return (int(node.attrib['l'])+int(node.attrib['r']))/2
