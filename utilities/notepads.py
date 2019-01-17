import logging

logging.basicConfig(
    format='[%(asctime)s][%(levelname)s]: %(message)s',
    level=logging.DEBUG, datefmt='%d/%b/%Y:%H:%M:%S'
)

class Notepad:
    def __init__(self, gameworld, notepad_id=None):
        self.client = gameworld
        self.id = notepad_id

    def __repr__(self):
        return self.id

    def new_notepad(self):
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

    def delete_notepad(self):
        if not self.id:
            return 'There is no notepad.' +\
                   '\nPlease create one use new_notepad method'
        r = self.client.player.removeNote(
            {
                'id': self.id
            }
        )
        if 'error' in r:
            logging.debug('Failed delete notepad.')
        print(f'Delete notepad id:{self.id}')
        return None

    def message(self, new_msg):
        if not self.id:
            return 'There is no notepad.' +\
                   '\nPlease create one use new_notepad method'
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
                    'text': f'{new_msg}'
                }
            }
        )
