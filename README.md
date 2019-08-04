---  
# tkpy

[Travian: Kingdom](https://www.kingdoms.com) (TK) utilities for your need. It provide several object that mostly used on TK such as `Map`, `Villages`, `Notepad`, and `Farmlist`.  

[![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-367/) [![Build Status](https://travis-ci.org/didadadida93/tkpy.svg?branch=master)](https://travis-ci.org/didadadida93/tkpy) [![codecov](https://codecov.io/gh/didadadida93/tkpy/branch/master/graph/badge.svg)](https://codecov.io/gh/didadadida93/tkpy)  

---  
# Installation  
>It is recommended to use [virtualenv](https://docs.python-guide.org/dev/virtualenvs/).  

Since `tkpy` depend on `primordial` package, first install [primordial package](https://github.com/lijok/primordial).  
Then install `tkpy.`
```sh
(venv)$ pip install git+https://github.com/lijok/primordial.git

(venv)$ pip install tkpy
```  
---  
# Basic usage  
`tkpy` need `Gameworld` object so it can get data from TK. Use `login` function for retrieve `Gameworld` object.  
```python
from tkpy import login

driver = login(email='your@email.com', password='your password', gameworld='com12')

# login as sitter or dual
driver = login(
    email='your@email.com',
    password='your password',
    gameworld='dual/sitter gameworld',
    avatar='avatar name of sitter/dual account'
)

# once you have `Gameworld` object, you can use another object of tkpy.

from tkpy import Map

m = Map(driver)
m.pull() # pulling map data

m.coordinate(0, 0)
<Cell({'id': '536887296', 'landscape': '9013', 'owner': '0'})>

unoccupied_oasis_list = [oasis for oasis in m.oasis if oasis['oasis']['oasisStatus'] == '3']
unoccupied_oasis_list[0]
<Cell({'id': '535019499', 'landscape': '2755', 'owner': '0', 'oasis': {'bonus': {'1': 0, ...}, ...}...})>

```  
---  
# Usage  
## Map  
  * `Map` object provide you an easy way to access data from TK map by using `pull` method.

  ```python
  from tkpy import Map

  m = Map(driver)
  m.pull()
  ```

  * Once you pulling map data, you can access every cell by using `coordinate` method.

  ```python
  m.coordinate(0, 0)
  <Cell({'id': '536887296', 'landscape': '9013', 'owner': '0'})>
  ```

  * Since TK provide you player data, and kingdom data when you pulling map data, `Map` object also provide you easy way to access this kind of data.

  ```python
  m.player('player name')
  <Player({'name': 'player name', 'country': 'en', 'tribeId': '1', ...})>

  m.kingdom('kingdom name')
  <Kingdom({'tag': 'kingdom name', 'kingdomId': '9999'})>
  ```

  * `Map` object have property that act as generator function and yield `Cell` object so you can get all data from every cell.

  ```python
  cell_list = list(m.cell)
  ```  
  > Side note for `Map.cell` property:  
  > Some `Cell` object have different data. Once with village data while another didn't have village data.  
  > Finding specific cell through `Map.cell` property may cause `KeyError Exception`. To prevent this use `try except` clause.
  >
  > ```python
  > for cell in m.cell:
  >     try:
  >         village = cell['village']
  >     except KeyError: # this cell didn't have village data
  >         continue
  >     ...
  > ```

  * `Map` object also have property that filter cell data so it only give specific data.

  ```python
  # make a list of cell that have village data on it
  villages = list(m.villages)

  # make a list of cell that have oasis data on it
  oasis = list(m.oasis)

  # make a list of cell that have 15c and 9c but didn't have village data on it (unsettled croppers)
  croppers = [tile for tile in m.tiles if tile['resType'] == '3339' or tile['resType'] == '11115']

  # make a list of cell that have village data on it and have population lower than 100
  village_list = [village for village in m.villages if int(village['village']['population']) < 100]
  ```

  * There is a property for generate player and kingdom data too

  ```python
  # make a list of inactive player
  inactive_list = [player for player in m.players if player.is_active is False]

  # make a list of kingdoms data
  kingdoms = list(m.kingdoms)
  ```  
---
## Villages
  `Villages` is a dict like object that store `Village` object and accessing it use village name.  
  But first `Villages` object need to pull data from TK.

  ```python
  from tkpy import Villages

  villages = Villages(driver)
  villages.pull()

  villages['my first village']
  <Village({'villageId': '537313245', 'playerId': '001', 'name': 'my first village',...})>

  # with `Village` object you can do several think, such as:
  # attack village at coordinate (0, 0)
  villages['my first village'].attack(0, 0, units={'1':-1, '11': 1})

  # defend another village at (0, 0)
  villages['my first village'].defend(0, 0, units={'1': -1, '2': -1, '11': 1})

  # raid another village at (0, 0)
  villages['my first village'].raid(0, 0, units={'1': 100})

  # siege another village at (0, 0)
  villages['my first village'].siege(0, 0, units={'1': -1, '6': -1, '7': -1, '11': 1})

  # upgrade building
  villages['my first village'].upgrade('main building')
  ```
  > Side note for `Villages` object:  
  > As you already know, you can naming your village with same name _(like 'my village' and 'my village')_.  
  > The problem is `Villages` object can't access this 2 kind of `Village` object with same name,  
  > in result `Villages` object will randomly return `Village` object that have same name.  
---  
## Farmlist
  `Farmlist` is a dict like object that store `FarmlistEntry` object and accessing it using farmlist name.  
  First `Farmlist` object need to pull data from TK.
  ```python
  from tkpy import Farmlist

  farmlist = Farmlist(driver)
  farmlist.pull()

  # after that you can access `FarmlistEntry` object use name of farmlist
  farmlist['Startup farm list']
  <FarmlistEntry({'listId': '1631', 'listName': 'Startup farm list', ...})>

  # you can create a new farmlist use `create_farmlist` method
  farmlist.create_farmlist(name='new farmlist')

  # now you can access new farmlist use it's name
  farmlist['new farmlist']
  <FarmListEntry({'listId': '1632', 'listName': 'new farmlist', ...})>

  # through `FarmlistEntry` object you can add, and toggle village use villageId
  farmlist['Startup farm list'].add(villageId=537313245)
  farmlist['Startup farm list'].toggle(villageId=537313245)
  ```
  > Side note for `Farmlist` object:  
  > As you already know, you can naming your farmlist with same name _(like 'farmlist 1', and 'farmlist 1')_.  
  > The problem is `Farmlist` object can't access this 2 kind of `FarmlistEntry` object with same name,  
  > in result `Farmlist` object will randomly return `FarmlistEntry` object that have same name.
---  
## Notepad
  `Notepad` is an object that when instantiate will create a new notepad in game.  
  ```python
  from tkpy import Notepad

  notepad = Notepad(driver) # new notepad will appear in game

  # message method will write your message to notepad
  notepad.message('this is new message on new notepad')

  # careful, use message method will overwrite message that previously on notepad
  notepad.message('this message will overwrite with old one.')
  ```
---  
# Document
For documentation, visit [tkpy wiki](https://github.com/didadadida93/tkpy/wiki).
