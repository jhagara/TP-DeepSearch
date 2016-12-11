import unittest
from lxml import etree
from parser.xml.article.assembler import Assembler
import re


class Testassemblerall(unittest.TestCase):
    def test_assembler_all_success(self):
        assembler = Assembler()
        Assembler.assembly_articles(etree.parse("input_test_assembler.xml"))
        chains = assembler.chains
        for i, page in enumerate(chains):
            print("page" + i)
            for j, chain in enumerate(page):
                print("chain" + j)
                for group in chain:
                    print(group.xpath('.//formatting').text)

