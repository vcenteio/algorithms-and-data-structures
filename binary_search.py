import random
import time
from memory_profiler import memory_usage

SIZE = 1000000
TARGET = 802456

def binary_search(list, target):
    first, last = 0, len(list)-1
    while first <= last:
        midpoint = (first+last) // 2
        if list[midpoint] == target:
            return midpoint
        elif list[midpoint] < target:
            first = midpoint + 1
        else:
            last = midpoint - 1
    return None

def recursive_binary_search(list, target):
    if not list:
        return False
    
    midpoint = len(list) // 2
    if list[midpoint] == target:
        return True
    elif list[midpoint] < target:
        return recursive_binary_search(list[midpoint+1:], target)
    else:
        return recursive_binary_search(list[:midpoint], target)

def linear_search(list, target):
    for i in range(len(list)):
        if list[i] == target:
            return i
    return None

l = [random.randint(0, SIZE) for i in range(SIZE)]
l.sort()

start = time.time()
print(binary_search(l, TARGET))
end = time.time()
print(f"elapsed time: {end-start}")

start = time.time()
print(recursive_binary_search(l, TARGET))
end = time.time()
print(f"elapsed time: {end-start}")

# start = time.time()
# print(linear_search(l, TARGET))
# end = time.time()
# print(f"elapsed time: {end-start}")
