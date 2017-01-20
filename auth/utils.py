import tempfile
import os
import stat


class GenPassFileException(Exception):
    pass


def generate_pass_file(password):
    temp_pass_filename = next(tempfile._get_candidate_names())

    try:
        with open(temp_pass_filename, 'w') as fd:
            fd.write(password)
        os.chmod(temp_pass_filename, stat.S_IRUSR)
    except Exception:
        raise GenPassFileException
    else:
        return temp_pass_filename


def remove_pass_file(filename):
    try:
        os.remove(filename)
    except:
        pass
