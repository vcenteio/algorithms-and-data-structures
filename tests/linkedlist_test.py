from typing import Iterable
import pytest
from random import randint

from src.algoandds.linkedlist import LinkedList, Node, INode


@pytest.fixture
def l0():
    return LinkedList()


@pytest.fixture
def l1():
    return LinkedList(1)


@pytest.fixture
def l2():
    return LinkedList([i for i in range(20)])


def test_linked_list_set_node_type_wrong_type(l0: LinkedList):
    with pytest.raises(TypeError):
        l0._set_node_type(str)
    with pytest.raises(TypeError):
        l0._set_node_type(LinkedList)
    with pytest.raises(TypeError):
        l0._set_node_type(1)


def test_linked_list_set_node_type_correct_type(l0: LinkedList):
    l0._set_node_type(Node)
    assert l0._node_type == Node


def test_linked_list_is_empty(l0: LinkedList, l1: LinkedList):
    assert l0.is_empty()
    assert not l1.is_empty()


def test_linked_list_tail(l0: LinkedList, l1: LinkedList):
    assert l0.tail is None
    assert l1.tail == 1
    l1.tail.set_next_node(l1._create_new_node(2))
    assert l1.tail == 2


def test_linked_list_append_empty_list(l0: LinkedList):
    l0.append(1)
    assert l0.head == 1


def test_linked_list_append_non_empty_list(l1: LinkedList):
    l1.append(2)
    assert l1.head == 1
    assert l1.tail == 2
    l1.append(3)
    assert l1.tail == 3


def test_linked_list_prepend(l0: LinkedList):
    l0.prepend(0)
    assert l0.head == 0
    assert l0.head.next_node is None
    l0.prepend(-1)
    assert l0.head == -1
    assert l0.head.next_node == 0


def test_get_index_simple(l0: LinkedList):
    assert l0._get_index("a") is None
    l0.append("a")
    assert l0._get_index("a") == 0
    l0.append("b")
    assert l0._get_index("b") == 1


def test_contains_simple(l0: LinkedList):
    assert "a" not in l0
    l0.append("a")
    assert "a" in l0
    l0.append("b")
    assert "b" in l0


@pytest.mark.parametrize("wrong_type", ("abc", b"abc", 1, LinkedList, list))
def test_linked_list_add_from_iterable_wrong_type(l0: LinkedList, wrong_type):
    with pytest.raises(TypeError):
        l0._add_from_iterable(wrong_type)


@pytest.mark.parametrize(
    "_iter",
    (
        range(20),
        (i for i in range(20)),
        tuple((i for i in range(20))),
        bytearray(range(20)),
        [i for i in range(20)],
        {i: i * 2 for i in range(20)},
        {i for i in range(20)},
    ),
)
def test_linked_list_add_from_iterable_correct_type(l0: LinkedList, _iter):
    l0._add_from_iterable(_iter)
    for item in _iter:
        assert item in l0


def test_linked_list_create_no_arguments(l0: LinkedList):
    assert l0.head is None
    assert l0.size == 0


@pytest.mark.parametrize(
    "wrong_type", ("a", 1, type, INode, str, LinkedList, Node(1))
)
def test_linked_list_create_wrong_node_type(wrong_type):
    with pytest.raises(TypeError):
        LinkedList(node_type=wrong_type)


@pytest.mark.parametrize("head", (Node(2), Node(None), Node((1, 2))))
def test_linked_list_create_single_item_node_type(head):
    lt = LinkedList(head)
    assert lt.head == Node(head) == head


@pytest.mark.parametrize("head", (2, "a", b"abc", 0))
def test_linked_list_create_single_item_non_node_type(head):
    lt = LinkedList(head)
    assert lt.head == Node(head) == head


@pytest.mark.parametrize(
    "itr",
    (
        range(20),
        (i for i in range(20)),
        tuple((i for i in range(20))),
        bytearray(range(20)),
        [i for i in range(20)],
        {i: i * 2 for i in range(20)},
        {i for i in range(20)},
    ),
)
def test_linked_list_create_from_iterable(itr):
    lt = LinkedList(itr)
    for item in itr:
        assert item in lt


@pytest.mark.parametrize(
    "value",
    (
        1,
        "abc",
        b"abc",
        (1, 2, 3),
        range(20),
        (i for i in range(200)),
        [i for i in range(2000)],
    ),
)
def test_linked_list_copy_no_arguments(value):
    lt = LinkedList(value)
    lc = lt.copy()
    for i in range(lt.size):
        lt[i] == lc[i]


@pytest.mark.parametrize(
    ("_from", "_until"),
    (("a", None), ("a", "b"), ([1, 2, 3], False), (type, INode), (1, int)),
)
def test_linked_list_copy_wrong_type(l2: LinkedList, _from, _until):
    with pytest.raises(TypeError):
        l2.copy(_from, _until)


@pytest.mark.parametrize(
    ("_from", "_until"), ((0, 5), (5, 10), (0, 20), (18, 19))
)
def test_linked_list_copy_with_arguments_positive_indexes(
    l2: LinkedList, _from, _until
):
    lt = LinkedList(range(_from, _until))
    l2c = l2.copy(_from, _until)
    for i in range(l2c.size):
        l2c[i] == lt[i]


@pytest.mark.parametrize(
    ("_from", "_until"),
    ((-5, None), (-15, 10), (-5, -2), (-20, 200), (-19, -18)),
)
def test_linked_list_copy_with_arguments_negative_indexes(
    l2: LinkedList, _from, _until
):
    lt = l2[_from:_until]
    l2c = l2.copy(_from, _until)
    for i in range(l2c.size):
        l2c[i] == lt[i]


@pytest.mark.parametrize(
    ("_from", "_until"), ((-5, -6), (-15, -20), (-5, -7), (5, 2), (19, 19))
)
def test_linked_list_copy_with_arguments_empty_list_expected(
    l2: LinkedList, _from, _until
):
    l2c = l2.copy(_from, _until)
    assert l2c.is_empty()


@pytest.mark.parametrize(
    "itr",
    (
        [i for i in range(20)],
        [i for i in range(200)],
        [i for i in range(1845)],
    ),
)
def test_linked_list_size(l0: LinkedList, itr):
    assert l0.size == 0
    l0.extend(itr)
    assert l0.size == len(itr)


@pytest.mark.parametrize(
    "wrong_index", ("a", b"a", True, False, None, [1, 2, 3], type)
)
def test_linked_list_insert_wrong_type(l0: LinkedList, wrong_index):
    with pytest.raises(TypeError):
        l0.insert(wrong_index, 1)


@pytest.mark.parametrize("index", (21, -21, 100, -100))
def test_linked_list_insert_index_out_of_range(l1: LinkedList, index):
    with pytest.raises(IndexError):
        l1.insert(index, 1)


@pytest.mark.parametrize("index", (20, -20, 10, -10, 8, -8, 3, -3))
def test_linked_list_insert_correct_index(l2: LinkedList, index):
    l2.insert(index, "a")
    index = index - 1 if index < 0 else index
    assert l2[index] == "a"


def test_linked_list_index_no_start_stop_value_found(l2: LinkedList):
    for value in l2:
        index = l2.index(value)
        assert l2[index] == value


def test_linked_list_index_no_start_stop_value_not_found(l2: LinkedList):
    for value in range(l2.size, l2.size + 20):
        with pytest.raises(ValueError):
            l2.index(value)


@pytest.mark.parametrize(
    ("start", "stop"), ((None, None), ([1], [1]), ("a", "b"), ({}, {}))
)
def test_linked_list_index_start_stop_wrong_type(l2: LinkedList, start, stop):
    with pytest.raises(TypeError):
        l2.index(1, start, stop)


@pytest.mark.parametrize(
    ("start", "stop"),
    ((-21, 22), (-21, 19), (0, 21), (5, 22), (-21, 5), (19, 100)),
)
def test_linked_list_index_start_stop_out_of_range_value_found(
    l2: LinkedList, start, stop
):
    for value in l2[start:stop]:
        index = l2.index(value, start, stop)
        assert l2[index] == value


@pytest.mark.parametrize(
    ("value", "start", "stop"),
    (
        (6, -21, 5),
        (19, -21, 18),
        (4, 5, 21),
        (8, 10, 22),
        (10, -100, 9),
        (18, 19, 100),
    ),
)
def test_linked_list_index_start_stop_out_of_range_value_not_found(
    l2: LinkedList, value, start, stop
):
    with pytest.raises(ValueError):
        l2.index(value, start, stop)


@pytest.mark.parametrize(
    ("start", "stop"),
    ((0, 20), (5, 20), (0, 10), (-5, -1), (-20, 20), (-15, 6)),
)
def test_linked_list_index_start_stop_within_range_value_found(
    l2: LinkedList, start, stop
):
    for value in l2[start:stop]:
        index = l2.index(value, start, stop)
        assert l2[index] == value


@pytest.mark.parametrize(
    ("value", "start", "stop"),
    (
        (11, 0, 10),
        (4, 5, 20),
        (11, 0, 10),
        (14, -5, -1),
        (0, -19, 20),
        (6, -15, 6),
        (19, 19, 19),
    ),
)
def test_linked_list_index_start_stop_within_range_value_not_found(
    l2: LinkedList, value, start, stop
):
    with pytest.raises(ValueError):
        l2.index(value, start, stop)


def test_linked_list_pop_empty_list(l0: LinkedList):
    with pytest.raises(IndexError):
        l0.pop()
    with pytest. raises(IndexError):
        l0._pop_head()


def test_linked_list_pop_no_index_non_empty_list(l2: LinkedList):
    tail = l2.tail
    assert l2.pop() == tail


@pytest.mark.parametrize(
    "wrong_index", ("a", b"abc", bytearray((1, 2, 3)), type, {})
)
def test_linked_list_pop_wrong_index_type(l2: LinkedList, wrong_index):
    with pytest.raises(TypeError):
        l2.pop(wrong_index)


def test_linked_list_pop_head_non_empty_list(l2: LinkedList):
    head = l2.head
    poped_head = l2.pop(0)
    assert poped_head == head
    assert l2.head == head.next_node
    head = l2.head
    poped_head = l2._pop_head()
    assert poped_head == head
    assert l2.head == head.next_node


def test_linked_list_pop_valid_indices(l2: LinkedList):
    for i in range(20):
        lt = l2.copy()
        lt.pop(i)
        assert i not in lt


@pytest.mark.parametrize(
    ("itr", "indices"),
    [
        (
            (randint(0, 9999) for _ in range(10000)),
            (randint(0, 9999) for _ in range(1000)),
        ),
        (
            (randint(0, 9999) for _ in range(10000)),
            (randint(-10000, 9999) for _ in range(1000)),
        ),
    ],
)
def test_linked_list_pop_random_valid_indices(itr, indices):
    lt = LinkedList(itr)
    count = 0
    for i in indices:
        if i != 0:
            i = i - count if i > 0 else i + count
        item = lt[i]
        assert lt.pop(i) == item
        count += 1


def test_linked_list_remove_empty_list(l0: LinkedList):
    with pytest.raises(ValueError):
        l0.remove(1)
    with pytest.raises(ValueError):
        l0.remove(None)


def test_linked_list_remove_value_not_in_list(l2: LinkedList):
    for value in range(l2.size, l2.size + 10):
        with pytest.raises(ValueError):
            l2.remove(value)


def test_linked_list_remove_value_in_list(l2: LinkedList):
    for value in range(0, l2.size):
        l2.remove(value)
        assert value not in l2


@pytest.mark.parametrize(
    ("value", "llst"),
    (
        (3, LinkedList((1 for _ in range(10)))),
        (
            101,
            LinkedList((i for i in range(100)))
        ),
    ),
)
def test_linked_list_remove_all_value_not_in_list(value, llst: LinkedList):
    with pytest.raises(ValueError):
        llst.remove_all(value)


@pytest.mark.parametrize(
    ("value", "llst"),
    (
        (1, LinkedList((1 for _ in range(10)))),
        (
            49,
            LinkedList((i for i in range(100))),
        ),
        ("a", LinkedList((("a" if i % 2 == 0 else 1) for i in range(100)))),
    ),
)
def test_linked_list_remove_all_value_in_list(value, llst: LinkedList):
    llst.remove_all(value)
    assert value not in llst


@pytest.mark.parametrize(
    "other",
    ("a", b"abc", [1, 2, 3], {}, {1: 2, 3: 4}, bytearray((1, 2, 3)))
)
def test_linked_list_eq_other_not_linked_list(l1: LinkedList, other):
    assert l1 != other


@pytest.mark.parametrize(
    "other",
    (LinkedList([1, 1]), LinkedList())
)
def test_linked_list_eq_other_different_size(l1: LinkedList, other):
    assert l1 != other


@pytest.mark.parametrize(
    ("itr1", "itr2"),
    (
        ((i for i in range(10)), (i for i in range(9))),
        ((i for i in range(10)), (i for i in range(1, 10))),
        (lst := [randint(0, 99) for _ in range(100)], reversed(lst))
    )
)
def test_linked_list_eq_other_different_items(itr1: Iterable, itr2: Iterable):
    assert LinkedList(itr1) != LinkedList(itr2)


@pytest.mark.parametrize(
    ("itr1", "itr2"),
    (
        ((i for i in range(10)), (i for i in range(10))),
        ((i for i in range(10)), (i for i in range(10))),
        (lst := [randint(0, 99) for _ in range(100)], lst)
    )
)
def test_linked_list_eq_other_equal(itr1: Iterable, itr2: Iterable):
    assert LinkedList(itr1) == LinkedList(itr2)


def test_linked_list_reverse_empty_list(l0: LinkedList):
    lr = l0.reverse()
    assert lr.is_empty()
    l0.head = Node(0)
    lr = l0.reverse()
    assert not lr.is_empty()
    l0.head = None
    lr = l0.reverse()
    assert lr.is_empty()


@pytest.mark.parametrize(
    "itr",
    (
        [i for i in range(10)],
        [randint(0, 99) for _ in range(100)],
        tuple((randint(0, 1000) for _ in range(1000)))
    )
)
def test_linked_list_reverse_non_empty_list(itr: Iterable):
    llst = LinkedList(itr)
    assert llst.reverse() == LinkedList(tuple(reversed(itr)))  # type: ignore


def test_linked_list_clear(l0: LinkedList, l1: LinkedList, l2: LinkedList):
    l0.clear()
    assert l0.is_empty()
    l1.clear()
    assert l1.is_empty()
    l2.clear()
    assert l2.is_empty()
    

@pytest.mark.parametrize(
    "wrong_index",
    ("a", b"abc", [1, 2, 3], {}, {1: 2, 3: 4}, bytearray((1, 2, 3))),
)
def test_linked_list_getitem_wrong_type(l0: LinkedList, wrong_index):
    with pytest.raises(TypeError):
        l0[wrong_index]


def test_getitem_empty_list(l0: LinkedList):
    with pytest.raises(IndexError):
        l0[8]
    with pytest.raises(IndexError):
        l0[0:]
    with pytest.raises(IndexError):
        l0[:0]


random_gen_k_items = (randint(0, 1000) for _ in range(1000))


@pytest.mark.parametrize(
    ("llst", "indices"),
    (
        [LinkedList((i for i in range(200))), (200, 201, -201)],
        [LinkedList({i for i in range(535)}), (535, 536, -536)],
        [
            LinkedList((chr(i) for i in random_gen_k_items)),
            (1000, 1001, -1001),
        ],
    ),
)
def test_linked_list_getitem_int_index_out_of_range(llst: LinkedList, indices):
    for i in indices:
        with pytest.raises(IndexError):
            llst[i]


@pytest.mark.parametrize(
    ("llst", "indices"),
    (
        [
            LinkedList((i for i in range(200))),
            [randint(-200, 199) for _ in range(10)],
        ],
        [
            LinkedList((i for i in range(535))),
            [randint(-535, 534) for _ in range(10)],
        ],
        [
            LinkedList([chr(i) for i in range(1000)]),
            [randint(-1000, 999) for _ in range(10)],
        ],
    ),
)
def test_linked_list_getitem_int_index_inside_range(llst: LinkedList, indices):
    for i in indices:
        item = llst[i]
        found_item = None
        count = 0
        for node in llst:
            if node == item:
                found_item = node
                break
            count += 1
        assert found_item is not None
        assert count == (i if i >= 0 else i + llst.size)


def test_linked_list_getitem_slice_invalid_step(l1: LinkedList):
    with pytest.raises(ValueError):
        l1[::0]
    with pytest.raises(ValueError):
        l1[::-1]


def test_linked_list_getitem_slice_start_equal_or_greater_than_stop(
    l2: LinkedList,
):
    for i in range(0, 20, 2):
        assert l2[i:i].is_empty()
        assert l2[i + 1: i].is_empty()


@pytest.mark.parametrize(
    ("llst", "indices"),
    (
        [
            LinkedList((i for i in range(200))),
            [(-201, None), (None, 500), (-500, 500)],
        ],
        [LinkedList((i for i in range(535))), [(-536, 535), (-1000, 1000)]],
        [
            LinkedList([chr(i) for i in range(1000)]),
            [(-2000, 1001), (-1001, 10000)],
        ],
    ),
)
def test_linked_list_getitem_slice_indices_out_of_range(
    llst: LinkedList, indices
):
    for start, stop in indices:
        full_list = llst[start:stop]
        assert llst == full_list


@pytest.mark.parametrize(
    ("llst", "indices"),
    (
        [
            LinkedList((i for i in range(200))),
            [
                (i1 := randint(0, 199), randint(0, i1 - 1)),
                (i2 := randint(51, 199), randint(50, i2 - 1)),
            ],
        ],
        [
            LinkedList((i for i in range(1000))),
            [
                (i1 := randint(0, 999), randint(0, i1 - 1)),
                (i2 := randint(501, 700), randint(50, i2 - 1)),
            ],
        ],
    ),
)
def test_linked_list_getitem_slice_indices_inside_range_step_equals_one(
    llst: LinkedList, indices
):
    for stop, start in indices:
        assert llst[start:stop] == llst.copy(start, stop)


@pytest.mark.parametrize(
    ("llst", "indices"),
    (
        [
            LinkedList((i for i in range(200))),
            [
                (i1 := randint(0, 199), randint(0, i1 - 1)),
                (i2 := randint(51, 199), randint(50, i2 - 1)),
            ],
        ],
        [
            LinkedList((i for i in range(1000))),
            [
                (i1 := randint(0, 999), randint(0, i1 - 1)),
                (i2 := randint(501, 700), randint(50, i2 - 1)),
            ],
        ],
    ),
)
def test_linked_list_getitem_slice_indices_inside_range_step_greater_than_one(
    llst: LinkedList, indices
):
    for stop, start in indices:
        for step in range(2, 5):
            sliced_list = llst[start:stop:step]
            count = start
            for node in sliced_list:
                assert node == llst[count]
                count += step

