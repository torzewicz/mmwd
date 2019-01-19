import json


class User:
    def __init__(self, house, modes, hours_per_day, number_of_days, max_amount_of_money, time_value, places):
        self.house = house
        self.modes = modes
        self.hours_per_day = hours_per_day
        self.number_of_days = number_of_days
        self.max_amount_of_money = max_amount_of_money
        self.time_value = time_value
        self.places = places

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)