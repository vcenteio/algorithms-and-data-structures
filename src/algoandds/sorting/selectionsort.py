from typing import Mapping, Sequence, Union
try:
    from ..tools.tools import get_class_name, minindex
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
    from tools.tools import get_class_name, minindex


def selection_sort(seq: Union[Sequence, Mapping]) -> Union[Sequence, Mapping]:
    if not isinstance(seq, (Sequence, Mapping)):
        raise TypeError(
            f"Inappropriate argument type ({get_class_name(seq)}).")
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


# for manual testing purposes
if __name__ == "__main__":
    from random import randint
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
    from linkedlist import LinkedList
    from tools.tools import scrumble

    l1 = scrumble(LinkedList((i for i in range(10))))
    l2 = [randint(0, 10) for _ in range(10)]
    t1 = tuple((i for i in range(10)))
    d1 = {randint(0, 10): randint(0, 10) for _ in range(10)}
