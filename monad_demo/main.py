#! /bin/env python
import argparse
import json
import sys

from generate_config import key_monad
from generate_config import generate_config

JSON_FILE = "fun_json.json"

GATEWAY_KEY = (
    'install_json/default_ilom_user',
    'install_json/default_ilom_password',
    'install_json/controlplane_subnet',
    'install_json/site_name',
    'install_json/seed_ilom',
    'install_json/seed_gateway',
    'install_json/seed_ip_addr',
    'install_json/root_user',
    'install_json/root_password',
    'install_json/external_dns',
    'install_json/nodeuser',
    'gateway/gateway_node_iloms')


def get_json(filename):
    with open(filename, 'r') as fd:
        try:
            j = json.load(fd)
            yield j
        except:
            pass


def printout(monad, validate=None):

    if validate is not None:
        not_valid_keys = monad.apply_validate(validate)
    else:
        not_valid_keys = monad.apply_validate()

    keys = monad.key
    result = monad.result
    str_json = json.dumps(result, indent=4, sort_keys=True)
    eg = getattr(monad, "eg", None)

    FORMAT = "Example {EG}\n\n" \
        "Keys:\n{KEYS}\n\nInvalid keys:\n{INVALID}\n\nResult:\n{result}"

    print(FORMAT.format(
        EG=eg, KEYS=keys, result=str_json, INVALID=not_valid_keys))


# example 1
def example_1(j):
    """
    Extract site_conf
    """
    site_conf = key_monad("install_json/siteconf", j)
    site_conf.eg = 1
    printout(site_conf)


# example 2
def example_2(j):
    """
    Extract site_conf, install_json, aggregate both.
    """
    site_conf = key_monad("install_json/siteconf", j)
    install_json = key_monad("install_json", j)
    result = site_conf.apply(install_json)
    result.eg = 2
    printout(result)


# example 3
def example_3(j):
    """
    Generate gateway podconfig.
    """
    gateway = generate_config(j, GATEWAY_KEY)
    gateway.eg = 3
    printout(gateway)


# example 4
def example_4(j):
    """
    Aggretage more...
    """
    gateway = generate_config(j, GATEWAY_KEY)
    nfs_location = key_monad("nfs_location", j)
    result = nfs_location.apply(gateway)
    result.eg = 4
    printout(result)


# example 5
def example_5(j):
    """
    Aggretage somethine does not exist...
    """
    gateway = generate_config(j, GATEWAY_KEY)
    nfs_location = key_monad("nfs_location", j)
    not_exist = key_monad("not_exist/hahaha", j)
    nfs_and_gateway = nfs_location.apply(gateway)
    result = nfs_and_gateway.apply(not_exist)
    result.eg = 5
    printout(result)


# example 6
def example_6(j):
    """
    Aggretage multiple times...
    """
    nfs_location_1 = key_monad("nfs_location", j)
    nfs_location_2 = key_monad("nfs_location", j)
    result = nfs_location_1.apply(nfs_location_2)
    result.eg = 6
    printout(result)


# example 7
def example_7(j):
    """
    Customize validator...
    """
    def check_has_iso(key, result):
        if key == "nfs_location":
            if "iso" in result[key]:
                return []
            else:
                return [key]

    nfs_location_1 = key_monad("nfs_location", j)
    nfs_location_1.eg = 7
    printout(nfs_location_1, check_has_iso)


def opt_parser():
    parser = argparse.ArgumentParser(
        description='{0} argument parser'.format(sys.argv[0]),
        epilog="monad example script.")

    parser.add_argument('-eg', metavar='example number', type=int,
                        default=1,
                        dest='eg',
                        help='example number to run')
    global argument
    argument = parser.parse_args()


if __name__ == "__main__":
    opt_parser()
    j = next(get_json(JSON_FILE))
    examples = {1: example_1,
                2: example_2,
                3: example_3,
                4: example_4,
                5: example_5,
                6: example_6,
                7: example_7}[argument.eg](j)
