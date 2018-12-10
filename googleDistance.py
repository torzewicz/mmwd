import googlemaps
from Distance import Distance

gMaps = None
while gMaps is None:
    try:
        key = input('Provide Google key: ')
        gMaps = googlemaps.Client(key=key)
    except:
        print("Please provide valid Google key.")

start = input('Type starting point: ')
end = input('Type destination: ')

print(Distance(start, end, gMaps).to_json())
