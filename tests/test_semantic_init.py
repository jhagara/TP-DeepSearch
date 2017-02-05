import unittest
import os
from semantic import Semantic


class TestSemanticInit(unittest.TestCase):
    def test_basic_init_test(self):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        header_conf_path = abs_path + "/page_header_conf_1941_1.json"
        xml_path = abs_path + "/slovak_1941_1_strana_1.xml"
        semantic = Semantic(xml=xml_path, header_config=header_conf_path)
        i = 7

