from __future__ import division
import os
import riot
import json
from damage import *


def get_by_name(data, name):
    for key in data:
        if data[key]['name'] == name:
            return data[key]


class Item(object):
    """Base class for all items. Handles standard stats present in the Riot 
    API, but needs to be extended for individual items."""

    def __init__(self, name, refresh=False):
        self.api = riot.LoLAPI(refresh=refresh)
        self.name = name

        self._set_api_data()

    def _set_api_data(self):
        items_data = self.api.get_item_list(['effect', 'from', 'gold', 'stats'])
        self.item_api_data = get_by_name(items_data['data'], self.name)

        stats = self.item_api_data['stats']

        # Offensive
        self.AD = stats.get('FlatPhysicalDamageMod', 0)
        self.AS = stats.get('PercentAttackSpeedMod', 0)
        self.crit = stats.get('FlatCritChanceMod', 0)
        self.LS = stats.get('PercentLifeStealMod', 0)

        # Defensive
        self.HP = stats.get('FlatHPPoolMod', 0)
        self.AR = stats.get('FlatArmorMod', 0)
        self.MR = stats.get('FlatSpellBlockMod', 0)

        # Ability
        self.AP = stats.get('FlatMagicDamageMod', 0)
        self.MP = stats.get('FlatMPPoolMod', 0)

        # Movement
        self.MS = stats.get('FlatMovementSpeedMod', 0)
        self.perc_MS = stats.get('PercentMovementSpeedMod', 0)

    def __repr__(self):
        return self.name


class Devourer(Item):
    """Enchantment: Devourer"""

    def __init__(self, stacks=0):
        super(Devourer, self).__init__("Enchantment: Devourer")
        self.stacks = stacks

    def __repr__(self):
        return "Devourer(%s)" % (self.stacks)

    @property
    def onhit(self):
        return Damage(0, 30 + self.stacks)

    @property
    def onhit_mult(self):
        return (5 / 4) if self.stacks == 30 else 1  # ranged


class Warrior(Item):
    """Enchantment: Warrior"""

    def __init__(self):
        super(Warrior, self).__init__("Enchantment: Warrior")
        self.CDR = 0.1

    def __repr__(self):
        return "Warrior"


class Ghostblade(Item):
    """ Youmuu's Ghostblade"""

    def __init__(self, active=False):
        super(Ghostblade, self).__init__("Youmuu's Ghostblade")
        self.active = active
        self.CDR = 0.1
        self.flat_APen = 20

    def __repr__(self):
        return '%s%s' % ('Ghostblade', '(active)' if self.active else '')

    @property
    def perc_MS(self):
        return 0.2 if self.active else 0

    @perc_MS.setter
    def perc_MS(self, perc_MS):
        pass

    @property
    def AS(self):
        return 0.4 if self.active else 0

    @AS.setter
    def AS(self, AS):
        pass


class BotRK(Item):
    """Blade of the Ruined King"""

    def __init__(self, active=True):
        super(BotRK, self).__init__("Blade of the Ruined King")
        self.active = active

    def __repr__(self):
        return self.name + ("(active)" if self.active else "")


class Bloodthirster(Item):
    """The Bloodthirster"""

    def __init__(self, shield=True):
        super(Bloodthirster, self).__init__("The Bloodthirster")
        self.shield = shield
        self.LS = 0.2


class RFC(Item):
    """Rapid Firecannon"""

    def __init__(self):
        super(RFC, self).__init__("Rapid Firecannon")


class Hurricane(Item):
    """Runaan's Hurricane"""

    def __init__(self, bolt=False):
        super(Hurricane, self).__init__("Runaan's Hurricane")
        self.bolt = bolt

    def __repr__(self):
        return self.name + ("(bolt)" if self.bolt else "")


class Berserkers(Item):

    def __init__(self):
        super(Berserkers, self).__init__("Berserker's Greaves")

    def __repr__(self):
        return "Berserker's"


class Tabi(Item):

    def __init__(self):
        super(Tabi, self).__init__("Ninja Tabi")


class Cleaver(Item):

    def __init__(self, stacks=0):
        super(Cleaver, self).__init__("The Black Cleaver")
        self.CDR = 0.2
        self.stacks = stacks

    def __repr__(self):
        return "Cleaver(%d)" % (self.stacks)

    @property
    def perc_APen(self):
        return 0.05 * self.stacks


class Steraks(Item):
    """Sterak's Gage"""

    def __init__(self, active=True):
        super(Steraks, self).__init__("Sterak's Gage")
        self.active = active


class Abyssal(Item):
    """Abyssal Scepter"""

    def __init__(self):
        super(Abyssal, self).__init__("Abyssal Scepter")
        self.flat_MPen = 20


class DMP(Item):

    def __init__(self):
        super(DMP, self).__init__("Dead Man's Plate")


class Sunfire(Item):

    def __init__(self):
        super(Sunfire, self).__init__("Sunfire Cape")


class FH(Item):

    def __init__(self):
        super(FH, self).__init__("Frozen Heart")
        self.CDR = 0.2


class SV(Item):
    """Spirit Visage"""

    def __init__(self):
        super(SV, self).__init__("Spirit Visage")
        self.CDR = 0.1
        self.HPR = 1.5


def main():
    item = Item("Phantom Dancer")
    print 'stats: %s' % item.item_api_data['stats']

if __name__ == '__main__':
    main()
