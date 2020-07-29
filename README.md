# tkpy

[Travian: Kingdom](https://www.kingdoms.com) utilities for your need.  
It provide several object that mostly used on Travian: Kingdom such as `Map`, `Villages`, `Notepad`, and `Farmlist`.  

[![PyPI version](https://badge.fury.io/py/tkpy.svg)](https://pypi.org/project/tkpy/) [![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-367/) [![Build Status](https://travis-ci.org/didadadida93/tkpy.svg?branch=master)](https://travis-ci.org/didadadida93/tkpy) [![codecov](https://codecov.io/gh/didadadida93/tkpy/branch/master/graph/badge.svg)](https://codecov.io/gh/didadadida93/tkpy) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## Table of Contents
* [Installation](https://github.com/didadadida93/tkpy#installation)
* [Getting started](https://github.com/didadadida93/tkpy#getting-started)
* [Usage](https://github.com/didadadida93/tkpy#usage)
    * [Map](https://github.com/didadadida93/tkpy#map)
    * [Villages](https://github.com/didadadida93/tkpy#villages)
    * [Farmlist](https://github.com/didadadida93/tkpy#farmlist)
    * [Notepad](https://github.com/didadadida93/tkpy#notepad)
* [Documentation](https://github.com/didadadida93/tkpy#documentation)
* [Disclaimer](https://github.com/didadadida93/tkpy#disclaimer)

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
grey_villages = list(m.gen_grey_villages()) # get all grey villages from map
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

If you want to slice map data based on the area of your interest, you can use `slice_map` method.
```python
sliced_map = m.slice_map(center=(0, 0), radius=5)

# now you can do the same thing as `Map` object
grey_villages = list(sliced_map.gen_grey_villages())
```

### Villages
Villages object is like built-in `dict` object from `Python` so you can access the village using its name as key. To get village data from Travian: Kingdom, you need to call `pull` method first.

```python
from tkpy import Villages

v = Villages(driver)
v.pull()

v['your first village']
<Village({'villageId': '537313245', 'playerId': '001', 'name': 'my first village',...})>
```

From `Villages` object you can get `Village` object and from this object you can do `send_attack`, `send_raid`, `send_defend`, `send_spy`, and `send_siege`.

> If you want to attack, you need to get troop enum from `tkpy`.

```python
from tkpy import RomanTroop # if you are a Roman tribe

first_village = v['your first village'] # get your first village object
units_siege = {RomanTroop.IMPERIAN: 1000, RomanTroop.BATTERING_RAM: 1} # prepare unit
units_attack = {RomanTroop.LEGIONNAIRE: 1000} # prepare unit
units_raid = {RomanTroop.EQUITES_IMPERATORIS: 50} # prepare unit
units_defend = {RomanTroop.PRAETORIAN: 1000} # prepare unit

first_village.send_siege(x=0, y=0, units=units_siege) # send siege
first_village.send_attack(x=0, y=0, units=units_attack) # send attack
first_village.send_raid(x=0, y=0, units=units_raid) # send raid
first_village.send_spy(x=0, y=0, amount=1) # send spy
first_village.send_defend(x=0, y=0, untis=unts_defend) # send defend
```

From `Village` object you can also upgrade building that on the village by using `upgrade` method. And if you want to construct building, you can use `construct` method.

> If you want to upgrade or construct building, you need to get building enum from `tkpy`.

```python
from tkpy import BuildingType

first_village = v['your first village'] # get your first village object
first_village.upgrade(building=BuildingType.MAIN_BUILDING) # upgrade main building
first_village.construct(buildng=BuildingType.WAREHOUSE) # construct warehouse
```

### Farmlist
`Farmlist` object is like built-in `dict` object from `Python` so you can access farmlist using its name as key. To get farmlist data from Travian: Kingdom, you need to call `pull` method first. From `Farmlist` you can create new farmlist by calling `create_farmlist`.

```python
from tkpy import Farmlist

f = Farmlist(driver)
f.pull()

f['Startup farm list']
<FarmlistEntry({'listId': '1631', 'listName': 'Startup farm list', ...})>

f.create_farmlist('new farmlist')
f['new farmlist']
<FarmlistEntry({'listId': '1632', 'listName': 'new farmlist', ...})>
```

From `Farmlist` object you can get `FarmlistEntry` object and from it you can add new village to the `FarmlistEntry`  and send this `FarmlistEntry`.

```python
f['Startup farm list'].add(villageId=536887296) # add village using village id to 'Startup farm list'
f['Startup farm list'].send(villageId=537051141) # send 'startup farm list' from village using village id
```

### Notepad
`Notepad` is an object that when instantiate will create new notepad in game. Use `message` method for write new message.

```python
from tkpy import Notepad

n = Notepad(driver) # new notepad will appear in game
n.message('this is new message on new notepad') # write message to the notepad

# careful, use `message` method will overwrite message previously on notepad
n.message('old message will be overwrited')
```

## Documentation
For documentation, you can go to this [wiki](https://github.com/didadadida93/tkpy/wiki).

## Disclaimer
_Please note that this is a research project, i am by no means responsible for any usage of this utilities._  
_Use on your own behalf, i am also not responsible if your accounts get banned due to extensive use of this utilites._
