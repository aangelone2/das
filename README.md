# `das`

![test](https://img.shields.io/badge/Tests-Passing-32CD32)
[![numpy](https://img.shields.io/badge/numpy-FF0000)](https://numpy.org)
[![rich](https://img.shields.io/badge/rich-FF0000)](https://github.com/Textualize/rich)
[![testing](https://img.shields.io/badge/testing-pytest-blue)](https://github.com/pytest-dev/pytest)
[![pylint](https://img.shields.io/badge/linting-pylint-blue)](https://github.com/pylint-dev/pylint)
[![black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![poetry](https://img.shields.io/badge/build-poetry-blue)](https://github.com/python-poetry/poetry)
[![mkdocs](https://img.shields.io/badge/documentation-mkdocs-blue)](https://github.com/mkdocs/mkdocs)


`das` (Data Analysis Suite) is a simple Python utility
for the analysis of (Monte Carlo) data.




## Dependencies and Setup

`das` is packaged with `poetry`: the command

```
$ poetry install
```

will setup a virtual environment will all required
dependencies. The command

```
$ poetry --directory <project directory> run das <arguments>
```

(`--directory ...` is optional if within the project
directory already) will execute the program.




## Current capabilities

The capabilities of `das` are programmed in *drivers*,
subcommands specialized for a specific task, and
include:

- Simple averaging and analysis of uncorrelated data
  (`avs`);
- Binsize scaling to compute accurate errors for
  correlated data (`ave`);
- Jackknife estimation of errors for mean value
  functionals (`jck`).

A list of available drivers, together with the
instructions for the main command, can be displayed as

```
$ poetry --directory=<project directory> run das -h
usage: das [-h] [--version] {avs,ave,jck} ...

positional arguments:
  {avs,ave,jck}

options:
  -h, --help     show this help message and exit
  --version      display version number and exit
```

Each driver is invoked as

```
$ das <driver> <arguments>
```

Executing the driver with no arguments will display a
help message.




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

generate the documentation, which can be browsed at the
URL [http://localhost:8000](http://localhost:8000).

Most of the documentation (including all the information
related to the UI and the statistical background) can be
consulted on the [github
wiki](https://github.com/aangelone2/das/wiki).
