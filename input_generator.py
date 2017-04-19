#!/usr/bin/python3

import random
import time
import datetime

def val_rand(a, b):
    return int(random.uniform(a, b) * 100) / 100.0


def generate():
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H_%M_%S')
    with open('generated_inputs/generated_' + timestamp, 'w') as f:

        # Pound limit
        P = val_rand(100, 200)
        # Dollar limit
        M = val_rand(100, 200)
        # Number of items
        N = 100
        # Number of constraints
        C = 20

        # Number of classes
        class_count = N // 3

        items = []
        constraints = []

        # Add items
        for i in range(N):
            name = "item" + str(i)
            item_class = random.randrange(class_count)
            weight = val_rand(P / 100, P/10)
            cost = val_rand(50, 100)
            resale = val_rand(50, 100)
            items.append((name, item_class, weight, cost, resale))

        # Add constraints
        for i in range(C):
            n = random.randrange(2, class_count // 3)
            classes = [random.randrange(class_count) for i in range(n)]
            constraints.append(tuple(classes))


        
        f.write(str(P)) # pounds
        f.write(str(M)) # dollars
        f.write(str(N)) # items
        f.write(str(C)) # contraints

        for item in items:
            f.write("; ".join([str(x) for x in item]))
        for constraint in constraints:
            f.write("; ".join([str(x) for x in constraint]))
generate()
