import logging

logging.basicConfig(
    format='[%(asctime)s][%(levelname)s]: %(message)s',
    level=logging.DEBUG, datefmt='%d/%b/%Y:%H:%M:%S'
)

class Notepad:
    def __init__(self, gameworld, notepad_id=None):
        self.gameworld = gameworld
        self.notepad_id = notepad_id

    def __repr__(self):
        return self.notepad_id

    def new_notepad(self):
        r = self.gameworld.cache.get({'names':['Collection:Notepad:']})
        if r['cache'][0]['data']['cache']:
            self.gameworld.post(
                action='changeSettings',
                controller='player',
                params= {
                    'newSettings': {
                        'notpadsVisible': True
                    }
                }
            )
            r = self.gameworld.player.addNote(
                {
                    'x': 4.5,
                    'y': 10.5
                }
            )
            nid = r['cache'][0]['data']['cache'][0]['data']['id']
        else:
            self.gameworld.post(
                action='changeSettings',
                controller='player',
                params= {
                    'newSettings': {
                        'notpadsVisible': False
                    }
                }
            )
            r = self.gameworld.post(
                action='addNote',
                controller='player',
                params={}
            )
            nid = r['cache'][0]['data']['cache'][0]['data']['id']
            self.gameworld.post(
                action='changeSettings',
                controller='player',
                params= {
                    'newSettings': {
                        'notpadsVisible': True
                    }
                }
            )
        self.notepad_id = nid

    def delete_notepad(self):
        if not self.notepad_id:
            return 'There is no notepad.' +\
                   '\nPlease create one use new_notepad method'
        r = self.gameworld.player.removeNote(
            {
                'id': self.notepad_id
            }
        )
        if 'error' in r:
            logging.debug('Failed delete notepad.')
        print(f'Delete notepad id:{self.notepad_id}')
        return None

    def message(self, new_msg):
        if not self.notepad_id:
            return 'There is no notepad.' +\
                   '\nPlease create one use new_notepad method'
        self.gameworld.player.changeNote(
            {
                'newSettings': {
                    'id': self.notepad_id,
                    'positionX': 4.5,
                    'positionY': 10.5,
                    'sizeX': 225,
                    'sizeY': 100,
                    'text': ''
                }
            }
        )
        self.gameworld.player.changeNote(
            {
                'newSettings': {
                    'id': self.notepad_id,
                    'positionX': 4.5,
                    'positionY': 10.5,
                    'sizeX': 225,
                    'sizeY': 100,
                    'text': f'{new_msg}'
                }
            }
        )
