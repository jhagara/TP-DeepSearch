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

        valid_path_v10 = os.path.dirname(os.path.abspath(__file__)) + "/../../narodna_jednota_v10.xml"  # xml v10
        valid_xml_v10 = etree.parse(valid_path_v10)
        validator.validate_inputxml(valid_xml_v10)

        invalid_path = os.path.dirname(os.path.abspath(__file__)) + "/invalid.xml"  # path to invalid xml
        invalid_xml = etree.parse(invalid_path)
        self.assertRaises(etree.DocumentInvalid, validator.validate_inputxml, invalid_xml)

    def test_alto_schema(self):
        validator = SchemaValidator()
        path = os.path.dirname(os.path.abspath(__file__)) + "/../../lidove_noviny/1943/19430203/XML/2_uuid:a7aaec20-6ae3-11dd-9a90-000d606f5dc6.xml"  # path to alto xml
        xml = etree.parse(path)
        validator.validate_inputxml(xml)

if __name__ == '__main__':
    unittest.main()
