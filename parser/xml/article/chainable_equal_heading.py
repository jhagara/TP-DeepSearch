from parser.xml.article.chainable import Chainable


class ChainableEqualHeading(Chainable):
    def is_valid(self, current_group):
        """2A, equal width of current_group and nearest heading above
        :param current_group:lxml.etree._Element
        :return: found heading as group element or None
        """

        result = self._Chainable__find_nearest_above(current_group)
        if result is None:
            return None
        elif result.attrib['type'] != 'headings':
            return None
        else:
            return self.__is_equal_2a(current_group, result)

    def __is_equal_2a(self, text, head):
        r1 = int(text.attrib['r']) + self.ERROR
        l1 = int(text.attrib['l']) - self.ERROR
        r = int(head.attrib['r'])
        l = int(head.attrib['l'])
        if l >= l1 and r <= r1:
            return head
        else:
            return None