import os


def root_path():
    return os.path.dirname(os.path.abspath(__file__))


def get_full_path(*path):
    return os.path.join(root_path(), *path)