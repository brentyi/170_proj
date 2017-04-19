#!/usr/bin/python3

import random
import time
import datetime

def val_rand(a, b):
    return int(random.uniform(a, b) * 100) / 100.0


def generate():
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%H_%M_%S-%Y_%m_%d')
    with open('generated_inputs/generated_' + timestamp, 'w') as f:

        # Pound limit
        P = val_rand(100, 200)
        # Dollar limit
        M = val_rand(100, 200)
        # Number of items
        N = 1000
        # Number of constraints
        C = 20

        # Number of classes
        class_count = N // 3

        items = []
        constraints = []
        item_data = []

        # Add items
        for i in range(N):
            name = "item" + str(i)
            item_class = random.randrange(class_count)
            weight = val_rand(P / 100, P/10)
            cost = val_rand(50, 100)
            resale = val_rand(50, 100)
            items.append((name, item_class, weight, cost, resale))
            item_data.append([resale, cost, weight, i])

        # Add constraints
        for i in range(C):
            n = random.randrange(2, class_count // 5)
            classes = [random.randrange(class_count) for i in range(n)]
            constraints.append(tuple(set(classes))) # remove duplicates in constraints with set



        ADDITIONAL_ITEMS = 3
        ADDITIONAL_CONSTRAINTS = class_count * 3 + 1
        # add items to fool greedy approaches

        item_data.sort(key=lambda entry: -(entry[0] - entry[1])/entry[2]) # sort by increasing profit/weight ratio
        best_item = item_data[0]

        best_weight = best_item[2]
        best_cost = best_item[1]
        best_resale = best_item[0]
       
        greedy_weight = best_weight - 0.01
        # make scale versions of cost and resale based on weight
        greedy_cost = best_cost
        greedy_resale = best_resale
        
        # scaled up version of best item, can only buy one due to weight, slightly better profit/weight ratio
        greedy_item0 = ['g0', class_count + 1, greedy_weight, greedy_cost, greedy_resale]
        greedy_item1 = ["g1", class_count + 2, 0, 0, 1]
        greedy_item2 = ["g2", class_count + 3, 1, 2 * M, 100 * M]

        
        # make greedy class constrained against all other class
        greedy_constraints = []
        for c in range(class_count):
            greedy_constraints.append((class_count + 1, c))
            greedy_constraints.append((class_count + 2, c))
            greedy_constraints.append((class_count + 3, c))
        
        f.write(str(P) + "\n") # pounds
        f.write(str(M) + "\n") # dollars
        f.write(str(N + ADDITIONAL_ITEMS) + "\n") # items
        f.write(str(C + len(greedy_constraints)) + "\n") # constraints

        for item in items:
            f.write(", ".join([str(x) for x in item]) + "\n")

        # add greedy item
        f.write("; ".join([str(x) for x in greedy_item0]) + "\n")
        f.write("; ".join([str(x) for x in greedy_item1]) + "\n")
        f.write("; ".join([str(x) for x in greedy_item2]) + "\n")


        
        for constraint in constraints:
            f.write(", ".join([str(x) for x in constraint]) + "\n")

        # add greedy constraints
        for constraint in greedy_constraints:
            f.write(", ".join([str(x) for x in constraint]) + "\n")
        # no greedy classes can join with each other
        # f.write(", ".join([str(class_count + 1),str(class_count +2), str(class_count + 3)])
generate()
