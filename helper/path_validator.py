import os
import sys
from lxml import etree
from parser.xml.cleaner import Cleaner
import glob

class PathValidator(object):
    marc_schema_path = "/MARC21schema.xsd"
    error_count = 0
    issue_count = 0
    journal_paths = set()

    def validate_issues_in_path(self,path):

        if os.path.exists(path):
            # make sure that path is absolute
            path = os.path.abspath(path)

            # find XML subdirectories of path
            for dirpath, dirnames, filenames in os.walk(path):
                for dirname in [d for d in dirnames if d == "XML"]:
                    xml_dir_path = os.path.join(dirpath, dirname)

                    # find .xml file in /XML directory
                    xml_path = self.__find_file_path(xml_dir_path,".xml")
                    if xml_path is None:
                        print("Error: .xml file of issue not found in: " + xml_dir_path)
                        self.error_count = self.error_count + 1

                    # get issue name
                    path, issue_name = os.path.split(xml_path)
                    issue_name = os.path.splitext(issue_name)[0]
                    issue_name = issue_name[:-6]

                    # get issue path
                    issue_path = os.path.abspath(os.path.join(path, os.pardir))
                    self.issue_count = self.issue_count + 1

                    # check .json config and images in STR directory
                    self.error_count = self.error_count + self.__check_needed_files(xml_path,issue_path,issue_name)

            # at last check journal directories if they contain valid marc21 record for journal
            for journal_path in self.journal_paths:
                self.error_count = self.error_count + self.__check_journal_marc(journal_path)

        # if path does not exists
        else:
            return {'error_count': -1, 'issue_count': -1}

        return {'error_count': self.error_count, 'issue_count': self.issue_count}

    @classmethod
    def __find_dir_path(cls,issue_path,dirname):
        dir_path = None
        for child_dir in [name for name in os.listdir(issue_path)
                          if os.path.isdir(os.path.join(issue_path, name))]:
            if child_dir == dirname:
                dir_path = os.path.join(issue_path,child_dir)
        return dir_path

    @classmethod
    def __find_file_path(cls, path, file_extension):
        xml_path = None
        for file in os.listdir(path):
            if file.endswith(file_extension):
                xml_path = os.path.join(path, file)
        return xml_path

    @classmethod
    def __check_needed_files(cls, xml_path, issue_path, issue_name):
        error_count = 0

        # check if path to images exists
        images_path = cls.__find_dir_path(issue_path, "STR")
        if images_path is None:
            print("Error: STR Directory for issue: " + issue_name + " was not found")
            error_count = error_count + 1
        else:
            # check if quantity of images correspond to quantity of pages in xml
            if cls.__validate_number_of_pages(xml_path, images_path, issue_name) is False:
                print("Error when validating number of pages and images in directory for issue: " + issue_name)
                error_count = error_count + 1

        # get path to main journal file
        year_path = os.path.abspath(os.path.join(issue_path, os.pardir))
        journal_path = os.path.abspath(os.path.join(year_path, os.pardir))
        cls.journal_paths.add(journal_path)

        # check if exists config file .json in issue directory
        json_path = cls.__find_file_path(issue_path, ".json")
        if json_path is None:

            # check if exists config file .json in year directory
            json_path = cls.__find_file_path(year_path, ".json")
            if json_path is None:

                # check if exists config file .json in journal directory
                json_path = cls.__find_file_path(journal_path, ".json")
                if json_path is None:
                    print("Error: No .json config file found for issue: " + issue_name + " in issue, year or journal directory")
                    error_count = error_count + 1

        return error_count

    @classmethod
    def __check_journal_marc(cls, journal_path):
        error_count = 0

        # check if exists marc21 record for journal
        marc_path = cls.__find_file_path(journal_path, "marc21.xml")
        if marc_path is None:
            print("Error: No marc21 record found for journal in directory: " + journal_path)
            error_count = error_count + 1
        else:
            # check if existing marc21 record is valid
            if cls.__validate_marcxml(marc_path) is False:
                print("Error: MarcXML is not valid for journal in directory : " + journal_path)
                error_count = error_count + 1
        return error_count

    @classmethod
    def __validate_marcxml(cls,marcxml_path):

        # get absolute path to schema of marc journal file
        schema_abs_path = os.path.dirname(os.path.abspath(__file__))+cls.marc_schema_path

        # parse schema of marc journal
        schema_doc = etree.parse(schema_abs_path)
        schema = etree.XMLSchema(schema_doc)

        # parse xml of marc journal
        marcxml = etree.parse(marcxml_path)

        # validate
        if schema.validate(marcxml):
            return True
        else:
            return False

    @classmethod
    def __validate_number_of_pages(cls,xml_path, images_path, issue_name):
        # load xml file
        xml = etree.parse(xml_path)
        xml = Cleaner.clean(xml)

        # get count of pages in xml
        pages_count = xml.xpath('count(//page)')

        # get count of images in path
        images_count = 0
        for file in os.listdir(images_path):
            if file.startswith(issue_name):
                images_count = images_count + 1

        if pages_count != images_count:
            return False
        else:
            return True

def main(*attrs):
    # handle input
    if len(attrs) == 0:
        path = input("Enter path to validate:\n")
    else:
        path = attrs[0]
    print("Validating path: " + path)

    try:
        path_validator = PathValidator()
        result = path_validator.validate_issues_in_path(path)
        error_count = result.get("error_count")
        issue_count = result.get("issue_count")

        result_code = 1
        if error_count == 0 & issue_count > 0 :
            result_code = 0
        elif error_count == -1:
            print("Path " + path + " does not exists")
        elif error_count > 0:
            print("There were found", error_count, "errors in", issue_count, "issues")
        else:
            print("No issues found in path: " + path)

    except:
        print("Invalid path")
        result_code = 1

    return result_code

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))