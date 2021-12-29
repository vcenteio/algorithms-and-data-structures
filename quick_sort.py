from typing import Mapping, Sequence, Union
from tools import *
from linked_list import LinkedList
from random import randint


def quick_sort(seq: Sequence) -> Sequence:
    if not isinstance(seq, Sequence) or isinstance(seq, (str, bytes)):
        raise TypeError(f"Inappropriate argument type {get_class_name(seq)}.")
    if len(seq) <= 1:
        return seq
    seq_type = seq.__class__
    pivot = seq[0] 
    lesser_than_pivot = list() 
    greater_than_pivot = list()
    for item in seq[1:]:
        if item <= pivot:
            lesser_than_pivot.append(item)
        else:
            greater_than_pivot.append(item)
    return seq_type(
        quick_sort(seq_type(lesser_than_pivot)) + \
        seq_type((pivot,)) + \
        quick_sort(seq_type(greater_than_pivot))
    )


# for manual testing purposes
if __name__ == "__main__":
    l1 = scrumble(LinkedList((i for i in range(10))))
    l2 = [randint(0,10) for i in range(10)]
    l3 = LinkedList((randint(0, 10000) for i in range(10000)))
    t1 = tuple((randint(0,10)*i for i in range(10)))
    d1 = {randint(0,10):randint(0,10) for i in range(10)}