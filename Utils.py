class Utils:
    def __int__(self):
        pass

    @staticmethod
    def get_length_without_measure(string_value):
        if "km" in string_value:
            value = int(string_value[:string_value.rfind('k')]) * 1000
        else:
            value = int(string_value[:string_value.rfind('m')])
        return value

    @staticmethod
    def get_time_from_string(string_value):
        if "day" in string_value:
            if "hour" in string_value:
                time = int(string_value[:(string_value.rfind('d') - 1)]) * 24 * 60 + int(string_value[(string_value.rfind('y') + 2):(string_value.rfind('h') - 1)]) * 60
            else:
                time = int(string_value[:(string_value.rfind('d') - 1)]) * 24 * 60
        elif "hour" in string_value:
            if "min" in string_value:
                time = int(string_value[:(string_value.rfind('h') - 1)]) * 60 + int(string_value[(string_value.rfind('r') + 2):(string_value.rfind('m') - 1)])
            else:
                time = int(string_value[:(string_value.rfind('h') - 1)]) * 60
        else:
            time = int(string_value[(string_value.rfind('m') - 4):(string_value.rfind('m') - 1)])
        return time