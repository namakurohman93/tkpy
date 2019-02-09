import time
from assets.buildings import buildings as BUILDINGS


class MasterBuilder:
    """just a bunch of function tied up at same class and wrapped by sequence
    of if else logic to make upgrading building as simple as possible
    example:
        villages = Villages(gameworld)
        master_builder = MasterBuilder(villages['village name'])
        master_builder.upgrade('marketplace')
    """
    def __init__(self, village):
        self.village = village
        self.buildings = BUILDINGS
        del village

    def _check_bcs(self, building_id):
        """building construction slot checker"""
        r = self.village.client.cache.get(
            {'names':[f'BuildingQueue:{self.village.villageId}']}
        )
        if self.village.client.tribe_id == 1 and building_id < 5:
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

    def _check_building(self, building_id):
        """building checker
        it check if building already installed/exist in village or not
        if installed return locationId
        if not installed find free locationId"""
        found = False
        buildings = self.village.buildings()
        # if building_id is resources type, find locationId lowest level of
        # that resources
        if building_id < 5:
            self._lowest_lid(building_id, buildings)
        for building in buildings:
            if building['data']['buildingType'] == str(building_id):
                # gotcha
                self.exist = True
                found = True
                location_id = building['data']['locationId']
                self.upgrade_cost = building['data']['upgradeCosts']
                break
        if not found:
            # find free location id
            self.exist = False
            for building in buildings:
                if building['data']['buildingType'] == '0':
                    location_id = building['data']['locationId']
                    break
        return int(location_id)

    def _lowest_lid(self, building_id, buildings):
        """building_id is resources type
        it will find location id of this resources type that have
        lowest level"""
        self.exist = True
        results = dict()
        for building in buildings:
            if building['data']['buildingType'] == str(building_id):
                location = int(building['data']['locationId'])
                level = int(building['data']['lvl'])
                upgrade_cost = building['data']['upgradeCosts']
                results[location] = {
                    'level':level, 'upgrade costs':upgrade_cost
                }
        lowlvl = min(results.keys(), key=lambda k: results[k]['level'])
        self.upgrade_cost = results[lowlvl]['upgrade costs']
        return lowlvl

    def _get_building_list(self, location_id):
        """building isnt exist, so need a building list for install
        it to location id"""
        r = self.village.client.building.getBuildingList(
            {
                'locationId': location_id,
                'villageId': self.village.villageId
            }
        )
        self.buildable = r['response']['buildings']['buildable'] # list
        self.unbuildable = r['response']['buildings']['notBuildable'] # list

    def _check_buildable(self, building_id):
        """check if building can be build or not"""
        for building in self.buildable:
            if building['buildingType'] == building_id:
                self.upgrade_cost = building['upgradeCosts']
                return True
        return False

    def _check_requirements(self, building_id):
        """cant build building due to lack of requirements
        check the requirements and return it as list"""
        results = list()
        for building in self.unbuildable:
            if building['buildingType'] == building_id:
                for requirements in building['requiredBuildings']:
                    if not requirements['valid']:
                        results.append(requirements)
        return results

    def _enough_resources(self):
        """check whether its enough resources or not for upgrade building"""
        results = list()
        ress = self.village.resources()
        for key in self.upgrade_cost:
            if ress['amount'][key] > self.upgrade_cost[key]:
                results.append(True)
            else:
                results.append(False)
        if False in results:
            return False
        else:
            return True

    def _validate(self, building_id, location_id):
        """validate building id is resources type and validate if this
        resources located on location_id"""
        if location_id:
            self._validate_resources_type(building_id)
            locid_list = list()
            buildings = self.village.buildings()
            for building in buildings:
                if building['data']['buildingType'] == str(building_id):
                    locid_list.append(int(building['data']['locationId']))
            errmsg = 'building isnt in location id'
            assert location_id in locid_list, errmsg
            self.exist = True

    def _validate_resources_type(self, building_id):
        errmsg = 'location_id only needed when upgrade spesific resources \
            on spesific location'
        assert building_id < 5, errmsg

    def upgrade(self, building, location_id=None):
        """method for upgrade building"""
        builid = self.buildings[building]
        self._validate(builid, location_id) # validate location_id with builid
        # 1. check building queue
        self._check_bcs(builid)
        if self.slot:
            # can upgrade building
            # 2. check building is installed or not and location id
            location = location_id or self._check_building(builid)
            # 3. check if resources is enough for upgrade building
            if self.exist:
                # building installed
                if self._enough_resources():
                    # upgrade
                    self._upgrade(builid, location)
                else:
                    # not enough resources, check mb_slot
                    # if mb_slot available then add it to master builder slot
                    if self._check_mbs():
                        # have free slot
                        self._add_to_queue(builid, location)
                    else:
                        # not enough resources and mb_slot not available
                        print('not enough resources and queue full')
            else:
                # building not exist
                # need to check if building can be upgrade or it still lack
                # of requirements
                self._get_building_list(location)
                if self._check_buildable(builid):
                    # check if resources is enough for ugprade building
                    if self._enough_resources():
                        # upgrade
                        self._upgrade(builid, location)
                    else:
                        # not enough resources, check mb_slot
                        # if mb_slot available then add it
                        # to master builder slot
                        if self._check_mbs():
                            # have free slot
                            self._add_to_queue(builid, location)
                        else:
                            # not enough resources and mb_slot not available
                            print('not enough resources and queue full')
                else:
                    # can't upgrade building due to lack of requirements
                    # check requirements and print it out
                    requirements = self._check_requirements(builid)
                    self.print_req(requirements)
        else:
            # building queue is being used
            # check mb_slot, if mb_slot available then add it
            # to master builder slot
            if self._check_mbs():
                # have free slot
                location = location_id or self._check_building(builid)
                if self.exist:
                    # building installed
                    self._add_to_queue(builid, location)
                else:
                    # building not exist
                    # need to check if building can be upgrade or it still
                    # lack of requirements
                    self._get_building_list(location)
                    if self._check_buildable(builid):
                        # can build this building
                        # put it on master builder slot
                        self._add_to_queue(builid, location)
                    else:
                        # can't upgrade building due to lack of requirements
                        # check requirements and print it out
                        requirements = self._check_requirements(builid)
                        self.print_req(requirements)
            else:
                # mb_slot not available
                print('queue full')

    def print_req(self, requirements):
        red = '\033[1;31m'
        normal = '\033[0;0m'
        msg = 'cant upgrade need requirements:\n'
        reverse = {v: k for k, v in self.buildings.items()}
        for req in requirements:
            current_lvl = int(req['currentLevel'])
            req_lvl = int(req['requiredLevel'])
            diff = req_lvl - current_lvl
            builid = req['buildingType']
            msg += f'{reverse[builid]} level {req_lvl}{red}(+{diff}){normal}\n'
        print(msg[:-1])

    def _upgrade(self, building_id, location):
        red = '\033[1;31m'
        green = '\033[1;32m'
        normal = '\033[0;0m'
        reverse = {v: k for k, v in self.buildings.items()}
        r = self.village.client.building.upgrade(
            {
            'buildingType': building_id, # id/type of building
            'locationId': location,
            'villageId': self.village.villageId
            }
        )
        if not r['response']:
            # succes upgrade building
            print(f'upgrade {reverse[building_id]} {green}success{normal}')
        else:
            # failed
            print(f'upgrade {reverse[building_id]} {red}failed{normal}')

    def _add_to_queue(self, building_id, location):
        red = '\033[1;31m'
        green = '\033[1;32m'
        normal = '\033[0;0m'
        reverse = {v: k for k, v in self.buildings.items()}
        r = self.village.client.building.useMasterBuilder(
            {
                'buildingType': building_id,
                'locationId': location,
                'villageId': self.village.villageId,
                'reserveResources': self._enough_resources()
            }
        )
        if not r['response']:
            # success add building to queue
            print(
                f'add {reverse[building_id]} to queue {green}success{normal}'
            )
        else:
            # failed
            print(f'add {reverse[building_id]} to queue {red}failed{normal}')


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
