from __future__ import division
import requests, riot

class Champion(object):

    def __init__(self, name, level=1):
        self.api = riot.LoLAPI()
        
        self.name = name
        self.level = level
        
        self._set_data()
        
    def _set_data(self):
        self._ability_ranks = { 'q': 0, 'w': 0, 'e': 0, 'r': 0 }
        
        self.apidata = self.api.get_champion(self.name, ['stats', 'spells'])
        stats = self.apidata['stats']
        
        # Offensive
        self.nat_AD = { 'base': stats['attackdamage'], 'growth': stats['attackdamageperlevel'] }
        self.nat_AS = { 'base': 0.625 / (1 + stats['attackspeedoffset']), 'growth': stats['attackspeedperlevel'] }
        self.nat_crit = { 'base': stats['crit'], 'growth': stats['critperlevel'] }
        self.base_range = stats['attackrange']

        # Defensive
        self.nat_HP = { 'base': stats['hp'], 'growth': stats['hpperlevel'] }
        self.nat_HPR = { 'base': stats['hpregen'], 'growth': stats['hpregenperlevel'] }
        self.nat_AR = { 'base': stats['armor'], 'growth': stats['armorperlevel'] }
        self.nat_MR = { 'base': stats['spellblock'], 'growth': stats['spellblockperlevel'] }
        
        # Ability
        self.nat_MP = { 'base': stats['mp'], 'growth': stats['mpperlevel'] }
        self.nat_MPR = { 'base': stats['mpregen'], 'growth': stats['mpregenperlevel'] }
        
        # Movement
        self.base_MS = stats['movespeed']

    def base(self, stat):
        return stat['base'] + stat['growth']*((7/400)*(pow(self.level, 2) - 1) + (267/400)*(self.level-1))
    
    ''' Stats '''
    if True:
        
        ''' Offensive '''
        if True:
            @property
            def bonus_AD(self):
                return 0
                
            @property
            def AD(self):
                return self.base(self.nat_AD) + self.bonus_AD
            
            @property
            def bonus_AS(self):
                # natural AS growth is bonus AS
                nat_bonus_AS = self.base(self.nat_AS) - self.base_AS
                return nat_bonus_AS
            
            @property
            def AS(self):
                return self.nat_AS['base'] + self.bonus_AS
            
            @property
            def crit_chance(self):
                return self.base(self.nat_crit)
            
            @property
            def crit_mult(self):
                return 2
            
            @property
            def flat_APen(self):
                return 0
            
            @property
            def perc_APen(self):
                return 0
            
            @property    
            def LS(self):
                return 0
        
        ''' Defensive '''
        if True:
            @property
            def bonus_HP(self):
                return 0
            
            @property
            def HP(self):
                return self.base(self.nat_HP) + self.bonus_HP
            
            @property
            def bonus_HPR(self):
                return 0
            
            @property
            def HPR(self):
                return self.base(self.nat_HPR) + self.bonus_HPR
            
            @property
            def bonus_AR(self):
                return 0
            
            @property
            def AR(self):
                return self.base(self.nat_AR) + self.bonus_APR
            
            @property
            def prop(self):
                return 0
            
            @property
            def bonus_MR(self):
                return 0
                
            @property
            def MR(self):
                return self.base(self.nat_MR) + self.bonus_MR

        ''' Ability '''
        if True:
            @property
            def AP(self):
                return 0
            
            @property
            def CDR(self):
                return 0
            
            @property
            def bonus_MP(self):
                return 0
            
            @property
            def MP(self):
                return self.base(self.nat_MP) + self.bonus_MP
            
            @property
            def bonus_MPR(self):
                return 0
                
            @property
            def MPR(self):
                return self.base(self.nat_MPR) + self.bonus_MPR
            
            @property
            def flat_MPen(self):
                return 0
            
            @property
            def perc_MPen(self):
                return 0
            
            @property
            def SV(self):
                return 0
        
        ''' Movement '''
        if True:
            @property
            def bonus_MS(self):
                return 0
            
            @property
            def MS(self):
                return self.base_MS + self.bonus_MS
    
    ''' Abilities '''
    def ability_ranks():
        def fget(self):
            return self._ability_ranks
        def fset(self, values):
            if type(values) is list:
                self._ability_ranks['q'] = values[0]
                self._ability_ranks['w'] = values[1]
                self._ability_ranks['e'] = values[2]
                self._ability_ranks['r'] = values[3]
            elif type(values) is dict:
                for key in values:
                    if values[key] is not None:
                        self._ability_ranks[key] = values[key]
        return locals()
    ability_ranks = property(**ability_ranks())
    
    def ability_str(self, vertical=False):
        ar = self.ability_ranks
        if vertical:
            return 'q: %s\nw: %s\ne: %s\nr: %s' % (ar['q'], ar['w'], ar['e'], ar['r'])
        return 'q: %s | w: %s | e: %s | r: %s' % (ar['q'], ar['w'], ar['e'], ar['r'])
    
def main():
    kindred = Champion('Kindred')
    # for i in range(1, 19):
    #     kindred.level = i
    #     print kindred.AD
    print kindred.ability_str()
        
if __name__ == "__main__":
    main()