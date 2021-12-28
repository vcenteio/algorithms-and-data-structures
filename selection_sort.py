from typing import Mapping, Sequence, Union
from tools import *
from linked_list import LinkedList
from random import randint


def selection_sort(seq: Union[Sequence, Mapping]) -> Union[Sequence, Mapping]:
    if not isinstance(seq, (Sequence, Mapping)):
        raise TypeError(f"Inappropriate argument type ({get_class_name(seq)}).")
    seq_type = seq.__class__
    seq_copy = seq.copy() if hasattr(seq, "copy") else seq[:]
    is_mapping = isinstance(seq, Mapping) 
    sorted_seq = dict() if is_mapping else list() 
    min_func = min if is_mapping else minindex
    insert_func = sorted_seq.update if is_mapping else sorted_seq.append
    while len(seq_copy):
        min_index = min_func(seq_copy)
        min_item = seq_copy.pop(min_index)
        item_to_insert = {min_index: min_item} if is_mapping else min_item
        insert_func(item_to_insert)
    return seq_type(sorted_seq)


# for manual test purposes
if __name__ == "__main__":
    l1 = scrumble(LinkedList((i for i in range(10))))
    l2 = [randint(0,10) for i in range(10)]
    t1 = tuple((i for i in range(10)))
    d1 = {randint(0,10):randint(0,10) for i in range(10)}
