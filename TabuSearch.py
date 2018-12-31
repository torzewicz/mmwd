import json
from Distance import Distance
from Utils import Utils


class TabuSearch:
    def __init__(self, user, places, g_maps):
        self.user = user
        self.places = places
        self.places_sequence = []
        self.g_maps = g_maps

    def calculate_function(self, time_value, places_sequence):
        value = 0
        for road in places_sequence:
            value += (road.time + road.cost/time_value)*(0.4 + 0.1 * self.get_transport_value(road.mode))
        return value

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
                first_move = False
            else:
                current_distance_object = self.find_minimum(self.places_sequence[-1].end, to_do_list)
            self.places_sequence.append(current_distance_object)

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
