import operator
from lxml import etree


class Assembler(object):
    def __init__(self, parsed_xml, **args):
        default = {'previous_page': None,
                   'current_page': None,
                   'ERROR': 3,
                   'current_page_num': None,
                   'chains': {},
                   'chains_mapper': {},
                   'last_chain_num': 0}
        args = {**default, **args}

        self.previous_page = args['previous_page']
        self.current_page = args['current_page']
        self.current_page_num = args['current_page_num']
        self.parsed_xml = parsed_xml
        self.ERROR = args['ERROR']
        self.chains = args['chains']
        self.chains_mapper = args['chains_mapper']
        self.last_chain_num = args['last_chain_num']
        self.articles = []
        # if self.parsed_xml is not None:
        #     self.tree = etree.ElementTree(self.parsed_xml)

    def assembly_articles(self):
        i = 0
        # first cycle of all groups in pages
        for page in self.parsed_xml.xpath("/document/page"):
            self.current_page = page
            i += 1
            self.current_page_num = i
            self.chains[i] = {}

            for group in page.xpath("group"):
                group.attrib['page'] = str(i)
                group.attrib['column_position'] = \
                    self.__find_column_position(group)

                chained = self.__chainable_equal_heading(group)
                if chained is None:
                    chained = self.__chainable_equal_ratio_heading(group)
                    if chained is None:
                        chained = self.__chainable_major_ratio_heading(group)

                if chained is not None:
                    self.__chain_groups(group, chained)

            self.previous_page = page

        self.previous_page = None
        self.current_page_num = None

        i = 0
        # second cycle of all ALONE in the dark groups
        for page in self.parsed_xml.xpath("/document/page"):
            self.current_page = page
            i += 1
            self.current_page_num = i

            for group in page.xpath("group[not(@chained)]"):

                if group.attrib['column_position'] == 'left':
                    chained = self.__chainable_left_alone(group)
                elif group.attrib['column_position'] == 'middle':
                    chained = self.__chainable_middle_alone(group)
                elif group.attrib['column_position'] == 'right':
                    chained = self.__chainable_right_alone(group)

                if chained is not None:
                    self.__chain_groups(group, chained)

            self.previous_page = page

        self.__order_groups_and_create_array()

    # PRIVATE

    def __chainable_equal_heading(self, current_group):
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

    def __chainable_equal_ratio_heading(self, current_group):
        """2B, equal ratio of groups below heading, this heading is above current_group

        :param current_group:lxml.etree._Element
        :return: found heading as group element or None
        """

        header = self.__find_nearest_above(current_group)
        if header is None:
            return None
        elif header.attrib['type'] != 'headings':
            return None
        else:
            result = self.__find_all_nearest_below(header)
            if result is None:
                return None
            elif len(result) > 1:
                if self.__all_groups_width_same(result, header):
                    return header
                else:
                    return None

    def __chainable_major_ratio_heading(self, current_group):
        """2C, current_group represents major width of above heading

        :param current_group:lxml.etree._Element
        :return: found heading as group element or None
        """

        header = self.__find_nearest_above(current_group)
        if header is None:
            return None
        elif header.attrib['type'] != 'headings':
            return None
        else:
            result = self.__find_all_nearest_below(header)
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

    def __chainable_left_alone(self, current_group):
        """2Di, group is ALONE and its location is in left column

        :param current_group:lxml.etree._Element
        :return: found possible chainable group element or None
        """

        nearest_above = self.__find_nearest_above(current_group)
        if (nearest_above is None
                or nearest_above.attrib['type'] == 'separators'):
            parent_group = self.__find_last_from_previous_page()
            return parent_group
        else:
            return None

    def __chainable_middle_alone(self, current_group):
        """2Dii, group is ALONE and its location is in middle column

        :param current_group:lxml.etree._Element
        :return: found possible chainable group element or None
        """

        left = self.__find_nearest_left(current_group)
        if left is not None and left.attrib['type'] == 'separators':
            return None
        return left

    def __chainable_right_alone(self, current_group):
        """2Diii, group is ALONE and its location is in right column

        :param current_group:lxml.etree._Element
        :return: found possible chainable group element or None
        """
        o = self.__find_middle_alone()
        last_mid = self.__find_last_middle()

        # end if there was not any middle group
        if last_mid is None:
            return None

        while (last_mid.attrib['type'] == 'separators'):
            last_mid = self.__find_nearest_above(last_mid)
            # bugfix last_mid is None,
            # that means there is no upper headings or fulltexts
            if last_mid is None:
                return None

        result = self.__find_nearest_above(last_mid)

        while (result is not None and result.attrib['type'] == 'separators'):
            result = self.__find_nearest_above(result)

        if o is not None and result is not None:
            return result
        else:
            return last_mid

    # PRIVATE HELPER METHODS

    # chain together two groups, creat associations between them
    def __chain_groups(self, group1, group2):
        # chain groups
        id1 = self.parsed_xml.getpath(group1)
        id2 = self.parsed_xml.getpath(group2)
        chain_num_same1 = self.chains_mapper.get(id1)
        chain_num_same2 = self.chains_mapper.get(id2)

        # chain group already exist
        if (chain_num_same1 is not None) or (chain_num_same2 is not None):
            if chain_num_same1 is not None:
                chain_num = chain_num_same1
                self.chains[chain_num[0]][chain_num[1]].append(group2)
                self.chains_mapper[id2] = chain_num
            else:
                chain_num = chain_num_same2
                self.chains[chain_num[0]][chain_num[1]].append(group1)
                self.chains_mapper[id1] = chain_num
        # chain group not exist
        else:
            self.last_chain_num += 1
            # add groups to newly created group
            self.chains[self.current_page_num][self.last_chain_num] = [group1, group2] # NOQA
            # add knowledge of appending groups to chains mapper
            self.chains_mapper[id1] = [self.current_page_num, self.last_chain_num]
            self.chains_mapper[id2] = [self.current_page_num, self.last_chain_num]

        # mark groups as already chained, as not ALONE, attrib chained=true
        group1.attrib['chained'] = 'true'
        group2.attrib['chained'] = 'true'

    # get column position
    def __find_column_position(self, group):
        exist_left = self.__exist_any_on_the_left(group)
        exist_right = self.__exist_any_on_the_right(group)

        if exist_left and exist_right:
            return 'middle'
        elif not exist_left and exist_right:
            return 'left'
        elif exist_left and not exist_right:
            return 'right'
        else:
            return 'left'

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

    # Jakub
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

    def __exist_any_on_the_left(self, group):
        """find all groups on the left from current group

        :param group:lxml.etree._Element
        :return: group:lxml.etree._Element or None
        """

        l = int(group.attrib['l']) + self.ERROR
        results = self.current_page.xpath(
                "group[@type != 'separators' and @r <= " + str(l) + "][1]")
        if len(results) != 0:
            return True
        else:
            return False

    def __exist_any_on_the_right(self, group):
        """find all groups on the left from current group

        :param group:lxml.etree._Element
        :return: group:lxml.etree._Element or None
        """

        r = int(group.attrib['r']) - self.ERROR
        results = self.current_page.xpath(
                "group[@type != 'separators' and @l >= " + str(r) + "][1]")
        if len(results) != 0:
            return True
        else:
            return False

    # Jozef
    def __find_last_middle(self):
        """find last group element located in middle column

        :param
        :return: group:lxml.etree._Element or None
        """

        groups = self.current_page.xpath("group[@column_position = 'middle']")
        most_right = self.__get_min_or_max(groups, -1, 'r', operator.gt)

        if most_right is not None:
            r = int(most_right.attrib['r'])
            query = "group[@column_position = 'middle' and @r >= " + str(r - self.ERROR) + " and @r <= " + str(r + self.ERROR) + "]" # NOQA
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

    # Martina
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

    def __is_equal_2a(self, text, head):
        r1 = int(text.attrib['r']) + self.ERROR
        l1 = int(text.attrib['l']) - self.ERROR
        r = int(head.attrib['r'])
        l = int(head.attrib['l'])
        if l >= l1 and r <= r1:
            return head
        else:
            return None

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

    def __order_groups_and_create_array(self):
        for page_num, articles in self.chains.items():
            self.articles.append([])
            for num, groups in articles.items():
                left_pos = self.__limit_pos_array(
                    self.ERROR,
                    list(map(lambda x: int(x.attrib['l']), groups)))
                top_pos = self.__limit_pos_array(
                    self.ERROR,
                    list(map(lambda x: int(x.attrib['t']), groups)))

                # initialize helper dictionary for next sorting
                sort_helper = []

                # assing helper variables to groups depending on
                # array position index
                for group in groups:
                    l = int(group.attrib['l'])
                    t = int(group.attrib['t'])
                    sortable = {'page': int(group.attrib['page']),
                                'group': group}

                    for index, poss in enumerate(left_pos):
                        if poss[0] <= l and poss[1] >= l:
                            sortable['l-index'] = index
                            break
                    for index, poss in enumerate(top_pos):
                        if poss[0] <= t and poss[1] >= t:
                            sortable['t-index'] = index
                            break

                    sort_helper.append(sortable)

                # sort groups by page and by left end top index,
                # represent virtual columns and
                # add then as new array into articles array by pages
                sorted_groups = sorted(
                    sort_helper,
                    key=operator.itemgetter('page', 'l-index', 't-index'))
                self.articles[page_num - 1].append(
                    list(map(lambda x: x['group'], sorted_groups)))

    @classmethod
    def __limit_pos_array(cls, error, array):
        poss_arr = []
        sorted_arr = sorted(array)
        previous = 0

        for index, pos in enumerate(sorted_arr):
            if len(poss_arr) == 0:
                poss_arr.append([pos, pos])
            elif index + 1 == len(sorted_arr)\
                    and previous + error >= pos:
                poss_arr[-1][1] = pos
            elif previous + error < pos:
                poss_arr[-1][1] = previous
                poss_arr.append([pos, pos])
            previous = pos

        return poss_arr
