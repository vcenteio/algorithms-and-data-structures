from typing import Sequence

try:
    from ..tools.tools import get_class_name, is_sorted, scrumble
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
    from tools.tools import get_class_name, is_sorted, scrumble


def bogo_sort(seq: Sequence) -> Sequence:
    if not isinstance(seq, Sequence):
        raise TypeError(
            f"Object of type {get_class_name(seq)} is not a sequence."
        )
    while not is_sorted(seq):
        seq = scrumble(seq)
    return seq


# for manual testing purposes
if __name__ == "__main__":
    from random import randint
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
    from linkedlist import LinkedList

    l2 = [randint(0, 10) for _ in range(10)]
    l3 = LinkedList((randint(0, 10000) for _ in range(10000)))
    t1 = tuple((randint(0, 10)*i for i in range(10)))
    d1 = {randint(0, 10): randint(0, 10) for _ in range(10)}
