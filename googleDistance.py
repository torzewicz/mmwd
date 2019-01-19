import googlemaps
from Place import Place
from User import User
from TabuSearch import TabuSearch
import time

gMaps = None
# places = []
places = [Place('New York Manhattan', '3', '1'), Place('New York Queens', '6', '1'), Place('New York Bronx', '6', '1'), Place('New York Kennedy Airport', '8', '1'), Place('New York Rikers Island', '7', '1')]
enough = False
available_modes = ['walking', 'transit', 'bicycling', 'driving']
wanted_modes = []
hours_per_day = None
number_of_days = None
max_amount_of_money = None
time_value = None

while gMaps is None:
    try:
        gMaps = googlemaps.Client(key=input('Provide Google key: '))
    except:
        print("Please provide valid Google key.")

print("Miejsc: " +  str(len(places)))
# house = input('Type starting (house) point: ')
#
# for mode in available_modes:
#     if input("Allow " + mode + " (yes/no)? ") == 'yes':
#         wanted_modes.append(mode)
#
# while hours_per_day is None:
#     hours = input("Provide maximum hours per day ")
#     if hours.isdigit() and 0 < int(hours) <= 24:
#         hours_per_day = int(hours)
#     else:
#         print("Wrong value")
#
# while number_of_days is None:
#     days = input("Provide maximum number of days ")
#     if days.isdigit() and 0 < int(days):
#         number_of_days = int(days)
#     else:
#         print("Wrong value")
#
#
# while max_amount_of_money is None:
#     money = input("Provide maximum amount of money to spend ")
#     if money.isdigit() and 0 < int(money):
#         max_amount_of_money = int(money)
#         currency = input("Type currency ")
#     else:
#         print("Wrong value")
#
# while time_value is None:
#     value = input("How much you value your hour in " + currency + " ? ")
#     if value.isdigit() and 0 < int(value):
#         time_value = int(value)
#     else:
#         print("Wrong value")
#
# while not enough:
#     place = input('Type destination: ')
#     priority = input('Priority (1 - 10): ')
#     time_there = input('Time there (in hours): ')
#     if not (priority.isdigit() and 1 <= int(priority) <= 10):
#         print("Wrong priority!")
#     else:
#         places.append(Place(place, priority, time_there))
#         next_place = input("Add next place (yes/no)? ")
#         if next_place != 'yes':
#             enough = True

user = User('New York Brooklyn', available_modes, '8', '3', '300', '6', places)
# user = User(house, wanted_modes, hours_per_day, number_of_days, max_amount_of_money, time_value, places, '1')

# print(user.to_json())
tabu = TabuSearch(user, places, gMaps, 60, 2000, 150)

start_time = time.time()
tabu.perform_search()
end_time = time.time() - start_time

# for place in tabu.places_sequence_distance_objects:
#     print(place.to_json())
    # print(tabu.get_time_and_distance_for_mode(place))


# print(tabu.calculate_function(tabu.places_sequence_distance_objects))
print(tabu.places_sequence_names)
print(tabu.final_combination)
print(tabu.final_cost)
# print(tabu.tabu_list)
print(tabu.final_time)
print(tabu.final_function_value)


# print(end_time)