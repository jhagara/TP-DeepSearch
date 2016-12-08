import unittest
from lxml import etree
from parser.xml.article.assembler import Assembler
import re


class Testassemblerall(unittest.TestCase):
    def test_assembler_all_success(self):

        desired_output = """"""

        chained_groups = \
            Assembler.assembly_articles(etree.parse("input_test_assembler.xml"))
        actual_output = ""
        for group in chained_groups:
            for g in group:
                actual_output = actual_output + etree.tostring(g).decode('utf-8')

        self.assertEqual(re.sub('[^\040-\176]| ', '',desired_output),
                         re.sub('[^\040-\176]| ', '',actual_output))


