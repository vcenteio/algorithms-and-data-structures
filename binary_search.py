
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

def binary_search_recursive(list, target):
    if not list:
        return None 
    midpoint = len(list) // 2
    if list[midpoint] == target:
        return midpoint
    elif list[midpoint] < target:
        return binary_search_recursive(list[midpoint+1:], target)
    else:
        return binary_search_recursive(list[:midpoint], target)


# for manual testing purposes
if __name__ == "__main__":
    import random
    import time
    from memory_profiler import memory_usage

    SIZE = 1000000
    TARGET = 802456

    l = [random.randint(0, SIZE) for i in range(SIZE)]
    l.sort()

    start = time.time()
    print(binary_search(l, TARGET))
    end = time.time()
    print(f"elapsed time: {end-start}")

    start = time.time()
    print(binary_search_recursive(l, TARGET))
    end = time.time()
    print(f"elapsed time: {end-start}")