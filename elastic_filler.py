import os
import sys
from semantic import Semantic
import re


def main(dir, name):
    print('Directory: ', dir)
    files = []

    for current_dir in os.popen("find " + dir + " -name '*.xml' -printf '%h\n' | sort -u").read().split('\n'):
        current_dir = re.sub("[\n]", '', current_dir)
        if current_dir == '':
            continue

        xml = re.sub("[\n]", '', os.popen("find " + current_dir + " -maxdepth 1 -type f -name '*.xml'").read())
        config = ''
        searched_dir = current_dir

        while True:
            config = os.popen("find " + searched_dir + " -maxdepth 1 -type f -name '*.json'").read()
            config = re.sub("[\n]", '', config)

            if config != '' or searched_dir == dir:
                break
            else:
                searched_dir = re.sub("[\n]", '', os.popen("dirname '" + searched_dir + "'").read())

        # return bad exit code if any xml did not search
        # particular config header
        if config == '':
            sys.exit("Missing config file in dir and parent dirs: " + searched_dir)

        files.append({'xml': xml, 'json': config})

    for file in files:
        semantic = Semantic(xml=file['xml'], header_config=file['json'])
        # call method with semantic and 'name' of journal

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
    sys.exit()



