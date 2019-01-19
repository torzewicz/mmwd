import json


class Place:
    def __init__(self, name, priority, time):
        self.name = name
        self.priority = priority
        self.time = time

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)