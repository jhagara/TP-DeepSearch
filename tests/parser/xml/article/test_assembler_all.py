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
        output = ""
        for i, page in enumerate(articles):
            # print("page " + str(i))
            output += "page " + str(i) + "\n"
            for j, article in enumerate(page):
                # print("article " + str(j))
                output += "article " + str(j) + "\n"
                for group in article:
                    for par in group:
                        for line in par:
                            for formatting in line:
                                # print(formatting.text)
                                output += formatting.text + "\n"
        desired_output = """page 0
article 0
strana 1 clanok 1 nadpis
strana 1 clanok 1
page 1
article 0
strana 2 clanok 1 nadpis
strana 2 clanok 1
page 2
article 0
strana 3 clanok 1 nadpis
strana 3 clanok 1
strana 3 clanok 1
strana 3 clanok 1
page 3
article 0
strana 4 clanok 1 nadpis
strana 4 clanok 1
article 1
strana 4 clanok 2 nadpis
strana 4 clanok 2
page 4
article 0
strana 5 clanok 3 nadpis
strana 5 clanok 3
article 1
strana 5 clanok 1 nadpis
strana 5 clanok 1
strana 5 clanok 1
article 2
strana 5 clanok 2 nadpis
strana 5 clanok 2
page 5
article 0
strana 6 clanok 1 nadpis
strana 6 clanok 1
page 6
article 0
strana 7 clanok 1
strana 7 clanok 1 nadpis
page 7
article 0
strana 8 clanok 1 nadpis
strana 8 clanok 1
page 8
article 0
strana 9 clanok 4 nadpis
strana 9 clanok 4
strana 9 clanok 4
article 1
strana 9 clanok 1 nadpis
strana 9 clanok 1
article 2
strana 9 clanok 5 nadpis
strana 9 clanok 5
article 3
strana 9 clanok 2 nadpis
strana 9 clanok 2
strana 9 clanok 2
article 4
strana 9 clanok 3 nadpis
strana 9 clanok 3
strana 9 clanok 3
page 9
article 0
strana 10 clanok 1 nadpis
strana 10 clanok 1
page 10
article 0
strana 11 clanok 1 nadpis
strana 11 clanok 1
article 1
strana 11 clanok 1 zo strany 10
strana 11 clanok 1 zo strany 10
strana 11 clanok 1 zo strany 10
page 11
article 0
strana 12 clanok 1 nadpis
strana 12 clanok 1
article 1
strana 12 clanok 2 nadpis
strana 12 clanok 2
article 2
strana 12 clanok 3 nadpis
strana 12 clanok 3
page 12
article 0
strana 13 clanok 3 nadpis
strana 13 clanok 3
article 1
strana 13 clanok 1 nadpis
strana 13 clanok 1
strana 13 clanok 1
article 2
strana 13 clanok 2 nadpis
strana 13 clanok 2
page 13
article 0
strana 14 clanok 1 nadpis
strana 14 clanok 1
strana 14 clanok 1
article 1
strana 14 clanok 2 nadpis
strana 14 clanok 2
strana 14 clanok 2
article 2
strana 14 clanok 3 nadpis
strana 14 clanok 3
strana 14 clanok 3
strana 14 clanok 3
strana 14 clanok 3
"""
        self.assertEqual(desired_output,output)
