# https://github.com/alsur/compare-requirements

import os
from typing import List, Dict
from pkg_resources import Requirement, working_set


def compare_requirements(directories: List[str]) -> None:
    reqs = {}
    unique_reqs = {}
    different_versions = {}
    for directory in directories:
        reqs[directory] = [str(req) for req in working_set]
        unique_reqs[directory] = set()
        different_versions[directory] = set()

    for i in range(len(directories) - 1):
        req_set_1 = set(reqs[directories[i]])
        req_set_2 = set(reqs[directories[i + 1]])

        unique_reqs[directories[i]] |= req_set_1 - req_set_2
        unique_reqs[directories[i + 1]] |= req_set_2 - req_set_1
        different_versions[directories[i]] |= req_set_1 & req_set_2

    for directory in directories:
        print(f"Packages unique to {directory}: {unique_reqs[directory]}")
        print(f"Packages with different versions: {different_versions[directory]}")
