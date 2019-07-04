import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkpy.utilities import credential, login
from tkpy.notepads import Notepad
from tkpy.map import Map

logging.basicConfig(
    format='[%(asctime)s][%(levelname)s]: %(message)s',
    level=logging.INFO, datefmt='%d/%b/%Y:%H:%M:%S'
)


def find_cropper(maps, resType):
    field = (cell for cell in maps.cell if 'resType' in cell)
    for cell in field:
        if cell['resType'] == resType:
            yield cell


def oasis_nearby(cell, oasis):
    for x in range(cell.coordinate[0]-3, cell.coordinate[0]+4):
        for y in range(cell.coordinate[1]-3, cell.coordinate[1]+4):
            try:
                yield oasis[(x, y)]
            except:
                continue


if __name__ == '__main__':
    logging.info('login')
    driver = login(*credential())

    logging.info('pulling map data')
    maps = Map(driver)
    maps.pull()

    logging.info('finding croppers...')
    oasis = {cell.coordinate: cell for cell in maps.oasis}

    for x in [('15 cropper:\n', '11115'), ('9 cropper:\n', '3339')]:
        r = dict()
        msg = x[0]
        for cell in find_cropper(maps, x[1]):
            bonuse = sorted(
                [o['oasis']['bonus']['4'] for o in oasis_nearby(cell, oasis)],
                reverse=True
            )
            r[cell.coordinate] = [sum(bonuse[:3]), cell]
        results = dict(
            sorted(r.items(), key=lambda k: k[1][0], reverse=True)
        )
        logging.info(f'print {msg[:-2]} to notepad')
        for x, y in results:
            msg += f'({x}|{y}) {results[(x, y)][0]} '
            try:
                village_id = results[(x, y)][1]['village']['villageId']
            except:
                msg += 'free\n'
            else:
                msg += f'[village:{village_id}]\n'
        notepad = Notepad(driver)
        notepad.message(msg)

    logging.info('done')
