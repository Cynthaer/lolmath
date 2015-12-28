from __future__ import division
import os, logging, json, httplib
import riot
from damage import *
from item import *

class Champion(object):

    def __init__(self, name, level=1, items=[], refresh=False):
        self.api = riot.LoLAPI()
        self.refresh = refresh
        
        self.name = name
        self.level = level
        self.items = items
        
        self._ability_ranks = { 'q': 0, 'w': 0, 'e': 0, 'r': 0 }
        
        self._set_api_data()
        
    def _set_api_data(self):
        cachepath = 'json_cache/%s.json' % self.name
        if self.refresh == False and os.path.isfile(cachepath):
            with open(cachepath, 'r') as f:
                self.champion_api_data = json.load(f)
        else:
            print 'invoking api'
            self.champion_api_data = self.api.get_champion(self.name, ['stats', 'spells'])
            with open(cachepath, 'w') as f:
                json.dump(self.champion_api_data, f, indent=4)
        
        stats = self.champion_api_data['stats']
        
        # Offensive
        self.nat_AD =   { 'base': stats['attackdamage'], 'growth': stats['attackdamageperlevel'] }
        self.nat_AS =   { 'base': 0.625 / (1 + stats['attackspeedoffset']), 'growth': stats['attackspeedperlevel'] }
        self.nat_crit = { 'base': stats['crit'], 'growth': stats['critperlevel'] }
        
        self.base_range = stats['attackrange']

        # Defensive
        self.nat_HP =  { 'base': stats['hp'],         'growth': stats['hpperlevel'] }
        self.nat_HPR = { 'base': stats['hpregen'],    'growth': stats['hpregenperlevel'] }
        self.nat_AR =  { 'base': stats['armor'],      'growth': stats['armorperlevel'] }
        self.nat_MR =  { 'base': stats['spellblock'], 'growth': stats['spellblockperlevel'] }
        
        # Ability
        self.nat_MP =  { 'base': stats['mp'],      'growth': stats['mpperlevel'] }
        self.nat_MPR = { 'base': stats['mpregen'], 'growth': stats['mpregenperlevel'] }
        
        # Movement
        self.base_MS = stats['movespeed']

    def base(self, stat):
        if type(stat) is str:
            if stat == 'MS':
                return self.base_MS
            stat = getattr(self, 'nat_' + stat)
        
        # AS growth is bonus AS
        if stat is self.nat_AS:
            return stat['base']
        
        return stat['base'] + stat['growth']*((7/400)*(pow(self.level, 2) - 1) + (267/400)*(self.level-1))
    
    def get_item_attr(self, attr):
        return sum(map(lambda item: getattr(item, attr), self.items))
    
    ''' Stats '''
    if True:
        
        ''' Offensive '''
        if True:
            @property
            def bonus_AD(self):
                item_AD = self.get_item_attr('AD')
                return item_AD
                
            @property
            def AD(self):
                return self.base('AD') + self.bonus_AD
            
            @property
            def bonus_AS(self):
                # natural AS growth is bonus AS
                nat_bonus_AS = (self.nat_AS['growth']/100)*((7/400)*(pow(self.level, 2) - 1) + (267/400)*(self.level-1))
                
                item_AS = self.get_item_attr('AS')
                
                return nat_bonus_AS + item_AS
            
            @property
            def AS(self):
                return self.base('AS') * (1 + self.bonus_AS)
            
            @property
            def crit_chance(self):
                return self.base('crit')
            
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
            def perc_bonus_APen(self):
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
                return self.base('HP') + self.bonus_HP
            
            @property
            def bonus_HPR(self):
                return 0
            
            @property
            def HPR(self):
                return self.base('HPR') + self.bonus_HPR
            
            @property
            def bonus_AR(self):
                return 0
            
            @property
            def AR(self):
                return self.base('AR') + self.bonus_APR
            
            @property
            def bonus_MR(self):
                return 0
                
            @property
            def MR(self):
                return self.base('MR') + self.bonus_MR

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
                return self.base('MP') + self.bonus_MP
            
            @property
            def bonus_MPR(self):
                return 0
                
            @property
            def MPR(self):
                return self.base('MPR') + self.bonus_MPR
            
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
                return self.base('MS') + self.bonus_MS
    
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
    
    ''' Attacks '''
    def AA_dmg(self, target=None):
        # average damage per hit after counting crits
        crit_factor = self.AD * (1 - self.crit_chance) + self.AD * self.crit_chance * self.crit_mult
        return crit_factor * self.AR_factor(target)
    
    def AA_DPS(self, target=None):
        return self.AA_dmg() * self.AS
        
    ''' Utility '''
    def AR_factor(self, target=None):
        if target is None:
            return 1
        
        net_AR = (target.base('AR') + target.bonus_AR * (1 - self.perc_bonus_APen)) * (1 - self.perc_APen) - self.flat_APen
        return 1 - (net_AR / (100 + net_AR))
    
    def MR_factor(self, target=None):
        if target is None:
            return 1
        
        net_MR = target.MR * (1 - self.perc_MPen) - self.flat_MPen
        return 1 - (net_MR / (100 + net_MR))
    
def main():
    # httplib.HTTPConnection.debuglevel = 1
    logging.basicConfig(filename='riot.log', level=logging.ERROR)
    
    kindred = Champion('Kindred', items=[Warrior()])
    for i in range(1, 19):
        kindred.level = i
    print 'level: %s,\tAD: %s,\tAA_dmg: %s,\tAS: %.3f,\tAA_DPS: %s' % (kindred.level, kindred.AD, kindred.AA_dmg(), kindred.AS, kindred.AA_DPS())
    print 'bonus_AD: %s,\tbonus_AS: %.3f' % (kindred.bonus_AD, kindred.bonus_AS)
    print kindred.ability_str()
    print kindred.items
        
if __name__ == "__main__":
    main()