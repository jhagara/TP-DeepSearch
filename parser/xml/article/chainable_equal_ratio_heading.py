from parser.xml.article.chainable import Chainable


class ChainableEqualRatioHeading(Chainable):
    def is_valid(self, current_group):
        """2A, equal width of current_group and nearest heading above
        :param current_group:lxml.etree._Element
        :return: found heading as group element or None
        """

        result = self.__find_nearest_above(current_group)
        if result is None:
            return None
        elif result.attrib['type'] != 'headings':
            return None
        else:
            return self.__is_equal_2a(current_group, result)

    def __all_groups_width_same(self, all_groups, header):
        l = int(header.attrib['l'])
        r = int(header.attrib['r'])
        error_width = r - l
        l = int(all_groups[0].attrib['l'])
        r = int(all_groups[0].attrib['r'])
        cmp_width = r - l
        min_width = cmp_width - (error_width * 0.1)
        max_width = cmp_width + (error_width * 0.1)

        for group in all_groups:
            if group.attrib['type'] != "fulltexts":
                return False
            l = int(group.attrib['l'])
            r = int(group.attrib['r'])
            width = r - l
            if width < min_width or width > max_width:
                return False
        return True