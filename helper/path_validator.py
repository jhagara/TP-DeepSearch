import os
from lxml import etree
from parser.xml.cleaner import Cleaner


class PathValidator(object):
    def validate_issues_in_path(self,path):
        for dirpath, dirnames, filenames in os.walk(path):
            for dirname in [d for d in dirnames if d == "XML"]:
                xml_dir_path = os.path.join(dirpath, dirname)

                # find .xml file in /XML directory
                xml_path = self.__find_file_path(xml_dir_path,".xml")
                if xml_path is None:
                    print("Error: .xml file of issue not found in: " + xml_dir_path)
                    return False
                else:
                    print("xml_path is: " + xml_path)

                # get issue name
                path, issue_name = os.path.split(xml_path)
                issue_name = os.path.splitext(issue_name)[0]
                issue_name = issue_name[:-6]
                print("issue name is: " + issue_name)

                # get issue path
                issue_path = os.path.abspath(os.path.join(path, os.pardir))
                print("issue path is: " + issue_path)

                # check all needed files: STR, .json config, marc21 record, PDF
                self.__check_needed_files(issue_path,issue_name)

                # check if quantity of images correspond to quantity of pages in xml
                # get path to images
                images_path = self.__find_dir_path(issue_path, "STR")
                if self.__validate_number_of_pages(xml_path, images_path, issue_name) is False:
                    print("Error when validating number of pages and images in directory for issue: " + issue_name)
                    # return False

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
    def __check_needed_files(cls, issue_path, issue_name):

        # get path to images
        images_path = cls.__find_dir_path(issue_path, "STR")
        if images_path is None:
            print("Error: STR Directory for issue: " + issue_name + " was not found")
            # return False

            # get path to PDF
            # pdf_path = self.__find_dir_path(issue_path, "PDF")
            # if pdf_path is None:
            # print("Error: PDF Directory for issue: " + issue_name + " was not found")
            # return False

        # get path to main journal file
        year_path = os.path.abspath(os.path.join(issue_path, os.pardir))
        journal_path = os.path.abspath(os.path.join(year_path, os.pardir))

        # check if exists config file .json in issue directory
        json_path = cls.__find_file_path(issue_path, ".json")
        if json_path is None:

            # check if exists config file .json in year directory
            json_path = cls.__find_file_path(year_path, ".json")
            if json_path is None:

                # check if exists config file .json in journal directory
                json_path = cls.__find_file_path(journal_path, ".json")
                if json_path is None:
                    print("Error: No .json config file found for issue: " + issue_name)
                    # return False

        # check if exists marc21 record for journal
        marc_path = cls.__find_file_path(journal_path, "marc21.xml")
        if marc_path is None:
            print("Error: No marc21 record found for journal of issue: " + issue_name)
            # return False



