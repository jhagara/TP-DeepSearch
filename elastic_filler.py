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
        searched_dir = current_dir

        while True:
            config_path = os.popen("find " + searched_dir + " -maxdepth 1 -type f -name '*.json'").read()
            config_path = re.sub("[\n]", '', config_path)

            if config_path != '' or searched_dir == parser_dir:
                break
            else:
                searched_dir = re.sub("[\n]", '', os.popen("dirname '" + searched_dir + "'").read())

        # return bad exit code if any xml did not search
        # particular config header
        if config_path == '':
            sys.exit("Missing config file in dir and parent dirs: " + searched_dir)

        files.append({'dir': current_dir, 'xml': xml, 'json': config_path})

    for file in files:
        semantic = Semantic(xml=file['xml'], header_config=file['json'])
        # call method with semantic and 'name' of journal
        print('xml: ', file['xml'])
        semantic.save_to_elastic(name, file['dir'], 'dummy/way/of/marc')

    # set environment to default
    config.set_environment(config.default_elastic_index)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    sys.exit()



