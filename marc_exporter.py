import sys
from semantic import Semantic
import config


def main(issue_id, environment):
    # set environment to new value
    config.set_environment(environment)

    # update articles key_words
    semantic = Semantic()
    semantic.export_marc_for_issue(issue_id)
    semantic.export_image_for_issue(issue_id)

    # set environment to default
    config.set_environment(config.default_elastic_index)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
    sys.exit()



