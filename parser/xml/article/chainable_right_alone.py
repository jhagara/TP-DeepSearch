from parser.xml.article.chainable import Chainable


class ChainableRightAlone(Chainable):
    def is_valid(self, current_group):
        """2Diii, group is ALONE and its location is in right column

        :param current_group:lxml.etree._Element
        :return: found possible chainable group element or None
        """

        o = self._Chainable__find_middle_alone()
        last_mid = self._Chainable__find_last_middle()

        # end if there was not any middle group
        if last_mid is None:
            return None

        while (last_mid.attrib['type'] == 'separators'):
            last_mid = self._Chainable__find_nearest_above(last_mid)
            # bugfix last_mid is None,
            # that means there is no upper headings or fulltexts
            if last_mid is None:
                return None

        result = self._Chainable__find_nearest_above(last_mid)

        while (result is not None and result.attrib['type'] == 'separators'):
            result = self._Chainable__find_nearest_above(result)

        if o is not None and result is not None:
            return result
        else:
            return last_mid