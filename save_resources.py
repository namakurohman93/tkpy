import sys
import time
import logging
import threading
from itertools import cycle
from random import randint
from utils import extended_login
from dodger import village_list, threads_list, diff_time, print_log

logging.basicConfig(
    format='[%(asctime)s][%(levelname)s]: %(message)s',
    level=logging.DEBUG, datefmt='%d/%b/%Y:%H:%M:%S'
)
for logs in logging.Logger.manager.loggerDict:
    logging.getLogger(logs).setLevel(logging.INFO)
VOI = [] # village of interest


def cancel_offer(t5, offer_id):
    t5.trade.cancelOffer({'offerId': offer_id})


def check_availability(ress):
    if True in ress.values():
        return True
    else:
        return False


def save_ress(t5, data, villages):
    print_log(data, villages)
    diff = diff_time(data)
    time.sleep(diff-20)
    logging.info(f'start saving resource for incoming id: {data["troopId"]}')
    village = villages.id(data['villageIdLocation'])
    merchants = village.merchants()
    av_mer = (int(merchants['max'])
             - int(merchants['inOffers'])
             - int(merchants['inTransport']))
    if av_mer:
        # merchant available
        id_list = id_offer_list(t5, village, av_mer, merchants)
        if id_list:
            time.sleep(40)
            for id in id_list:
                cancel_offer(t5, id)
        else:
            # merchant is available but amount of every resource is less than
            # cranny so its just do nothing until attack land
            time.sleep(21)
    else:
        # no merchant available
        logging.info('no merchant available')
        time.sleep(21)


def id_offer_list(t5, village, av_mer, merchants):
    id_list = list()
    cranny = village.cranny()
    resources = village.resources()
    amount = {k: int(v) for k, v in resources['amount'].items()}
    res_cycle = cycle(range(1, 5))
    ress = {'1': True, '2': True, '3': True, '4': True}
    while True:
        res = str(next(res_cycle))
        if ress[res]:
            if amount[res] >= cranny:
                id = offer_resource(t5, village.villageId, res, merchants)
                id_list.append(id)
                amount[res] -= int(merchants['carry'])
                av_mer -= 1
            else:
                # amount of this resources less than cranny capacity so it is
                # save and didn't need to check again
                ress[res] = False
        if av_mer <= 0:
            break
        if not check_availability(ress):
            break
    return id_list


def offer_resource(t5, vil_id, res, merchants):
    offered_amount = int(merchants['carry'])
    offered_res = int(res)
    search_amount = 2 * offered_amount
    search_res = 2 if offered_res == 1 else 1
    village_id = int(vil_id)
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


def check_village(t5):
    if not VOI:
        return
    villages = village_list(t5)
    for village_name in VOI:
        errmsg = f'you didnt have village {village_name}'
        assert village_name in villages.keys(), errmsg


def incoming_list(village):
    results = list()
    temp = VOI or village
    for village_name in temp:
        incoming = village[village_name].incoming_attack()
        if incoming:
            results.extend(incoming)
    return results


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
                    target=save_ress,
                    name=data['troopId'],
                    args=(gameworld, data, villages)
                ).start()
        time.sleep(randint(20, 25))
