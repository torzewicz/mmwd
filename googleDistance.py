import googlemaps

key = input('Provide Google key: ')

gMaps = googlemaps.Client(key=key)

start = input('Type starting point: ')
end = input('Type destination: ')
mode = ""

while mode != 'driving' and mode != 'walking' and mode != 'bicycling' and mode != 'transit':
    mode = input('Type one of the mode (driving/walking/bicycling/transit): ')

directions = gMaps.directions(start, end, mode=mode)
distance = directions[0]['legs'][0]['distance']['text']
duration = directions[0]['legs'][0]['duration']['text']
print("Distance: " + distance)
print("Duration: " + duration)