"""
 _     _
| |_  | | __  _ __    _   _
| __| | |/ / | '_ \  | | | |
| |_  |   <  | |_) | | |_| |
 \__| |_|\_\ | .__/   \__, |
             |_|      |___/


Class model for tkpy
"""


class ImmutableDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __setitem__(self, name, value):
        if name in self.keys():
            raise TypeError(
                f"'{type(self).__name__}' object does not implement item assignment"
            )
        raise KeyError(f"{name}")


class Dataclass:
    __slots__ = ["data"]

    def __init__(self, data):
        self.data = ImmutableDict(data)

    def __repr__(self):
        return f"{type(self).__name__}({self.data})"

    def __getitem__(self, name):
        return self.__getattribute__("data")[name]

    def __getattr__(self, name):
        if name in self.__getattribute__("data").keys():
            return self.__getattribute__("data")[name]
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )

    def __setattr__(self, name, value):
        if name in self.__getattribute__("__slots__"):
            try:
                self.__getattribute__(name)
            except:
                super().__setattr__(name, value)
            else:
                raise AttributeError(f"can't set attribute '{name}'")
        elif name in self.keys():
            raise AttributeError(f"can't set attribute '{name}'")
        else:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}'"
            )

    def __contains__(self, key):
        return self.__getattribute__("data").__contains__(key)

    def __dir__(self):
        return [
            *filter(lambda d: d.startswith("_") is False, super().__dir__()),
            *self.__getattribute__("data").keys(),
        ]

    def keys(self):
        return self.__getattribute__("data").keys()
