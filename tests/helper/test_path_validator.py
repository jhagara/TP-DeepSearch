import unittest
import os
from helper.path_validator import PathValidator


class TestPathValidator(unittest.TestCase):
    # def test_issue(self):
    #    abs_path = os.path.dirname(os.path.abspath(__file__))
    #    test_path = os.path.abspath(os.path.join(abs_path, os.pardir))
    #   path_validator = PathValidator()
    #  path_validator.validate_issues_in_path(test_path+'/elastic_filler/slovak/1939/19390526')

    # def test_year(self):
    #    abs_path = os.path.dirname(os.path.abspath(__file__))
    #    test_path = os.path.abspath(os.path.join(abs_path, os.pardir))
    #    path_validator = PathValidator()
    #    path_validator.validate_issues_in_path(test_path+'/elastic_filler/slovak/1939')

    def test_journal(self):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        test_path = os.path.abspath(os.path.join(abs_path, os.pardir))
        path_validator = PathValidator()
        path_validator.validate_issues_in_path(test_path + '/elastic_filler/slovak')