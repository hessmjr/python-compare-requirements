#!/usr/bin/env python3
import os
import urllib.request
from collections import defaultdict
from dataclasses import dataclass

from art import tprint
from packaging import version

__version__ = '0.1.0'
__date__ = '2023-01-16'
__author__ = 'Mark Hess'
__licence__ = 'BSD'

REQUIREMENTS_TXT = 'requirements.txt'
REQUIREMENTS = 'requirements'

# For the dependency identifier specification, see
# https://www.python.org/dev/peps/pep-0508/#complete-grammar
# https://www.python.org/dev/peps/pep-0440/#version-specifiers
# arbitrary equality operator is ignored at this time
SPECIFIERS = ["<", ">", "=", "!", "~"]


@dataclass(frozen=True)
class Package:
    name: str
    version: str = None
    version_spec: str = None

    def __str__(self):
        if self.version_spec and self.version:
            return f'{self.name} {self.version_spec} {self.version}'
        return self.name

    def _can_compare(self, other):
        if not isinstance(other, Package):
            raise TypeError(f'Cannot compare {type(self)} with {type(other)}')

    def __ne__(self, other):
        self._can_compare(other)
        return self.name != other.name or \
            self.version != other.version or \
            self.version_spec != other.version_spec

    def __eq__(self, other):
        self._can_compare(other)
        return self.name == other.name and \
            self.version == other.version and \
            self.version_spec == other.version_spec

    def __gt__(self, other):
        self._can_compare(other)

        if self.name != other.name:
            return self.name > other.name

        if not all((self.version, other.version)):
            if self.version is None and other.version is not None:
                return True
        else:
            self_version_parsed = version.parse(self.version)
            other_version_parsed = version.parse(other.version)
            if self_version_parsed != other_version_parsed:
                return self_version_parsed > other_version_parsed

            if self.version_spec != other.version_spec:
                return self.version_spec > other.version_spec

        return False

    def __lt__(self, other):
        return not self >= other

    def __ge__(self, other):
        return self > other or self == other

    def __le__(self, other):
        return self < other or self == other


def _establish_filepath(directory_path):
    """
    Get file path from local file system or create local file from URL.

    # param directory_path: (str) path to directory containing requirements.txt
    # return: (str) directory_path
    """
    if REQUIREMENTS not in directory_path.lower():
        file_path = os.path.join(directory_path, REQUIREMENTS_TXT)
    else:
        file_path = directory_path

    if file_path.startswith("http"):
        filename = os.path.basename(file_path)
        urllib.request.urlretrieve(file_path, filename)
        file_path = filename

    # currently only supporting local files and web URLs
    elif not os.path.exists(file_path):
        raise ValueError(f"Invalid directory path {file_path}")

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

    for package_str in data:
        deliminated = False

        for idx, char in enumerate(package_str):
            # only care about specifier characters to split on
            if char in SPECIFIERS:
                deliminated = True
                # in the case there is additional '=' in the specifier
                # no long a 'char' but just semantics at this point
                if package_str[idx + 1] in SPECIFIERS:
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


def _compare_reqs(*directories):
    """
    Compare requirements.txt files in directories.  More than 1 required for comparison.
    Setup as internal function to allow for easier testing.

    # param directories: (list) list of directories to compare
    # return: (tuple) tuple of package results
    """
    if not directories:
        raise ValueError("No directories provided")
    elif len(directories) == 1:
        raise ValueError("Only one directory provided")

    filepaths = [_establish_filepath(directory) for directory in directories]
    packages = {filepath: parse_requirements(filepath) for filepath in filepaths}

    # we want to track packages unique to each directory, differing by versions
    # in at least one directory, and packages that are the same across all
    unique_packages = defaultdict(list)
    diff_packages = defaultdict(list)
    same_packages = defaultdict(list)

    for filepath, package_set in packages.items():
        for package in package_set:
            found, is_same_package = False, False

            for filepath2, package_set2 in packages.items():
                if filepath == filepath2:
                    continue

                # compare package to all packages in this directory by searching for
                # exact match or different version, if exact match continue keep
                # searching for different version but if different version then stop
                # and add to diff_packages, if neither easily can assume unique
                for package2 in package_set2:
                    if package == package2:
                        found = True
                        is_same_package = True
                    elif package.name == package2.name:
                        found = True
                        is_same_package = False
                        diff_packages[package].append(filepath)
                        break

                # if we found a match but it was a different version
                # then no reason to keep looking
                if found and not is_same_package:
                    break

            if found and is_same_package:
                same_packages[package].append(filepath)
            elif not found:
                unique_packages[package].append(filepath)

    return diff_packages, unique_packages, same_packages


def _print_table(diff_packages, unique_packages, same_packages, show_diff_versions,
                 show_unique, show_same, remove_spaces):
    """
    Prints table of packages comparison results.

    :param diff_packages: (dict) packages with different versions
    :param unique_packages: (dict) packages unique to directory
    :param same_packages: (dict) packages with same versions
    :param show_diff_versions: (bool) show packages with different versions
    :param show_unique: (bool) show packages unique to directory
    :param show_same: (bool) show packages with same versions
    :param remove_spaces: (bool) remove spaces from package versions
    """
    tprint("Package  Comparison", font="small")
    print(f"Show Diff Package Versions:   {show_diff_versions}")
    print(f"Show Unique Packages:         {show_unique}")
    print(f"Show Shared Packages:         {show_same}")
    print()

    if show_diff_versions:
        print("Packages with different versions across directories:")
        sorted_packages = sorted(diff_packages.items(), key=lambda x: (x[0].name, x[0].version))
        for package, filepaths in sorted_packages:
            for filepath in filepaths:
                package_str = str(package)
                if remove_spaces:
                    package_str = str(package).replace(" ", "")
                print(f'{package_str.ljust(30)} - {filepath}')
        print()

    if show_unique:
        print("Packages only found in a specific directory:")
        sorted_packages = sorted(unique_packages.items(), key=lambda x: x[0].name)
        for package, filepaths in sorted_packages:
            package_str = str(package)
            if remove_spaces:
                package_str = package_str.replace(" ", "")
            print(f'{package_str.ljust(30)} - {filepaths[0]}')
        print()

    if show_same:
        print("Packages with same versions across directories:")
        sorted_packages = sorted(same_packages.items(), key=lambda x: x[0].name)
        for package, filepaths in sorted_packages:
            package_str = str(package)
            if remove_spaces:
                package_str = package_str.replace(" ", "")
            print(f'{package_str}')
        print()


def compare_reqs(*directories, show_diff_versions=True, show_same=False, show_unique=False, remove_spaces=False):
    """
    Prints table of packages comparison results.

    # param directories: (list) list of directories to compare
    # param show_diff_versions: (bool) show packages with different versions
    # param show_same: (bool) show packages with same versions
    # param show_unique: (bool) show packages unique to directory
    # param remove_spaces: (bool) remove spaces from package versions
    """
    try:
        diff_packages, unique_packages, same_packages = _compare_reqs(*directories)

        # split internal and public methods to allow for testing and utilize this method to print
        _print_table(diff_packages, unique_packages, same_packages, show_diff_versions,
                     show_unique, show_same, remove_spaces)
    except ValueError as e:
        raise e
    except Exception as e:
        print(e)
        return False

    return True
