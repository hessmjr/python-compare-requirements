#!/usr/bin/env python3
"""
Compare requirements between projects.
"""

__version__ = '0.1.0'
__date__ = '2023-01-16'
__author__ = 'Mark Hess'
__licence__ = 'BSD'

from pip._internal.req import parse_requirements
import os
import urllib.request


def establish_filepath(directory_path):
    """
    Get file path from local file system or create local file from URL.

    # param directory_path: (str) path to directory containing requirements.txt
    # return: (str) directory_path
    """
    file_path = None

    if not directory_path.endswith("requirements.txt"):
        file_path = directory_path + '/requirements.txt'
    else:
        file_path = directory_path

    # if the directory_path is a URL, download the file
    if file_path.startswith("http"):
        filename = os.path.basename(file_path)
        urllib.request.urlretrieve(file_path, filename)
        file_path = filename

    # currently only supporting local files and web URLs
    elif not os.path.isfile(directory_path):
        raise ValueError("Invalid directory path")

    if os.path.exists(file_path):
        return file_path
    else:
        raise ValueError("requirements.txt not found in directory")


def parse_requirements_file(file_path):
    """
    Parses the requirements file at the file_path given.

    # param file_path: (str) path to directory containing requirements.txt
    # re
    """
    packages = {}
    reqs = parse_requirements(file_path, session=False)

    for req in reqs:
        packages[req.name] = str(req.req)

    return packages


def compare_reqs():
    pass


def parse_args():
    pass


def main():
    # parse args
    compare_reqs()
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
