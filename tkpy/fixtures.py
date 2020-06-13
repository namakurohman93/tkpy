import enum


buildingDict = {
    'wood': '1',
    'clay': '2',
    'iron mine': '3',
    'crop': '4',
    'sawmill': '5',
    'brickyard': '6',
    'iron foundry': '7',
    'grain mill': '8',
    'bakery': '9',
    'warehouse': '10',
    'granary': '11',
    'smithy': '13',
    'tournament square': '14',
    'main building': '15',
    'rally point': '16',
    'marketplace': '17',
    'embassy': '18',
    'barrack': '19',
    'stable': '20',
    'workshop': '21',
    'academy': '22',
    'cranny': '23',
    'town hall': '24',
    'residence': '25',
    'palace': '26',
    'treasury': '27',
    'trade office': '28',
    'great barrack': '29',
    'great stable': '30',
    'city wall': '31',
    'earth wall': '32',
    'palisade': '33',
    'stonemason': '34',
    'brewery': '35',
    'trapper': '36',
    'great warehouse': '38',
    'great granary': '39',
    'world of wonder': '40',
    'horse drinking trough': '41',
    'water ditch': '42',
    'natarian wall': '43',
    'hidden treasury': '45'
}

unitDict = {
    1: {
        'legionnaire': '1',
        'praetorian': '2',
        'imperian': '3',
        'equites legati': '4',
        'equites imperatoris': '5',
        'equites caesaris': '6',
        'ram': '7',
        'fire catapult': '8',
        'senator': '9',
        'settler': '10',
        'hero': '11'
    },
    2: {
        'clubswinger': '1',
        'spearman': '2',
        'axeman': '3',
        'scout': '4',
        'paladin': '5',
        'teutonic knight': '6',
        'ram': '7',
        'catapult': '8',
        'chief': '9',
        'settler': '10',
        'hero': '11'
    },
    3: {
        'phalanx': '1',
        'swordsman': '2',
        'pathfinder': '3',
        'theutates thunder': '4',
        'druidrider': '5',
        'haeduan': '6',
        'ram': '7',
        'catapult': '8',
        'chief': '9',
        'settler': '10',
        'hero': '11'
    }
}

tribeName = {1: 'Roman', 2: 'Teuton', 3: 'Gauls'}

tribeOffset = {1: 0, 2: 10, 3: 20, 4: 30, 5: 40}

adventureDict = {
    'short': {
        'questId': 991,
        'usingAdventurePoint': 1
    },
    'long': {
        'questId': 992,
        'usingAdventurePoint': 2
    }
}


class Building(enum.Enum):
    WOOD = 1
    CLAY = 2
    IRON_MINE = 3
    CROP = 4
    SAWMILL = 5
    BRICKYARD = 6
    IRON_FOUNDRY = 7
    GRAIN_MILL = 8
    BAKERY = 9
    WAREHOUSE = 10
    GRANARY = 11
    SMITHY = 13
    TOURNAMENT_SQUARE = 14
    MAIN_BUILDING = 15
    RALLY_POINT = 16
    MARKETPLACE = 17
    EMBASSY = 18
    BARRACKS = 19
    STABLE = 20
    WORKSHOP = 21
    ACADEMY = 22
    CRANNY = 23
    TOWN_HALL = 24
    RESIDENCE = 25
    PALACE = 26
    TREASURY = 27
    TRADE_OFFICE = 28
    GREAT_BARRACKS = 29
    GREAT_STABLE = 30
    CITY_WALL = 31
    EARTH_WALL = 32
    PALISADE = 33
    STONEMASON = 34
    BREWERY = 35
    TRAPPER = 36
    GREAT_WAREHOUSE = 38
    GREAT_GRANARY = 39
    WORLD_OF_WONDER = 40
    HORSE_DRINKING_TROUGH = 41
    WATER_DITCH = 42
    NATARIAN_WALL = 43
    HIDDEN_TREASURY = 45

    # def __init__(self, building_id):
    #     self.details = building_dict[id]

    @property
    def normalized_name(self):
        return self.name.replace('_', ' ').title()


class Resources(enum.Enum):
    Wood = 1
    Clay = 2
    Iron = 3
    Crop = 4
