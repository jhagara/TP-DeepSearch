from parser.xml.article.chainable import Chainable


class ChainableMajorRatioHeading(Chainable):
    def is_valid(self, current_group):
        """2C, current_group represents major width of above heading

        :param current_group:lxml.etree._Element
        :return: found heading as group element or None
        """

        header = self._Chainable__find_nearest_above(current_group)
        if header is None:
            return None
        elif header.attrib['type'] != 'headings':
            return None
        else:
            result = self._Chainable__find_all_nearest_below(header)
            if result is None:
                return None
            elif len(result) == 1:
                if result[0].attrib['type'] == 'fulltexts':
                    return header
                else:
                    None
            elif len(result) > 1:
                if self.__all_groups_width_main_larger(current_group, result):
                    return header
                elif self.__all_groups_fulltext_alone(current_group, result):
                    return header
                else:
                    return None

    def __all_groups_width_main_larger(self, current, all_groups):
        curr_l = int(current.attrib['l'])
        curr_r = int(current.attrib['r'])
        cmp_width = curr_r - curr_l

        for group in all_groups:
            if group.attrib['type'] != "fulltexts":
                return False
            l = int(group.attrib['l'])
            r = int(group.attrib['r'])
            if curr_r == r and curr_l == l:
                continue
            width = r - l
            if width > cmp_width:
                return False
        return True

    def __all_groups_fulltext_alone(self, current, all_groups):
        if current.attrib['type'] != "fulltexts":
            return False
        curr_l = int(current.attrib['l'])
        curr_r = int(current.attrib['r'])

        for group in all_groups:
            l = int(group.attrib['l'])
            r = int(group.attrib['r'])
            if curr_r == r and curr_l == l:
                continue
            if group.attrib['type'] == "fulltexts":
                return False
        return True