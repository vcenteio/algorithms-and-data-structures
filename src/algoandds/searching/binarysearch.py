
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

    SIZE = 1000000
    TARGET = 802456

    l1 = [random.randint(0, SIZE) for _ in range(SIZE)]
    l1.sort()

    start = time.time()
    print(binary_search(l1, TARGET))
    end = time.time()
    print(f"elapsed time: {end-start}")

    start = time.time()
    print(binary_search_recursive(l1, TARGET))
    end = time.time()
    print(f"elapsed time: {end-start}")
