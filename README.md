# tkpy
travian kingdom utilities for your need.


[![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-367/)

---
### instalation
1. install [primordial package](https://github.com/lijok/primordial)
2. git clone [this repo](https://github.com/didadadida93/tkpy.git)
3. change directory to tkpy
4. enjoy
---
### how it work
1. zoo tamer: `python3 zoo_tamer.py dummy@email.com dummypassword com9`, then check your ingame notepad.
> by default zoo tamer will find crocodile, tiger, and elephant on all unoccupied oasis. if you want to find bear as well, you need to:
> * open zoo_tamer.py with any text editor
> * change the SOI value.
```python
SOI = {'7', '8', '9', '10'}```
> * save and run it again
2. cropper: `python3 cropper.py dummy@email.com dummypassword com9`, then check your ingame notepad.
3. greyer: `python3 greyer.py dummy@email.com dummypassword com9`, then check your farm list.
> by default greyer will find all grey village and add them to farm list.
> if you want to find spesific village like minimum population and minimum/maximum distance, you need to:
> * open greyer.py with any text editor
> * then change:
>	* `MIN_POPULATION` value based on your need
>	* `MAX_POPULATION` value based on your need
>	* `CENTER` value (coordinate of village where you send a farmlist)
>	* `MIN_DISTANCE` value based on your need
>	* `MAX_DISTANCE` value based on your need
> * save and run it again
4. dodger: `python3 dodger.py dummy@email.com dummypassword com9`, then enjoy your day.
> by default dodger will cover all your village, but before you run dodger, you need to:
> * open dodger.py with any text editor
> * then change the TARGET value (usually coordinate of nearest occupied oasis)
> * if you just want to cover some village (usually scout village and hammer village), you need to edit VOI as well. example:
```python
VOI = ['scout village name', 'hammer village name']
TARGET = -13, 13```
> * save and run it again

---
### postscript

you have an idea? or found a bug? wanna contribute to project? open an issue and make a PR.
it is open project after all :wink:

---
_we love lowercase_
