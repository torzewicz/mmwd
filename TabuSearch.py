import json
from Distance import Distance
from utils import *
import itertools
import math
import time


class TabuSearch:
    def __init__(self, user, places, g_maps, max_tabu_size, max_combinations):
        self.user = user
        self.places = places
        self.places_sequence_distance_objects = []
        self.g_maps = g_maps
        self.places_sequence_names = []
        self.final_combination = []
        self.tabu_list = []
        self.max_tabu_size = max_tabu_size
        self.distance_dictionary = {self.user.house: {}}
        self.max_combinations = max_combinations
        self.final_cost = None

        print("Collecting data from Google")
        current_data = 0
        collecting_data_time = pow(len(self.places), 2)
        for place in self.places:
            current_data += 1
            self.distance_dictionary[self.user.house][place.name] = Distance(self.user.house, place.name, self.user.modes, self.g_maps)
            print(str(math.floor(current_data*100/collecting_data_time)) + "%")
        for place in self.places:
            self.distance_dictionary[place.name] = {}
            for place2 in self.places:
                if place.name != place2.name:
                    current_data += 1
                    self.distance_dictionary[place.name][place2.name] = Distance(place.name, place2.name, self.user.modes, self.g_maps)
                    print(str(math.floor(current_data * 100 / collecting_data_time)) + "%")
        print("Done")
        print("Wait for the tabu search algorithm to finish")

    def calculate_function(self, distance_sequence):
        minimum_value = math.inf
        final_combination = []
        all_possible_combinations = list(itertools.product(self.user.modes, repeat=len(distance_sequence)))
        for max_combination in range(0, min(self.max_combinations, len(all_possible_combinations))):
            index = get_random_index(len(all_possible_combinations) - 1)
            combination = all_possible_combinations[index]
            value = 0
            time_value = 0
            cost = 0
            for i in range(0, len(distance_sequence)):
                time_and_distance = get_time_and_distance_for_mode(distance_sequence[i], combination[i])
                if time_and_distance['distance'] == math.inf:
                    value += math.inf
                else:
                    value += (time_and_distance['time'] + calculate_cost(combination[i], time_and_distance['distance'])/float(self.user.time_value))*(0.4 + 0.1 * get_transport_value(combination[i]))
                    time_value += time_and_distance['time']
                    cost += calculate_cost(combination[i], time_and_distance['distance'])
            if value < minimum_value:
                minimum_value = value
                final_combination = combination
                final_time = time_value + int(self.user.time_per_place) * (len(distance_sequence) + 1) * 60
                final_cost = cost
        return {
            'minimum_value': minimum_value,
            'final_combination': final_combination,
            'final_time': final_time,
            'final_cost': final_cost,
            'names_list': create_names_list(distance_sequence)
        }

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
        first_attempt = self.calculate_function(self.places_sequence_distance_objects)
        self.final_combination = first_attempt['final_combination']
        final_list = self.places_sequence_names.copy()

        best_solution = final_list
        best_candidate = final_list
        tabu_list = [final_list]
        iterator = 0
        start_time = time.time()
        function_for_best_solution = self.calculate_function(self.create_distance_list(best_solution))

        file_is_created = False
        index = 0
        while not file_is_created:
            try:
                file = open('data/data_file' + str(self.max_combinations) + "_" + str(self.max_tabu_size) + "v" + str(index) + ".csv", 'r')
                file.close()
            except FileNotFoundError:
                file = open('data/data_file' + str(self.max_combinations) + "_" + str(self.max_tabu_size) + "v" + str(index) + ".csv", 'a')
                file_is_created = True
            index += 1

        file.write("time,function_value\n")

        stopping_condition = False

        while not stopping_condition:
            function_for_best_candidate = self.calculate_function(self.create_distance_list(best_candidate))
            solution_neighborhood = get_random_neighborhood(best_candidate)
            for solution_candidate in solution_neighborhood:
                function_for_solution_candidate = self.calculate_function(self.create_distance_list(solution_candidate))
                if solution_candidate not in tabu_list and function_for_solution_candidate['minimum_value'] < function_for_best_candidate['minimum_value']:
                    function_for_best_candidate = function_for_solution_candidate
                    best_candidate = function_for_best_candidate['names_list']
            if function_for_best_candidate['minimum_value'] < function_for_best_solution['minimum_value']:
                function_for_best_solution = function_for_best_candidate
                best_solution = function_for_best_solution['names_list']
                iterator = 0
            file.write(str(time.time() - start_time) + "," + str(function_for_best_solution['minimum_value']) + "\n")
            iterator += 1
            tabu_list.append(best_candidate)
            if len(tabu_list) > self.max_tabu_size:
                tabu_list.pop(0)
            if iterator >= 5 and function_for_best_solution['final_cost'] > float(self.user.max_amount_of_money):
                found_first_item = False
                index = 0
                while not found_first_item:
                    if self.places[index].name in best_candidate:
                        minimum_priority = self.places[index]
                        found_first_item = True
                    else:
                        index += 1
                for i in range(index, len(self.places) - 1):
                    if int(minimum_priority.priority) > int(self.places[i].priority) and self.places[i] in best_candidate:
                        minimum_priority = self.places[i]
                best_candidate.remove(minimum_priority.name)
                iterator = 0
            if iterator >= 10:
                stopping_condition = True

        final = function_for_best_candidate
        self.places_sequence_names = best_solution
        self.places_sequence_distance_objects = self.create_distance_list(best_solution)
        self.tabu_list = tabu_list
        self.final_combination = final['final_combination']
        self.final_cost = final['final_cost']
        file.close()

    def find_minimum(self, start_point, possibilities):
        minimum = self.distance_dictionary[start_point][possibilities[0].name]
        for i in range(1, len(possibilities)):
            current_distance_object = self.distance_dictionary[start_point][possibilities[i].name]
            if get_length_without_measure(current_distance_object.custom_length) < get_length_without_measure(minimum.custom_length):
                minimum = current_distance_object
        return minimum

    def create_distance_list(self, names_list):
        distance_list = []
        for i in range(0, len(names_list) - 1):
            distance_list.append(self.distance_dictionary[names_list[i]][names_list[i+1]])
        return distance_list

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)
