from damage import *
from champion import *


class Kindred(Champion):

    def __init__(self, stacks=0, **kwargs):
        super(Kindred, self).__init__('Kindred', **kwargs)
        self.stacks = stacks

    def onhit(self, target=None):
        ''' overrides base champion function to include Kindred passive '''
        sup_onhit = super(Kindred, self).onhit(target)
        if target is None:
            return sup_onhit

        mast_perc_mult = 1 + self.masterypage.perc_dmg_out
        raw_stack_dmg = Damage(self.stacks * 0.0125 * (target.HP / 2))
        net_stack_dmg = (
            raw_stack_dmg * self.def_factor(target) * mast_perc_mult)

        return sup_onhit + net_stack_dmg

    def q(self, target=None):
        rank = self.ability_ranks['q'] - 1
        if rank < 0:
            return {}

        spelldata = self.champion_api_data['spells'][0]
        effectdata = spelldata['effect']

        # per-bolt damage
        qdata = {}
        qdata['base_dmg'] = Damage(effectdata[1][rank], 0)
        qdata['scaling_dmg'] = Damage(effectdata[2][rank] * self.AD, 0)
        qdata['total_dmg'] = qdata['base_dmg'] + qdata['scaling_dmg']
        qdata['dps'] = qdata['total_dmg'] / effectdata[4][rank]

        qdata = self.apply_spell_mult(qdata, target)
        return qdata

    def w(self, target=None):
        rank = self.ability_ranks['w'] - 1
        if rank < 0:
            return {}

        spelldata = self.champion_api_data['spells'][1]
        effectdata = spelldata['effect']

        wdata = {}
        wdata['base_dmg'] = Damage(effectdata[5][rank], 0)
        wdata['scaling_dmg'] = Damage(0.4 * self.AD, 0)
        wdata['stack_dmg'] = (Damage(0) if target is None
                              else Damage(self.stacks * 0.005 * (target.HP / 2)))
        wdata['total_dmg'] = (wdata['base_dmg'] +
                              wdata['scaling_dmg'] + wdata['stack_dmg'])
        wdata['dps'] = wdata['total_dmg'] * (0.625 + self.bonus_AS / 2)

        wdata = self.apply_spell_mult(wdata, target)
        return wdata

    def e(self, target=None):
        rank = self.ability_ranks['e'] - 1
        if rank < 0:
            return {}

        spelldata = self.champion_api_data['spells'][2]
        effectdata = spelldata['effect']

        edata = {}
        edata['base_dmg'] = Damage(effectdata[1][rank])
        edata['scaling_dmg'] = Damage(0.2 * self.AD)
        edata['hp_dmg'] = (
            Damage(0.05 * target.HP) if target is not None else Damage(0))
        edata['total_dmg'] = (edata['base_dmg'] +
                              edata['scaling_dmg'] + edata['hp_dmg'])

        edata = self.apply_spell_mult(edata, target)
        return edata

    def total_DPS(self, target=None):
        return self.AA_DPS(target) + self.q(target)['dps'] + self.w(target)['dps']

    def total_burst(self, target=None):
        mast_perc_mult = 1 + self.masterypage.perc_dmg_out
        raw_item_dmg = Damage(0)
        if target is not None and self.get_item(BotRK) is not None:
            raw_item_dmg += Damage(0.1 * target.HP, 0)
        if self.get_item(RFC) is not None:
            raw_item_dmg += Damage(0, 50 if self.level <= 4
                                   else (50.5 + 11.5 * (self.level - 5)))
        item_dmg = raw_item_dmg * self.def_factor(target) * mast_perc_mult
        return self.e(target)['total_dmg'] + item_dmg


class Malphite(Champion):

    def __init__(self, **kwargs):
        super(Malphite, self).__init__("Malphite", **kwargs)

    @property
    def bonus_AR(self):
        return super(Malphite, self).bonus_AR * 1.3

    @property
    def shield(self):
        sup_shield=super(Malphite, self).shield
        passive_shield=0.1 * self.HP
        return sup_shield + passive_shield
