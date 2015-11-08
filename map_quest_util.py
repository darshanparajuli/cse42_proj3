# Darshan Parajuli 16602518
# ICS 32 Fall 2015
# Project 3


import urllib.parse
import urllib.request
import urllib.error
import json


'''
Private constants
'''
_CONSUMER_KEY = 'hF8WB1XSFN6nGVl5LhXeL9uYwVBUkFMG'
_CONSUMER_SECRET = 'nH7pkK7f0oCh77hb'


class MapQuestAPI(object):

    _BASE_URL = 'http://open.mapquestapi.com'

    # Private method
    def _build_url(self, path, query_params):
        return MapQuestAPI._BASE_URL + path + '?' + urllib.parse.urlencode(query_params)

    def _get_result(self, url) -> 'Dictionary object':
        response = None
        try:
            response = urllib.request.urlopen(url)
            json_text = response.read().decode(encoding = 'utf-8')

            return json.loads(json_text)
        except (urllib.error.URLError, urllib.error.ContentTooShortError, ValueError):
            return None
        finally:
            if response != None:
                response.close()


class MapQuestDirectionAPI(MapQuestAPI):

    _URL_PATH = '/directions/v2/route'

    def __init__(self, locations: [str]):
        self.locations = locations

    def get_result(self) -> 'Dictionary object':
        return self._get_result(self._build_this_url())

    def _build_this_url(self):
        query_params = [
            ('key', _CONSUMER_KEY),
            ('from', self.locations[0]),
        ]

        for location in self.locations[1:]:
            query_params.append(('to', location))

        return self._build_url(MapQuestDirectionAPI._URL_PATH, query_params)


class MapQuestElevationAPI(MapQuestAPI):

    _URL_PATH = '/elevation/v1/profile'

    def __init__(self, lat_lng: ('latitudes', 'longitutes')):
        self.lat_lng = lat_lng

    def get_result(self) -> 'Dictionary object':
        return self._get_result(self._build_this_url())

    def _build_this_url(self):
        lat_lng_value = '{},{}'.format(self.lat_lng[0], self.lat_lng[1])

        query_params = [
            ('key', _CONSUMER_KEY),
            ('shapeFormat', 'raw'),
            ('latLngCollection', lat_lng_value),
            ('unit', 'f')
        ]

        return self._build_url(MapQuestElevationAPI._URL_PATH, query_params)
