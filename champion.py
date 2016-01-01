from __future__ import division
import os, logging, json, httplib
import riot
from damage import *
from item import *
from rune import *
from mastery import *

class Champion(object):

    def __init__(self, name, level=1, runepage=None, masterypage=None, abilities=None, items=[], refresh=False):
        self.api = riot.LoLAPI()
        self.refresh = refresh
        
        self.name = name
        self.level = level
        self.items = items
        
        if runepage is None:
            self.runepage = Runepage()
        elif type(runepage) == str:
            self.runepage = Runepage(runepage)
        else:
            self.runepage = runepage
        
        if masterypage is None:
            self.masterypage = MasteryPage()
        elif type(masterypage) == str:
            self.masterypage = MasteryPage(masterypage)
        else:
            self.masterypage = masterypage
        
        self._ability_ranks = { 'q': 0, 'w': 0, 'e': 0, 'r': 0 }
        if abilities is not None:
            self.ability_ranks = abilities
        
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
    
    def get_ext_stat(self, source, attr):
        '''Total stats from a given external source (i.e., items)'''
        return sum(map(lambda item: getattr(item, attr, 0), source))
    
    ''' Stats '''
    if True:
        
        ''' Offensive '''
        if True:
            @property
            def range(self):
                return self.base_range
            
            @property
            def bonus_AD(self):
                rune_AD = self.runepage.AD
                item_AD = self.get_ext_stat(self.items, 'AD')
                return rune_AD + item_AD
                
            @property
            def AD(self):
                return self.base('AD') + self.bonus_AD
            
            @property
            def bonus_AS(self):
                # natural AS growth is bonus AS
                nat_bonus_AS = (self.nat_AS['growth']/100)*((7/400)*(pow(self.level, 2) - 1) + (267/400)*(self.level-1))
                rune_AS = self.runepage.AS
                mast_AS = self.masterypage.AS
                item_AS = self.get_ext_stat(self.items, 'AS')
                
                return nat_bonus_AS + rune_AS + mast_AS + item_AS
            
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
                rune_APen = self.runepage.APen
                mast_APen = self.masterypage.flat_APen + (self.masterypage.flat_APen_per_lvl * self.level)
                item_APen = self.get_ext_stat(self.items, 'flat_APen')
                return rune_APen + mast_APen + item_APen
            
            @property
            def perc_APen(self):
                mast_perc_APen = self.masterypage.perc_APen
                return mast_perc_APen
            
            @property
            def perc_bonus_APen(self):
                return 0
            
            @property    
            def LS(self):
                rune_LS = self.runepage.LS
                mast_LS = self.masterypage.LS
                item_LS = self.get_ext_stat(self.items, 'LS')
                return rune_LS + mast_LS + item_LS
        
        ''' Defensive '''
        if True:
            @property
            def bonus_HP(self):
                rune_HP = self.runepage.HP
                item_HP = self.get_ext_stat(self.items, 'HP')
                return rune_HP + item_HP
            
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
                rune_AR = self.runepage.AR
                item_AR = self.get_ext_stat(self.items, 'AR')
                return rune_AR + item_AR
            
            @property
            def AR(self):
                return self.base('AR') + self.bonus_AR
            
            @property
            def bonus_MR(self):
                rune_MR = self.runepage.MR
                return rune_MR
                
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
                mast_MPen = self.masterypage.flat_MPen + (self.masterypage.flat_MPen_per_lvl * self.level)
                return mast_MPen
            
            @property
            def perc_MPen(self):
                return 0
            
            @property
            def SV(self):
                mast_SV = self.masterypage.SV
                return mast_SV
        
        ''' Movement '''
        if True:
            @property
            def bonus_MS(self):
                return 0
            
            @property
            def MS(self):
                return self.base('MS') + self.bonus_MS
    
    def statblock(self, show_details=False):
        s = '%s lvl %d\n' % (self.name, self.level)
        s += 'Items: %s\n' % self.items
        if show_details:
            s += 'HPR:  %.1f\t\t| MPR:  %.1f\n' % (self.HPR, self.MPR)
            s += 'APen: %.1f/%d%%\t| MPen: %.1f/%d%%\n' % (self.flat_APen, self.perc_APen*100, self.flat_MPen, self.perc_MPen*100)
            s += 'LS:   %d%%\t\t| SV:   %d%%\n' % (self.LS*100, self.SV*100)
            s += 'Rg:   %d\t\t| ??: \n' % (self.range)
            s += 'AD:   %d\t\t| AP:   %d\n' % (self.AD, self.AP)
            s += 'AR:   %d(%d%%)\t| MR:   %d(%d%%)\n' % (self.AR, (self.AR / (100 + self.AR))*100, self.MR, (self.MR / (100 + self.MR))*100)
            s += 'AS:   %.3f\t\t| CDR:  %d\n' % (self.AS, self.CDR*100)
            s += '??:   \t\t\t| MS:   %d\n' % (self.MS)
        s += self.ability_str()
        return s
    
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
    
    def q(self, target=None):
        pass
    
    def w(self, target=None):
        pass
        
    def e(self, target=None):
        pass
    
    def r(self, target=None):
        pass
    
    def apply_spell_mult(self, spelldata, target=None):
        return { k: v * self.def_factor(target) * (1 + self.masterypage.Ab_mult) 
            for k, v in spelldata.iteritems() }
    
    def ability_str(self, vertical=False):
        ar = self.ability_ranks
        if vertical:
            return 'q: %s\nw: %s\ne: %s\nr: %s' % (ar['q'], ar['w'], ar['e'], ar['r'])
        return 'q: %s | w: %s | e: %s | r: %s' % (ar['q'], ar['w'], ar['e'], ar['r'])
    
    ''' Attacks '''
    def AA_dmg(self, target=None):
        # average damage per hit after counting crits
        crit_factor = Damage(self.AD * (1 - self.crit_chance) + self.AD * self.crit_chance * self.crit_mult, 0)
        if target is not None and any(map(lambda i: type(i) is Tabi, target.items)):
            crit_factor *= 0.9
        
        onhit = self.get_ext_stat(self.items, 'onhit') * self.get_ext_stat(self.items, 'onhit_mult')
        raw_dmg = crit_factor + onhit
        
        mast_perc_mult = 1 + self.masterypage.perc_dmg_out
        return raw_dmg * self.def_factor(target) * mast_perc_mult
    
    def AA_DPS(self, target=None):
        dps = self.AA_dmg(target) * self.AS
        if target is not None:
            if any(map(lambda i: type(i) is FH, target.items)):
                dps *= 0.85
        return dps
    
    def AA_stats(self, target=None):
        s = 'AA_dmg = %.0f %s | AA_DPS = %.0f %s' % (self.AA_dmg(target).total, self.AA_dmg(target), self.AA_DPS(target).total, self.AA_DPS(target))
        return s
    
    ''' Utility '''
    def def_factor(self, target=None):
        ''' combines AR and MR factors into a tuple for ease of use with Damage() type '''
        return (self.AR_factor(target), self.MR_factor(target))
    
    def AR_factor(self, target=None):
        if target is None:
            return 1
        
        net_AR = (target.base('AR') + target.bonus_AR * (1 - self.perc_bonus_APen)) * (1 - self.perc_APen) - self.flat_APen
        mast_perc_mult = 1 + target.masterypage.perc_dmg_in
        return (1 - (net_AR / (100 + net_AR))) * mast_perc_mult
    
    def MR_factor(self, target=None):
        if target is None:
            return 1
        
        net_MR = target.MR * (1 - self.perc_MPen) - self.flat_MPen
        mast_perc_mult = 1 + target.masterypage.perc_dmg_in
        return (1 - (net_MR / (100 + net_MR))) * mast_perc_mult
    
    ''' Totals '''
    def total_DPS(self, target=None):
        ''' Extend this for specific champions '''
        return self.AA_DPS(target)
    
    def total_burst(self, target=None):
        ''' Extend this for specific champions '''
        return Damage()
    
    def time_to_kill(self, target):
        return (target.HP - self.total_burst(target).total) / self.total_DPS(target).total
    
def main():
    # httplib.HTTPConnection.debuglevel = 1
    logging.basicConfig(filename='champion.log', level=logging.INFO)
    
    kindred = Champion('Kindred', level=2, items=[Devourer()])
    print kindred.statblock()
    print '---'
    # for i in range(1, 19):
    #     kindred.level = i
    print 'AA_dmg: %s;\tAA_DPS: %s' % (kindred.AA_dmg(kindred), kindred.AA_DPS())
    print 'bonus_AD: %s;\tbonus_AS: %d%%' % (kindred.bonus_AD, kindred.bonus_AS*100)
        
if __name__ == "__main__":
    main()