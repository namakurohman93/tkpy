"""
 _     _
| |_  | | __  _ __    _   _
| __| | |/ / | '_ \  | | | |
| |_  |   <  | |_) | | |_| |
 \__| |_|\_\ | .__/   \__, |
             |_|      |___/


Class model for tkpy
"""

import dataclasses


class ImmutableDict(dict):
    """ :class:`ImmutableDict` is an object that inherit from built-in
    :class:`dict` but didn't implement item assignment.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __setitem__(self, name, value):
        if name in self.keys():
            raise TypeError(
                f"'{type(self).__name__}' object does not implement item assignment"
            )
        raise KeyError(f"{name}")


@dataclasses.dataclass(frozen=True)
class ImmutableDataclass:
    """ :class:`ImmutableDataclass` is a slotted class that simply cant
    reassign attribute and cant add new attribute.
    Furthemore, data of this class is stored on :attr:`data` and it
    has :class:`ImmutableDict` type.
    Data can be accessed using key, or for simplicity sake, can be accessed
    as an 'attribute' too.

    Usage:
        >>> foo = ImmutableDataclass(data={'a':'a', 'b':'b', 'c':'c'})
        >>> foo.data
        {'a': 'a', 'b': 'b', 'c': 'c'}
        >>> foo.data = 'z'
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "<string>", line 3, in __setattr__
        dataclasses.FrozenInstanceError: cannot assign to field 'data'
        >>> foo.z = 'z'
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "<string>", line 3, in __setattr__
        dataclasses.FrozenInstanceError: cannot assign to field 'z'
        >>> foo.data['a']
        'a'
        >>> foo.data['a'] = 'z'
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "/tkpy/models.py", line 27, in __setitem__
            f"'{type(self).__name__}' object does not implement item assignment"
        TypeError: 'ImmutableDict' object does not implement item assignment
        >>> foo['a']
        'a'
        >>> foo.a
        'a'
        >>> dir(foo)
        ['a', 'b', 'c', 'data']
        >>> foo
        <ImmutableDataclass({'a': 'a', 'b': 'b', 'c': 'c'})>
        >>>
    """

    __slots__ = ["data"]
    data: dict

    def __post_init__(self):
        object.__setattr__(self, "data", ImmutableDict(self.data))

    def __getattr__(self, name):
        if name in self.__getattribute__("data").keys():
            return self.__getattribute__("data")[name]
        self.__getattribute__(name)

    def __getitem__(self, name):
        try:
            return self.__getattribute__("data")[name]
        except:
            raise

    def __setitem__(self, name, value):
        try:
            self.__getattribute__("data")[name] = value
        except:
            raise

    def __dir__(self):
        return [
            *filter(
                lambda d: d.startswith("_") is False, object.__dir__(self)
            ),
            *self.__getattribute__("data").keys(),
        ]

    def __contains__(self, keys):
        return self.__getattribute__("data").__contains__(keys)

    def __repr__(self):
        return f"<{type(self).__name__}({self.data})>"
