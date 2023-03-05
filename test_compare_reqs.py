import os
import unittest
from compare_reqs import _establish_filepath, parse_requirements, _compare_reqs


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


class TestParseRequirements(unittest.TestCase):

    def test_parse_requirements(self):
        tmp_file = 'tmp_requirements.txt'
        with open(tmp_file, 'w') as f:
            f.write('requests==2.22.0' + '\n')
            f.write('numpy>1.19.2' + '\n')
            f.write('pandas' + '\n')
            f.write('matplotlib~=3.3.2' + '\n')

        parsed_reqs = parse_requirements(tmp_file)
        os.remove(tmp_file)

        self.assertIsInstance(parsed_reqs, tuple)
        self.assertEqual(len(parsed_reqs), 4)

        parsed_reqs = sorted(parsed_reqs)
        self.assertEqual(parsed_reqs[0].name, 'matplotlib')
        self.assertEqual(parsed_reqs[0].version_spec, '~=')
        self.assertEqual(parsed_reqs[0].version, '3.3.2')
        self.assertEqual(parsed_reqs[1].name, 'numpy')
        self.assertEqual(parsed_reqs[1].version_spec, '>')
        self.assertEqual(parsed_reqs[1].version, '1.19.2')
        self.assertEqual(parsed_reqs[2].name, 'pandas')
        self.assertIsNone(parsed_reqs[2].version_spec)
        self.assertIsNone(parsed_reqs[2].version)
        self.assertEqual(parsed_reqs[3].name, 'requests')
        self.assertEqual(parsed_reqs[3].version_spec, '==')
        self.assertEqual(parsed_reqs[3].version, '2.22.0')


class TestCompareReqs(unittest.TestCase):

    def test_zero_directories(self):
        # Test calling _compare_reqs with zero directories
        with self.assertRaises(ValueError):
            _compare_reqs([])

    def test_one_directory(self):
        # Test calling _compare_reqs with one directory
        with self.assertRaises(ValueError):
            _compare_reqs(['directory'])

    def test_two_files_with_all_package_comparisons(self):
        tmp_file1 = 'tmp_requirements1.txt'
        with open(tmp_file1, 'w') as f:
            f.write('requests==2.22.0' + '\n')
            f.write('numpy>=1.22.2' + '\n')
            f.write('pandas==1.1.3' + '\n')
            f.write('matplotlib==3.3.2' + '\n')
            f.write('scipy==1.5.2' + '\n')
            f.write('seaborn==0.7.0' + '\n')
            f.write('beautifulsoup4==4.9.3' + '\n')
            f.write('selenium==3.141.0' + '\n')

        tmp_file2 = 'tmp_requirements2.txt'
        with open(tmp_file2, 'w') as f:
            f.write('requests==2.22.0' + '\n')
            f.write('numpy==1.19.2' + '\n')
            f.write('pandas' + '\n')
            f.write('matplotlib==3.3.2' + '\n')
            f.write('scipy==1.5.2' + '\n')
            f.write('seaborn==0.11.0' + '\n')
            f.write('scikit-learn==0.23.2' + '\n')
            f.write('scikit-image==0.17.2' + '\n')
            f.write('scikit-optimize==0.8.1' + '\n')
            f.write('scikit-surprise==1.1.1' + '\n')

        diff_packages, unique_packages, same_packages = _compare_reqs(tmp_file1, tmp_file2)
        os.remove(tmp_file1)
        os.remove(tmp_file2)

        self.assertEqual(len(diff_packages), 6)
        self.assertEqual(len(unique_packages), 6)
        self.assertEqual(len(same_packages), 3)

        diff_packages = [(package, filenames) for package, filenames in diff_packages.items()]
        diff_packages = sorted(diff_packages, key=lambda x: x[0])

        self.assertEqual(diff_packages[0][0].name, 'numpy')
        self.assertEqual(diff_packages[0][1], ['tmp_requirements2.txt'])
        self.assertEqual(diff_packages[1][0].name, 'numpy')
        self.assertEqual(diff_packages[1][1], ['tmp_requirements1.txt'])
        self.assertEqual(diff_packages[2][0].name, 'pandas')
        self.assertEqual(diff_packages[2][1], ['tmp_requirements1.txt'])
        self.assertEqual(diff_packages[3][0].name, 'pandas')
        self.assertEqual(diff_packages[3][1], ['tmp_requirements2.txt'])
        self.assertEqual(diff_packages[4][0].name, 'seaborn')
        self.assertEqual(diff_packages[4][1], ['tmp_requirements1.txt'])
        self.assertEqual(diff_packages[5][0].name, 'seaborn')
        self.assertEqual(diff_packages[5][1], ['tmp_requirements2.txt'])

        unique_packages = [(package, filenames) for package, filenames in unique_packages.items()]
        unique_packages = sorted(unique_packages, key=lambda x: x[0])

        self.assertEqual(unique_packages[0][0].name, 'beautifulsoup4')
        self.assertEqual(unique_packages[0][1], ['tmp_requirements1.txt'])
        self.assertEqual(unique_packages[1][0].name, 'scikit-image')
        self.assertEqual(unique_packages[1][1], ['tmp_requirements2.txt'])
        self.assertEqual(unique_packages[2][0].name, 'scikit-learn')
        self.assertEqual(unique_packages[2][1], ['tmp_requirements2.txt'])
        self.assertEqual(unique_packages[3][0].name, 'scikit-optimize')
        self.assertEqual(unique_packages[3][1], ['tmp_requirements2.txt'])
        self.assertEqual(unique_packages[4][0].name, 'scikit-surprise')
        self.assertEqual(unique_packages[4][1], ['tmp_requirements2.txt'])
        self.assertEqual(unique_packages[5][0].name, 'selenium')
        self.assertEqual(unique_packages[5][1], ['tmp_requirements1.txt'])

        for package, filenames in same_packages.items():
            self.assertEqual(len(filenames), 2)

    def test_three_files_with_all_package_comparisons(self):
        tmp_file1 = 'tmp_requirements1.txt'
        with open(tmp_file1, 'w') as f:
            f.write('beautifulsoup4==4.9.3' + '\n')
            f.write('matplotlib==3.3.2' + '\n')
            f.write('numpy>=1.22.2' + '\n')
            f.write('pandas==1.1.3' + '\n')
            f.write('requests==2.22.0' + '\n')
            f.write('scipy==1.5.2' + '\n')
            f.write('seaborn==0.7.0' + '\n')
            f.write('selenium==3.141.0' + '\n')

        tmp_file2 = 'tmp_requirements2.txt'
        with open(tmp_file2, 'w') as f:
            f.write('matplotlib==3.3.2' + '\n')
            f.write('numpy==1.19.2' + '\n')
            f.write('pandas' + '\n')
            f.write('requests==2.22.0' + '\n')
            f.write('scipy==1.5.2' + '\n')
            f.write('scikit-learn==0.23.2' + '\n')
            f.write('scikit-image==0.17.2' + '\n')
            f.write('scikit-optimize==0.8.1' + '\n')
            f.write('scikit-surprise==1.1.1' + '\n')
            f.write('seaborn==0.11.0' + '\n')

        tmp_file3 = 'tmp_requirements3.txt'
        with open(tmp_file3, 'w') as f:
            f.write('beautifulsoup4==3.0.0' + '\n')
            f.write('matplotlib==3.3.2' + '\n')
            f.write('numpy==1.19.2' + '\n')
            f.write('pandas==1.0.0' + '\n')
            f.write('pytorch==1.7.1' + '\n')
            f.write('requests==2.22.0' + '\n')
            f.write('scikit-learn==0.23.2' + '\n')
            f.write('seaborn==0.11.0' + '\n')

        requiresments = [tmp_file1, tmp_file2, tmp_file3]
        diff_packages, unique_packages, same_packages = _compare_reqs(*requiresments)

        os.remove(tmp_file1)
        os.remove(tmp_file2)
        os.remove(tmp_file3)

        self.assertEqual(len(diff_packages), 9)
        self.assertEqual(len(unique_packages), 5)
        self.assertEqual(len(same_packages), 4)

        diff_packages = [(package, filenames) for package, filenames in diff_packages.items()]
        diff_packages = sorted(diff_packages, key=lambda x: x[0])

        self.assertEqual(diff_packages[0][0].name, 'beautifulsoup4')
        self.assertEqual(diff_packages[0][1], ['tmp_requirements3.txt'])
        self.assertEqual(diff_packages[1][0].name, 'beautifulsoup4')
        self.assertEqual(diff_packages[1][1], ['tmp_requirements1.txt'])
        self.assertEqual(diff_packages[2][0].name, 'numpy')
        self.assertEqual(diff_packages[2][1], ['tmp_requirements2.txt', 'tmp_requirements3.txt'])
        self.assertEqual(diff_packages[3][0].name, 'numpy')
        self.assertEqual(diff_packages[3][1], ['tmp_requirements1.txt'])
        self.assertEqual(diff_packages[4][0].name, 'pandas')
        self.assertEqual(diff_packages[4][1], ['tmp_requirements3.txt'])
        self.assertEqual(diff_packages[5][0].name, 'pandas')
        self.assertEqual(diff_packages[5][1], ['tmp_requirements1.txt'])
        self.assertEqual(diff_packages[6][0].name, 'pandas')
        self.assertEqual(diff_packages[6][1], ['tmp_requirements2.txt'])
        self.assertEqual(diff_packages[7][0].name, 'seaborn')
        self.assertEqual(diff_packages[7][1], ['tmp_requirements1.txt'])
        self.assertEqual(diff_packages[8][0].name, 'seaborn')
        self.assertEqual(diff_packages[8][1], ['tmp_requirements2.txt', 'tmp_requirements3.txt'])

        unique_packages = [(package, filenames) for package, filenames in unique_packages.items()]
        unique_packages = sorted(unique_packages, key=lambda x: x[0])

        self.assertEqual(unique_packages[0][0].name, 'pytorch')
        self.assertEqual(unique_packages[0][1], ['tmp_requirements3.txt'])
        self.assertEqual(unique_packages[1][0].name, 'scikit-image')
        self.assertEqual(unique_packages[1][1], ['tmp_requirements2.txt'])
        self.assertEqual(unique_packages[2][0].name, 'scikit-optimize')
        self.assertEqual(unique_packages[2][1], ['tmp_requirements2.txt'])
        self.assertEqual(unique_packages[3][0].name, 'scikit-surprise')
        self.assertEqual(unique_packages[3][1], ['tmp_requirements2.txt'])
        self.assertEqual(unique_packages[4][0].name, 'selenium')
        self.assertEqual(unique_packages[4][1], ['tmp_requirements1.txt'])

        same_packages = [(package, filenames) for package, filenames in same_packages.items()]
        same_packages = sorted(same_packages, key=lambda x: x[0])

        self.assertEqual(same_packages[0][0].name, 'matplotlib')
        self.assertEqual(same_packages[0][1], [
            'tmp_requirements1.txt',
            'tmp_requirements2.txt',
            'tmp_requirements3.txt',
        ])
        self.assertEqual(same_packages[1][0].name, 'requests')
        self.assertEqual(same_packages[1][1], [
            'tmp_requirements1.txt',
            'tmp_requirements2.txt',
            'tmp_requirements3.txt',
        ])
        self.assertEqual(same_packages[2][0].name, 'scikit-learn')
        self.assertEqual(same_packages[2][1], ['tmp_requirements2.txt', 'tmp_requirements3.txt'])
        self.assertEqual(same_packages[3][0].name, 'scipy')
        self.assertEqual(same_packages[3][1], ['tmp_requirements1.txt', 'tmp_requirements2.txt'])
