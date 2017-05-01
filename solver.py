#!/usr/bin/env python

from __future__ import division
import argparse
from decimal import *
import math
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
    def __init__(self):
        self.lst = [self.h0, self.h1, self.h2, self.h3,self.h4,self.h5,self.h6,self.h7,self.h8,self.h9,self.h10]

    def h0(self, item):
        return item.profit/(item.cost + 0.01) # add 0.01 for 0 cost items
    
    def h1(self, item):
        return item.profit/(item.weight + 1) # add 1 to avoid div by zero error

    def h2(self, item):
        return self.h0(item) * self.h1(item)

    def h3(self, item):
        return self.h0(item) + self.h1(item)

    def h4(self, item):
        return self.h0(item) + 2 * self.h1(item)

    def h5(self, item):
        return 2 * self.h0(item) + self.h1(item)
        
    def h6(self, item):
        return item.profit/(1 +math.log(item.weight + 1))

    def h7(self, item):
        return math.log(item.profit + 1)/(item.weight + 1)
    
    def h8(self, item):
        return item.profit**2/(item.cost + 0.01) # add 0.01 for 0 cost items
    
    def h9(self, item):
        return item.profit**2/(item.weight + 1) # add 1 to avoid div by zero error

    def h10(self, item):
        return item.profit**2/((item.weight + 1) * (item.cost + 0.01)) # add 1 to avoid div by zero error

def solve(P, M, N, C, items, constraints, heuristic=Heuristic().lst[0], constraints_map=None, item_list=list()):
    """
    Write your amazing algorithm here.

    constraints_map:  key: a class; value: set of incompatible classes
    item_list: list of item objects

    Return: a list of strings, corresponding to item names.
    """
    invalid_classes = set()     # classes that are constrained by what you've selected
    items_chosen = []

    def create_constraints():
        constraint_counter = 1
        for c in constraints:
            constraint_counter += 1
            for cls in c:
                if not cls in constraints_map:
                    constraints_map[cls] = set()
                # constraints_map[cls].update(({v for v in c if v != cls}))
                constraints_map[cls].update(c)
                constraints_map[cls].remove(cls)
        print("Created ", constraint_counter, " constraints.")

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
        print("Finished sorting items")
        item_list.reverse()
        return item_list

    def print_items(lst, num_show=10):
        for i in range(num_show):
            print(item_list[i], "\tHeuristic Value: " + str(heuristic(item_list[i])))

    def select_item(item):
        if item.cls not in invalid_classes and item.weight <= P and item.cost < M:
            incompat = constraints_map.get(item.cls) 
            if incompat:
                invalid_classes.update(incompat)

            # print("Selected item ", counter, "\t", item)
            return item
        else:
            # print("Didn't select item ", counter, "\t", item)
            return None

            
    if not constraints_map:
        constraints_map = dict()
        create_constraints()
    else:
        print("Reuse old constraint map")

    if not item_list:
        item_list = create_item_objects()
    else:
        print("Reuse old item list")

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
        if(counter % hundreth == 0):
            print(".", end="")
    print("")
    
    names = [item.name for item in items_chosen]
    net_money = M + sum([item.resell for item in items_chosen])

    return net_money, names, constraints_map, item_list

 

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

def run_with_heuristics(P, M, N, C, items, constraints):
    """ Run each case with each heuristic and pick best one
    """
    print("P", P, "M", M, "N", N, "C", C)
    h_counter = 0

    max_money = M
    max_item_list = []
    max_heuristic = h_counter

    # create constraint map and item list to reuse between heuristics
    c_map = None;
    i_list = None;

    
    
    for h in Heuristic().lst:
        if c_map and i_list:
            money, lst, c_map, i_list = solve(P, M, N, C, items, constraints, h, c_map, i_list)
        else:
            money, lst, c_map, i_list = solve(P, M, N, C, items, constraints, h)

        if money > max_money:
            max_money = money
            max_item_list = lst
            max_heuristic = h
            print("MAX\t", "Heuristic number", h_counter, "got money:", money)
        else:
            print("\t", "Heuristic number", h_counter, "got money:", money)
        h_counter += 1
    return max_item_list, max_money, max_heuristic





def run_all(start=1, end=21):
    summary_info = []
    for c in range(start,end + 1):
        print("*"*10, "PROBLEM",c,"*"*10)
        input_file = "hard_inputs/problem" + str(c) + ".in"
        output_file = "output/problem" + str(c) + ".out"
        P, M, N, C, items, constraints = read_input(input_file)
        items_chosen, best_money, best_heuristic = run_with_heuristics(P, M, N, C, items, constraints)
        summary_info.append(["Problem ", str(c), "Best Heuristic: " + str(best_heuristic), "Best Money: " + str(best_money)])
        write_output(output_file, items_chosen)
        print("*"*30)
        print()

    for summary in summary_info:
        print('\t'.join(summary))

run_all()
