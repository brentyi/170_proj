#!/usr/bin/env python

from __future__ import division
import argparse
from decimal import *
getcontext().prec = 2

"""
===============================================================================
  Please complete the following function.
===============================================================================
"""

def solve(P, M, N, C, items, constraints):
    """
  Write your amazing algorithm here.

  Return: a list of strings, corresponding to item names.
  """
    pass


"""
===============================================================================
  No need to change any code below this line.
===============================================================================
"""

def read_input(filename):
    """
  P: float
  M: float
  N: integer
  C: integer
  items: list of tuples
  constraints: list of sets
  """
    with open(filename) as f:
        P = float(Decimal(f.readline()))
        M = float(Decimal(f.readline()))
        N = int(f.readline())
        C = int(f.readline())
        items = []
        constraints = []
        for i in range(N):
            name, cls, weight, cost, val = f.readline().split(";")
            items.append((name, int(cls), float(weight), float(cost), float(val)))
        for i in range(C):
            constraint = set(eval(f.readline()))
            constraints.append(constraint)
        return P, M, N, C, items, constraints

def write_output(filename, items_chosen):
    with open(filename, "w") as f:
        items_chosen = items_chosen if items_chosen else []
        for i in items_chosen:
            f.write("{0}\n".format(i))



def run_all(start=1, end=21):
    for c in range(start,end + 1):
        input_file = "hard_inputs/problem" + str(c) + ".in"
        output_file = "outputs/problem" + str(c) + ".out"
        P, M, N, C, items, constraints = read_input(input_file)
        items_chosen = solve(P, M, N, C, items, constraints)
        write_output(output_file, items_chosen)

run_all(end=1)
