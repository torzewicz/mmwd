import json
from Distance import Distance
from Utils import Utils


class TabuSearch:
    def __init__(self, user, places, g_maps):
        self.user = user
        self.places = places
        self.places_sequence_distance_objects = []
        self.g_maps = g_maps
        self.places_sequence_names = []

    def calculate_function(self):
        value = 0

        for road in self.places_sequence_distance_objects:
            best_fit = self.find_best_time_and_its_distance(road)
            value += (best_fit['time'] + self.calculate_cost(best_fit['mean_of_transport'], best_fit['distance'])/float(self.user.time_value))*(0.4 + 0.1 * self.get_transport_value(best_fit['mean_of_transport']))
        return value

    def find_best_time_and_its_distance(self, distance):
        all_modes = self.user.modes
        minimum = Utils.get_time_from_string(getattr(distance, all_modes[0])['duration'])
        mean_of_transport = all_modes[0]

        for i in range(1, len(all_modes)):
            if getattr(distance, all_modes[i])['duration'] != 'No data' and Utils.get_time_from_string(getattr(distance, all_modes[i])['duration']) < minimum:
                minimum = Utils.get_time_from_string(getattr(distance, all_modes[i])['duration'])
                mean_of_transport = all_modes[i]

        road_distance = Utils.get_length_without_measure(getattr(distance, mean_of_transport)['distance'])
        return {
            'mean_of_transport': mean_of_transport,
            'time': minimum,
            'distance': road_distance
        }

    @staticmethod
    def calculate_cost(mode, distance):
        value = {
            'driving': distance/100 * 8 * 5,
            'walking': 0,
            'bicycling': 0,
            'transit': 3
        }
        return value.get(mode)

    @staticmethod
    def get_transport_value(mode):
        value = {
            'driving': 5,
            'walking': 4,
            'bicycling': 2,
            'transit': 2
        }
        return value.get(mode)

    def perform_search(self):
        first_move = True
        to_do_list = self.places.copy()
        while len(to_do_list) is not 0:
            if first_move:
                current_distance_object = self.find_minimum(self.user.house, to_do_list)
                self.places_sequence_names.append(self.user.house)
                first_move = False
            else:
                current_distance_object = self.find_minimum(self.places_sequence_distance_objects[-1].end, to_do_list)

            self.places_sequence_distance_objects.append(current_distance_object)
            self.places_sequence_names.append(current_distance_object.end)

            for i in range(len(to_do_list) - 1, -1, -1):
                if to_do_list[i].name == current_distance_object.end:
                    to_do_list.pop(i)

    def find_minimum(self, start_point, possibilities):
        minimum = Distance(start_point, possibilities[0].name, self.user.modes, self.g_maps)
        for i in range(1, len(possibilities)):
            current_distance_object = Distance(start_point, possibilities[i].name, self.user.modes, self.g_maps)
            if Utils.get_length_without_measure(current_distance_object.custom_length) < Utils.get_length_without_measure(minimum.custom_length):
                minimum = current_distance_object
        return minimum

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)
