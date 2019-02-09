import sys
import time
import logging
import threading
from random import randint
from utils import extended_login
from utilities.villages import Villages

logging.basicConfig(
    format='[%(asctime)s][%(levelname)s]: %(message)s',
    level=logging.DEBUG, datefmt='%d/%b/%Y:%H:%M:%S'
)
for logs in logging.Logger.manager.loggerDict:
    logging.getLogger(logs).setLevel(logging.INFO)
VILLAGE = '' # village where you send farmlist


def sender(client, timeout, ids, village_id, name):
    to = timeout*60
    while True:
        client.troops.startFarmListRaid(
            {
                'listIds': [
                    ids
                ],
                'villageId': village_id
            }
        )
        logging.info(f'send farm {name} and sleep for ~{to}')
        time.sleep(randint(to, to+60))


def farmlist_dict(client):
    results = dict()
    r = client.cache.get({'names':['Collection:FarmList:']})
    for x in r['cache'][0]['data']['cache']:
        if 'tkpy' in x['data']['listName']:
            n = int(''.join(filter(str.isdigit, x['data']['listName'])))
            results[int(x['data']['listId'])] = [n, x['data']['listName']]
    return results


def village_list(client):
    villages = Villages(client)
    villages.pull()
    return villages


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
    gameworld = extended_login(email, password, gameworld_name)
    farmlist = farmlist_dict(gameworld)
    villages = village_list(gameworld)
    for k, v in farmlist.items():
        threading.Thread(
            target=sender,
            name=k,
            args=(gameworld, v[0], villages[VILLAGE].villageId, v[1])
        ).start()
    while True:
        gameworld.is_authenticated()
        time.sleep(randint(20, 25))
