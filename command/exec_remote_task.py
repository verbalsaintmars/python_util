#!/usr/bin/env python
import multiprocessing


# nimbula modules
from nimbula.admin.nimbulaexec import NimbulaExec


# global variables
cpu_count = multiprocessing.cpu_count()
thread_threshhold_fold = 4


def get_nimbula_exec(siteuser_name, siteuser_pass,
                     nodeuser_name, nodeuser_pass,
                     api_address):
    client = NimbulaExec()
    client.user = siteuser_name
    client.password = siteuser_pass
    client.nodeuser = nodeuser_name
    client.nodepass = nodeuser_pass
    client.threads = cpu_count * thread_threshhold_fold
    client.address = api_address
    return client


def process_execute_result(result):
    failed = []
    succeeded = []
    unreachable = []
    for k, v in result.items():
        if v is None:
            unreachable.append(k)
            continue
        if v.failed:
            failed.append(k)
        else:
            succeeded.append(k)
    return succeeded, failed, unreachable
