from lxml import etree
import os


class SchemaValidator(object):
    INPUT_SCHEMA = "/schemas/input_schema.xsd"

    def validate(self, xml, schema):
        if xml is None or schema is None:
            return -1
        schema.assertValid(xml)

    def validate_xml_schema(self, xml_path, schema_path):
        # load xml file to init stage
        xml = etree.parse(xml_path)

        # load schema from file
        schema_doc = etree.parse(schema_path)
        schema = etree.XMLSchema(schema_doc)

        return self.validate(xml, schema)

    def validate_schema(self, xml, schema_path):
        # load schema from file
        schema_doc = etree.parse(schema_path)
        schema = etree.XMLSchema(schema_doc)

        return self.validate(xml, schema)

    def validate_inputxml(self, xml):
        # load input schema from file
        schema_path = os.path.dirname(os.path.abspath(__file__)) + self.INPUT_SCHEMA
        schema_doc = etree.parse(schema_path)
        schema = etree.XMLSchema(schema_doc)

        return self.validate(xml, schema)
