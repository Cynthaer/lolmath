class MasteryPage(object):
    def __init__(self, name='', masteries=[]):
        self.name = name
        self.masteries = masteries
        
        if name in ("ADC", "Marksman"):
            self.masteries = ["Fury", "Feast", "Vampirism", "Bounty Hunter", "Savagery", "Secret Stash", "Merciless", "Dangerous Game", "Precision", "Thunderlord's Decree"]