import json


def create_json(input):
    return json.load(input)


def extract_value(expect_keys, json_dict):
    """
    expect_keys: tuple , e.g ("nodeuser", "user")
    return: None if no value, else value
    """
    temp_val = json_dict.get(expect_keys[0])

    if isinstance(temp_val, dict) and len(expect_keys) > 1:
        return extract_value(expect_keys[1:], temp_val)
    elif len(expect_keys) > 1:
        return None
    else:
        return temp_val
