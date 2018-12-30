import json


class Place:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)