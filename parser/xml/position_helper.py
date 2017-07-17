import array
import re


ERROR = 3


class PositionHelper:
    # separatorsid, article/merger
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

    # separatorsid, article/merger
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

    # heading, elastic_filler
    # get font size from element formatting
    @classmethod
    def get_fs(cls, formatting):
        fs_string = formatting.get("fs")
        fs = int(re.match("\d+", fs_string).group(0))
        return fs

    # article/merger, cleaner
    # method to calculate and set coordinates to established groups
    @classmethod
    def add_coordinates_from_child(cls, node):
        node_t = -1
        node_b = -1
        node_r = -1
        node_l = -1
        for child in node.getchildren():
            if int(child.attrib['t']) < node_t or node_t == -1:
                node_t = int(child.attrib['t'])
            if int(child.attrib['b']) > node_b:
                node_b = int(child.attrib['b'])
            if int(child.attrib['r']) > node_r:
                node_r = int(child.attrib['r'])
            if int(child.attrib['l']) < node_l or node_l == -1:
                node_l = int(child.attrib['l'])

        node.attrib['l'] = str(node_l)
        node.attrib['t'] = str(node_t)
        node.attrib['r'] = str(node_r)
        node.attrib['b'] = str(node_b)