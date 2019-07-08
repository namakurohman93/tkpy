import time
import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkpy.utilities import credential, login
from tkpy.map import Map, distance

logging.basicConfig(
    format='[%(asctime)s][%(levelname)s]: %(message)s',
    level=logging.INFO, datefmt='%d/%b/%Y:%H:%M:%S'
)
min_population = 0
max_population = 9999
center = 0, 0
min_distance = 0
max_distance = 9999


def filteredVillage(villageList):
    for village in villageList:
        if min_population < int(village['village']['population']) <= max_population:
            if min_distance < distance(village.coordinate, center) <= max_distance:
                yield village


def toggleFarmlist(client, villageId, farmlistId):
    client.farmList.toggleEntry({
        'listId': farmlistId,
        'villageId': villageId
    })


if __name__ == '__main__':
    logging.info('login')
    driver = login(*credential())

    if driver.plus_account <= 0:
        logging.info('Need Travian Plus Feature for running this script')
        sys.exit(0)

    logging.info('pulling farmlist data...')
    farmlist = Farmlist(driver)
    farmlist.pull()

    logging.info('pulling map data...')
    maps = Map(driver)
    maps.pull()

    logging.info('processing...')
    inactivePlayer = [player.id for player in maps.players if player.is_active is False]
    villageList = [cell for cell in maps.villages if cell['playerId'] in inactivePlayer]
    villages = [village for village in filteredVillage(villageList)]

    if len(villages) == 0:
        logging.info('no grey village found')
        sys.exit(0)

    for _ in range((len(villages) // 100)+1):
        n = int(time.time())
        logging.info(f'create farmlist name: {n}')
        farmlist.create_farmlist(n)
        for _ in range(100):
            village = villages.pop()
            toggleFarmlist(driver, village.id, farmlist[n].id)
            logging.info(f'add {village["village"]["name"]} to farmlist {n}')
            if not villages:
                break
    logging.info('done')
