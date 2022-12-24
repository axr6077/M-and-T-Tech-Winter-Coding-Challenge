#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'encryption' function below.
#
# The function is expected to return a STRING.
# The function accepts STRING s as parameter.
#

def encryption(s):
    # Write your code here
    rem_space = s.replace(' ', '')
    cols = int(math.ceil(math.sqrt(len(rem_space))))
    res = ""
    for col in range(cols):
        for idx in range(col, len(rem_space), cols):
            res += rem_space[idx]
        res = res + ' '
    return res

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    s = input()

    result = encryption(s)

    fptr.write(result + '\n')

    fptr.close()
