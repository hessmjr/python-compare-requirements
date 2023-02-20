# Python Requirements Diff
Compares, or diffs, requirements files between multiple python requirements.

TODO
- finilze the readme
- add branch protection
- add action to run tests in github

my_project/
├── src/
│   ├── my_project/
│   │   ├── __init__.py
│   │   ├── core.py
│   │   ├── commands/
│   │   │   ├── __init__.py
│   │   │   ├── command1.py
│   │   │   └── command2.py
│   ├── __main__.py
├── scripts/
│   ├── my_project.sh
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   ├── test_commands/
│   │   ├── __init__.py
│   │   ├── test_command1.py
│   │   └── test_command2.py
├── requirements.txt
├── README.md
└── setup.py

This structure separates the code for the command line interface and the core functionality, and also separates the tests, which is a good practice. It also provides a clear entry point for the script, which is the __main__.py file, and it also separates the different commands in different modules inside the commands package.
It's worth mentioning that this is just one possible structure, and it may not be the best fit for every project, but it serves as a general guideline that can be adapted to suit the needs of your specific project.
Please let me know if you have any questions, or if you need more help.


what else
Include a requirements.txt file: This file should list all the dependencies of your project, so that other users can easily install them using pip install -r requirements.txt.

Provide clear usage instructions: You should provide clear instructions on how to use the tool, including any command line arguments or options that it accepts. This information can be included in a README.md file in the root of the project.

Make the package available for distribution: Use tools like PyPI(Python Package Index) or other platforms like GitHub Releases to distribute your package
