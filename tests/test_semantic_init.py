import unittest
import os
from semantic import Semantic


class TestSemanticInit(unittest.TestCase):
    def test_basic_init_test(self):
        header_conf_path = os.path.dirname(os.path.abspath(__file__))
        + "/page_header_conf_1941_1.json"
        xml_path = os.path.dirname(os.path.abspath(__file__))
        + "/slovak_1941_1_strana_1.xml"
        semantic = Semantic(xml=xml_path, header_config=header_conf_path)
        i = 7

