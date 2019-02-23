import time
from assets.buildings import buildings as BUILDINGS

def _instant_5_finish(slot, village_id):
    r = self.village.client.premiumFeature.finishNow(
        {
            'price': 0,
            'queueType': slot,
            'villageId': village_id
        }
    )
    try:
        # report if 5 min finish earlier failed
        if r['response']['data'] is False:
            return '5 minute finish earlier failed'
    except KeyError:
        pass


class Building:
    """building object for collecting details of upgraded building"""
    def __init__(self, village, building_id):
        self.village = village
        self.b_id = building_id
        self.details = dict()
        self.get_building_details()
        if not self.exist and self.details:
            # building not exist and have free location id
            self.update_details()
        elif not self.details:
            # can't upgrade building cause there is no free slot
            self.buildable = False
        else:
            self.buildable = True
        # check if it is wall cause they have fixed location id
        the_wall = [31, 32, 33, 43]
        if self.b_id in the_wall:
            self.details['data']['locationId'] = '33'
        # if rally point, change location id in to fixed location id
        if self.b_id == 16:
            self.details['data']['locationId'] = '32'

        # TODO:
        # need to check if building can't be upgrade due to lack of
        # warehouse and granary capacity

    def __getitem__(self, key):
        return self.details[key]

    def __repr__(self):
        return str(self.details)

    def get_building_details(self):
        if self.b_id < 5:
            self._resources_detail()
        else:
            self._building_detail()

    def _building_detail(self):
        found = False
        cache = dict()
        results = dict()
        buildings = self.village.buildings()
        for building in buildings:
            if building['data']['buildingType'] == str(self.b_id):
                location = int(building['data']['locationId'])
                results[location] = building
                found = True
            elif building['data']['buildingType'] == '0' and not cache:
                cache.update(building)
            else:
                continue
        if not found:
            self.exist = False
            self.details.update(cache)
        else:
            loc = min(results.keys(), key=lambda l: int(results[l]['data']['lvl']))
            if results[loc]['data']['isMaxLvl'] is True:
                self.exist = False
                self.details.update(cache)
            else:
                self.exist = True
                self.details.update(results[loc])

    def _resources_detail(self):
        self.exist = True
        results = dict()
        buildings = self.village.buildings()
        for building in buildings:
            if building['data']['buildingType'] == str(self.b_id):
                location = int(building['data']['locationId'])
                results[location] = building
        loc = min(results.keys(), key=lambda l: int(results[l]['data']['lvl']))
        self.details.update(results[loc])

    def update_details(self):
        found = False
        cache = self.details
        r = self.village.client.building.getBuildingList(
            {
                'locationId': cache['data']['locationId'],
                'villageId': self.village.villageId
            }
        )
        for building in r['response']['buildings']['buildable']:
            if building['buildingType'] == self.b_id:
                found = True
                cache['data'].update(building)
                self.buildable = True
                break
        if not found:
            for building in r['response']['buildings']['notBuildable']:
                if building['buildingType'] == self.b_id:
                    found = True
                    cache['data'].update(building)
                    # can't upgrade building due to lack of requirements
                    self.buildable = False
                    break
        if not found:
            # it seems the building have max level and can't build another
            self.buildable = False
        self.details.update(cache)


class MasterBuilder:
    """object that make upgrade building so simple
       example:
        mb = MasterBuilder(village)
        mb.upgrade('bakery')"""
    def __init__(self, village):
        self.village = village
        del village

    def _check_bcs(self):
        """building construction slot checker"""
        r = self.village.client.cache.get(
            {'names':[f'BuildingQueue:{self.village.villageId}']}
        )
        if self.village.client.tribe_id == 1 and self.b_id < 5:
            # it's roman and building is resources type
            # check slots '2'
            self.slot = r['cache'][0]['data']['freeSlots']['2'] # boolean
            self.slots = r['cache'][0]['data']['freeSlots'] # dict
            # self.queues = r['cache'][0]['data']['queues']['2'][0] # dict
        else:
            # it's all tribe and building is building type
            # check slots '1'
            self.slot = r['cache'][0]['data']['freeSlots']['1'] # boolean
            self.slots = r['cache'][0]['data']['freeSlots'] # dict
            # self.queues = r['cache'][0]['data']['queues']['1'][0] # dict

    def _check_mbs(self):
        """master builder slot checker"""
        results = list()
        for key in ['4', '5', '6', '7']:
            try:
                if self.slots[key]:
                    # its free
                    results.append(True)
            except KeyError:
                continue
        return True in results

    def _check_resources(self):
        """check whether its enough resources or not for upgrade building"""
        results = list()
        ress = self.village.resources()
        upgrade_cost = self.building['data']['upgradeCosts']
        for key in upgrade_cost:
            if ress['amount'][key] > upgrade_cost[key]:
                results.append(True)
            else:
                results.append(False)
        if False in results:
            self.enough_resource = False
        else:
            self.enough_resource = True

    def upgrade(self, building):
        """interface for upgrade building"""
        self.b_id = BUILDINGS[building.lower()]
        self.building = Building(self.village, self.b_id)
        if self.building.buildable:
            # can upgrade building
            self._check_bcs()
            self._check_resources()
            if self.slot and self.enough_resource:
                # building construction slot is empty
                self._upgrade()
            else:
                # building construction slot isn't empty
                # check master builder slot
                if self._check_mbs():
                    # master builder slot empty
                    # add it to master builder slot
                    self._add_to_queue()
                else:
                    # master builder slot full
                    print('master builder slot is full')
        else:
            # can't upgrade building
            try:
                requirements = self.building['data']['requiredBuildings'] # list
            except KeyError:
                try:
                    if self.building['data']['isMaxLvl'] is True:
                        print('cant upgrade building cause its already at max level')
                    else:
                        print('cant upgrade building due to unknown reason')
                except KeyError:
                    # can't upgrade cause location is full
                    print('cant upgrade building cause there is no slot in village')
            else:
                # can't upgrade due to lack of requirements
                self.print_req(requirements)

    def _upgrade(self):
        red = '\033[1;31m'
        green = '\033[1;32m'
        normal = '\033[0;0m'
        reverse = {v: k for k, v in BUILDINGS.items()}
        r = self.village.client.building.upgrade(
            {
                'buildingType': self.b_id, # id/type of building
                'locationId': int(self.building['data']['locationId']),
                'villageId': self.village.villageId
            }
        )
        if not r['response']:
            # succes upgrade building
            print(f'upgrade {reverse[self.b_id]} {green}success{normal}')
        else:
            # failed
            print(f'upgrade {reverse[self.b_id]} {red}failed{normal}')

    def _add_to_queue(self):
        red = '\033[1;31m'
        green = '\033[1;32m'
        normal = '\033[0;0m'
        reverse = {v: k for k, v in BUILDINGS.items()}
        r = self.village.client.building.useMasterBuilder(
            {
                'buildingType': self.b_id,
                'locationId': int(self.building['data']['locationId']),
                'villageId': self.village.villageId,
                'reserveResources': self.enough_resource
            }
        )
        if not r['response']:
            # success add building to queue
            print(
                f'add {reverse[self.b_id]} to queue {green}success{normal}'
            )
        else:
            # failed
            print(f'add {reverse[self.b_id]} to queue {red}failed{normal}')

    def print_req(self, requirements):
        red = '\033[1;31m'
        normal = '\033[0;0m'
        msg = 'cant upgrade need requirements:\n'
        reverse = {v: k for k, v in BUILDINGS.items()}
        for req in requirements:
            if req['valid'] is False:
                current_lvl = int(req['currentLevel'])
                req_lvl = int(req['requiredLevel'])
                diff = req_lvl - current_lvl
                builid = req['buildingType']
                msg += f'{reverse[builid]} level {req_lvl}{red}(+{diff}){normal}\n'
        print(msg[:-1])
