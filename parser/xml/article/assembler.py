class Assembler(object):
    previous_page = None
    current_page = None
    parsed_xml = None

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

    @classmethod
    def __chainable_equal_heading(cls, current_group):
        """2A, equal width of current_group and neerest heading above

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
    @classmethod
    def __find_nearest_above(cls, group):
        """find neerest group element located above current group element

        :param group:lxml.etree._Element
        :return: lxml.etree._Element or Non
        """

    @classmethod
    def __find_last_from_previous_page(cls):
        """find last group element from previous page

        :param
        :return: group:lxml.etree._Element or None
        """
