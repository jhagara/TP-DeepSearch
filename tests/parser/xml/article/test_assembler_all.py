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
        for node in xml.iter():
            try:
                has_namespace = node.tag.startswith('{')
            except AttributeError:
                return node
            if has_namespace:
                node.tag = node.tag.split('}', 1)[1]
        assembler = Assembler(xml)
        assembler.assembly_articles()
        articles = assembler.articles
        for i, page in enumerate(articles):
            for j, article in enumerate(page):
                art_numbers = []
                for group in article:
                    for par in group:
                        for line in par:
                            for formatting in line:
                                number = re.findall('\d+', formatting.text)
                                art_numbers.append(number[1])
                art_numb = art_numbers[0]
                for n in art_numbers:
                    self.assertEqual(art_numb, n, "article " + str(n) + " not correctly assembled on page " + str(i+1))
