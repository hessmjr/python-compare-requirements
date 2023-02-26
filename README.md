# Python Compare Requirements
Python Compare Requirements is a Python package that compares two or more `requirements.txt` files and outputs the differences between them. It is a useful tool for developers and project managers who need to keep track of the dependencies of multiple projects.

## Usage
Python Compare Requirements can be used as a Python console command or as a Python module.  Example:

```python
from compare_reqs import compare_reqs

requirements = 'requirements.txt'
requirements2 = 'https://raw.githubusercontent.com/psf/requests/master/requirements.txt'
compare_reqs(requirements, requirements2)

requirements3 = 'path/to/requirements.txt'
compare_reqs(requirements, requirements2, requirements3)
```

## License
Requirements Comparator is licensed under the BSD 3-Clause "New" or "Revised" License. See the LICENSE file for more details.

## Contributing
Contributions are welcome! If you would like to contribute to Requirements Comparator, please create a pull request on GitHub.
