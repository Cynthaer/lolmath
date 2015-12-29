import sys, pprint, re
from damage import *
from champion import *

class Kindred(Champion):
    def __init__(self, stacks=0, **kwargs):
        super(Kindred, self).__init__('Kindred', **kwargs)
        self.stacks = stacks
    
    def q(self, target=None):
        spelldata = self.champion_api_data['spells'][0]
        effectdata = spelldata['effect']
        rank = self.ability_ranks['q'] - 1
        if rank < 0:
            return 0
        
        # per-bolt damage
        qdata = {}
        qdata['base_dmg'] = Damage(effectdata[1][rank], 0)
        qdata['scaling_dmg'] = Damage(effectdata[2][rank] * self.AD, 0)
        qdata['total_dmg'] = qdata['base_dmg'] + qdata['scaling_dmg']
        qdata['dps'] = qdata['total_dmg'] / effectdata[4][rank]
        
        qdata = self.apply_spell_def(qdata, target)
        return qdata
    
    def w(self, target=None):
        spelldata = self.champion_api_data['spells'][1]
        effectdata = spelldata['effect']
        rank = self.ability_ranks['w'] - 1
        if rank < 0:
            return 0
        
        wdata = {}
        wdata['base_dmg'] = Damage(effectdata[5][rank], 0)
        wdata['scaling_dmg'] = Damage(0.4 * self.AD, 0)
        wdata['stack_dmg'] = Damage(0) if target is None else Damage(self.stacks * 0.005 * (target.HP/2))
        wdata['total_dmg'] = wdata['base_dmg'] + wdata['scaling_dmg'] + wdata['stack_dmg']
        wdata['dps'] = wdata['total_dmg'] * (1 + self.bonus_AS/2)
        
        wdata = self.apply_spell_def(wdata, target)
        return wdata
    
    def e(self, target=None):
        spelldata = self.champion_api_data['spells'][2]
        effectdata = spelldata['effect']
        rank = self.ability_ranks['e'] - 1
        if rank < 0:
            return 0
        
        edata = {}
        edata['base_dmg'] = Damage(effectdata[1][rank])
        edata['scaling_dmg'] = Damage(0.2 * self.AD)
        edata['hp_dmg'] = Damage(0) if target is None else Damage(0.05 * target.HP)
        edata['total_dmg'] = edata['base_dmg'] + edata['scaling_dmg'] + edata['hp_dmg']
        
        edata = self.apply_spell_def(edata, target)
        return edata
    
    def apply_spell_def(self, spelldata, target=None):
        return { k: v * self.def_factor(target) for k, v in spelldata.iteritems() }
    
    def total_DPS(self, target=None):
        return self.AA_DPS(target) + self.q(target)['dps'] + self.w(target)['dps']
    
    def total_burst(self, target=None):
        return self.e(target)['total_dmg']
    
    def time_to_kill(self, target):
        return (target.HP - self.total_burst(target).total) / self.total_DPS(target).total

class Malphite(Champion):
    def __init__(self, **kwargs):
        super(Malphite, self).__init__("Malphite", **kwargs)
    
    @property
    def bonus_AR(self):
        return super(Malphite, self).bonus_AR * 1.3