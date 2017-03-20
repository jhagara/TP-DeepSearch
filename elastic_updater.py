import os
import sys
from semantic import Semantic
import re
import config


def main(issue_id, environment):
    print('Directory: ', dir)
    files = []

    # set environment to new value
    config.set_environment(environment)

    semantic = Semantic()
    semantic.insert_key_words(issue_id)

    # set environment to default
    config.set_environment(config.default_elastic_index)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
    sys.exit()



