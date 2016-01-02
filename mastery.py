class MasteryPage(object):

    def __init__(self, name='', masteries=[], stats={}):
        self.name = name
        self.masteries = masteries

        for stat in ["AS",
                     "Ab_mult",
                     "perc_dmg_out",
                     "perc_dmg_in",
                     "LS",
                     "SV",
                     "AD",
                     "AD_per_lvl",
                     "AP",
                     "AP_per_lvl",
                     "perc_APen",
                     "perc_MPen",
                     "flat_APen",
                     "flat_APen_per_lvl",
                     "flat_MPen",
                     "flat_MPen_per_lvl",
                     "CDR",
                     "perc_bonus_AR",
                     "perc_bonus_MR",
                     "HP"]:
            setattr(self, stat, 0)

        # fuck it, let's just get this shit done
        if name in ("ADC", "Marksman"):
            stats = {
                'AS': 0.04,
                'perc_dmg_out': 0.065,
                'perc_dmg_in': 0.02,
                'LS': 0.02,
                'SV': 0.02,
                # splitting the difference between Battering Blows and
                # Precision
                'perc_APen': 0.035,
                'flat_APen': 2.5,
                'flat_APen_per_lvl': 0.25,
                'flat_MPen': 1.5,
                'flat_MPen_per_lvl': 0.15
            }
        elif name == "Bruiser":
            stats = {
                'Ab_mult': 0.02,
                'perc_dmg_out': 0.055,
                'perc_dmg_in': 0.015,
                'LS': 0.02,
                'SV': 0.02,
                'perc_APen': 0.07,
                'perc_bonus_AR': 0.05,
                'perc_bonus_MR': 0.05
            }
        elif name == "Tank":
            stats = {
                'Ab_mult': 0.02,
                'LS': 0.02,
                'SV': 0.02,
                'perc_dmg_out': 0.025,
                'perc_bonus_AR': 0.05,
                'perc_bonus_MR': 0.05,
                'HP': 45,
                'AR': 6,
                'MR': 6
            }

        for key in stats:
            setattr(self, key, stats[key])

        # if name in ("ADC", "Marksman"):
        #     self.masteries = ["Fury", "Feast", "Vampirism", "Bounty Hunter", "Savagery", "Secret Stash", "Merciless", "Dangerous Game", "Precision", "Thunderlord's Decree"]

        # if "Fury" in self.masteries:
        #     self.AS += 0.04
        # if "Sorcery" in self.masteries:
        #     self.Ab_mult += 0.02
        # if "Double Edged Sword" in self.masteries:
        #     pass


def main():
    mpage = MasteryPage('Tank')
    print mpage.flat_APen_per_lvl

if __name__ == '__main__':
    main()
