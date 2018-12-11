import googlemaps
from Distance import Distance

gMaps = None
while gMaps is None:
    try:
        gMaps = googlemaps.Client(key=input('Provide Google key: '))
    except:
        print("Please provide valid Google key.")

start = input('Type starting point: ')
end = input('Type destination: ')

print(Distance(start, end, gMaps).to_json())
