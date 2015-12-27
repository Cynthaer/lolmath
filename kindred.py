from champion import *

class Kindred(Champion):
    def __init__(self):
        super(Kindred, self).__init__('Kindred')
    
    def q(self):
        spelldata = self.apidata['spells'][0]
        effectdata = spelldata['effect']
        rank = self.ability_ranks['q'] - 1
        
        qdata = {}
        qdata['base_dmg'] = effectdata[1][rank]
        qdata['scaling_dmg'] = effectdata[2][rank] * self.AD
        qdata['total_dmg'] = qdata['base_dmg'] + qdata['scaling_dmg']
        qdata['dps'] = qdata['total_dmg'] / effectdata[4][rank]
        return qdata

def main():
    kindred = Kindred()
    target = Kindred()
    for i in range(1, 6):
        kindred.ability_ranks = { 'q': i }
        kindred.level = 2 * i - 1
        print 'level: ' + str(kindred.level)
        print kindred.ability_str()
        print kindred.q()
        print ''

if __name__ == '__main__':
    main()