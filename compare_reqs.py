#!/usr/bin/env python3
import os
import urllib.request
from dataclasses import dataclass


__version__ = '0.1.0'
__date__ = '2023-01-16'
__author__ = 'Mark Hess'
__licence__ = 'BSD'


REQUIREMENTS_TXT = 'requirements.txt'


@dataclass(frozen=True)
class Package:
    name: str
    version: str = None
    version_spec: str = None

    def __str__(self):
        if self.version_spec and self.version:
            return f'{self.name}{self.version_spec}{self.version}'
        return self.name

    def __ne__(self, other):
        if isinstance(other, Package):
            return self.name != other.name \
                or self.version != other.version \
                or self.version_spec != other.version_spec

    def __eq__(self, other):
        if isinstance(other, Package):
            return self.name == other.name \
                and self.version == other.version \
                and self.version_spec == other.version_spec


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


def parse_requirements(filepath):
    """
    Parse requirements.txt file and return list of packages.  Performs only
    basic parsing of requirements.txt file.  Does not support all features
    and formats.

    # param filepath: (str) path to requirements.txt file
    # return: (tuple) tuple of packages
    """
    with open(filepath, 'r') as f:
        data = []
        for line in f.readlines():
            if line != '\n' and line[0].isalpha():
                data.append(line.strip())

    packages = set([])
    # For the dependency identifier specification, see
    # https://www.python.org/dev/peps/pep-0508/#complete-grammar
    delim = ["<", ">", "=", "!", "~"]

    for package_str in data:
        deliminated = False

        for idx, char in enumerate(package_str):
            # only care about delimiters characters to split on
            if char in delim:
                deliminated = True
                # in the case there is additional '=' in the specifier
                # no long a 'char' but just semantics at this point
                if package_str[idx + 1] in delim:
                    char = char + package_str[idx + 1]

                module = package_str.split(char)
                module_data = {'name': module[0]}
                if len(module) > 1:
                    module_data.update({
                        'version_spec': char,
                        'version': module[1],
                    })

                packages.add(Package(**module_data))
                break

        # Check for modules w/o a specifier.
        if not deliminated:
            packages.add(Package(name=package_str))

    return tuple(packages)


def compare_reqs():
    # print packages that are same
    # print packages that are unique
    # print packages that are different versions
    pass
