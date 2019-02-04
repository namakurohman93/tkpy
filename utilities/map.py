from utils import vid, fishout, COLOR


class Cell:
    def __init__(self, client, cell_id, data):
        self.client = client
        self.id = cell_id
        self.coord = fishout(self.id)
        self._data = data or dict()

    def __getitem__(self, key):
        return self._data[key]

    def __repr__(self):
        return f'{type(self).__name__}({self._data})'

    def details(self):
        r = self.client.cache.get(
            {
                'names': [
                    f'MapDetails:{self.id}'
                ]
            }
        )
        return r

    def coloring_cell(self, color=None):
        color = color.upper() or 'BLUE'
        r = self.client.cache.get({'names':['Collection:MapMarker:']})
        for caches in r['cache'][0]['data']['cache']:
            if caches['data']['targetId'] == str(self.id):
                if caches['data']['color'] == str(COLOR[color]):
                    return
                self._edit_cell_color(int(caches['data']['id']), color)
                return
        markers = [
            {
                'color': COLOR[color],
                'editType': 3,
                'owner': 1,
                'ownerId': self.client.player_id,
                'targetId': self.id,
                'type': 3
            }
        ]
        self.client.post(
            action='editMapMarkers',
            controller='map',
            params={
                'markers': markers
            }
        )

    def delete_cell_color(self):
        r = self.client.cache.get({'names':['Collection:MapMarker:']})
        for caches in r['cache'][0]['data']['cache']:
            if caches['data']['targetId'] == str(self.id):
                markers = [
                    {
                        'editType': 2,
                        'id': int(caches['data']['id'])
                    }
                ]
                self.client.post(
                    action='editMapMarkers',
                    controller='map',
                    params={
                        'markers': markers
                    }
                )
                return

    def _edit_cell_color(self, id, color):
        markers = [
            {
                'color': COLOR[color],
                'editType': 1,
                'owner': 1,
                'ownerId': self.client.player_id,
                'targetId': self.id,
                'type': 3,
                'id': id
            }
        ]
        self.client.post(
            action='editMapMarkers',
            controller='map',
            params={
                'markers': markers
            }
        )

    def message(self, msg):
        self.client.post(
            action='editMapMarkers',
            controller='map',
            params={
                'fieldMessage': {
                    'cellId': self.id,
                    'duration': 12,
                    'targetId': self.client.player_id,
                    'text': msg,
                    'type': 5
                },
                'markers': []
            }
        )

    def kingdom_message(self, msg):
        if not self.client.kingdom_id:
            print('not in any kingdom')
            return
        self.client.post(
            action='editMapMarkers',
            controller='map',
            params={
                'fieldMessage': {
                    'cellId': self.id,
                    'duration': 48,
                    'targetId': 0,
                    'text': msg,
                    'type': 2
                },
                'markers': []
            }
        )


class Map:
    """a container for cell object on gameworld"""
    def __init__(self, client, data=None):
        self.client = client
        self._data = data or dict()

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(list(self._data.keys()))

    def __repr__(self):
        return f'{type(self).__name__}({dict(self._data.items())})'

    def pull(self):
        """git pull like function for pulling map data from server"""
        req_list = list()
        for x in range(-13, 14):
            for y in range(-13, 14):
                req_list.append(vid(x, y))
        r = self.client.map.getByRegionIds(
            {
                'regionIdCollection': {
                    '1': req_list
                }
            }
        )
        for vids in r['response']['1']['region']:
            for result in r['response']['1']['region'][vids]:
                id = int(result['id'])
                self.__setitem__(fishout(id), Cell(self.client, id, result))

    def coordinate(self, x, y):
        return self._data[(x, y)]

    @property
    def color_list(self):
        for color in COLOR:
            print(f'{color}')

    def _filter(self, group):
        results = dict()
        for coord in self._data.keys():
            try:
                test = self._data[coord][group]
                results[coord] = self._data[coord]
            except KeyError:
                continue
        return results

    def oasis(self):
        return Map(self.client, self._filter('oasis'))

    def tiles(self):
        return Map(self.client, self._filter('resType'))
