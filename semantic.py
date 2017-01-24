from parser.xml.xml_parser import XmlParser


class Semantic(object):
    def __init__(self, **args):
        default = {'pdf': None, 'xml': None, 'header_config': None}
        args = {**default, **args}

        if args['xml'] is not None:
            header, chains = XmlParser.parse(args['header_config'], args['xml'])

