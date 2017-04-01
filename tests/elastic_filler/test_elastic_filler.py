import unittest
import os
import sys
import config
import elastic_filler


class TestElasticFiller(unittest.TestCase):
    def test_basic_filler_script_call(self):
        path = config.get_full_path('tests/elastic_filler/slovak')
        parser_dir = config.get_full_path('tests', 'elastic_filler')
        elastic_filler.main(parser_dir, path, 'slovak', config.default_elastic_index)
        self.assert_

    def test_extend_filler_script_call(self):
        path = config.get_full_path('tests/elastic_filler/slovak/1939/19390526')
        parser_dir = config.get_full_path('tests', 'elastic_filler')
        elastic_filler.main(parser_dir, path, 'slovak/1939/19390526', config.default_elastic_index)
        self.assert_




