#!/usr/bin/python
__author__ = 'chukwuyem'

#source: https://www.hackerrank.com/contests/countercode/challenges/campers

#this worked!!!


def main():
    n, k = raw_input('').split(' ')
    m_team_id = [] #list with sniper ids and ids consecutive to sniper ids
    for x in raw_input('').split(' '):
        m_team_id.append(int(x))
        m_team_id.append(int(x) + 1)
        if x > 1: m_team_id.append(int(x) - 1)
    #print m_team_id
    possible_team = [x for x in range(1, int(n) + 1)] #list of all possible ids for team
    #print possible_team
    #list of ids that can be picked after picking snipers
    possible_team_left = set(possible_team).difference(set(m_team_id))
    #print possible_team_left

    possible_team_left = sorted(list(possible_team_left))
    #go through sorted list of remaining ids, deleting the next item if it is a consecutive id
    it = 0
    while it < len(possible_team_left) - 1:
        if possible_team_left[it + 1] == possible_team_left[it] + 1:
            del possible_team_left[it + 1]
        it += 1
    #print possible_team_left
    print len(possible_team_left) + int(k)

main()
