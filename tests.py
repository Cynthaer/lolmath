import sys
import pprint
import re
import csv
import itertools
import operator

from champion import *
from kindred import *

detail_lvl = 2  # determines how much debugging detail we print out
result = [['Level', 'Items', 'Stacks', 'Squishy TTK', 'Squishy DMG',
           'Bruiser TTK', 'Bruiser DMG', 'Tank TTK', 'Tank DMG']]


def main():
    global result
    with open('out.txt', 'w') as out:
        old_stdout = sys.stdout
        sys.stdout = out

        def test_itemsets(testfun, kindred, itemsets, stackvals):
            for itemset in itemsets:
                kindred.items = itemset
                for s in stackvals:
                    kindred.stacks = s
                    testfun(kindred)

        # def test_stacks(testfun, kindred, stackvals):

        kindred = Kindred(runepage='ADC', masterypage='ADC')

        # 1-item tests
        kindred.level = 5
        kindred.ability_ranks = [3, 1, 1, 0]
        stackvals = [1, 3, 5]
        itemsets = [
            [Warrior()],
            [Devourer(0)],
            [Devourer(15)],
            [Devourer(30)]
        ]

        test_itemsets(test_one_item, kindred, itemsets, stackvals)

        # 2-item tests
        kindred.level = 11
        kindred.ability_ranks = [5, 3, 1, 2]
        stackvals = [3, 5, 8]
        itemsets = [
            [Warrior(), Berserkers(), BotRK(False)],
            [Warrior(), Berserkers(), BotRK()],
            [Warrior(), Berserkers(), Ghostblade()],
            [Warrior(), Berserkers(), Ghostblade(True)],
            [Devourer(0), Berserkers(), BotRK(False)],
            [Devourer(0), Berserkers(), BotRK()],
            [Devourer(0), Berserkers(), Ghostblade()],
            [Devourer(0), Berserkers(), Ghostblade(True)],
            [Devourer(15), Berserkers(), BotRK(False)],
            [Devourer(15), Berserkers(), BotRK()],
            [Devourer(15), Berserkers(), Ghostblade()],
            [Devourer(15), Berserkers(), Ghostblade(True)],
            [Devourer(30), Berserkers(), BotRK(False)],
            [Devourer(30), Berserkers(), BotRK()],
            [Devourer(30), Berserkers(), Ghostblade()],
            [Devourer(30), Berserkers(), Ghostblade(True)],
        ]

        test_itemsets(test_two_items, kindred, itemsets, stackvals)

        # 3-item tests
        kindred.level = 14
        kindred.ability_ranks = [5, 5, 2, 2]
        stackvals = [4, 6, 9]
        itemsets = [
            [Warrior(), Berserkers(), Ghostblade(), BotRK(False)],
            [Warrior(), Berserkers(), Ghostblade(True), BotRK()],
            [Warrior(), Berserkers(), Ghostblade(), RFC()],
            [Warrior(), Berserkers(), Ghostblade(True), RFC()],
            [Warrior(), Berserkers(), Ghostblade(), Cleaver(5)],
            [Warrior(), Berserkers(), Ghostblade(True), Cleaver(5)],
            [Devourer(30), Berserkers(), Ghostblade(), BotRK(False)],
            [Devourer(30), Berserkers(), Ghostblade(True), BotRK()],
            [Devourer(30), Berserkers(), BotRK(), Hurricane()],
            [Devourer(30), Berserkers(), BotRK(False), Hurricane()],
            [Devourer(30), Berserkers(), Ghostblade(), Cleaver(5)],
            [Devourer(30), Berserkers(), Ghostblade(True), Cleaver(5)],
        ]

        test_itemsets(test_three_items, kindred, itemsets, stackvals)
        
        # 4-item tests
        kindred.level = 16
        kindred.ability_ranks = [5, 5, 3, 3]
        stackvals = [6, 8, 10]
        itemsets = [
            # actives up
            [Warrior(), Berserkers(), Ghostblade(True), BotRK(), LDR()],
            [Warrior(), Berserkers(), Ghostblade(True), RFC(), LDR()],
            [Warrior(), Berserkers(), Ghostblade(True), BotRK(), Cleaver(5)],
            [Warrior(), Berserkers(), Ghostblade(True), Cleaver(5), LDR()],
            [Devourer(30), Berserkers(), Ghostblade(True), BotRK(), Hurricane()],
            [Devourer(30), Berserkers(), Ghostblade(True), BotRK(), LDR()],
            [Devourer(30), Berserkers(), BotRK(), Hurricane(), LDR()],
            # actives down
            [Warrior(), Berserkers(), Ghostblade(), BotRK(False), LDR()],
            [Warrior(), Berserkers(), Ghostblade(), RFC(), LDR()],
            [Warrior(), Berserkers(), Ghostblade(), BotRK(False), Cleaver(5)],
            [Warrior(), Berserkers(), Ghostblade(), Cleaver(5), LDR()],
            [Devourer(30), Berserkers(), Ghostblade(), BotRK(False), Hurricane()],
            [Devourer(30), Berserkers(), Ghostblade(), BotRK(False), LDR()],
            [Devourer(30), Berserkers(), BotRK(False), Hurricane(), LDR()],
        ]

        test_itemsets(test_three_items, kindred, itemsets, stackvals)

        result = ([result[0]] + sorted(result[1:],
                                       key=lambda l: ' '.join([l[0], l[2], l[1]])))

        print_table(result)

        sys.stdout = old_stdout

    with open('out.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(result)


def test_one_item(kindred):
    scenario = "lvl %d st %d %s" % (
        kindred.level, kindred.stacks, kindred.items)
    print '--- %s ---' % scenario
    lucian = Champion('Lucian', level=5, runepage='ADC')
    renekton = Champion('Renekton', level=5,
                        runepage='Bruiser', items=[Cleaver()])
    malphite = Malphite(level=5, runepage='Tank', items=[Sunfire()])
    test(scenario, kindred, lucian, renekton, malphite)


def test_two_items(kindred):
    scenario = "lvl %d st %d %s" % (
        kindred.level, kindred.stacks, kindred.items)
    print '--- %s ---' % scenario
    lucian = Champion('Lucian', level=11, runepage='ADC')
    renekton = Champion('Renekton', level=11, runepage='Bruiser',
                        items=[Cleaver(), Tabi(), DMP()])
    malphite = Malphite(level=11, runepage='Tank',
                        items=[Sunfire(), Tabi(), FH()])
    test(scenario, kindred, lucian, renekton, malphite)


def test_three_items(kindred):
    scenario = "lvl %d st %d %s" % (
        kindred.level, kindred.stacks, kindred.items)
    print '--- %s ---' % scenario
    lucian = Champion('Lucian', level=14, runepage='ADC')
    renekton = Champion('Renekton', level=14, runepage='Bruiser',
                        items=[Cleaver(), Tabi(), DMP(), SV()])
    malphite = Malphite(level=14, runepage='Tank',
                        items=[Sunfire(), Tabi(), FH(), Abyssal()])
    test(scenario, kindred, lucian, renekton, malphite)


def test_four_items(kindred):
    scenario = "lvl %d st %d %s" % (
        kindred.level, kindred.stacks, kindred.items)
    print '--- %s ---' % scenario
    lucian = Champion('Lucian', level=16, runepage='ADC',
                      items=[Bloodthirster()])
    renekton = Champion('Renekton', level=16, runepage='Bruiser',
                        items=[Cleaver(), Tabi(), DMP(), SV(), Steraks(True)])
    malphite = Malphite(level=16, runepage='Tank',
                        items=[Sunfire(), Tabi(), FH(), Abyssal(), Thornmail()])
    test(scenario, kindred, lucian, renekton, malphite)


def test(scenario, kindred, squishy, bruiser, tank):
    print indent(kindred.statblock(detail_lvl >= 2))
    print 'Stacks: %d' % kindred.stacks
    print_matchup(kindred, squishy)
    print_matchup(kindred, bruiser)
    print_matchup(kindred, tank)
    print '---\n'
    result.append([str(kindred.level), str(kindred.items), str(kindred.stacks)] +
                  reduce(operator.add, map(lambda t: ['%.1f' % kindred.time_to_kill(t), '%.0f%s/s + %.0f%s' % (kindred.total_DPS(t).total, kindred.total_DPS(t), kindred.total_burst(t).total, kindred.total_burst(t))], [squishy, bruiser, tank])))


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
