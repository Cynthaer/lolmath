import sys, pprint, re
from champion import *
from kindred import *

detail_lvl = 2
result = [['Level', 'Items', 'Stacks', 'Squishy', 'Bruiser', 'Tank']]
def main():
    global result
    with open('out.txt', 'w') as out:
        sys.stdout = out
        def test_stacks(test, kindred):
            for s in [3, 6]:
                kindred.stacks = s
                test(kindred)
        
        # 1-item tests
        kindred = Kindred(stacks=0, runepage='ADC', masterypage='ADC', level=6, abilities=[3, 1, 1, 1], items=[Warrior()])
        test_stacks(test_one_item, kindred)
        for ds in [0, 15, 30]:
            kindred.items = [Devourer(ds)]
            test_stacks(test_one_item, kindred)
        
        # 2-item tests
        kindred.level = 9
        kindred.items = [Warrior(), Berserkers(), Ghostblade(True)]
        test_stacks(test_two_items, kindred)
        
        kindred.items = [Devourer(15), Berserkers(), Ghostblade(True)]
        test_stacks(test_two_items, kindred)
        
        result = [result[0]] + sorted(result[1:], key=lambda l: ' '.join([l[0], l[2], l[1]]))
        
        print_table(result)

def test(scenario, kindred, squishy, bruiser, tank):
    print indent(kindred.statblock())
    print 'Stacks: %d' % kindred.stacks
    print_matchup(kindred, squishy)
    print_matchup(kindred, bruiser)
    print_matchup(kindred, tank)
    print '---\n'
    result.append([str(kindred.level), str(kindred.items), str(kindred.stacks)] + map(lambda t: '%.1f' % kindred.time_to_kill(t), [squishy, bruiser, tank]))

def test_one_item(kindred):
    scenario = "lvl %d %s" % (kindred.level, kindred.items)
    print '--- %s ---' % scenario
    lucian = Champion('Lucian', level=6, runepage='ADC')
    renekton = Champion('Renekton', level=6, runepage='Bruiser', items=[Cleaver()])
    malphite = Malphite(level=6, runepage='Bruiser', items=[Sunfire()])
    test(scenario, kindred, lucian, renekton, malphite)

def test_two_items(kindred):
    scenario = "lvl %d %s" % (kindred.level, kindred.items)
    print '--- %s ---' % scenario
    lucian = Champion('Lucian', level=9, runepage='ADC')
    renekton = Champion('Renekton', level=9, runepage='Bruiser', items=[Cleaver(), Tabi(), DMP()])
    malphite = Malphite(level=9, runepage='Bruiser', items=[Sunfire(), Tabi(), FH()])
    test(scenario, kindred, lucian, renekton, malphite)

def print_matchup(kindred, target):
    print '-'
    print 'vs. lvl %d %s %s (%d HP, %d AR, %d MR)' % (target.level, target.name, target.items, target.HP, target.AR, target.MR)
    if detail_lvl >= 1:
        print kindred.AA_stats(target)
        if detail_lvl >= 2:
            print 'q:\n%s' % pprint.pformat(kindred.q(target), indent=4)
            print 'w:\n%s' % pprint.pformat(kindred.w(target), indent=4)
            print 'e:\n%s' % pprint.pformat(kindred.e(target), indent=4)
        print 'Total DPS = %.0f %s' % (kindred.total_DPS(target).total, kindred.total_DPS(target))
        print 'Total Burst = %.0f %s' % (kindred.total_burst(target).total, kindred.total_burst(target))
    print 'Time to Kill = %.1fs' % kindred.time_to_kill(target)

def indent(s):
    return re.sub('^', '\t', s, flags=re.M)

def print_table(table):
    col_width = [max(len(x) for x in col) for col in zip(*table)]
    for line in table:
        col_gen = ["{:{}}".format(x, col_width[i]) for i, x in enumerate(line)]
        print '| ' + ' | '.join(col_gen) + ' |'

if __name__ == '__main__':
    main()