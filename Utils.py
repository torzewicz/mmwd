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