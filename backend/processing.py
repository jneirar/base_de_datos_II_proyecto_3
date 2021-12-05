from typing import Collection
import numpy
import matplotlib.pyplot as plt
import random
import json
import linecache
import io
from rtree import index
import os
from queue import PriorityQueue
from timeit import default_timer as timer

line = linecache.getline('data.json', 1).rstrip()
item_json = json.load(io.StringIO(line))
dict128VectorPhotos = dict(item_json)
dictPhotos = {}
vectors = []
for key in dict128VectorPhotos:
    np = numpy.array(list(map(float, key.strip("()").split(', '))))
    vectors.append(np)
    nameKey = dict128VectorPhotos[key].split('/')[1]
    if nameKey not in dictPhotos:
        dictPhotos[nameKey] = [np]
    else:
        dictPhotos[nameKey].append(np)

n = len(vectors)

print("Total: ", n)
m = 5000
values = []

for i in range(m):
    arr1 = vectors[random.randrange(n-1)]
    arr2 = vectors[random.randrange(n-1)]
    dist = numpy.linalg.norm(arr1-arr2)
    values.append(dist)

plt.hist(values, bins=100)
plt.show()
