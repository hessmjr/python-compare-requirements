from setuptools import setup, find_packages

install_requires = [
    'pip',
    'setuptools',
    'art',
    'packaging',
]

setup(
    name='python-compare-requirements',
    version='0.1.0',
    packages=find_packages(),
    install_requires=install_requires,
    author='Mark Hess',
    description='A tool for comparing 2 or more requirements files',
    keywords='python requirements comparison tool'
)
