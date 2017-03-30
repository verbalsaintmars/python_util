#!/usr/bin/env python
import argparse
import logging

import sys
from multiprocessing import Pool

from contextlib import contextmanager
from oracle.cloud.compute.tools.ilom import Ilom

log = logging.getLogger(__name__)

DEFAULT_ILOM_CONNECT_TIMEOUT = 60  # in seconds


def _ilom_connect(
        ip,
        username,
        password,
        timeout=DEFAULT_ILOM_CONNECT_TIMEOUT):
    """Connect to Ilom"""
    log.info('Connecting to {0}'.format(ip))
    try:
        ilom = Ilom(ip, username, password,
                    log, timeout)
    except Exception as e:
        log.error('Error connecting to ILOM: {0}'.format(e))
        raise
    return ilom


def _ilom_disconnect(ilom):
    """Disconnect from Ilom"""
    ilom.logout()


@contextmanager
def ilom_connection(
        ip,
        username,
        password,
        timeout=DEFAULT_ILOM_CONNECT_TIMEOUT):
    """Context manager for Ilom connections"""
    ilom = None

    try:
        ilom = _ilom_connect(
            ip,
            username,
            password,
            timeout=timeout)
        yield ilom
    finally:
        if ilom:
            _ilom_disconnect(ilom)


def opt_parser():
    parser = argparse.ArgumentParser(
        description='{0} argument parser'.format(sys.argv[0]),
        epilog="ilom type check.")

    parser.add_argument('-p', metavar='ilom password', type=str,
                        default='ADMIN000',
                        dest='password',
                        help='ilom password')
    parser.add_argument('-u', metavar='ilom user', type=str,
                        default='ADMIN',
                        dest='user',
                        help='ilom user')
    parser.add_argument('nodes', metavar='ilom nodes', type=str, nargs='+',
                        help='ilom nodes')
    global arg
    arg = parser.parse_args()


OUTPUT_TMP = "{0} is of type {1}"


def check_ilom(ilom):
    param = (ilom,
             arg.user,
             arg.password)
    with ilom_connection(*param) as i:
        if hasattr(i, "has_host_storage_device"):
            if i.has_host_storage_device():
                print(OUTPUT_TMP.format(ilom, "X5"))
            else:
                print(OUTPUT_TMP.format(ilom, "X4 or earlier type."))
        if hasattr(i, "model"):
            print(OUTPUT_TMP.format(ilom, i.model()))


if __name__ == "__main__":
    opt_parser()
    pool = Pool()  # by default using multiprocessing.cpu_count()
    pool.map(check_ilom, arg.nodes)
