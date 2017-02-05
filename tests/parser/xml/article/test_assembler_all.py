import unittest
from lxml import etree
from parser.xml.article.assembler import Assembler
import re
import os


class Testassemblerall(unittest.TestCase):
    def test_assembler_all_success(self):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        path = abs_path + "/input_test_assembler.xml"
        xml = etree.parse(path)
        assembler = Assembler(xml)
        assembler.assembly_articles
        chains = assembler.chains
        for i, page in enumerate(chains):
            print("page" + i)
            for j, chain in enumerate(page):
                print("chain" + j)
                for group in chain:
                    print(group.xpath('.//formatting').text)
