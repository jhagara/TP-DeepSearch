from parser.xml.article.chainable import Chainable


class ChainableLeftAlone(Chainable):
    def is_valid(self, current_group):
        """2Di, group is ALONE and its location is in left column

                :param current_group:lxml.etree._Element
                :return: found possible chainable group element or None
                """

        nearest_above = self._Chainable__find_nearest_above(current_group)
        if (nearest_above is None
            or nearest_above.attrib['type'] == 'separators'):
            parent_group = self._Chainable__find_last_from_previous_page()
            return parent_group
        else:
            return None
