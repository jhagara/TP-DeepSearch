import operator


class Assembler(object):
    # previous_page = None
    # current_page = None
    # parsed_xml = None
    # ERROR = 3

    def __init__(self, parsed_xml, **args):
        default = {'previous_page': None, 'current_page': None, 'ERROR': 3,
                   'current_page_num': None, 'chains': {}, 'chains_mapper': {}, 'last_chain_num': 0}
        args = {**default, **args}

        self.previous_page = args['previous_page']
        self.current_page = args['current_page']
        self.current_page_num = args['current_page_num']
        self.parsed_xml = parsed_xml
        self.ERROR = args['ERROR']
        self.chains = args['chains']
        self.chains_mapper = args['chains_mapper']
        self.last_chain_num = args['last_chain_num']

    def assembly_articles(self, parsed_xml):
        self.parsed_xml = parsed_xml

        i = 0
        # first cycle of all groups in pages
        for page in parsed_xml.xpath("/document/page"):
            self.current_page = page
            i += 1
            self.current_page_num = i
            self.chains[i] = {}

            for group in page.xpath("group"):

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
        for page in parsed_xml.xpath("/document/page"):
            self.current_page = page
            i += 1
            self.current_page_num = i

            for group in page.xpath("group[not(@chained)]"):
                group.attrib['column_position'] = \
                    self.__find_column_position(group)

                if group.attrib['column_position'] == 'left':
                    chained = self.__chainable_left_alone(group)
                elif group.attrib['column_position'] == 'middle':
                    chained = self.__chainable_middle_alone(group)
                elif group.attrib['column_position'] == 'right':
                    chained = self.__chainable_right_alone(group)

                if chained is not None:
                    self.__chain_groups(group, chained)

            self.previous_page = page

    # PRIVATE

    @classmethod
    def __chainable_equal_heading(cls, current_group):
        """2A, equal width of current_group and nearest heading above

        :param current_group:lxml.etree._Element
        :return: found heading as group element or None
        """

    @classmethod
    def __chainable_equal_ratio_heading(cls, current_group):
        """2B, equal ratio of groups below heading, this heading is above current_group

        :param current_group:lxml.etree._Element
        :return: found heading as group element or None
        """

    @classmethod
    def __chainable_major_ratio_heading(cls, current_group):
        """2C, current_group represents major width of above heading

        :param current_group:lxml.etree._Element
        :return: found heading as group element or None
        """

    @classmethod
    def __chainable_left_alone(cls, current_group):
        """2Di, group is ALONE and its location is in left column

        :param current_group:lxml.etree._Element
        :return: found possible chainable group element or None
        """

    @classmethod
    def __chainable_middle_alone(cls, current_group):
        """2Dii, group is ALONE and its location is in middle column

        :param current_group:lxml.etree._Element
        :return: found possible chainable group element or None
        """

    @classmethod
    def __chainable_right_alone(cls, current_group):
        """2Diii, group is ALONE and its location is in right column

        :param current_group:lxml.etree._Element
        :return: found possible chainable group element or None
        """

    # PRIVATE HELPER METHODS

    # chain together two groups, creat associations between them
    def __chain_groups(self, group1, group2):
        # chain groups
        id1 = id(group1)
        id2 = id(group2)
        chain_num_same1 = self.chains_mapper.get(id1)
        chain_num_same2 = self.chains_mapper.get(id2)

        # chain group already exist
        if (chain_num_same1 is not None) or (chain_num_same2 is not None):
            if (chain_num_same1 is not None):
                chain_num = chain_num_same1
                self.chains[self.current_page_num][chain_num].append(group2)
                self.chains_mapper[id2] = chain_num
            else:
                chain_num = chain_num_same2
                self.chains[self.current_page_num][chain_num].append(group1)
                self.chains_mapper[id1] = chain_num
        # chain group not exist
        else:
            # plus 1 - we're gonna create new chain group
            self.last_chain_num += 1
            # add groups to newly created group
            self.chains[self.current_page_num][self.last_chain_num] = [group1, group2]
            # add knowledge of appending groups to chains mapper
            self.chains_mapper[id1] = self.last_chain_num
            self.chains_mapper[id2] = self.last_chain_num

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

        # De Morgan's law - check intersection - (StartA >= EndB)  and  (EndA <= StartB)
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

        # De Morgan's law - check intersection - (StartA >= EndB)  and  (EndA <= StartB)
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
        results = self.current_page.xpath("group[@type != 'separators' and @r <= " + str(l) + "][1]")
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
        results = self.current_page.xpath("group[@type != 'separators' and @l >= " + str(r) + "][1]")
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
            query = "group[@column_position = 'middle' and @r >= " \
                    "" + str(r - self.ERROR) + " and @r <= " + str(r + self.ERROR) + "]"
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

        groups = self.current_page.xpath("group[@column_position = 'middle' and not(@chained)][1]")
        if len(groups) != 0:
            return groups[0]
        else:
            return None

    # Martina
    @classmethod
    def __find_nearest_above(cls, group):
        """find nearest group element located above current group element

        :param group:lxml.etree._Element
        :return: lxml.etree._Element or Non
        """

    @classmethod
    def __find_last_from_previous_page(cls):
        """find last group element from previous page

        :param
        :return: group:lxml.etree._Element or None
        """
