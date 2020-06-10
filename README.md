# tkpy

[Travian: Kingdom](https://www.kingdoms.com) utilities for your need.  
It provide several object that mostly used on Travian: Kingdom such as `Map`, `Villages`, `Notepad`, and `Farmlist`.  

[![PyPI version](https://badge.fury.io/py/tkpy.svg)](https://pypi.org/project/tkpy/) [![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-367/) [![Build Status](https://travis-ci.org/didadadida93/tkpy.svg?branch=master)](https://travis-ci.org/didadadida93/tkpy) [![codecov](https://codecov.io/gh/didadadida93/tkpy/branch/master/graph/badge.svg)](https://codecov.io/gh/didadadida93/tkpy)  

## Installation

>It is recommended to use [virtualenv](https://docs.python-guide.org/dev/virtualenvs/) or any other similar virtual environment management for python.

Since `tkpy` depend on `primordial` package, first you need to install [primordial package](https://github.com/didadadida93/primordial).

```sh
pip install git+https://github.com/didadadida93/tkpy.git
```

## Getting started

`tkpy` need `Gameworld` object from `primordial` package so it can request data from Travian: Kingdom. Use `authenticate` function to retrieve `Gameworld` object.  

```python
from tkpy import authenticate

driver = authenticate(email='your@email.com', password='your password', gameworld='com12')
```  
