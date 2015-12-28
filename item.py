from __future__ import division
import os, riot, json
from damage import *
                
def get_by_name(data, name):
    for key in data:
        if data[key]['name'] == name:
            return data[key]
    
class Item(object):
    def __init__(self, name, refresh=False):
        self.api = riot.LoLAPI()
        self.name = name
        
        self._set_api_data(refresh)
        
    def _set_api_data(self, refresh):
        cachepath = 'json_cache/items.json'
        if refresh == False and os.path.isfile(cachepath):
            with open(cachepath, 'r') as f:
                items_data = json.load(f)
        else:
            print 'invoking api'
            items_data = self.api.get_item_list(['effect', 'from', 'gold', 'stats'])
            with open(cachepath, 'w') as f:
                json.dump(items_data, f, indent=4, sort_keys=True)
        
        self.item_api_data = get_by_name(items_data['data'], self.name)
        
        stats = self.item_api_data['stats']
        
        # Offensive
        self.AD = stats.get('FlatPhysicalDamageMod', 0)
        self.AS = stats.get('PercentAttackSpeedMod', 0)
        self.crit = stats.get('FlatCritChanceMod', 0)
        self.LS = stats.get('PercentLifeStealMod', 0)
        
        # Defensive
        
        # Ability
        self.MP = stats.get('FlatMPPoolMod', 0)
        
        # Movement
        self.MS = stats.get('FlatMovementSpeedMod', 0)
        self.perc_MS = stats.get('PercentMovementSpeedMod', 0)

class Devourer(Item):
    def __init__(self, stacks=0):
        super(Devourer, self).__init__("Enchantment: Devourer")
        self.stacks = stacks
    
    @property
    def onhit(self):
        return Damage(0, 30 + self.stacks)
    
    @property
    def onhit_mult(self):
        return (5/4) if self.stacks == 30 else 1 # ranged

class Warrior(Item):
    def __init__(self):
        super(Warrior, self).__init__("Enchantment: Warrior")
        self.CDR = 0.1

class Berserkers(Item):
    def __init__(self):
        super(Berserkers, self).__init__("Berserker's Greaves")

def main():
    item = Item("Phantom Dancer")
    print 'stats: %s' % item.item_api_data['stats']

if __name__ == '__main__':
    main()