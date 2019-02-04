import sys
import time
import logging
import threading
from random import randint
from utils import extended_login, send_troops, vid, abort_troop_movement
from utilities.villages import Villages

logging.basicConfig(
    format='[%(asctime)s][%(levelname)s]: %(message)s',
    level=logging.DEBUG, datefmt='%d/%b/%Y:%H:%M:%S'
)
for logs in logging.Logger.manager.loggerDict:
    logging.getLogger(logs).setLevel(logging.INFO)
VOI = [] # village of interest
TARGET = 0, 0 # x, y coordinate


def evader(t5, data, villages):
    print_log(data, villages)
    diff = diff_time(data)
    time.sleep(diff-3)
    units = villages.id(data['villageIdLocation']).troops()
    if units:
        id = send_troops(t5, vid(*TARGET), data['villageIdLocation'], 5, units)
        logging.info(f'evading incoming id: {data["troopId"]}')
        time.sleep(4)
        abort_troop_movement(t5, id)
    else:
        # no troop, do nothing till attack landing
        village_name = villages.id(data["villageIdLocation"]).name
        logging.info(f'no troop in {village_name}')
        time.sleep(4)


def village_list(t5):
    villages = Villages(t5)
    villages.pull()
    return villages


def incoming_list(village, voi=VOI):
    results = list()
    temp = voi or village
    for village_name in temp:
        incoming = village[village_name].incoming_attack()
        if incoming:
            results.extend(incoming)
    return results


def threads_list():
    result = list()
    for thread in threading.enumerate():
        result.append(thread.name)
    return result


def check_village(t5, voi=VOI):
    if not voi:
        return
    villages = village_list(t5)
    for village_name in voi:
        errmsg = f'you didnt have village {village_name}'
        assert village_name in villages.keys(), errmsg


def diff_time(data):
    time_finish = int(data['movement']['timeFinish'])
    time_now = int('{:.0f}'.format(time.time()).replace('.', ''))
    diff = time_finish - time_now
    return diff


def print_log(data, villages):
    time_finish = int(data['movement']['timeFinish'])
    arrive = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_finish))
    msg = f'{villages.id(data["villageIdLocation"]).name}: '+\
          f'incoming (id: {data["troopId"]}, player: {data["playerName"]}'+\
          f', village: {data["villageName"]}, arrive: {arrive})'
    logging.info(msg)


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
    if TARGET == (0, 0):
        print('please change the target first')
        sys.exit()
    logging.info('loging in')
    gameworld = extended_login(email, password, gameworld_name)
    check_village(gameworld)
    logging.info(f'{sys.argv[0]} started, enjoy your day :)')
    while True:
        villages = village_list(gameworld)
        incoming = incoming_list(villages)
        threads = threads_list()
        for data in incoming:
            if data['troopId'] in threads:
                continue
            else:
                threading.Thread(
                    target=evader,
                    name=data['troopId'],
                    args=(gameworld, data, villages)
                ).start()
        time.sleep(randint(20, 25))
