import math
from random import randint


def get_length_without_measure(string_value):
    if "km" in string_value:
        value = float(string_value[:string_value.rfind('k')]) * 1000
    else:
        value = float(string_value[:string_value.rfind('m')])
    return value


def get_time_from_string(string_value):
    if "day" in string_value:
        if "hour" in string_value:
            time = int(string_value[:(string_value.rfind('d') - 1)]) * 24 * 60 + int(string_value[(string_value.rfind('y') + 2):(string_value.rfind('h') - 1)]) * 60
        else:
            time = int(string_value[:(string_value.rfind('d') - 1)]) * 24 * 60
    elif "hour" in string_value:
        if "min" in string_value:
            time = int(string_value[:(string_value.rfind('h') - 1)]) * 60 + int(string_value[(string_value.rfind('r') + 2):(string_value.rfind('m') - 1)])
        else:
            time = int(string_value[:(string_value.rfind('h') - 1)]) * 60
    else:
        time = int(string_value[:(string_value.rfind('m') - 1)])
    return time


def get_time_and_distance_for_mode(distance, mode):
    if getattr(distance, mode)['duration'] != "No data":
        road_duration = get_time_from_string(getattr(distance, mode)['duration'])
        road_distance = get_length_without_measure(getattr(distance, mode)['distance'])
    else:
        road_duration = math.inf
        road_distance = math.inf
    return {
        'time': road_duration,
        'distance': road_distance
    }


def calculate_cost(mode, distance):
    value = {
        'driving': distance/100000 * 12 * 8,
        'walking': 0.2,
        'bicycling': 2,
        'transit': 2
    }
    return value.get(mode)


def get_transport_value(mode):
    value = {
        'driving': 1,
        'walking': 0.5,
        'bicycling': 3.5,
        'transit': 3
    }
    return value.get(mode)


def get_random_neighborhood(best_candidate):
    neighborhood = []
    for i in range(0, randint(1, len(best_candidate))):
        new_list = best_candidate.copy()
        a, b = randint(1, len(best_candidate) - 1), randint(1, len(best_candidate) - 1)
        new_list[a], new_list[b] = new_list[b], new_list[a]
        neighborhood.append(new_list)
    return neighborhood


def get_random_index(max_index):
    return randint(0, max_index)


def create_names_list(distance_list):
    names_list = [distance_list[0].start]
    for i in range(0, len(distance_list)):
        names_list.append(distance_list[i].end)
    return names_list