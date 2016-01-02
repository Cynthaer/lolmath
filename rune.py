from damage import *

class Runepage(object):
    """Represents a complete runepage. Has some defaults for easy testing."""
    def __init__(self, name=''):
        self.name = name
        
        for stat in ['AD', 'AS', 'APen', 'HP', 'AR', 'MR', 'AP', 'CDR', 'LS']:
            setattr(self, stat, 0)
        
        if name in ('ADC', 'Marksman'):
            self.AD = 0.95 * 9
            self.MR = 1.34 * 9
            self.AR = 1 * 9
            self.AS = 0.045 * 9
        elif name in ('Bruiser'):
            self.AD = 0.95 * 9 + 2.25 * 3
            self.MR = 1.34 * 9
            self.AR = 1 * 9
        elif name in ('Tank'):
            self.MR = 1.34 * 9
            self.AR = 1 * 9

def main():
    page = Runepage('ADC')
    print page.APen

if __name__ == '__main__':
    main()