#!/usr/bin/env python3
import os
import urllib.request
from dataclasses import dataclass
from art import tprint

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
            return f'{self.name} {self.version_spec} {self.version}'
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

    return packages


def print_package(package, filepath):
    """
    Prints package information.

    :param package: (Package) package to print
    :param filepath: (str) filepath of package
    """
    print(f'{str(package).ljust(40)} - {filepath}')


def print_table(diff_packages, unique_packages, same_packages, show_diff_versions, show_unique, show_same):
    """
    Prints table of packages comparison results.

    :param diff_packages: (dict) packages with different versions
    :param unique_packages: (dict) packages unique to directory
    :param same_packages: (dict) packages with same versions
    :param show_diff_versions: (bool) show packages with different versions
    :param show_unique: (bool) show packages unique to directory
    :param show_same: (bool) show packages with same versions
    """
    tprint("Package Summary")
    print(f"Show Diff Package Versions: {show_diff_versions}")
    print(f"Show Unique Packages: {show_unique}")
    print(f"Show Shared Packages: {show_same}")
    print()

    if show_diff_versions:
        print("Packages with different versions across directories:")
        for filepath, package in diff_packages.items():
            print_package(package, filepath)
        print()
    if show_unique:
        print("Packages to specific directories:")
        for filepath, package in unique_packages.items():
            print_package(package, filepath)
        print()
    if show_same:
        print("Packages with same versions across directories:")
        for filepath, package in same_packages.items():
            print_package(package, filepath)
        print()


def compare_reqs(*directories, show_diff_versions=True, show_same=False, show_unique=False):
    """
    Compare requirements.txt files in directories.  More than 1 required for comparison.

    # param directories: (list) list of directories to compare
    # param show_diff_versions: (bool) show packages with different versions
    # param show_same: (bool) show packages with same versions
    # param show_unique: (bool) show packages unique to directory
    """
    if not directories:
        raise ValueError("No directories provided")
    elif len(directories) == 1:
        raise ValueError("Only one directory provided")

    filepaths = [establish_filepath(directory) for directory in directories]
    packages = {filepath: parse_requirements(filepath) for filepath in filepaths}

    # we want to track packages unique to each directory, differing by versions
    # in at least one directory, and packages that are the same across all
    unique_packages, diff_packages, same_packages = {}, {}, {}

    for idx, (filepath, package_set) in enumerate(packages.items()):
        # no other packages to compare to at this point
        if idx == len(packages) - 1:
            break

        for package in package_set:
            found = False
            # start from the next directory to compare to ensure comparisons only happen once
            for idx2, (filepath2, package_set2) in enumerate(packages.items(), idx + 1):
                for package2 in package_set2:
                    if package == package2:
                        found = True
                        same_packages[filepath] = package # TODO fix this assignment
                    elif package.name == package2.name:
                        found = True
                        diff_packages[filepath] = package
                    if found:
                        break

            if not found:
                unique_packages[filepath].append(package)

    print_table(diff_packages, unique_packages, same_packages, show_diff_versions, show_unique, show_same)
