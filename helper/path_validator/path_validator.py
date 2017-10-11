import math
import os
import sys
import time
import re
import datetime
from lxml import etree
import json


class PathValidator(object):
    # Class attributes:
    #    path to marc xml schema
    #    path to issue xml schema
    #    approximate time needed to validate one issue
    marc_schema_path = "/MARC21_journal_schema.xsd"
    xml_issue_schema_path = "/issue_xml_schema.xsd"
    issue_validate_time = 1.6

    # this is method which will be called before parsing issue
    # argument should be path to issue directory, such as 1336-4464/1336-4464_1939/19390101 containing STR,XML etc.
    def validate_issue(self, issue_path, limit_path):

        error_list = []

        # check if limit path can be recursively reached from limit_path
        # because of using /while True/ in check_config and check_journal_marc
        relpath = os.path.relpath(issue_path, limit_path)
        if '..' in relpath:
            error = "Error before validating: Limit path: " + limit_path + "can't be recursively reached " \
                                                                           "from validating path: " + limit_path
            print(error)
            error_list.append(error)
            return error_list

        issue_path = os.path.abspath(issue_path)
        xml_dir_path = self.__find_dir_path(issue_path, "XML")
        xml_path = self.__find_file_path(xml_dir_path, ".xml")

        # get issue name
        path, issue_name = os.path.split(xml_path)
        issue_name = (os.path.splitext(issue_name)[0])

        # check if name of xml contains date in the same format as is searched for
        function_error_list = self.__validate_issue_name(issue_name, xml_dir_path)
        error_list = error_list + function_error_list

        # check validity of .xml issue in path
        invalid_issue_xml = False
        function_error_list = self.__validate_issue_xml(xml_path)
        if len(function_error_list) > 0:
            invalid_issue_xml = True
            error_list = error_list + function_error_list

        # check existence of STR directory and quantity of images and pages
        function_error_list = self.__validate_images(xml_path, issue_path, issue_name, invalid_issue_xml)
        error_list = error_list + function_error_list

        # check existence of journal_marc and validate it to schema
        function_error_list = self.__check_journal_marc(issue_path,limit_path)
        error_list = error_list + function_error_list
        # check existence of config file and validate it
        error_list = error_list + self.__check_config(issue_path, limit_path)

        return error_list

    # method returns list, which contains all found errors and at last, count of all issues
    # method returns None, when no issue has been found
    def validate_issues_in_path(self, path, limit_path):

        # Method arguments:
        #    list of errors, which will this method returned by this method
        #    count of issues, which will be appended to the list of errors to return
        #    set (no same values) of issue parent paths, serves for grouping errors when no marcjournal found
        error_list = []
        issue_count = 0
        issue_parent_paths = set()

        if os.path.exists(path):

            # first make sure that path is absolute
            path = os.path.abspath(path)

            total_count = self.count_issues_in_path(path)
            # find XML subdirectories of path
            for dirpath, dirnames, filenames in os.walk(path):
                for dirname in [d for d in dirnames if d == "XML"]:
                    # join /XML to path
                    xml_dir_path = os.path.join(dirpath, dirname)

                    invalid_issue_xml = False

                    # print progress bar
                    issue_count = issue_count + 1
                    progress = issue_count/total_count*100
                    print('\rProgress is: [{0}{1}] {2:.2f}%'.format('#' * (math.floor(progress / 10))
                                            ,' ' * (10-(math.floor(progress / 10))), progress), end='')

                    # find .xml file in /XML directory and validate xml to schema
                    xml_path = self.__find_file_path(xml_dir_path,".xml")
                    if xml_path is None:
                        error = "Error: .xml file of issue not found in: " + xml_dir_path
                        error_list.append(error)
                        continue
                    else:
                        function_error_list = self.__validate_issue_xml(xml_path)
                        if len(function_error_list) > 0:
                            invalid_issue_xml = True
                            error_list = error_list + function_error_list

                    # get issue name
                    path, issue_name = os.path.split(xml_path)
                    issue_name = (os.path.splitext(issue_name)[0])

                    # validate filename of xml issue
                    function_error_list = self.__validate_issue_name(issue_name, xml_dir_path)
                    error_list = error_list + function_error_list

                    # get issue path
                    issue_path = os.path.abspath(os.path.join(path, os.pardir))

                    # try to search for journal_marc in issue path and validate it to schema
                    marc_found = False
                    for file in os.listdir(issue_path):
                        if 'journal_marc' in file:
                            marc_path = os.path.join(issue_path, file)
                            err = self.__validate_marcxml(marc_path)
                            if err != "":
                                error = "Error: MarcXML " + os.path.split(marc_path)[1] + " is not valid for " + \
                                        "journal in directory : " + os.path.split(marc_path)[0] + " Detail: " + err
                                error_list.append(error)
                            marc_found = True
                            break

                    # save parent directory of issue to set of paths, which will be used in the end of this method
                    if marc_found is False and issue_path != limit_path:
                        issue_parent_path = os.path.abspath(os.path.join(issue_path, os.pardir))
                        issue_parent_paths.add(issue_parent_path)

                    # if issue path is the same as limit path, it means that we searched everywhere so we print error
                    elif marc_found is False and issue_path == limit_path:
                        error = "Error: No XML file journal_marc21 found for journal in directory: " + issue_path \
                                + " Where was expected file with name containing 'journal_marc'"
                        error_list.append(error)

                    # find STR directory check in issue path and validate number of images with number of pages
                    function_error_list = self.__validate_images(xml_path,issue_path, issue_name, invalid_issue_xml)
                    error_list = error_list + function_error_list

            # check parent directories of issues if they contain valid marc21 record for journal
            # send limit_path as argument so it will be searching recursively from parent dir of issue up to limit_path
            for parent_issue_path in issue_parent_paths:
                function_error_list = self.__check_journal_marc(parent_issue_path, limit_path)
                error_list = error_list + function_error_list

        # if path does not exists
        else:
            return None

        # delete progress bar
        print('\r',end='')
        error_list.append(issue_count)
        return error_list

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

    def count_issues_in_path(cls, path):
        counter = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for dirname in [d for d in dirnames if d == "XML"]:
                counter = counter + 1
        return counter

    @classmethod
    def __validate_issue_name(cls, issue_name, xml_dir_path):
        error_list = []

        # search for 8 numbers-long string between _ character -> representing date format
        release_dates = re.search('_[0-9]{8}_', issue_name)
        if release_dates is None:
            error = "Error: Name of .xml file for issue: " + issue_name + ".xml in: " + xml_dir_path + \
                    " does not contain 8 characters long string which represents date e.g. 19390526"
            error_list.append(error)
        else:
            release_date = release_dates.group(0)[1:-1]

            # if 8 numbers-long string exists, try to parse it as a date
            try:
                datetime.datetime.strptime(release_date, '%Y%m%d')
            except:
                error = "Error: Incorrect date format found in the name of .xml issue: " + issue_name + ".xml in: " + \
                        xml_dir_path + " Format should be YYYYMMDD like 19390526"
                error_list.append(error)

        return error_list

    # find STR directory and if xml of issue is valid, validate number of pages to number of images in STR dir
    @classmethod
    def __validate_images(cls, xml_path, issue_path, issue_name, invalid_issue_xml):
        error_list = []

        # check if path to images exists
        images_path = cls.__find_dir_path(issue_path, "STR")
        if images_path is None:
            error = "Error: STR Directory for issue: " + issue_name + " was not found. " + \
                    "Expected STR directory in path: " + issue_path
            error_list.append(error)
        else:
            # check if quantity of images correspond to quantity of pages in xml
            if invalid_issue_xml is True:
                error = "Warning: Validation of quantity of images was skipped, because XML of issue: " + issue_name + \
                        " in directory " + os.path.abspath(os.path.join(xml_path, os.pardir)) + " is invalid"
                error_list.append(error)
            else:
                function_error_list = cls.__validate_number_of_pages(xml_path, images_path, issue_name)
                error_list = error_list + function_error_list
        return error_list

    @classmethod
    def __check_config(cls, issue_path, limit_path):
        error_list = []

        # for each path in list, search recursively for config.json in that path up to limit path
        current_path = issue_path
        config_path = None
        while current_path!="/":
            for file in os.listdir(current_path):
                if 'config.json' in file:
                    config_path = os.path.join(current_path, file)
            if current_path == limit_path or config_path is not None:
                break
            current_path = os.path.abspath(os.path.join(current_path, os.pardir))

        # if config_path was founded, validate its json
        if config_path is not None:
            try:
                with open(config_path, encoding='utf8') as f:
                    config = json.load(f)
                    config['Number']['path']
                    config['Volume']['path']
            except:
                error = "Error: For issues in: " + issue_path + " founded Config file " + os.path.split(config_path)[
                    1] + " is not valid as header config in directory : " \
                        + os.path.split(config_path)[0] + ". Should contain keys 'Number', 'Volume', both containing " \
                                                          "hash with key 'path' with String value"
                error_list.append(error)

        # else generate error
        else:
            error = "Error: For issues in: " + issue_path + " Config file for Issue was not found from " + \
                    "this path up to " + limit_path
            error_list.append(error)

        return error_list

    @classmethod
    def __check_journal_marc(cls, issue_path, limit_path):
        error_list = []

        # for each path in list, search recursively for marc_journal in that path up to limit path
        current_path = issue_path
        marc_path = None
        while current_path != "/":
            for file in os.listdir(current_path):
                if 'journal_marc' in file:
                    marc_path = os.path.join(current_path, file)
            if current_path == limit_path or marc_path is not None:
                break
            current_path = os.path.abspath(os.path.join(current_path, os.pardir))

        # if marc_path was founded, validate its xml to schema
        if marc_path is not None:
            err = cls.__validate_marcxml(marc_path)
            if err != "":
                error = "Error: For issues in: " + issue_path + " founded MarcXML " + os.path.split(marc_path)[
                    1] + " is not valid for journal in directory : " \
                        + os.path.split(marc_path)[0] + " Detail: " + err
                error_list.append(error)

        # else generate error
        else:
            error = "Error: For issues in: " + issue_path + " MarcXML for journal was not founded from " + \
                    "this path up to " + limit_path
            error_list.append(error)

        return error_list

    @classmethod
    def __validate_marcxml(cls, marcxml_path):

        # get absolute path to schema of marc journal file
        schema_abs_path = os.path.dirname(os.path.abspath(__file__)) + cls.marc_schema_path

        # parse schema of marc journal
        schema_doc = etree.parse(schema_abs_path)
        schema = etree.XMLSchema(schema_doc)

        # parse xml of marc journal
        try:
            marcxml = etree.parse(marcxml_path)
        except etree.XMLSyntaxError as err:
            return str(err)

        # validate xml to schema
        try:
            schema.assertValid(marcxml)
        except etree.DocumentInvalid as err:
            return str(err)

        return ""

    @classmethod
    def __validate_issue_xml(cls, xml_path):

        error_list = []

        # get absolute path to schema of marc journal file
        schema_abs_path = os.path.dirname(os.path.abspath(__file__)) + cls.xml_issue_schema_path

        # parse schema of issue xml
        schema_doc = etree.parse(schema_abs_path)
        schema = etree.XMLSchema(schema_doc)

        # parse xml issue
        try:
            issue_xml = etree.parse(xml_path)
        except etree.XMLSyntaxError as err:
            error = "Error: Unparsable xml of issue " + os.path.split(xml_path)[1] + " in " + os.path.split(xml_path)[0]\
                    + " Detail: " + str(err)
            error_list.append(error)
            return error_list

        # validate it to schema
        try:
            schema.assertValid(issue_xml)
        except etree.DocumentInvalid as err:
            error = "Error: Invalid xml of issue " + os.path.split(xml_path)[1] + " in " + os.path.split(xml_path)[0] \
                    + " Detail: " + str(err)
            error_list.append(error)

        return error_list

    @classmethod
    def __validate_number_of_pages(cls, xml_path, images_path, issue_name):
        error_list = []

        # get line from xml issue which contains element pagesCount
        pages_count_line = None
        pages_count = 0
        with open(xml_path,"r",encoding="utf-8") as f:
            for line in f:
                if 'pagesCount="' in line:
                    pages_count_line = line
                    break

        # if no line with element pagesCount found, use lxml to count element <page>
        if pages_count_line is None:
            xml = etree.parse(xml_path)
            for node in xml.iter():
                has_namespace = node.tag.startswith('{')
                if has_namespace:
                    node.tag = node.tag.split('}', 1)[1]
            pages_count = xml.xpath('count(//page)')

        # else parse pagesCount value from line
        else:
            for s in pages_count_line.split():
                if s.startswith('pagesCount='):
                    pages_count = int(list(filter(str.isdigit, s))[0])
                    break

        # get count of images in path
        images_count = 0
        for file in os.listdir(images_path):
            if file.endswith(".jpg"):
                images_count = images_count + 1

        # validate number of images and pages
        if pages_count > images_count:
            error = "Error: issue " + issue_name + " in: " + os.path.abspath(os.path.join(xml_path, os.pardir)) + \
                  " has " + str(pages_count) + " page(s), but there are only " + str(images_count) + \
                    " .jpg image(s) in " + images_path
            error_list.append(error)

        return error_list


def main(*attrs):

    # input can be 2 args:
    #   1. validating path
    #   2. limiting path, up which will be searched for marc_journal
    # input can be 1 argument as well, in that case validating path and limiting path will be the same
    # if no args received, ask for user to enter them

    if len(attrs) == 0:
        path = input("Enter path to validate:\n")
        limit_path = input("Enter limit path, which will be max depth to be searched, or leave blank (press enter) " +
                           "if it's the same as validating path:\n")
        if len(limit_path) == 0:
            limit_path = path

    elif len(attrs) == 1:
        path = attrs[0]
        limit_path = path
    else:
        path = attrs[0]
        limit_path = attrs[1]

    # validating that limiting path can be recursively reached from validating path
    path = os.path.abspath(path)
    limit_path = os.path.abspath(limit_path)
    while True:
        relpath = os.path.relpath(path, limit_path)
        if '..' in relpath:
            print("Error: Limit path can't be recursively reached from validating path")
            limit_path = input("Enter path, which will be max depth to be searched, or leave blank (press enter) " +
                               "if it's the same as validating path ):\n")
            if len(limit_path) == 0:
                limit_path = path
        else:
            break

    print("Validating path: " + path)
    print("Max recursive depth to be searched is path: " + limit_path)
    print("Validation started at: " + time.strftime("%H:%M:%S"))

    path_validator = PathValidator()

    # get approximate running time and print it
    if os.path.exists(path):
        approximate_time =  path_validator.count_issues_in_path(path) * PathValidator.issue_validate_time
        if approximate_time<60:
            print("Approximate running time is : {0:.2f} seconds".format(approximate_time))
        else:
            print("Approximate running time is : {0:.2f} minutes".format(approximate_time/60))

    print("... please wait ...")
    try:
        # prepare logfile for printing errors
        time_str = time.strftime("%d%m%Y-%H%M%S")
        log_name = "logs/log_" + os.path.split(path)[1] + "_" + time_str + ".log"
        if not os.path.exists("logs"):
            os.makedirs("logs")
        logfile = open(log_name,"w+")
        print("Validating path: " + path, file = logfile)

        # run path validation

        result = path_validator.validate_issues_in_path(path, limit_path)

        # handle results of path validation
        result_code = 1
        error_count = 0
        warning_count = 0
        if result is None:
            print("Error: Path " + path + " does not exists")
            logfile.close()
            os.remove(log_name)
        elif len(result) > 1:
            issue_count = result[len(result)-1]
            for i in range(0, len(result) - 1):
                print(result[i])
                print(result[i], file=logfile)
                if result[i].startswith("Warning"):
                    warning_count = warning_count + 1
                else:
                    error_count = error_count + 1
            print("------------------------------------------")
            print("There were found", error_count, "error(s),", warning_count,
                  "warning(s), and total of", issue_count, "issue(s)")
            print("There were found", error_count, "error(s),", warning_count,
                  "warning(s), and total of", issue_count, "issue(s)", file = logfile)
            print("Created logfile: " + os.path.abspath(log_name))
            result_code = 0
        elif len(result) == 1 and result[0] == 0:
            print("No issues found in path: " + path)
            logfile.close()
            os.remove(log_name)
        else:
            print("No errors and total of", result[len(result)-1], "issue(s) found in path " + path)
            result_code = 0
            logfile.close()
            os.remove(log_name)
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        print("Invalid path")
        result_code = 1

    return result_code

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
