import dataclasses
from typing import Any

from .models import ImmutableDataclass
from .fixtures import adventureDict
from .exception import HeroNotInHome
from .exception import NotEnoughAdventurePoint


@dataclasses.dataclass(frozen=True, repr=False)
class Hero(ImmutableDataclass):
    """ :class:`Hero` is a :class:`dict` - like object that represent
    of 'Hero' object for TK. This class is where hero data from TK
    stored.

    Usage:
        >>> hero = Hero(driver)
        >>> hero.pull()
        >>> r = hero.adventures('short')
    """

    __slots__ = ["client"]
    client: Any

    def __init__(self, client, data={}):
        super().__init__(data)
        object.__setattr__(self, "client", client)

    def pull(self):
        """ :meth:`pull` for pulling hero data from TK. """
        self.data.update(
            self.client.cache.get({
                "names": [f"Hero:{self.client.player_id}"]
            })["cache"][0]["data"]
        )

    @property
    def exp(self):
        """ :property:`exp` return current exp of hero.

        return: :class:`int`
        """
        return int(self.xp) - int(self.xpThisLevel)

    @property
    def exp_next_level(self):
        """ :property:`exp_next_level` is how much exp needed for hero
        to level up.

        return: :class:`int`
        """
        return int(self.xpNextLevel) - int(self.xpThisLevel)

    @property
    def in_home(self):
        """ :property:`in_home` is checking if hero is in home or not.

        return: :class:`boolean`
        """
        return not self.isMoving and self.status == "0"

    def _check_adventure_point(self, adventure):
        # check if current adventure point is enough to be used for
        # sent hero to adventure.
        return int(self.adventurePoints) < adventure["usingAdventurePoint"]

    def adventures(self, adventureType):
        """ :meth:`adventures` send hero to adventure.

        :param adventureType: - :class:`str` type of adventure, it is
                                either `'short'` or `'long'`.

        return: :class:`dict`
        """
        adventure = adventureDict[adventureType]

        if self._check_adventure_point(adventure):
            raise NotEnoughAdventurePoint()

        if not self.in_home:
            raise HeroNotInHome()

        return self.client.quest.dialogAction({
            "command": "activate",
            "dialogId": 0,
            "questId": adventure["questId"],
        })
