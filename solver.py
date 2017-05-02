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
    def __init__(self, lst, constraints):
        self.name = lst[0]
        self.cls = lst[1]
        self.weight = lst[2]
        self.cost = lst[3]
        self.resell = lst[4]
        self.profit = self.resell - self.cost
        self.constraint_count = len(constraints) if constraints else 0

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

    def h7(item):
        return item.profit/(item.constraint_count + 1)


    def h8(item):
        return item.profit/((item.constraint_count + 1) * (item.cost + 0.01))

    def h9(item):
        return item.profit/((item.constraint_count + 1) * (item.weight + 1))

    def h10(item):
        return item.profit/((item.cost + 0.01) *(item.constraint_count + 1) * (item.weight + 1))
    canon_lst = [h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10]

    def a0(item):
        return 1/(1 + item.constraint_count)

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

    lst = [a0,a1,a3,a4,a5,a7,a8,a9]# override

new_h = Heuristic.canon_lst[:]

def multiplied(i, j):
    return lambda item: i(item) * j(item)

def recursive_reapply(depth, func, min_idx=0 ):
    if depth == 0:
        new_h.append(func)
    else:
        for i in range(min_idx, len(Heuristic.lst)):
            recursive_reapply(depth-1, multiplied(Heuristic.lst[i], func), min_idx+1)

reapp_depth = 2
for h in Heuristic.canon_lst:
    recursive_reapply(reapp_depth, h, min_idx=3)
#for i in range(len(Heuristic.lst)):
#    for j in range(i, len(Heuristic.lst)):
#        f = multiplied(i, j)
#        new_h.append(f)
#
def weighted(weights):
    def h(item):
        output = 0
        for i in range(len(weights)):
            output += weights[i] * Heuristic.canon_lst[i](item)
        return output
    return h

def recursive_weight_gen(depth):
    if depth == 0:
        return [[]]
    output = []
    following = recursive_weight_gen(depth - 1)
    for w in [0, 0.3, 0.7, 1]:
        for f in following:
            output.append(f + [w])
    return output

for weights in recursive_weight_gen(2): #len(Heuristic.canon_lst)):
    new_h.append(weighted(weights))


# commented this out because it's causing duplicate heuristics
# Heuristic.lst.extend(Heuristic.canon_lst)
Heuristic.lst += new_h

heuristic_index_lookup = dict()
for i in range(len(Heuristic.lst)):
    heuristic_index_lookup[Heuristic.lst[i]] = i


def solve(P, M, N, C, items, constraints, heuristic=Heuristic().lst[0], constraint_map=None, item_list=None):
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
            cls = i[1]
            item = Item(i, constraint_map.get(cls))
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

    if item_list == None:
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
        print("Heuristic " + str(heuristic_index_lookup[option[2]]) + ": \t", str(round(option[1] / max(0.01, best[1]) * 100.0, 2)) + "% of best\t", str(round((option[1] - average) / max(0.01, average) * 100.0, 2)), "% from avg")
    return best


def test_heuristics(problem, P, M, N, C, items, constraints, count_money_map):
    """ Test and ranks heuristics in map
    """
    print("P", P, "M", M, "N", N, "C", C)

    # create constraint map and item list to reuse between heuristics
    c_map = None;
    i_list = None;

    options = []
    count = 0

    most_money = 0
    print("Running", len(Heuristic.lst), "heuristics!")
    for h in Heuristic.lst:
        money, lst, c_map, i_list = solve(P, M, N, C, items, constraints, h, c_map, i_list)
        options.append((lst, money, h, count))
        if money > most_money:
            most_money = money
        count += 1
    options.sort(key=lambda k: -k[1])

    o = 0
    for lst, money, h, count in options:
        o += 1
        ratio = money / most_money
        # print("Heuristic", count, "has ranking ", o, "and makes", money, "moneys", ratio, "of best")
        count_money_map[h].append(ratio) # use 15 - ranking value; larger values mean better ranking



def sample_prune_heuristics(num_heuristics, is_hard):
    """
    Run all generated heuristics on 21 hard files to reduce number of heuristics to be used.
    Then remove heuristics that are not the best
    """
    heuristic_rank_map = dict()
    for h in Heuristic.lst:
      heuristic_rank_map[h] = []

    old_lst = Heuristic.lst

    def print_stats(stats):
        print("\n\n")
        max_score = max([s[1] for s in stats])
        print("---")
        for s in stats:
            h = s[0]
            score = s[1]
            if s[1] > 0:
              print("Heuristic", heuristic_index_lookup[h], "\t", score, heuristic_rank_map[h])

        print("\n\n")
        for s in stats:
            h = s[0]
            score = s[1]
            if s[1] > 0:
                print("Heuristic", heuristic_index_lookup[h], "\t", "*"*int((score * 100)//max_score))
        print("---")

    for c in range(1,100): # run sampling over first few 
        Heuristic.lst = old_lst

        print("*"*10, "PRUNING WITH SAMPLE PROBLEM",c,"*"*10)
        input_file = ("hard_inputs/problem" if is_hard else "new_problems/problem") + str(c) + ".in"
        P, M, N, C, items, constraints = read_input(input_file)
        test_heuristics(c, P, M, N, C, items, constraints, heuristic_rank_map)


        old_lst = Heuristic.lst
        # Heuristic.lst =  [Heuristic.lst[i] for i in sorted(range(len(Heuristic.lst)), key=lambda h: sum(heuristic_rank_map[h]) if h in heuristic_rank_map else 0)[-30:]]
        # Heuristic.lst = sorted(Heuristic.lst, key=lambda h: -sum(heuristic_rank_map[h]))
        # stats = [(i,sum(heuristic_rank_map.get(i) if heuristic_rank_map.get(i) else []) )
        #    for i in sorted(range(len(Heuristic.lst)), key=lambda h: sum(heuristic_rank_map[h]) if h in heuristic_rank_map else 0)[-30:]]
        # stats = [(h, sum([p[1] for p in heuristic_rank_map[h]])) for h in Heuristic.lst]
        stats = []
        # Heuristic.lst = sorted(Heuristic.lst, key=lambda h: -sum([p[1] for p in heuristic_rank_map[h]]))
        solved_problems = set()
        def score_heuristic(h):
          score = 0
          problem = 1
          for s in heuristic_rank_map[h]:
              if problem not in solved_problems and s > 0.995:
                  score += s
              problem += 1
          return score

        to_process = list(Heuristic.lst)
        while len(to_process) > 0:
            best = max(to_process, key=lambda h: score_heuristic(h))
            score = score_heuristic(best)

            # if score == 0 and len(heuristic_rank_map[h]:
            #     

            to_process.remove(best)

            if score >= 0:
              problem = 1
              for s in heuristic_rank_map[best]:
                  if s > 0.995:
                      solved_problems.add(problem)
                  problem += 1
              stats.append((best, score))

        if len(heuristic_rank_map[Heuristic.lst[0]]) == 10:
            to_remove = []
            for h1 in Heuristic.lst:
                if h1 in to_remove:
                    continue
                for h2 in Heuristic.lst:
                    if h1 == h2:
                        continue
                    # mean_error = 0.0
                    max_error = 0.0
                    for i in range(10):
                        error = abs(heuristic_rank_map[h1][i] - heuristic_rank_map[h2][i])
                        # mean_error += error
                        max_error = max(max_error, error)
                    # mean_error /= 10.0
                    # if mean_error < 0.005:
                    if max_error < 0.005:
                        to_remove.append(h2)
            for h in to_remove:
                if h in Heuristic.lst:
                    Heuristic.lst.remove(h)

        print_stats(stats)

    print_stats(stats)




    # rank_heuristics_array = sorted([sum(v) for v in heuristic_rank_map.values()], key=lambda x: -x)
    # rank_heuristics = rank_heuristics_array[min(len(rank_heuristics_array)-1, num_heuristics)] # gets (num_heuristics)th sum of rankings
    # best_heuristics_lst = [Heuristic.lst[i] for i in range(len(Heuristic.lst)) if sum(heuristic_rank_map.get(i)) < rank_heuristics] # only take the best (num_heuristics) heuristics
    # Heuristic.lst = best_heuristics_lst


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
            summary_info.append(["Problem ", str(c), "Best Heuristic: " + str(heuristic_index_lookup[best_heuristic]), "Best Money: " + str(best_money)])
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
                summary_info.append(["Problem ", str(c), "Best Heuristic: " + str(heuristic_index_lookup[best_heuristic]), "Best Money: " + str(best_money)])
                write_output(supposed_output_path, items_chosen)
                print("*"*30 + "\n")

    for summary in summary_info:
        print('\t'.join(summary))


# Heuristic.lst = [Heuristic.lst[13]]
# new_h = list()
# for i in [241,186,38,212,248,0,22,81,95,96,135,155,160]:
#     new_h.append(Heuristic.lst[i])
# Heuristic.lst = new_h

is_hard = 1 # 0: run all inputs, 1: run hard inputs

print("Originally have ", len(Heuristic.lst), "heuristics")
# sample_prune_heuristics(30, 0)
print("After pruning, we  have ", len(Heuristic.lst), "heuristics")
run_all(is_hard, start=1)
