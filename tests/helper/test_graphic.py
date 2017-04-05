import unittest
from helper.graphic import Graphic
from lxml import etree
import os
from parser.xml.cleaner import Cleaner
from semantic import Semantic


class TestGraphic(unittest.TestCase):
    # draw elements par with coordinates
    def test_draw_single_page_groups(self):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        xml = etree.parse(abs_path + '/slovak_1941_1_strana_1.xml')
        xml = Cleaner.clean(xml)
        Graphic.draw_elem_network(xml.xpath("/document/page[1]")[0], [{'elem_path': '//par', 'attrib': ['l', 't', 'r', 'b']}])

    # draw elements group with types
    def test_draw_single_page_groups(self):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        header_conf_path = abs_path + "/page_header_conf_1941_1.json"
        xml_path = abs_path + "/slovak_1941_1_strana_1.xml"
        semantic = Semantic(xml=xml_path, header_config=header_conf_path)
        Graphic.draw_elem_network(semantic.xml.xpath("/document/page[1]")[0],
                                  [{'elem_path': '//group', 'attrib': ['type']}])

    # draw articles with groups
    def test_draw_single_page_groups(self):
        # abs_path = os.path.dirname(os.path.abspath(__file__))
        # header_conf_path = abs_path + "/page_header_conf_1941_1.json"
        # xml_path = '/home/vasko/PycharmProjects/TP-DeepSeach/tests/slovak_1939_05_26_full.xml'
        # semantic = Semantic(xml=xml_path, header_config=header_conf_path)
        # Graphic.draw_articles(semantic.articles, '/home/vasko/Documents/skola/TP/turtle_test')
        self.assert_