import os
import sys
from semantic import Semantic
import re
import config
from elasticsearch import Elasticsearch
import copy


class IssueFacade(object):
    @classmethod
    def bulk_insert(cls, environment, parser_dir, dir, name):
        cls.__set_env(environment)

        print('PARSING Directory: ', dir)
        files = []

        for current_dir in os.popen("find " + dir + " -path '*/XML/*.xml' -printf '%h\n' | sort -u").read().split('\n'):
            xml = re.sub("[\n]", '', os.popen("find " + current_dir + " -maxdepth 1 -type f -name '*.xml'").read())

            current_dir = re.sub("[\n]", '', os.popen("dirname '" + re.sub("[\n]", '', current_dir) + "'").read())
            config_path = cls.__find_file(copy.copy(current_dir), parser_dir, "*.json")
            journal_marc21_path = cls.__find_file(copy.copy(current_dir), parser_dir, "*journal_marc21.xml")

            # return bad exit code if any xml did not search
            if config_path == '' or journal_marc21_path == '':
                print("Missing config file or journal marc21 file in dir and parent dirs: " + current_dir)
                return False

            files.append({'dir': current_dir, 'xml': xml, 'json': config_path, 'journal_marc21': journal_marc21_path})

        for file in files:
            print('# Loaded Files: ', file)
            semantic = Semantic(xml=file['xml'], header_config=file['json'])
            issue_id = semantic.save_to_elastic(name, file['dir'], file)
            semantic.insert_key_words(issue_id)

        cls.__unset_env()

    @classmethod
    def update_issue(cls, environment, issue_id):
        cls.__set_env(environment)

        es = Elasticsearch()
        semantic = Semantic()
        semantic.insert_key_words(issue_id)

        cls.__unset_env()

    @classmethod
    def export_issue(cls, environment, issue_id):
        cls.__set_env(environment)

        es = Elasticsearch()
        semantic = Semantic()
        semantic.export_marc_for_issue(issue_id)
        semantic.export_image_for_issue(issue_id)

        cls.__unset_env()

    def __find_file(self, current_dir, parser_dir, name):
        while True:
            path = os.popen("find " + current_dir + " -maxdepth 1 -type f -name '" + name + "'").read()
            path = re.sub("[\n]", '', path)

            if path != '' or current_dir == parser_dir:
                break
            else:
                current_dir = re.sub("[\n]", '', os.popen("dirname '" + current_dir + "'").read())

        return path

    def __set_env(self, environment):
        config.set_environment(environment)

    def __unset_env(self):
        config.set_environment(config.default_elastic_index)
