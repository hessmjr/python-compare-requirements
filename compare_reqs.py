#!/usr/bin/env python3
import os
import pathlib
import urllib.request

import pkg_resources


__version__ = '0.1.0'
__date__ = '2023-01-16'
__author__ = 'Mark Hess'
__licence__ = 'BSD'


REQUIREMENTS_TXT = 'requirements.txt'


def establish_filepath(directory_path):
    """
    Get file path from local file system or create local file from URL.

    # param directory_path: (str) path to directory containing requirements.txt
    # return: (str) directory_path
    """
    if not directory_path.endswith(REQUIREMENTS_TXT):
        file_path = os.path.join(directory_path, REQUIREMENTS_TXT)
    else:
        file_path = directory_path

    if file_path.startswith("http"):
        filename = os.path.basename(file_path)
        urllib.request.urlretrieve(file_path, filename)
        file_path = filename

    # currently only supporting local files and web URLs
    elif not os.path.exists(file_path):
        raise ValueError("Invalid directory path")

    if os.path.isfile(file_path):
        return file_path
    else:
        raise ValueError("requirements.txt not found in directory")


def parse_requirements_file(file_path):
    """

    :param file_path:
    :return:
    """
    packages = []
    with pathlib.Path(file_path).open() as requirements_txt:
        packages.append(pkg_resources.parse_requirements(requirements_txt))
    return packages


def compare_reqs():
    pass
