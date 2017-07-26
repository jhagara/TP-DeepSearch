import unittest
from helper.rules_tester import RulesTester


class TestRulesTester(unittest.TestCase):
    def test_all_issues(self):
        tester = RulesTester()


if __name__ == '__main__':
    unittest.main()
