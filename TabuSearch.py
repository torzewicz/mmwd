import json
from Distance import Distance
from Utils import Utils
import itertools
import math


class TabuSearch:
    def __init__(self, user, places, g_maps):
        self.user = user
        self.places = places
        self.places_sequence_distance_objects = []
        self.g_maps = g_maps
        self.places_sequence_names = []
        self.final_combination = []

    def calculate_function(self, distance_sequence):
        minimum_value = math.inf
        final_combination = []
        all_possible_combinations = list(itertools.product(self.user.modes, repeat=len(distance_sequence)))
        for combination in all_possible_combinations:
            value = 0
            for i in range(0, len(distance_sequence)):
                time_and_distance = self.get_time_and_distance_for_mode(distance_sequence[i], combination[i])
                value += (time_and_distance['time'] + self.calculate_cost(combination[i], time_and_distance['distance'])/float(self.user.time_value))*(0.4 + 0.1 * self.get_transport_value(combination[i]))
            if value < minimum_value:
                minimum_value = value
                final_combination = combination
        return {
            'minimum_value': minimum_value,
            'final_combination': final_combination
        }

    @staticmethod
    def get_time_and_distance_for_mode(distance, mode):
        road_duration = Utils.get_time_from_string(getattr(distance, mode)['duration'])
        road_distance = Utils.get_length_without_measure(getattr(distance, mode)['distance'])
        return {
            'time': road_duration,
            'distance': road_distance
        }

    @staticmethod
    def calculate_cost(mode, distance):
        value = {
            'driving': distance/100 * 8 * 3,
            'walking': 2,
            'bicycling': 30,
            'transit': 30
        }
        return value.get(mode)

    @staticmethod
    def get_transport_value(mode):
        value = {
            'driving': 1,
            'walking': 5,
            'bicycling': 6,
            'transit': 6
        }
        return value.get(mode)

    def perform_search(self):
        # first attempt - append points by their distance to each other
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

        # start tabu search
        road_weight = self.calculate_function(self.places_sequence_distance_objects)['minimum_value']
        final_list = self.places_sequence_names.copy()
        for i in range(1, len(self.places_sequence_names) - 1):
            for j in range(i + 1, len(self.places_sequence_names)):
                new_list = self.places_sequence_names.copy()
                new_list[i], new_list[j] = new_list[j], new_list[i]
                calculate_new_list = self.calculate_function(self.create_distance_list(new_list))
                if calculate_new_list['minimum_value'] < road_weight:
                    road_weight = calculate_new_list['minimum_value']
                    self.final_combination = calculate_new_list['final_combination']
                    final_list = new_list

        self.places_sequence_names = final_list
        self.places_sequence_distance_objects = self.create_distance_list(final_list)

    def find_minimum(self, start_point, possibilities):
        minimum = Distance(start_point, possibilities[0].name, self.user.modes, self.g_maps)
        for i in range(1, len(possibilities)):
            current_distance_object = Distance(start_point, possibilities[i].name, self.user.modes, self.g_maps)
            if Utils.get_length_without_measure(current_distance_object.custom_length) < Utils.get_length_without_measure(minimum.custom_length):
                minimum = current_distance_object
        return minimum

    def create_distance_list(self, names_list):
        distance_list = []
        for i in range(0, len(names_list) - 1):
            distance_list.append(Distance(names_list[i], names_list[i+1], self.user.modes, self.g_maps))
        return distance_list

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)
