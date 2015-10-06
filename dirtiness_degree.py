#!/usr/bin/python
__author__ = 'chukwuyem'

#source: https://www.hackerrank.com/contests/countercode/challenges/degree-of-dirtiness

#this worked!!!

def toilet_function(n, m):
    d_o_d = (m-1)/n                # degree of dirtiness
    # (m-1) because for example 10 10 should have dirtiness degree of 0 but 10/10 is 1 so...
    temp_m = m - (n* d_o_d)
    if n%2 == 0 or n == 0:     # n is even
        if m%2 == 0 or m == 0: # m is even
            toilet_num = n - ((temp_m/2) - 1)
            print toilet_num, d_o_d
        else:                  # m is odd
            toilet_num = (temp_m/2) + 1
            print toilet_num, d_o_d
    else:                      # n is odd
        if d_o_d%2 == 0 or d_o_d == 0: #degree of dirtiness is even
            if m%2 == 0 or m == 0: # m is even
                toilet_num = n - ((temp_m/2) -1)
                print toilet_num, d_o_d
            else:                  # m is odd
                toilet_num = (temp_m/2) + 1
                print toilet_num, d_o_d
        else:                          #degree of dirtiness is odd
            if m%2==0 or m == 0:       # m is even
                toilet_num = n - temp_m/2
                print toilet_num, d_o_d
            else:                      # m is odd
                toilet_num = temp_m/2
                print toilet_num, d_o_d


def main():
    test_cases = int(raw_input(''))
    while test_cases > 0:
        n, m = raw_input('').split(' ')
        toilet_function(int(n), int(m))
        test_cases -= 1

main()
