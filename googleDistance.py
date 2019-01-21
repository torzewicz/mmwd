import googlemaps
from Place import Place
from User import User
from TabuSearch import TabuSearch
import time
import requests


gMaps = None

while gMaps is None:
    try:
        gMaps = googlemaps.Client(key=input('Provide Google key: '))
    except:
        print("Please provide valid Google key.")

request = requests.get('https://wzorek.jaom.pl/mmwd/jsonFile/jsonFile.txt?fbclid=IwAR2Ms6VYVYVQ-uCC4tZlk82WyfJTI2csOm4kWJzQhfme6L6vAyLcLb7suTA').json()

driving_data = request[0]

max_days = driving_data['days']
max_hours = driving_data['hours']
max_money = driving_data['money']
time_value = driving_data['hour_value']
is_bike = driving_data['bike']
is_car = driving_data['car']
is_bus = driving_data['bus']
places_names = request[1]['places']
priority_values = request[2]['priority_values']
time_in_places = request[3]['time_in_places']
start_index = request[4]['start_id']

available_modes = ['walking']
places = []
start_place_name = None
#
if is_bike:
    available_modes.append('bicycling')
if is_bus:
    available_modes.append('transit')
if is_car:
    available_modes.append('driving')

for i in range(len(places_names)):
    if i is not start_index:
        places.append(Place(places_names[i], priority_values[i], time_in_places[i]))
    else:
        start_place_name = places_names[i]

user = User(start_place_name, available_modes, max_hours, max_days, max_money, time_value, places)

tabu = TabuSearch(user, places, gMaps, 60, 500, 200)

start_time = time.time()
tabu.perform_search()
end_time = time.time() - start_time

print(tabu.places_sequence_names)
print(tabu.final_combination)
print(tabu.final_cost)
print(tabu.final_time)
print(tabu.final_function_value)

post_request = requests.post("https://wzorek.jaom.pl/mmwd/jsonFile/post.php", json={"data": {"places": tabu.places_sequence_names, "combination": tabu.final_combination, "price": tabu.final_cost, "time": tabu.final_time, "function_value": tabu.final_function_value}}, auth=('user', 'passwd'))
