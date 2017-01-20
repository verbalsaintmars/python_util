# Copyright (c) 2015 VMware, Inc. All Rights Reserved.


class AtomicCounter(object):
    """ Atomic Counter
    1. add / sub have to be a 'add happen before sub' pair relation.
    2. breaking rule 1., the minimum value of the counter is 0.
    """
    def __init__(self):
        self._fake_atomic_variable = []

    def add(self):
        # atomic operation.
        self._fake_atomic_variable.append(None)

    def sub(self):
        try:
            # atomic operation.
            self._fake_atomic_variable.pop()
        except IndexError:
            pass

    def reset(self):
        # atomic operation.
        self._fake_atomic_variable[0:] = []

    def value(self):
        # len as an atomic operation.
        return len(self._fake_atomic_variable)
