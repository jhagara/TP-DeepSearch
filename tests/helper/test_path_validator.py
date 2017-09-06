import unittest
import os
from helper.path_validator.path_validator import PathValidator


class TestPathValidator(unittest.TestCase):

    def test_path_validator(self):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        test_path = os.path.abspath(os.path.join(abs_path, os.pardir))
        path_validator = PathValidator()
        result = path_validator.validate_issues_in_path(test_path + '/elastic_filler/slovak',
                                                        test_path + '/elastic_filler/slovak')

        # testing path with 3 issues, there should be 3 errors in that path because of images
        self.assertEquals(len(result)-1,3)
        self.assertEquals(result[len(result)-1], 3)

        # testing nonexisting path - return should be None
        result = path_validator.validate_issues_in_path(test_path + '/elastic_filler/slovakasdsa',
                                                        test_path + '/elastic_filler/slovakasdsa')
        self.assertEquals(result,None)

        # testing path with no issues - there should be 0 errors and 0 issues
        result = path_validator.validate_issues_in_path(test_path + '/helper', test_path + '/helper')
        self.assertEquals(len(result)-1, 0)
        self.assertEquals(result[len(result)-1], 0)