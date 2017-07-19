import unittest
import os
from lxml import etree
from parser.xml.schema_validator import SchemaValidator


class MyTestCase(unittest.TestCase):
    def test_validate_inputxml(self):
        validator = SchemaValidator()
        valid_path = os.path.dirname(os.path.abspath(__file__)) + "/valid.xml"  # path to valid xml
        valid_xml = etree.parse(valid_path)
        validator.validate_inputxml(valid_xml)

        invalid_path = os.path.dirname(os.path.abspath(__file__)) + "/invalid.xml"  # path to invalid xml
        invalid_xml = etree.parse(invalid_path)
        self.assertRaises(etree.DocumentInvalid, validator.validate_inputxml, invalid_xml)

if __name__ == '__main__':
    unittest.main()
