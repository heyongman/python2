def init():
    global _global_dict
    _global_dict = {}


def set_value(value):
    _global_dict['_value'] = value


def get_value():
    return _global_dict.get('_value', [])

