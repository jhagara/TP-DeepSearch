class Assembler(object):
    previous_page = None
    current_page = None
    parsed_xml = None
    ERROR = 3

    def assembly_articles(self, parsed_xml):
        self.parsed_xml = parsed_xml

        # first cycle of all groups in pages
        for page in parsed_xml.xpath("/document/page"):
            self.current_page = page

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

        # second cycle of all ALONE in the dark groups
        for page in parsed_xml.xpath("/document/page"):
            self.current_page = page

            for group in page.xpath("group[@chained]"):
                group.attrib['column_position'] = \
                    self._find_column_position(group)

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

    def __chainable_equal_heading(self, current_group):
        """2A, equal width of current_group and neerest heading above

        :param current_group:lxml.etree._Element
        :return: found heading as group element or None
        """

        result = self.__find_nearest_above(current_group)
        if result is None:
            return None
        elif result.tag != 'heading':
            return None
        else:
            return self.__is_equal_2a(current_group, result)



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
    @classmethod
    def __chain_groups(cls, group1, group2):
        # chain groups

        # mark groups as already chained, as not ALONE, attrib chained=true
        group1.attrib['chained'] = 'true'
        group2.attrib['chained'] = 'true'

    # get column position
    @classmethod
    def _find_column_position(cls, group):
        left = cls.__find_neerest_left(group)
        right = cls.__find_neerest_right(group)

        if (left is not None) and (right is not None):
            return 'middle'
        elif (left is None) and (right is not None):
            return 'left'
        elif (left is not None) and (right is None):
            return 'right'
        else:
            return 'left'

    # Jakub
    @classmethod
    def __find_neerest_left(cls, group):
        """find neerest left group

        :param group:lxml.etree._Element
        :return: group:lxml.etree._Element or None
        """

    @classmethod
    def __find_neerest_right(cls, group):
        """find neerest right group

        :param group:lxml.etree._Element
        :return: group:lxml.etree._Element or None
        """

    # Jozef
    @classmethod
    def __find_last_middle_alone(cls):
        """find last ALONE group element located in middle column

        :param
        :return: group:lxml.etree._Element or None
        """

    # Martina
    def __find_nearest_above(self, group):

        """find neerest group element located above current group element

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

    @classmethod
    def __find_last_from_previous_page(cls):
        """find last group element from previous page

        :param
        :return: group:lxml.etree._Element or None
        """

    def __is_equal_2a(self, text, head):
        r1 = int(text.attrib['r']) + self.ERROR
        l1 = int(text.attrib['l']) - self.ERROR
        r = int(head.attrib['r'])
        l = int(head.attrib['l'])
        if l >= l1 and r <= r1:
            return head
        else:
            return None

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
        max_elem = self.__get_min_or_max(results, results[0].attrib['t'], 't',
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
