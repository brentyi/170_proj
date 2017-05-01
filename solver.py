#!/usr/bin/env python

from __future__ import division
import argparse
from decimal import *
import math
import time
import sys
getcontext().prec = 2

"""
===============================================================================
  Please complete the following function.
===============================================================================
"""


class Item:
    """
    Object version of item for ease of use and future features
    """
    def __init__(self, lst):
        self.name = lst[0]
        self.cls = lst[1]
        self.weight = lst[2]
        self.cost = lst[3]
        self.resell = lst[4]
        self.profit = self.resell - self.cost

    def __str__(self):
        return "Name: " + self.name + "\tClass: " + str(self.cls) + "\tWeight: " + str(self.weight) + "\tCost: " + str(self.cost) + "\tProfit: " + str(round(self.profit,2))
    def __repr__(self):
        return self.__str__()

class Heuristic:
    """
    Heuristic class has a list of functions to pass in as heuristics to compare the
    relative value of two items.
    """

    def h0(item):
        return item.profit/(item.cost + 0.01) # add 0.01 for 0 cost items

    def h1(item):
        return item.profit/(item.weight + 1) # add 1 to avoid div by zero error

    def h2(item):
        return item.profit/(1 +math.log(item.weight + 1))

    def h3(item):
        return math.log(item.profit + 1)/(item.weight + 1)

    def h4(item):
        return item.profit**2/(item.cost + 0.01) # add 0.01 for 0 cost items

    def h5(item):
        return item.profit**2/(item.weight + 1) # add 1 to avoid div by zero error

    def h6(item):
        return item.profit/((item.cost + 0.01) * (item.weight + 1))

    canon_lst = [h0, h1, h2, h3, h4, h5, h6]

    def a0(item):
        return math.log(item.profit)

    def a1(item):
        return item.profit
    
    def a2(item):
        return math.sqrt(item.profit)

    def a3(item):
        return 1/ (item.cost +0.01)

    def a4(item):
        return 1/ (1 + math.log(item.cost + 0.01))

    def a5(item):
        return math.sqrt(1/(item.cost + 0.01))
    
#    def a6(item):
 #       return math.sqrt(1/(1+ math.log(item.cost + 0.01)))

    def a7(item):
        return 1/ (item.weight +0.01)

    def a8(item):
        return 1/(1+math.log(item.weight + 0.01))

    def a9(item):
        return math.sqrt(1/(item.weight + 0.01))
    
  #  def a10(item):
   #     return math.sqrt(1/(1+ math.log(item.weight + 0.01)))

    lst = [a1,a2,a3,a4,a5,a7,a8,a9] # override

new_h = Heuristic.canon_lst[:]

def multiplied(i, j):
    return lambda item: i(item) * j(item)

def recursive_reapply(depth, func, min_idx=0 ):
    if depth == 0:
        new_h.append(func)
    else:
        for i in range(min_idx, len(Heuristic.lst)):
            recursive_reapply(depth-1, multiplied(Heuristic.lst[i], func), min_idx+1)
    
d = 2
for h in Heuristic.canon_lst:
    recursive_reapply(d, h, min_idx=3)
#for i in range(len(Heuristic.lst)):
#    for j in range(i, len(Heuristic.lst)):
#        f = multiplied(i, j)
#        new_h.append(f)
#
def weighted(weights):
    def h(item):
        output = 0
        for i in range(len(weights)):
            output += weights[i] * Heuristic.lst[i](item)
        return output
    return h

def recursive_weight_gen(depth):
    if depth == 0:
        return [[]]
    output = []
    following = recursive_weight_gen(depth - 1)
    for w in [0, 0.5, 1]:
        for f in following:
            output.append(f + [w])
    return output

for weights in recursive_weight_gen(3): # len(Heuristic.lst)):
    new_h.append(weighted(weights))

Heuristic.lst.extend(new_h)

def solve(P, M, N, C, items, constraints, heuristic=Heuristic().lst[0], constraint_map=None, item_list=list()):
    """
    Write your amazing algorithm here.

    constraints_map:  key: a class; value: set of incompatible classes
    item_list: list of item objects

    Return: a list of strings, corresponding to item names.
    """
    invalid_classes = set()     # classes that are constrained by what you've selected
    items_chosen = []

    def create_constraint_map():
        constraint_map = {}
        for c in constraints:
            for cls in c:
                if cls not in constraint_map:
                    constraint_map[cls] = []
                constraint_map[cls].append(c)
        return constraint_map

    def create_item_objects():
        lst = []
        for i in items:
            item = Item(i)
            if item.weight <= P and item.cost <= M and item.profit > 0: # add item only if weight and cost within reason
                lst.append(item)
        print("Finished creating ", len(lst), " valid item objects out of ", len(items), " original items")
        return lst

    def sort_item_objects(lst):
        item_list = sorted(lst, key=heuristic)
        # print("Finished sorting items")
        item_list.reverse()
        return item_list

    def print_items(lst, num_show=10):
        for i in range(num_show):
            print(item_list[i], "\tHeuristic Value: " + str(heuristic(item_list[i])))

    cls_visited = {}
    def select_item(item):
        if (item.cls in cls_visited or item.cls not in invalid_classes) and item.weight <= P and item.cost < M:
            if item.cls not in cls_visited:
                if item.cls in constraint_map:
                    for c in constraint_map[item.cls]:
                        if item.cls in c:
                            invalid_classes.update(c)
                            invalid_classes.remove(item.cls)
                cls_visited[item.cls] = True

            # print("Selected item ", counter, "\t", item)
            return item
        else:
            # print("Didn't select item ", counter, "\t", item)
            return None

    # else:
    #     print("Reuse old constraint map")
    if constraint_map == None:
        print("generating constraint map")
        constraint_map = create_constraint_map()

    if not item_list:
        item_list = create_item_objects()
    # else:
    #     print("Reuse old item list")

    # must resort items based on heuristic each time..
    item_list = sort_item_objects(item_list)

    counter = 0
    hundreth = len(item_list)//100
    for item in item_list:
        selected_item = select_item(item)
        if selected_item:
            items_chosen.append(selected_item)
            P -= selected_item.weight
            M -= selected_item.cost
        counter +=1
    print(">", end="")
    sys.stdout.flush()

    names = [item.name for item in items_chosen]
    net_money = M + sum([item.resell for item in items_chosen])

    return net_money, names, constraint_map, item_list

 

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
            name, cls, weight, cost, val = [s for s in f.readline().split(";")]
            items.append((name, int(cls), float(weight), float(cost), float(val)))
        for i in range(C):
            constraint = set([int(s) for s in f.readline().split(",")])
            constraints.append(constraint)
        return P, M, N, C, items, constraints

def write_output(filename, items_chosen):
    with open(filename, "w") as f:
        items_chosen = items_chosen if items_chosen else []
        for i in items_chosen:
            f.write("{0}\n".format(i))

def run_with_heuristics(P, M, N, C, items, constraints):
    """ Run each case with each heuristic and pick best one
    """
    print("P", P, "M", M, "N", N, "C", C)

    # create constraint map and item list to reuse between heuristics
    c_map = None;
    i_list = None;

    options = []
    for h in Heuristic.lst:
        money, lst, c_map, i_list = solve(P, M, N, C, items, constraints, h, c_map, i_list)
        options.append((lst, money, h))

    best = max(options, key=lambda x: x[1])
    average = sum([x[1] for x in options]) / len(Heuristic.lst)
    for i in range(len(options)):
        option = options[i]
        print("Heuristic " + str(i) + ": \t", str(round(option[1] / max(0.01, best[1]) * 100.0, 2)) + "% of best\t", str(round((option[1] - average) / max(0.01, average) * 100.0, 2)), "% from avg")
    return best





def run_all(is_hard, start=1, end=None, fill_missing=False):
    if not end:
        end = 21 if is_hard else 980

    summary_info = []
    if not fill_missing:
        for c in range(start,end + 1):
            print("*"*10, "PROBLEM",c,"*"*10)
            input_file = "hard_inputs/problem" + str(c) + ".in" if is_hard else "new_problems/problem" + str(c) + ".in"
            output_file = "output/problem" + str(c) + ".out" if is_hard else "new_problems_outputs/problem" + str(c) + ".out"
            P, M, N, C, items, constraints = read_input(input_file)
            # try:
            items_chosen, best_money, best_heuristic = run_with_heuristics(P, M, N, C, items, constraints)
            # except Exception:
            #     print("Giving up on this one\n")
            #     continue
            summary_info.append(["Problem ", str(c), "Best Heuristic: " + str(Heuristic.lst.index(best_heuristic)), "Best Money: " + str(best_money)])
            write_output(output_file, items_chosen)
            print("*"*30 + "\n")
    else:
        # only operate on output files that do not exist
        from pathlib import Path

        for c in range(start,end + 1):
            supposed_output_path = "output/problem" + str(c) + ".out" if is_hard else "new_problems_outputs/problem" + str(c) + ".out"
            output_file = Path(supposed_output_path)
            if not output_file.is_file():
                print("*"*10, "REFILLING PROBLEM",c,"*"*10)
                input_file = "hard_inputs/problem" + str(c) + ".in" if is_hard else "new_problems/problem" + str(c) + ".in"
                P, M, N, C, items, constraints = read_input(input_file)
                items_chosen, best_money, best_heuristic = run_with_heuristics(P, M, N, C, items, constraints)
                summary_info.append(["Problem ", str(c), "Best Heuristic: " + str(Heuristic.lst.index(best_heuristic)), "Best Money: " + str(best_money)])
                write_output(supposed_output_path, items_chosen)
                print("*"*30 + "\n")
                
                


    for summary in summary_info:
        print('\t'.join(summary))

is_hard = 1 # 0: run all inputs, 1: run hard inputs
run_all(is_hard, fill_missing=True)

