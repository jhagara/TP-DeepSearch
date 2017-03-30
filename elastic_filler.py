import os
import sys
from semantic import Semantic
import re
import config


def main(parser_dir, dir, name, environment):
    print('Directory: ', dir)
    files = []

    # set environment to new value
    config.set_environment(environment)

    for current_dir in os.popen("find " + dir + " -name '*.xml' -printf '%h\n' | sort -u").read().split('\n'):
        current_dir = re.sub("[\n]", '', current_dir)
        if current_dir == '':
            continue

        xml = re.sub("[\n]", '', os.popen("find " + current_dir + " -maxdepth 1 -type f -name '*.xml'").read())
        config_path = ''
        searched_config_dir = current_dir
        searched_journal_marc21_dir = current_dir

        # search for header config file
        while True:
            config_path = os.popen("find " + searched_config_dir + " -maxdepth 1 -type f -name '*.json'").read()
            config_path = re.sub("[\n]", '', config_path)

            if config_path != '' or searched_config_dir == parser_dir:
                break
            else:
                searched_config_dir = re.sub("[\n]", '', os.popen("dirname '" + searched_config_dir + "'").read())

        # search for main journal marc21 path
        journal_marc21_path = ''
        while True:
            journal_marc21_path = os.popen("find " + searched_journal_marc21_dir + " -maxdepth 1 -type f -name '*journal_marc21.txt'").read()
            journal_marc21_path = re.sub("[\n]", '', journal_marc21_path)

            if journal_marc21_path != '' or searched_journal_marc21_dir == parser_dir:
                break
            else:
                searched_journal_marc21_dir = re.sub("[\n]", '', os.popen("dirname '" + searched_journal_marc21_dir + "'").read())

        # return bad exit code if any xml did not search
        # particular config header
        if config_path == '' or journal_marc21_path == '':
            sys.exit("Missing config file or journal marc21 file in dir and parent dirs: " + current_dir)

        files.append({'dir': current_dir, 'xml': xml, 'json': config_path, 'journal_marc21': journal_marc21_path})

    for file in files:
        semantic = Semantic(xml=file['xml'], header_config=file['json'])
        # call method with semantic and 'name' of journal
        print('# Loaded Files: ')
        print(file)
        semantic.save_to_elastic(name, file['dir'], file['journal_marc21'])

    # set environment to default
    config.set_environment(config.default_elastic_index)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    sys.exit()



