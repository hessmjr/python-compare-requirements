import os
import unittest
from compare_reqs import _establish_filepath, parse_requirements, compare_reqs


class TestEstablishFilepath(unittest.TestCase):

    def test_valid_requirements(self):

        # create a temp file called requirements.txt
        # write some requirements to it
        # call _establish_filepath on the temp file
        # assert that the return value is the temp file
        # delete the temp file
        tmp_file = 'tmp_requirements.txt'
        with open(tmp_file, 'w') as f:
            f.write('requests==2.22.0')
        self.assertEqual(_establish_filepath(tmp_file), tmp_file)
        os.remove(tmp_file)

    def test_missing_requirements(self):
        # assert that an exception is raised when the requirements.txt file is missing
        with self.assertRaises(ValueError):
            _establish_filepath('not_here_requirements.txt')

    def test_http_url(self):
        filepath = _establish_filepath(
            'https://github.com/numpy/numpy/blob/main/build_requirements.txt'
        )
        self.assertEqual(filepath, 'build_requirements.txt')
        os.remove(filepath)


# TODO
# write a test suite for parse_requirements
# a test with requirements full of various package requirements
class TestParseRequirements(unittest.TestCase):

    def test_parse_requirements(self):
        # create a temp file called requirements.txt
        # write some requirements to it
        # call parse_requirements on the temp file
        # assert that the return value is a tuple of packages
        # delete the temp file
        tmp_file = 'tmp_requirements.txt'
        with open(tmp_file, 'w') as f:
            f.write('requests==2.22.0')
        self.assertIsInstance(parse_requirements(tmp_file), tuple)
        os.remove(tmp_file)


# write a test suite for compare_req function with:
# write a test with zero files
# write a test with one file
# write a test with two files, all 3 types of packages
# write a test with three files, all 3 types of packages
