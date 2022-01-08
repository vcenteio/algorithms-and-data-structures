from typing import Sequence

try:
    from ..tools.tools import get_class_name
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
    from tools.tools import get_class_name


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
        quick_sort(seq_type(lesser_than_pivot)) +
        seq_type((pivot,)) +
        quick_sort(seq_type(greater_than_pivot))
    )


# for manual testing purposes
if __name__ == "__main__":
    from random import randint
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
    from linkedlist import LinkedList
    from tools.tools import scrumble

    l1 = scrumble(LinkedList((i for i in range(10))))
    l2 = [randint(0, 10) for i in range(10)]
    l3 = LinkedList((randint(0, 10000) for _ in range(10000)))
    t1 = tuple((randint(0, 10)*i for i in range(10)))
    d1 = {randint(0, 10): randint(0, 10) for _ in range(10)}
