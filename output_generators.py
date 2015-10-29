from map_quest_util import MapQuestDirectionAPI
from map_quest_util import MapQuestElevationAPI
import multiprocessing
from concurrent.futures import ThreadPoolExecutor


# Private constants
_STEPS = 'STEPS'
_TOTAL_DISTANCE = 'TOTALDISTANCE'
_TOTAL_TIME = 'TOTALTIME'
_LAT_LONG = 'LATLONG'
_ELEVATION = 'ELEVATION'


class OutputGenerators(object):

    def __init__(self, locations: str):
        self.locations = locations
        self.output_generators = {}
        self.location_info = self._get_location_info()
        
    def get_ouput_generator(self, output_generator_type: str) -> 'Output generator object':
        # get cached output generator if available
        output_generator = self.output_generators.get(output_generator_type, None)

        if output_generator == None:
            if output_generator_type == _STEPS:
                output_generator = StepsOutputGenerator(self.location_info)
            elif output_generator_type == _TOTAL_DISTANCE:
                output_generator = TotalDistanceOutputGenerator(self.location_info)
            elif output_generator_type == _TOTAL_TIME:
                output_generator = TotalTimeOutputGenerator(self.location_info)
            elif output_generator_type == _LAT_LONG:
                output_generator = LatLongOutputGenerator(self.location_info)
            else:
                output_generator = ElevationOutputGenerator(self._get_all_elevation_info())

            # cache the output generator in case it's needed more than once to improve performance
            self.output_generators[output_generator_type] = output_generator

        return output_generator
        
    def _get_location_info(self):
        map_quest_direction_api = MapQuestDirectionAPI(self.locations)
        return map_quest_direction_api.get_result()
    
    def _get_all_elevation_info(self):
        lat_lngs = []

        # multithread the calls to MapQuestElevationAPI to improve performance
        executor = ThreadPoolExecutor(max_workers = multiprocessing.cpu_count())
        result = executor.map(self._get_elevation_info, self.location_info['route']['locations'])

        for element in result:
            lat_lngs.append(element)

        return lat_lngs

    def _get_elevation_info(self, location):
        lat_lng = location['latLng']
        map_quest_elevation_api = MapQuestElevationAPI((lat_lng['lat'], lat_lng['lng']))
        return map_quest_elevation_api.get_result()
    
    # Static method
    def is_valid_output_generator(output_generator: str) -> bool:
        valid_ouput_generators = [_STEPS, _TOTAL_DISTANCE, _TOTAL_TIME, _LAT_LONG, _ELEVATION]
        return output_generator in valid_ouput_generators
    

class OutputGenerator(object):

    def __init__(self, response: 'response in a dictionary object form'):
        self.response = response

    def _get_error(self, response = None) -> str:
        if response == None:
            response = self.response

        statuscode = response['info']['statuscode']
        if statuscode != 0:
            if statuscode == 403 or statuscode == 500:
                return 'MAPQUEST ERROR'
            else:
                return 'NO ROUTE FOUND'
        else:
            return ''
        
    
class StepsOutputGenerator(OutputGenerator):

    def get_output(self) -> [str]:
        output = ['']
        
        error = self._get_error()
        if error == '':
            output.append('DIRECTIONS')
            legs = self.response['route']['legs']
            for leg in legs:
                for maneuver in leg['maneuvers']:
                    output.append(maneuver['narrative'])
        else:
            output.append(error)

        return output

    
class TotalDistanceOutputGenerator(OutputGenerator):

    def get_output(self) -> [str]:
        output = ['']
        
        error = self._get_error()
        if error == '':
            distance = round(self.response['route']['distance'])
            output.append('TOTAL DISTANCE: {} mile{}'.format(distance, 's' if distance > 1 else ''))
        else:
            output.append(error)

        return output

    
class TotalTimeOutputGenerator(OutputGenerator):

    def get_output(self) -> [str]:
        output = ['']
        
        error = self._get_error()
        if error == '':
            time = round(self.response['route']['time'] / 60.0)
            output.append('TOTAL TIME: {} minutes{}'.format(time, 's' if time > 1 else ''))
        else:
            output.append(error)

        return output

    
class LatLongOutputGenerator(OutputGenerator):

    def get_output(self) -> [str]:
        output = ['']
        
        error = self._get_error()
        if error == '':
            output.append('LATLONGS')
            for location in self.response['route']['locations']:
                lat_lng = location['latLng']
                lat = lat_lng['lat']
                lng = lat_lng['lng']
                output.append('{:.2f}{} {:.2f}{}'.format(abs(lat), 'N' if lat >= 0 else 'S', abs(lng), 'E' if lng >= 0 else 'W'))
        else:
            output.append(error)

        return output
        
    
class ElevationOutputGenerator(OutputGenerator):

    def get_output(self) -> [str]:
        output = ['']

        valid_responses = []
        for response in self.response:
            error = self._get_error(response)
            if error == '':
                valid_responses.append(response)
            else:
                output.append(error)
                
        if len(valid_responses) > 0:
            output.append('ELEVATIONS')
            for response in valid_responses:
                for elevation_profile in response['elevationProfile']:
                    output.append(round(elevation_profile['height']))

        return output
