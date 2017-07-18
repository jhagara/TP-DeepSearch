from parser.xml.article.chainable import Chainable


class ChainableMiddleAlone(Chainable):
    def is_valid(self, current_group):
        """2Dii, group is ALONE and its location is in middle column

        :param current_group:lxml.etree._Element
        :return: found possible chainable group element or None
        """

        if current_group.attrib['column_position'] != 'middle':
            return None

        left = self._Chainable__find_nearest_left(current_group)
        if left is not None and left.attrib['type'] == 'separators':
            return None
        return left