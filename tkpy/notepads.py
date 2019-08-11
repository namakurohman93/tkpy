class Notepad:
    """ :class:`Notepad` represent as notepad object on TK.

    Usage::
        >>> n = Notepad(driver) # this will create new notepad in game
        >>> n.message('first message') # this will add message to notepad
        >>> # carefull, this will overwrite old message
        ...
        >>> n.message('overwrited..')
    """
    def __init__(self, client):
        self.client = client
        self.id = None
        self._init()

    def _init(self):
        """ :meth:`_init` send requests to TK for creating new notepad.
        Internal use.
        """
        r = self.client.cache.get({'names':['Collection:Notepad:']})
        if r['cache'][0]['data']['cache']:
            self.client.post(
                action='changeSettings',
                controller='player',
                params= {
                    'newSettings': {
                        'notpadsVisible': True
                    }
                }
            )
            r = self.client.player.addNote(
                {
                    'x': 4.5,
                    'y': 10.5
                }
            )
            nid = r['cache'][0]['data']['cache'][0]['data']['id']
        else:
            self.client.post(
                action='changeSettings',
                controller='player',
                params= {
                    'newSettings': {
                        'notpadsVisible': False
                    }
                }
            )
            r = self.client.post(
                action='addNote',
                controller='player',
                params={}
            )
            nid = r['cache'][0]['data']['cache'][0]['data']['id']
            self.client.post(
                action='changeSettings',
                controller='player',
                params= {
                    'newSettings': {
                        'notpadsVisible': True
                    }
                }
            )
        self.id = nid

    def message(self, msg):
        """ :meth:`message` send a requests to TK to write message to this
        :class:`Notepad`.
        """
        self.client.player.changeNote(
            {
                'newSettings': {
                    'id': self.id,
                    'positionX': 4.5,
                    'positionY': 10.5,
                    'sizeX': 225,
                    'sizeY': 100,
                    'text': ''
                }
            }
        )
        self.client.player.changeNote(
            {
                'newSettings': {
                    'id': self.id,
                    'positionX': 4.5,
                    'positionY': 10.5,
                    'sizeX': 225,
                    'sizeY': 100,
                    'text': f'{msg}'
                }
            }
        )
