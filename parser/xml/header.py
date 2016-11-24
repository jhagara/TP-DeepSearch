import json
import sys
import argparse
import ast

from parser.xml.cleaner import Cleaner
from lxml import etree


class Header(object):
    
    def __init__(self):
        self.cost = ''
        self.address = ''
        self.date_location = ''
        self.annual_set = ''
        self.subscribtion = ''
        self.founder = ''
        self.number = ''

    def read_from_json(self, readfile):
        with open(readfile, 'r') as f:
            try:
                return json.load(f)
            except ValueError:
                print('Error! Unable to read file!')
                return {}

    def write_to_json(self, data, writefile):
        with open(writefile, 'w') as f:
            try:
                json.dump(data, f)
            except ValueError:
                print('Error! Non-valid write file!')

    #just for help
    def read_from_xml(self, xmlfile):
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xmlfile, parser)
        return tree.getroot()

    def assign_cost(self, data, xmlfile):
        local_path = data["marc21"][0]["path"]
        words = xmlfile.xpath(local_path)
        result = ''
        for word in words:
            result = result + str(word)
        return result 

    def assign_address(self, data, xmlfile):
        local_path = data["marc21"][1]["path"]
        words = xmlfile.xpath(local_path)
        result = ''
        for word in words:
            result = result + str(word)
        return result 

    def assign_date_location(self, data, xmlfile):
        local_path = data["marc21"][2]["path"]
        words = xmlfile.xpath(local_path)
        result = ''
        for word in words:
            result = result + str(word)
        return result 

    def assign_annual_set(self, data, xmlfile):
        local_path = data["marc21"][3]["path"]
        words = xmlfile.xpath(local_path)
        result = ''
        for word in words:
            result = result + str(word)
        return result 

    def assign_subscribtion(self, data, xmlfile):
        local_path = data["marc21"][4]["path"]
        words = xmlfile.xpath(local_path)
        result = ''
        for word in words:
            result = result + str(word)
        return result 

    def assign_founder(self, data, xmlfile):
        local_path = data["marc21"][5]["path"]
        words = xmlfile.xpath(local_path)
        result = ''
        for word in words:
            result = result + str(word)
        return result 
        
    def assign_number(self, data, xmlfile):
        local_path = data["marc21"][6]["path"]
        words = xmlfile.xpath(local_path)
        result = ''
        for word in words:
            result = result + str(word)
        return result 

    def assign_values(self, conffile, xml):
        data = self.read_from_json(conffile)
        # xml = self.read_from_xml(xmlfile)
        # xml = Cleaner.clean(xml)
        self.cost = self.assign_cost(data, xml)
        self.address = self.assign_address(data, xml)
        self.date_location = self.assign_date_location(data, xml)
        self.annual_set = self.assign_annual_set(data, xml)
        self.subscribtion = self.assign_subscribtion(data, xml)
        self.founder = self.assign_founder(data, xml)
        self.number = self.assign_number(data, xml)
