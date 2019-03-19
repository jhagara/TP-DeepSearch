import unittest
import os
from helper.path_validator.path_validator import PathValidator


class TestPathValidator(unittest.TestCase):

    def test_path_validator(self):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        test_path = os.path.abspath(os.path.join(abs_path, os.pardir))
        path_validator = PathValidator()

        # testing path with 3 issues, there should be 3 errors in that path because of images
        result = path_validator.validate_issues_in_path(test_path + '/elastic_filler/slovak',
                                                        test_path + '/elastic_filler/slovak')
        self.assertEquals(len(result)-1,3)
        self.assertEquals(result[len(result)-1], 3)

        # testing non-existing path - return should be None
        result = path_validator.validate_issues_in_path(test_path + '/elastic_filler/slovakasdsa',
                                                        test_path + '/elastic_filler/slovakasdsa')
        self.assertEquals(result,None)

        # testing path with no issues - there should be 0 errors and 0 issues
        result = path_validator.validate_issues_in_path(test_path + '/helper', test_path + '/helper')
        self.assertEquals(len(result)-1, 0)
        self.assertEquals(result[len(result)-1], 0)

        # testing issue validation:
        issue_path = test_path + '/elastic_filler/slovak/1939/19390526'

        # 1. originally there should be 1 error, because of 1 image and 8 pages
        result = path_validator.validate_issue(issue_path, test_path + '/elastic_filler/slovak')
        print(result)
        self.assertEquals(len(result), 1)

        # 2. changing filename of xml issue to name which doesn't contain date number should raise another error
        os.rename(issue_path+'/XML/1336-4464_1939_19390526_00001.xml', issue_path+'/XML/1336-4464_1939_193_001.xml')
        result = path_validator.validate_issue(issue_path, test_path + '/elastic_filler/slovak')
        os.rename(issue_path + '/XML/1336-4464_1939_193_001.xml', issue_path + '/XML/1336-4464_1939_19390526_00001.xml')
        print(result)
        self.assertEquals(len(result), 2)

        # 3. changing filename of xml issue to incorrect format should raise error, for example 19392526 - month 25
        os.rename(issue_path + '/XML/1336-4464_1939_19390526_00001.xml',
                  issue_path + '/XML/1336-4464_1939_19392526_00001.xml')
        result = path_validator.validate_issue(issue_path, test_path + '/elastic_filler/slovak')
        os.rename(issue_path + '/XML/1336-4464_1939_19392526_00001.xml',
                  issue_path + '/XML/1336-4464_1939_19390526_00001.xml')
        print(result)
        self.assertEquals(len(result), 2)

        # 4. validate existence of /STR folder in issue path
        # should raise only 1 error, because error with validation number of images and pages won't be raised
        os.rename(issue_path+'/STR',issue_path+'/STRD')
        result = path_validator.validate_issue(issue_path, test_path + '/elastic_filler/slovak')
        os.rename(issue_path + '/STRD', issue_path + '/STR')
        print(result)
        self.assertEquals(len(result), 1)

        # 5. validate searching for journal_marc, renaming it should raise error
        os.rename(test_path + '/elastic_filler/slovak/journal_marc21.xml',test_path + '/elastic_filler/slovak/a.xml')
        result = path_validator.validate_issue(issue_path, test_path + '/elastic_filler/slovak')
        os.rename(test_path + '/elastic_filler/slovak/a.xml', test_path + '/elastic_filler/slovak/journal_marc21.xml')
        print(result)
        self.assertEquals(len(result), 2)

        # 6. validate functionality of limit path
        # changing it to child of dir where journal marc is located, should raise error
        result = path_validator.validate_issue(issue_path, test_path + '/elastic_filler/slovak/1939')
        print(result)
        self.assertEquals(len(result), 2)

    def test_path_validator_alto(self):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        path_validator = PathValidator()
        result = path_validator.validate_issue(abs_path + '/../lidove_noviny/1943/19430203', abs_path + '/../lidove_noviny')
        print(result)
