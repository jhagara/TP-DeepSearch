import os
from semantic import Semantic
from helper.path_validator.path_validator import PathValidator
import re
import config
import copy
import sys
from elasticsearch import Elasticsearch
from helper.downloader import Downloader


class IssueFacade(object):
    @staticmethod
    def validate_issue_before_parsing(issue_path, limit_path):
        path_validator = PathValidator()
        error_list = ""
        result = ""
        if len(error_list) == 0:
            result = "Validation was successful for " + issue_path
        else:
            for err in error_list:
                result = result + err + '|'
            raise ValueError(result)
        return result

    @classmethod
    def insert_by_fullpath(cls, parser_dir, target_fullpath, name):
        xml = re.sub("[\n]", '', os.popen("find '" + target_fullpath + "/XML' -maxdepth 1 -type f -name '*.xml' | head -n 1").read())
        config_path = cls.__find_file(copy.copy(target_fullpath), parser_dir, "*.json")
        journal_marc21_path = cls.__find_file(copy.copy(target_fullpath), parser_dir, "*journal_marc21.xml")
        file = {'dir': target_fullpath, 'xml': xml, 'json': config_path, 'journal_marc21': journal_marc21_path}
        print("Parsing: " + str(file))

        # return bad exit code if any xml did not search
        if xml == '' or config_path == '' or journal_marc21_path == '':
            raise FileNotFoundError("Missing xml, config file or journal marc21 file in dir and parent dirs")

        print('Parsing File: ', target_fullpath)
        semantic = Semantic(xml=file['xml'], header_config=file['json'])
        issue_id = semantic.save_to_elastic(name, file['dir'], file)
        semantic.compress_images(file['dir'])
        semantic.insert_key_words(issue_id)

        return 'Insert by fullpath was successful'

    @classmethod
    def bulk_insert(cls, parser_dir, dir, name):
        print('PARSING Directory: ', dir)
        files = []

        for current_dir in os.popen("find " + dir + " -path '*/XML/*.xml' -printf '%h\n' | sort -u").read().split('\n'):
            if current_dir == '':
                break

            xml = re.sub("[\n]", '', os.popen("find " + current_dir + " -maxdepth 1 -type f -name '*.xml' | head -n 1").read())

            current_dir = re.sub("[\n]", '', os.popen("dirname '" + re.sub("[\n]", '', current_dir) + "' | xargs readlink -f").read())
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
            semantic.compress_images(file['dir'])
            semantic.insert_key_words(issue_id)

        return 'Bulk insert was successful'

    @classmethod
    def download_tree(cls, url, uuid, dir):
        print("Downloading " + uuid + " form url " + url)

        downloader = Downloader()
        downloader.download_tree(url, uuid, dir)

        return "Download was successful"

    @classmethod
    def download_item(cls, url, uuid, dir):
        print("Downloading " + uuid + " form url " + url)

        downloader = Downloader()
        downloader.download_item(url, uuid, dir)

        return "Download was successful"

    @classmethod
    def update_issue(cls, issue_id):
        semantic = Semantic()
        semantic.insert_key_words(issue_id)

        return 'Updating Issue with id: ' + str(issue_id) + ' was successful'

    @classmethod
    def export_issue(cls, issue_id):
        semantic = Semantic()
        semantic.export_marc_for_issue(issue_id)
        semantic.export_image_for_issue(issue_id)

        # set exported flag to true
        es = Elasticsearch()
        es.update(index=config.elastic_index(), doc_type='issue', id=issue_id, body={'doc': {'was_exported': True}})

        return 'Exporting Issue with id: ' + str(issue_id) + ' was successful'

    # PRIVATE

    @classmethod
    def __find_file(cls, current_dir, parser_dir, name):
        while True:
            path = os.popen("find " + current_dir + " -maxdepth 1 -type f -name '" + name + "'").read()
            path = re.sub("[\n]", '', path)

            if path != '' or current_dir == parser_dir:
                break
            else:
                current_dir = re.sub("[\n]", '', os.popen("dirname '" + current_dir + "'").read())

        return path

def main(*attrs):
    action = attrs[0]
    environment = attrs[1]
    prms = attrs[2:]

    print(action)
    print(environment)
    print(prms)

    config.set_environment(environment)

    try:
        print(getattr(IssueFacade, action)(*prms))
        result_code = 0
    except:
        print(sys.exc_info())
        result_code = 1

    config.set_environment(config.default_elastic_index)
    return result_code

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
