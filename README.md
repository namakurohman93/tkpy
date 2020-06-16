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

## Usage
### Map

Map object is an object for keeping map data from Travian: Kingdom.  
To get map data from Travian: Kingdom, you need to call `pull` method.

```python
from tkpy import Map

m = Map(driver)
m.pull()
```

Once you call `pull` method, now you can get all tiles data using several method.

```python
all_villages = list(m.gen_villages()) # get all villages from map
abandoned_valleys = list(m.gen_abandoned_valley()) # get all unsettled tiles from map
oases = list(m.gen_oases()) # get all oases from map
```

Or if you want to get data from specific tile, you can use `coordinate` method.

```python
m.coordinate(0, 0)
<Cell({'id': '536887296', 'landscape': '9013', 'owner': '0'})>
```

When you call `pull` method, you also will get player data and kingdom data. Map object will keep this data and you can get player data or kingdom data using several method.

```python
player_list = list(m.gen_players()) # get all players
kingdom_list = list(m.gen_kingdoms()) # get all kingdoms
inactive_player_list = list(m.gen_inactive_players()) # get all inactive players
```

If you want to get data from specific player or kingdom, you can use `get_player` method and `get_kingdom` method.

```python
m.get_player('player name')
<Player({'name': 'player name', 'country': 'en', 'tribeId': '1', ...})>

m.get_kingdom('kingdom name')
<Kingdom({'tag': 'kingdom name', 'kingdomId': '9999'})>
```
