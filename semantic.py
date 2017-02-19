from parser.xml.xml_parser import XmlParser
from lxml import etree


class Semantic(object):
    def __init__(self, **args):
        default = {'pdf': None, 'xml': None, 'header_config': None}
        args = {**default, **args}

        if args['xml'] is not None:
            self.header, self.articles = XmlParser.parse(args['header_config'], args['xml'])

    def print_articles(self):
        for key, value in self.chains.items():
            print('\n\n--PAGE---------------------------------------------------')
            for key, value in value.items():
                print('==ARTICLE==========')
                for group in value:
                    print('::TYPE: ' + group.attrib['type'])
                    for par in group.xpath('par'):
                        for line in par.xpath('line'):
                            for formatting in line.xpath('formatting'):
                                print(formatting.text)

    def print_correct_articles(self):
        for page in self.articles:
            print('\n\n--PAGE------------------------------------------------------------------------------------')
            for article in page:
                print('==ARTICLE==============================================')
                for group in article:
                    print('::TYPE: ' + group.attrib['type'])
                    for par in group.xpath('par'):
                        for line in par.xpath('line'):
                            for formatting in line.xpath('formatting'):
                                print(formatting.text)
