import sys
import time
import logging
import threading
from itertools import cycle
from random import randint
from utils import extended_login
from dodger import (village_list, incoming_list,
threads_list, check_village, diff_time, print_log)

logging.basicConfig(
    format='[%(asctime)s][%(levelname)s]: %(message)s',
    level=logging.DEBUG, datefmt='%d/%b/%Y:%H:%M:%S'
)
for logs in logging.Logger.manager.loggerDict:
    logging.getLogger(logs).setLevel(logging.INFO)
VOI = [] # village of interest
TOLERANCE_THRESHOLD = 1000


def prttm(t5, data, villages): # put resources to the marketplace
    id_list = list()
    ress = {'1': True, '2': True, '3': True, '4': True}
    print_log(data, villages)
    diff = diff_time(data)
    time.sleep(diff-20)
    logging.info(f'saving the resources for incoming id: {data["troopId"]}')
    resources = villages.id(data['villageIdLocation']).resources()
    merchants = villages.id(data['villageIdLocation']).merchants()
    cranny = villages.id(data['villageIdLocation']).cranny()
    re_cycle = cycle(range(1, 5))
    av_mer = (int(merchants['max'])
             - int(merchants['inOffers'])
             - int(merchants['inTransport']))
    if av_mer:
        while True:
            res = str(next(re_cycle))
            if ress[res]:
                if int(resources['amount'][res]) >= cranny:
                    temp = int(resources['amount'][res]) - cranny
                    if temp >= TOLERANCE_THRESHOLD:
                        offered_amount = int(merchants['carry'])
                        offered_res = int(res)
                        search_amount = offered_amount * 2
                        search_res = 2 if offered_res == 1 else 1
                        id = create_offer(
                            t5, offered_amount, offered_res,
                            search_amount, search_res,
                            int(data['villageIdLocation'])
                        )
                        id_list.append(id)
                        av_mer -= 1
                else:
                    ress[res] = False
            if not av_mer:
                break
            if not check_availability(ress):
                break
        if id_list:
            time.sleep(40)
            for id in id_list:
                cancel_offer(t5, id)
        else:
            time.sleep(21)
    else:
        logging.info('there is no merchant available')
        time.sleep(21)


def create_offer(t5, offered_amount, offered_res,
    search_amount, search_res, village_id):
    r = t5.trade.createOffer(
        {
            'kingdomOnly': False,
            'offeredAmount': offered_amount,
            'offeredResource': offered_res,
            'searchedAmount': search_amount,
            'searchedResource': search_res,
            'villageId': village_id
        }
    )
    return r['cache'][0]['data']['cache'][0]['data']['offerId']


def cancel_offer(t5, offer_id):
    t5.trade.cancelOffer({'offerId': offer_id})


def check_availability(ress):
    if True in ress.values():
        return True
    else:
        return False


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
                    target=prttm,
                    name=data['troopId'],
                    args=(gameworld, data, villages)
                ).start()
        time.sleep(randint(20, 25))
