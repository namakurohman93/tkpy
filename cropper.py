import sys
import time
import logging
from utils import basic_login
from utilities.notepads import Notepad
from utilities.map import Map

logging.basicConfig(
    format='[%(asctime)s][%(levelname)s]: %(message)s',
    level=logging.DEBUG, datefmt='%d/%b/%Y:%H:%M:%S'
)
TOI = ( # tuple of interest
    {
        'res_type': '11115',
        'msg': '15 croppers:\n',
        'results': dict()
    },
    {
        'res_type': '3339',
        'msg': '9croppers:\n',
        'results': dict()
    }
)


def crop_finder(t5):
    maps = Map(t5)
    maps.init()
    oasis = maps.oasis()
    tiles = maps.tiles()
    for coord in tiles:
        if tiles.coordinate(*coord)['resType'] == TOI[0]['res_type']:
            TOI[0]['results'][coord] = list((0,))
        elif tiles.coordinate(*coord)['resType'] == TOI[1]['res_type']:
            TOI[1]['results'][coord] = list((0,))
        else:
            continue
    for toi in TOI:
        new_msg = toi['msg']
        for coord in toi['results']:
            x, y = coord
            for x2 in range(x-3, x+4):
                for y2 in range(y-3, y+4):
                    try:
                        bonus = oasis.coordinate(x2, y2)['oasis']['bonus']['4']
                        toi['results'][coord].append(bonus)
                    except KeyError:
                        continue
            sorted_bonus = sorted(toi['results'][coord], reverse=True)
            toi['results'][coord] = sum(sorted_bonus[:3])
        sorted_result = {
            k: toi['results'][k] for k in sorted(
                toi['results'], key=toi['results'].__getitem__, reverse=True
            )
        }
        for coord in sorted_result:
            x, y = coord
            bonus = sorted_result[coord]
            new_msg += f'({x}|{y}) -> bonus: {bonus}\n'
        notepad = Notepad(t5)
        notepad.new_notepad()
        notepad.message(new_msg)


if __name__ == '__main__':
    try:
        email = sys.argv[1]
        password = sys.argv[2]
        gameworld_name = sys.argv[3]
    except IndexError:
        errmsg = 'Missing arguments\n'+\
                 f'Usage: \tpython3 {sys.argv[0]} <email> <password> <gameworld>'
        print(errmsg)
        sys.exit()
    gameworld = basic_login(email, password, gameworld_name)
    crop_finder(gameworld)
    print(f'done, please check your {gameworld_name}\'s notepad.')
