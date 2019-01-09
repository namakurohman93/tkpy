import sys
import time
import logging
from utils import basic_login, vid, fishout
from utilities.notepads import Notepad

logging.basicConfig(
    format='[%(asctime)s][%(levelname)s]: %(message)s',
    level=logging.DEBUG, datefmt='%d/%b/%Y:%H:%M:%S'
)
TOI = ('11115', '3339') # tuple of interest


def crop_finder(t5):
    nine = dict()
    fifteen = dict()
    results = dict()
    req_list = list()
    for x in range(-13, 14):
        for y in range(-13, 14):
            req_list.append(vid(x, y))
    r = t5.map.getByRegionIds(
        {
            'regionIdCollection': {
                '1': req_list
            }
        }
    )
    for vids in r['response']['1']['region']:
        for result in r['response']['1']['region'][vids]:
            results[result['id']] = result
            try:
                res_type = result['resType']
                cell_id = result['id']
            except KeyError:
                continue
            if res_type == TOI[0]:
                fifteen[cell_id] = list((0,))
            elif res_type == TOI[1]:
                nine[cell_id] = list((0,))
            else:
                continue
    new_msg = '15 croppers:\n'
    for cell_id in fifteen:
        x, y = fishout(int(cell_id))
        for x2 in range(x-3, x+4):
            for y2 in range(y-3, y+4):
                try:
                    bonus = results[str(vid(x2, y2))]['oasis']['bonus']['4']
                    fifteen[cell_id].append(bonus)
                except KeyError:
                    continue
        sorted_bonus = sorted(fifteen[cell_id], reverse=True)
        fifteen[cell_id] = sum(sorted_bonus[:3])
    sorted_result = {
        k: fifteen[k] for k in sorted(
            fifteen, key=fifteen.__getitem__, reverse=True
        )
    }
    for cell_id in sorted_result:
        x, y = fishout(int(cell_id))
        bonus = sorted_result[cell_id]
        new_msg += f'({x}|{y}) -> bonus: {bonus}\n'
    fifteen_notepad = Notepad(t5)
    fifteen_notepad.new_notepad()
    fifteen_notepad.message(new_msg)
    new_msg = '9 croppers:\n'
    for cell_id in nine:
        x, y = fishout(int(cell_id))
        for x2 in range(x-3, x+4):
            for y2 in range(y-3, y+4):
                try:
                    bonus = results[str(vid(x2, y2))]['oasis']['bonus']['4']
                    nine[cell_id].append(bonus)
                except KeyError:
                    continue
        sorted_bonus = sorted(nine[cell_id], reverse=True)
        nine[cell_id] = sum(sorted_bonus[:3])
    sorted_result = {
        k: nine[k] for k in sorted(
            nine, key=nine.__getitem__, reverse=True
        )
    }
    for cell_id in sorted_result:
        x, y = fishout(int(cell_id))
        bonus = sorted_result[cell_id]
        new_msg += f'({x}|{y}) -> bonus: {bonus}\n'
    nine_notepad = Notepad(t5)
    nine_notepad.new_notepad()
    nine_notepad.message(new_msg)


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
