# `das`

![test](https://img.shields.io/badge/Tests-Passing-32CD32)
[![numpy](https://img.shields.io/badge/numpy-FF0000)](https://numpy.org)
[![rich](https://img.shields.io/badge/rich-FF0000)](https://github.com/Textualize/rich)
[![testing](https://img.shields.io/badge/testing-pytest-blue)](https://github.com/pytest-dev/pytest)
[![pylint](https://img.shields.io/badge/linting-pylint-blue)](https://github.com/pylint-dev/pylint)
[![black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![poetry](https://img.shields.io/badge/build-poetry-blue)](https://github.com/python-poetry/poetry)
[![mkdocs](https://img.shields.io/badge/documentation-mkdocs-blue)](https://github.com/mkdocs/mkdocs)


`das` (Data Analysis Suite) is a simple Python utility for the
analysis of (Monte Carlo) data.




## Current capabilities

- Simple averaging and analysis of uncorrelated data
- Binsize scaling to compute accurate errors for correlated
  data




## Dependencies and Setup

`das` is packaged with `poetry`: the command

```
$ poetry install
```

will setup a virtual environment will all required
dependencies. The command

```
$ poetry run python -m modules.main <arguments>
```

or a call to the launch bash script

```
$ ./das <arguments>
```

will execute the program.




## Documentation

The commands

```
$ poetry run mkdocs build
$ poetry run mkdocs serve
```

or

```
$ make docs
```

generate the documentation, which can be browsed at the URL
[http://localhost:8000](http://localhost:8000).
