# Copyright (c) 2015 VMware, Inc. All Rights Reserved.
import threading
import unittest

from hamcrest import *  # noqa
from matchers import *  # noqa

from common.rwlock import RWLock


class TestRWLock(unittest.TestCase):
    def test_read_lock(self):
        rwlock = RWLock()

        threads = []

        def run():
            with rwlock.read_lock():
                assert_that(rwlock._writer[0], is_(False))
                assert_that(rwlock._read_count[0], greater_than(0))

        for i in xrange(1000):
            t = threading.Thread(target=run)
            t.start()
            threads.append(t)

        for i in threads:
            i.join()

        assert_that(rwlock._read_count[0], equal_to(0))

    def test_write_lock(self):
        rwlock = RWLock()
        threads = []
        data = {0: 0}

        def run():
            with rwlock.write_lock():
                assert_that(rwlock._writer[0], is_(True))
                data[0] += 1

        for i in xrange(1000):
            t = threading.Thread(target=run)
            t.start()
            threads.append(t)

        for i in threads:
            i.join()

        assert_that(data[0], equal_to(1000))
        assert_that(rwlock._writer[0], is_(False))

    def test_rwlock(self):
        """ Test RWLock functionality
        """
        class Producer(object):
            def __init__(self):
                self.data = {}
                self.data[0] = 1
                self.rwlock = RWLock()

            def produce(self):
                with self.rwlock.write_lock():
                    old = self.data
                    self.data = {}
                    self.data[0] = 42
                    old[0] = 2

            def consume_1(self):
                with self.rwlock.read_lock():
                    assert_that(self.data[0] == 1 or
                                self.data[0] == 42, is_(True))

            def consume_2(self):
                with self.rwlock.read_lock():
                    assert_that(self.data[0] == 1 or
                                self.data[0] == 42, is_(True))

        producer = Producer()
        threads = []
        stop_flag = False

        def run():
            while True:
                producer.consume_1()
                producer.consume_2()

                if stop_flag:
                    break

        for i in xrange(1000):
            t = threading.Thread(target=run)
            t.start()
            threads.append(t)

        producer.produce()
        stop_flag = True

        for i in threads:
            i.join()
