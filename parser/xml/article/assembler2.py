import operator
from lxml import etree
from parser.xml.article.chainable_equal_heading import ChainableEqualHeading
from parser.xml.article.chainable_equal_ratio_heading import ChainableEqualRatioHeading
from parser.xml.article.chainable_left_alone import ChainableLeftAlone
from parser.xml.article.chainable_middle_alone import ChainableMiddleAlone
from parser.xml.article.chainable_right_alone import ChainableRightAlone
from parser.xml.article.chainable_major_ratio_heading import ChainableMajorRatioHeading


class Assembler2(object):
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
            chainable = self.__get_chain_of_first_chainable_rules

            for group in page.xpath("group"):
                group.attrib['page'] = str(i)
                group.attrib['column_position'] = \
                    self.__find_column_position(group)
                chained = chainable.find_chain(group.attrib['column_position'], group)
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
            chainable = self.__get_chain_of_alone_chainable_rules

            for group in page.xpath("group[not(@chained)]"):
                chained = chainable.find_chain(group.attrib['column_position'], group)
                if chained is not None:
                    self.__chain_groups(group, chained)

            self.previous_page = page

        self.__order_groups_and_create_array()

    # initialize first chainable rules to:
    #   equal_heading -> equal_ratio_heading -> major_ratio_heading
    def __get_chain_of_first_chainable_rules(self):
        chainable_equal_heading = ChainableEqualHeading(self)
        chainable_equal_ratio_heading = ChainableEqualRatioHeading(self)
        chainable_major_ratio_heading = ChainableMajorRatioHeading(self)

        chainable_equal_ratio_heading.set_next_chainable(chainable_major_ratio_heading)
        chainable_equal_heading.set_next_chainable(chainable_equal_ratio_heading)

        return chainable_equal_heading

    # initialize alone chainable rules to:
    #   left_alone -> middle_alone -> alone_alone
    def __get_chain_of_alone_chainable_rules(self):
        chainable_left_alone = ChainableLeftAlone(self, 'left')
        chainable_middle_alone = ChainableMiddleAlone(self, 'middle')
        chainable_right_alone = ChainableRightAlone(self, 'right')

        chainable_middle_alone.set_next_chainable(chainable_right_alone)
        chainable_left_alone.set_next_chainable(chainable_middle_alone)

        return chainable_left_alone

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
            self.chains[self.current_page_num][self.last_chain_num] = [group1, group2]  # NOQA
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