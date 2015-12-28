from collections import Iterable
from functools import wraps

class Damage(object):
    def __init__(self, p=0.0, m=0.0):
        self.p = float(p)
        self.m = float(m)
    
    def __getitem__(self, index):
        if index == 0:
            return self.p
        elif index == 1:
            return self.m
        raise StopIteration

    def __add__(self, other):
        return Damage(self.p + other.p, self.m + other.m)

    def __sub__(self, other):
        return Damage(self.p - other.p, self.m - other.m)

    def __mul__(self, other):
        try:
            return Damage(self.p * other[0], self.m * other[1])
        except TypeError:
            return Damage(self.p * other, self.m * other)

    def __div__(self, other):
        try:
            return Damage(self.p / other[0], self.m / other[1])
        except TypeError:
            return Damage(self.p / other, self.m / other)

    def __neg__(self):
        return Damage(-self.p, -self.m)

    def __eq__(self, other):
        return self.p == other.p and self.m == other.m

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return '(%g, %g)' % (self.p, self.m)

    def __repr__(self):
        return 'Damage' + str(self)

    def __pow__(self, power):
        raise NotImplementedError('Damage ** not implemented')
    
def main():
    
    # tests
    att = Damage(12, 10)
    print att
    assert att == Damage(12, 10)
    for d in att:
        print d
    print att * Damage(2, 1)
    print att * 2
    # assert att + 3.2 == 15.2
    # assert att - 1 == 11
    # assert att.dmg_type == 'm'
    # assert type(att) == damage
    # assert type(att - 1) == damage
    # assert type(att * 2) == damage
    # assert type(att / 0.5) == damage
    

if __name__ == '__main__':
    main()
