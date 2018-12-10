import json


class Distance:
    def __init__(self, start_point, end_point, gMaps):
        modes = ['driving', 'walking', 'bicycling', 'transit']
        for i in modes:
            try:
                current_mode = gMaps.directions(start_point, end_point, mode=i)[0]['legs'][0]
                setattr(self, i, {
                    "distance": current_mode['distance']['text'],
                    "duration": current_mode['duration']['text']
                }
                        )
            except:
                setattr(self, i, {
                    "distance": "No data",
                    "duration": "No data"
                }
                        )

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
