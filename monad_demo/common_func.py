import json
import os


def get_dict_obj(config, key, create=False, separator='/'):
    current = config

    for next in key.split(separator):
        if not next:
            continue
        elif next[0] != "_" and hasattr(current, next):
            current = getattr(current, next)
        elif isinstance(current, dict) and \
                dict.__contains__(current, next):
            current = current[next]
        elif create:
            newdict = {}
            current[next] = newdict
            current = newdict
        else:
            return None
    return current


def createJsonFile(contents_dict, contents_file, read_only=True, pretty=False):
    try:
        if os.path.exists(contents_file):
            os.chmod(contents_file, 0777)

        out_file = open(contents_file, 'w')

        if pretty:
            str_json = json.dumps(contents_dict, indent=4, sort_keys=True)
        else:
            str_json = json.dumps(contents_dict)

        out_file.write(str_json)
        out_file.close()
        if read_only:
            os.chmod(contents_file, 0400)

    except Exception:
        raise

    return contents_file
