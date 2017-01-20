# Copyright (c) 2015 VMware, Inc. All Rights Reserved.

import threading


class base_lock(object):
    def __init__(self, writer, condition, read_count):
        self._writer = writer
        self._condition = condition
        self._read_count = read_count


class rlock(base_lock):
    def __init__(self, writer, condition, read_count, read_lock):
        super(rlock, self).__init__(writer, condition, read_count)
        self._read_lock = read_lock

    def __enter__(self):
        with self._condition:
            while self._writer[0]:
                self._condition.wait()
        with self._read_lock:
            self._read_count[0] += 1

    def __exit__(self, type, value, traceback):
        with self._read_lock:
            self._read_count[0] -= 1

            if self._read_count[0] == 0:
                with self._condition:
                    self._condition.notify_all()


class wlock(base_lock):
    def __init__(self, writer, condition, read_count, write_lock):
        super(wlock, self).__init__(writer, condition, read_count)
        self._write_lock = write_lock

    def __enter__(self):
        self._write_lock.acquire()
        self._writer[0] = True
        with self._condition:
            while self._read_count[0]:
                self._condition.wait()

    def __exit__(self, type, value, traceback):
        with self._condition:
            self._writer[0] = False
            self._condition.notify_all()

        self._write_lock.release()


class RWLock(object):
    def __init__(self):
        self._writer = [False]
        self._condition = threading.Condition()
        self._read_count = [0]
        self._read_lock = threading.Lock()
        self._write_lock = threading.Lock()

    def read_lock(self):
        return rlock(self._writer, self._condition,
                     self._read_count, self._read_lock)

    def write_lock(self):
        return wlock(self._writer, self._condition,
                     self._read_count, self._write_lock)
