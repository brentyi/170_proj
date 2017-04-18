#!/usr/bin/python3

import random

def val_rand(a, b):
    return int(random.uniform(a, b) * 100) / 100.0

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


print(P) # pounds
print(M) # dollars
print(N) # items
print(C) # contraints

for item in items:
    print("; ".join([str(x) for x in item]))
for constraint in constraints:
    print("; ".join([str(x) for x in constraint]))

