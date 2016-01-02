from collections import Iterable

class Damage(object):
    def __init__(self, p=0.0, m=0.0):
        self.p = float(p)
        self.m = float(m)
    
    def __getitem__(self, index):
        if index in (0, 'p'):
            return self.p
        elif index in (1, 'm'):
            return self.m
        raise StopIteration

    def __add__(self, other):
        try:
            return Damage(self.p + other.p, self.m + other.m)
        except AttributeError:
            return Damage(self.p + other, self.m + other)
    
    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        try:
            return Damage(self.p - other.p, self.m - other.m)
        except AttributeError:
            return Damage(self.p - other, self.m - other)

    def __mul__(self, other):
        try:
            return Damage(self.p * other[0], self.m * other[1])
        except TypeError:
            return Damage(self.p * other, self.m * other)
            
    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        try:
            return Damage(self.p / other[0], self.m / other[1])
        except TypeError:
            return Damage(self.p / other, self.m / other)
            
    def __rdiv__(self, other):
        return self.__rdiv__(other)

    def __neg__(self):
        return Damage(-self.p, -self.m)

    def __eq__(self, other):
        return self.p == other.p and self.m == other.m

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return '(%.1f, %.1f)' % (self.p, self.m)

    def __repr__(self):
        return 'Damage' + str(self)
    
    @property
    def total(self):
        return self.p + self.m
    
def main():
    
    # tests
    att = Damage(12, 10)
    print att
    assert att == Damage(12, 10)
    for d in att:
        print d
    print att * Damage(2, 1)
    print att * 2
    

if __name__ == '__main__':
    main()
