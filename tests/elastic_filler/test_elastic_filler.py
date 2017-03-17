import unittest
import os
import sys
import config
import elastic_filler


class TestElasticFiller(unittest.TestCase):
    def test_basic_filler_script_call(self):
        path = config.get_full_path('tests/elastic_filler/slovak')
        elastic_filler.main(path, 'slovak')
        self.assert_




