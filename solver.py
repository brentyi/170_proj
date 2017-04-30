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
        self.lst = [self.h0]

    def h0(self, item1):
        return item1.profit/item1.resell
    
        


def solve(P, M, N, C, items, constraints, heuristic=Heuristic().lst[0]):
    """
    Write your amazing algorithm here.

    Return: a list of strings, corresponding to item names.
    """
    constraints_map = dict()    # key: a class; value: set of incompatible classes
    item_list = []              # list of item objects
    invalid_classes = set()     # classes that are constrained by what you've selected
    items_chosen = []

    def create_constraints():
        constraint_counter = 1
        for c in constraints:
            constraint_counter += 1
            for cls in c:
                if not cls in constraints_map:
                    constraints_map[cls] = set()
                constraints_map[cls].update(({v for v in c if v != cls}))
        print("Created ", constraint_counter, " constraints.")

    def create_item_objects():
        lst = []
        for i in items:
            item = Item(i)
            if item.weight <= P and item.cost <= M: # add item only if weight and cost within reason
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
            item_list.append(item)
            invalid_classes.update(constraints_map[item.cls])
            # print("Selected item ", counter, "\t", item)
            return item
        else:
            # print("Didn't select item ", counter, "\t", item)
            return None

            
    create_constraints()
    item_list = create_item_objects()
    item_list = sort_item_objects(item_list)
    print_items(item_list)

    select_counter = 0
    for item in item_list:
        selected_item = select_item(item)
        if selected_item:
            items_chosen.append(selected_item)
            P -= selected_item.weight
            M -= selected_item.cost
            select_counter +=1

    names = [item.name for item in items_chosen]
    net_money = M + sum([item.profit for item in items_chosen])

    return net_money, names

 

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

def run_with_heuristics(P, M, N, C, items, constraints):
    """ Run each case with each heuristic and pick best one
    """
    h_counter = 0

    max_money = M
    max_item_list = []
    max_heuristic = h_counter

    for h in Heuristic().lst:
        money, lst = solve(P, M, N, C, items, constraints, h)
        if money > max_money:
            max_money = money
            max_item_list = lst
            max_heuristic = h
            print("MAX", "Heuristic number", h_counter, "got money:", money)
        else:
            print("\t", "Heuristic number", h_counter, "got money:", money)
        h_counter += 1
    return max_item_list 





def run_all(start=1, end=21):
    for c in range(start,end + 1):
        input_file = "hard_inputs/problem" + str(c) + ".in"
        output_file = "outputs/problem" + str(c) + ".out"
        P, M, N, C, items, constraints = read_input(input_file)
        items_chosen = run_with_heuristics(P, M, N, C, items, constraints)
        write_output(output_file, items_chosen)

run_all(end=1)
