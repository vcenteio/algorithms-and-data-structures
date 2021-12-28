from typing import Sequence
from linked_list import LinkedList
from random import randint
from tools import *


def bogo_sort(seq: Sequence) -> Sequence:
    if not isinstance(seq, Sequence):
        raise TypeError(
            f"Object of type {get_class_name(seq)} is not a sequence."
        )
    while not is_sorted(seq):
        seq = scrumble(seq)
    return seq


if __name__ == "__main__":
    l1 = scrumble(LinkedList((i for i in range(10))))
    l2 = [randint(0,10) for i in range(10)]
    t1 = tuple((i for i in range(10)))
    d1 = {randint(0,10):randint(0,10) for i in range(10)}