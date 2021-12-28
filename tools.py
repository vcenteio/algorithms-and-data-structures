from typing import Sequence, Mapping, Any
from random import shuffle


def is_sorted(seq: Sequence) -> bool:
    for i in range(len(seq)-1):
        if seq[i] > seq[i+1]:
            return False
    return True

def get_class_name(obj: Any):
    return obj.__class__.__name__

def generate_random_indexes(length: int) -> list:
    indexes = [i for i in range(length)]
    shuffle(indexes)
    return indexes

def scrumble(seq: Sequence) -> Sequence:
    seq_type = seq.__class__
    new_sequence = list()
    random_indexes = generate_random_indexes(len(seq))
    for i in random_indexes:
        new_sequence.append(seq[i])
    return seq_type(new_sequence)

def minindex(seq: Sequence) -> int:
    if not isinstance(seq, (Sequence, Mapping)):
        raise TypeError(f"Inappropriate argument type ({get_class_name(seq)}).")
    iter_obj = iter(seq)
    current_item = minimum = next(iter_obj)
    index = minimum_index = 0
    while True:
        try:
            current_item = next(iter_obj)
            index += 1
            if current_item < minimum:
                minimum = current_item
                minimum_index = index
        except StopIteration:
            break
    return minimum_index 