#!/usr/bin/env python3

import sys


def usage():
    pass


def fingerprint():
    pass


def shuffle(nStart, nEnd, nBy):
    for n in range(nStart, nEnd + 1, nBy):
        twoNPlusOne = 2 * n + 1
        s = 1
        k = 2
        while (k != 1):
            s += 1
            if 2 <= k <= n:
                k *= 2
            elif k > n:
                k = 2 * k - twoNPlusOne
            else:
                break
        print(str(n) + " " + str(s) + " ")


def main():
    argv = sys.argv[1:]
    argc = len(argv)
    if argc == 1:
        shuffle(int(argv[0]), int(argv[0]), 1)
    elif argc == 2:
        shuffle(int(argv[0]), int(argv[1]), 1)
    elif argc == 3:
        shuffle(int(argv[0]), int(argv[1]), int(argv[2]))


if __name__ == "__main__":
    main()
