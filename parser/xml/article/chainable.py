import operator
from lxml import etree


class Chainable(object):
    def __init__(self, assembler, column_position=None):
        self.previous_page = assembler.previous_page
        self.current_page = assembler.current_page
        self.ERROR = assembler.ERROR
        self.next_chainable = None
        self.column_position = column_position

    def set_next_chainable(self, next_chainable):
        self.next_chainable = next_chainable

    def find_chain(self, column_position, current_group):
        group = None

        if self.column_position is None or self.column_position == column_position:
            group = self.is_valid(current_group)
        if group is None and self.next_chainable is not None:
            group = self.next_chainable.find_chain(self, current_group)
        return group

    def is_valid(self, current_group):
        return True

    # get min or max from collection of groups
    # just change input parameter to get certain coordinate and min or max
    def __get_min_or_max(self, groups, compare_val, coordinate, compare):
        if len(groups) == 0:
            return None

        for group in groups:
            val = int(group.attrib[coordinate])
            if compare(val, compare_val):
                compare_val = val
                target_elem = group

        return target_elem

    def __find_nearest_left(self, group):
        """find nearest left group
        :param group:lxml.etree._Element
        :return: group:lxml.etree._Element or None
        """

        t = int(group.attrib['t'])
        if t >= self.ERROR:
            t -= self.ERROR
        b = int(group.attrib['b']) + self.ERROR
        l = int(group.attrib['l']) + self.ERROR

        # De Morgan's law - check intersection - (StartA >= EndB)  and  (EndA <= StartB) # NOQA
        # StartA = @b, EndA = @t
        # StartB = b, EndB = t
        query = "group[@type != 'separators' and @b >= " + str(t) + \
                " and @t <= " + str(b) + " and @r <= " + str(l) + "]"
        results = self.current_page.xpath(query)

        return self.__get_min_or_max(results, -1, 'r', operator.gt)

    def __find_nearest_right(self, group):
        """find nearest right group

        :param group:lxml.etree._Element
        :return: group:lxml.etree._Element or None
        """

        t = int(group.attrib['t'])
        if t >= self.ERROR:
            t -= self.ERROR
        b = int(group.attrib['b']) + self.ERROR
        r = int(group.attrib['r']) - self.ERROR

        # De Morgan's law - check intersection - (StartA >= EndB)  and  (EndA <= StartB) # NOQA
        # StartA = @b, EndA = @t
        # StartB = b, EndB = t
        query = "group[@type != 'separators' and @b >= " + str(t) + \
                " and @t <= " + str(b) + " and @l >= " + str(r) + "]"
        results = self.current_page.xpath(query)

        return self.__get_min_or_max(results, 100000, 'l', operator.lt)

    def __find_last_middle(self):
        """find last group element located in middle column

        :param
        :return: group:lxml.etree._Element or None
        """

        groups = self.current_page.xpath("group[@column_position = 'middle']")
        most_right = self.__get_min_or_max(groups, -1, 'r', operator.gt)

        if most_right is not None:
            r = int(most_right.attrib['r'])
            query = "group[@column_position = 'middle' and @r >= " + str(r - self.ERROR) + " and @r <= " + str(
                r + self.ERROR) + "]"  # NOQA
            groups = self.current_page.xpath(query)
            most_bottom = self.__get_min_or_max(groups, -1, 'b', operator.gt)
            return most_bottom
        else:
            return None

    def __find_middle_alone(self):
        """find any ALONE group element located in middle column

        :param
        :return: group:lxml.etree._Element or None
        """

        groups = self.current_page.xpath(
            "group[@column_position = 'middle' and not(@chained)][1]")
        if len(groups) != 0:
            return groups[0]
        else:
            return None

    def __find_nearest_above(self, group):
        """find nearest group element located above current group element
        :param group:lxml.etree._Element
        :return: lxml.etree._Element or Non
        """

        l = int(group.attrib['l'])
        r = int(group.attrib['r'])
        t = int(group.attrib['t'])

        query = "group[@l <= " + str(r) + " and " \
                                          "@r >= " + str(l) + " and @b <= " + str(t) + "]"
        results = self.current_page.xpath(query)
        return self.__get_min_or_max(results, -1, 'b', operator.gt)

    def __find_last_from_previous_page(self):
        """find last group element from previous page

        :param
        :return: group:lxml.etree._Element or None
        """

        if self.previous_page is None:
            return None
        max = 0
        groups = self.previous_page.xpath("group[@column_position = 'right']")

        result = None
        if len(groups) != 0:
            for group in groups:
                b = int(group.attrib['b'])
                if group.attrib['type'] != 'separators' and max < b:
                    max = b
                    result = group
        return result

    def __find_all_nearest_below(self, group):
        """find all nearest group element located below current group element
        :param group:lxml.etree._Element
        :return: array of lxml.etree._Element or None
        """
        l = int(group.attrib['l'])
        r = int(group.attrib['r'])
        b = int(group.attrib['b'])

        query = "group[@l <= " + str(r) + " and " \
                "@r >= " + str(l) + " and @t >= " + str(b) + "]"

        results = self.current_page.xpath(query)
        max_elem = self.__get_min_or_max(
                results,
                int(self.current_page.attrib['height']),
                't',
                operator.lt)
        if max_elem is None:
            return None
        else:
            t_min = int(max_elem.attrib['t'])
            t_max = t_min + self.ERROR
            relative = []
            for result in results:
                t = int(result.attrib['t'])
                if t_min <= t <= t_max:
                    relative.append(result)

            return relative