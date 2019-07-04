# tkpy
travian kingdom utilities for your need.


[![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-367/) [![Build Status](https://travis-ci.org/didadadida93/tkpy.svg?branch=master)](https://travis-ci.org/didadadida93/tkpy) [![codecov](https://codecov.io/gh/didadadida93/tkpy/branch/master/graph/badge.svg)](https://codecov.io/gh/didadadida93/tkpy)



---
## Installation
1. install [primordial package](https://github.com/lijok/primordial)
2. git clone [this repo](https://github.com/didadadida93/tkpy.git)
3. change directory to tkpy
4. run `pip3 install -r requirements.txt`
4. enjoy

---
## Basic usage
```
>>> from tkpy.utilities import login
>>>
>>> driver = login(email='your@email.com', password='your password', gameworld='com12')
>>>
>>> # login as sitter or dual
...
>>> driver = login(email='your@email.com', password='your password', gameworld='dual/sitter gameworld', avatar='avatar name of sitter/dual account')
>>>
>>> from tkpy.notepads import Notepad
>>>
>>> n = Notepad(driver) # this will create in-game notepad
>>> n.message('your message') # this will write message to notepad
>>>
>>> from tkpy.map import Map
>>>
>>> m = Map(driver)
>>> m.pull() # pulling map data
...
>>> m.coordinate(0, 0)
{'id': '536887296', 'landscape': '9013', 'owner': '0'}
>>>
>>> unoccupied_oasis_list = [oasis for oasis in m.oasis if oasis['oasis']['oasisStatus'] == '3']
>>> unoccupied_oasis_list[0]
{'id': '535019499', 'landscape': '2755', 'owner': '0', 'oasis': {'bonus': {'1': 0, '2': 25, '3': 0, '4': 25}, 'units': [], 'type': '21', 'oasisStatus': '3', 'kingdomId': '0', 'kingId': '0'}}
```

---
### Features
[click here](https://github.com/didadadida93/tkpy/tree/master/features) to see some features that i've been created
