import googlemaps


def startup():
    global g_maps
    g_maps = None
    while g_maps is None:
        try:
            g_maps = googlemaps.Client(key=input('Provide Google key: '))
        except:
            print("Please provide valid Google key.")

    print("\"Czas to pieniadz\" app initialization\n")


startup()