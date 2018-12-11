import json


class Distance:
    def __init__(self, start_point, end_point, gMaps):
        modes = ['driving', 'walking', 'bicycling', 'transit']
        attributes = ['distance', 'duration']
        for i in modes:
            for a in attributes:
                try:
                    current_mode = gMaps.directions(start_point, end_point, mode=i)[0]['legs'][0][a]['text']
                except:
                    current_mode = "No data"
                if hasattr(self, i):
                    getattr(self, i)[a] = current_mode
                else:
                    setattr(self, i, {
                        a: current_mode
                    }
                            )

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
