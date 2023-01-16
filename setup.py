from setuptools import setup, find_packages

setup(
    name='my_project',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pipreqs==0.4.9',
    ],
    entry_points={
        'console_scripts': [
            'my_project=my_project.__main__:main'
        ]
    },
    author='Your Name',
    author_email='your_email@example.com',
    description='A tool for comparing 2 or more requirements files',
    keywords='requirements comparison tool'
)

# The setup() function is used to configure the package for distribution and installation.
# The name and version fields are used to specify the package name and version number, respectively.
# The packages field is used to specify the packages that should be included in the distribution.
# In this case, we're using find_packages() to automatically discover all the packages
