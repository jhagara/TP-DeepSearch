import unittest
import os
import time
import shutil
from helper.path_validator.path_validator import PathValidator


class TestPathValidator(unittest.TestCase):

    def test_path_validator(self):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        test_path = os.path.abspath(os.path.join(abs_path, os.pardir))
        time_str = time.strftime("%Y%m%d-%H%M%S")
        log_name = "logs/log" + time_str + ".log"
        if not os.path.exists("logs"):
            os.makedirs("logs")
        logfile = open(log_name, "w+")
        path_validator = PathValidator()
        result = path_validator.validate_issues_in_path(test_path + '/elastic_filler/slovak', logfile)

        # testing path with 3 issues, there should be 3 errors in that path because of images
        self.assertEquals(result.get("error_count"),3)
        self.assertEquals(result.get("issue_count"), 3)

        # testing nonexisting path - there should be -1 errors
        result = path_validator.validate_issues_in_path(test_path + '/elastic_filler/slovakasdsa', logfile)
        self.assertEquals(result.get("error_count"), -1)

        # testing path with no issues - there should be 0 errors and 0 issues
        result = path_validator.validate_issues_in_path(test_path + '/helper', logfile)
        self.assertEquals(result.get("error_count"), 0)
        self.assertEquals(result.get("issue_count"), 0)

        shutil.rmtree("logs")