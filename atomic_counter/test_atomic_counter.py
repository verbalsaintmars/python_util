# Copyright (c) 2015 VMware, Inc. All Rights Reserved.
import threading
import unittest

from hamcrest import *  # noqa

from common.atomic_counter import AtomicCounter


class TestAtomicCounter(unittest.TestCase):
    def test_atomic_counter(self):
        """ Test AtomicCounter functionality
        """
        counter = AtomicCounter()

        threads = []

        def add():
            counter.add()

        def sub():
            counter.sub()

        # test concurrent pair add / sub, counter's value should be 0.
        def test_run_1():
            add()
            sub()

        for i in xrange(999):
            t = threading.Thread(target=test_run_1)
            t.start()
            threads.append(t)

        for i in threads:
            i.join()

        assert_that(counter.value(), equal_to(0))

        threads[0:] = []

        # test concurrent pair add / sub, and sub is 10 less then add,
        # counter's value should be 10.
        def test_run_2():
            add()

        def test_run_3():
            sub()

        for i in xrange(500):
            t = threading.Thread(target=test_run_2)
            t.start()
            threads.append(t)

        for i in threads:
            i.join()

        threads[0:] = []

        for i in xrange(490):
            t = threading.Thread(target=test_run_3)
            t.start()
            threads.append(t)

        for i in threads:
            i.join()

        assert_that(counter.value(), equal_to(10))
