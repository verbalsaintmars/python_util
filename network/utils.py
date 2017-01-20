import socket
import string


# offset between two ip_address
def ip_dist(a, b):
    def to_num(addr):
        # parse the address string into integer quads
        quads = map(ord, socket.inet_aton(addr))
        # spread the quads out
        return reduce(lambda x, y: x * 0x10000 + y, quads)
    return abs(to_num(a) - to_num(b))


def ip_cmp(ip1, ip2):
    parts1 = map(lambda x: int(x), string.split(ip1, '.'))
    parts2 = map(lambda x: int(x), string.split(ip2, '.'))
    comparisons = map(lambda x, y: cmp(x, y), parts1, parts2)
    return reduce(lambda x, y: x or y, comparisons)
