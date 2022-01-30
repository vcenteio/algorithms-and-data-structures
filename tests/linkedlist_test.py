import pytest
from typing import Generator, Iterable, Tuple, Sized
from random import randint, choice
from secrets import token_bytes, token_urlsafe

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


@pytest.mark.parametrize("value", (1, "a", b"abc", [1, 2, 3]))
def test_linked_list_count_empty_list(l0: LinkedList, value):
    assert l0.count(value) == 0


@pytest.mark.parametrize(
    ("values", "llst"),
    [
        (
            vs1 := {-1, -5, 21, 25, 99},
            LinkedList([i for i in range(100) if i not in vs1]),
        ),
        (
            vs2 := {randint(0, 1000) for _ in range(10)},
            LinkedList([i for i in range(1000) if i not in vs2]),
        ),
        (
            vs3 := {chr(randint(0, 100)) for _ in range(10)},
            LinkedList([chr(i) for i in range(100) if chr(i) not in vs3]),
        ),
    ],
)
def test_linked_list_count_non_existent_value(llst: LinkedList, values):
    for value in values:
        assert llst.count(value) == 0


@pytest.mark.parametrize(
    ("values", "llst"),
    [
        ({-1, -5, 21, 25, 99}, LinkedList([i for i in range(-100, 100)])),
        (
            {randint(0, 999) for _ in range(10)},
            LinkedList([i for i in range(1000)]),
        ),
        (
            {chr(randint(0, 99)) for _ in range(10)},
            LinkedList([chr(i) for i in range(100)]),
        ),
    ],
)
def test_linked_list_count_existent_value_one_occurrence(
    llst: LinkedList, values
):
    for value in values:
        assert llst.count(value) == 1


@pytest.mark.parametrize(
    ("values", "llst"),
    [
        ({-1, -5, 5, 3}, LinkedList([randint(-5, 5) for _ in range(200)])),
        (
            {randint(-10, 10) for _ in range(10)},
            LinkedList([randint(-10, 10) for _ in range(1000)]),
        ),
        (
            {chr(randint(0, 20)) for _ in range(10)},
            LinkedList([chr(randint(0, 20)) for _ in range(1000)]),
        ),
    ],
)
def test_linked_list_count_existent_value_many_occurrences(
    llst: LinkedList, values
):
    for value in values:
        assert llst.count(value) > 1


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


def test_linked_list_copy_empty_list(l0: LinkedList):
    assert l0.copy().is_empty()
    assert l0.size == 0


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
    with pytest.raises(IndexError):
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
        (101, LinkedList((i for i in range(100)))),
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
    "other", ("a", b"abc", [1, 2, 3], {}, {1: 2, 3: 4}, bytearray((1, 2, 3)))
)
def test_linked_list_eq_other_not_linked_list(l1: LinkedList, other):
    assert l1 != other


@pytest.mark.parametrize("other", (LinkedList([1, 1]), LinkedList()))
def test_linked_list_eq_other_different_size(l1: LinkedList, other):
    assert l1 != other


@pytest.mark.parametrize(
    ("itr1", "itr2"),
    (
        ((i for i in range(10)), (i for i in range(9))),
        ((i for i in range(10)), (i for i in range(1, 10))),
        (lst := [randint(0, 99) for _ in range(100)], reversed(lst)),
    ),
)
def test_linked_list_eq_other_different_items(itr1: Iterable, itr2: Iterable):
    assert LinkedList(itr1) != LinkedList(itr2)


@pytest.mark.parametrize(
    ("itr1", "itr2"),
    (
        ((i for i in range(10)), (i for i in range(10))),
        ((i for i in range(10)), (i for i in range(10))),
        (lst := [randint(0, 99) for _ in range(100)], lst),
    ),
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
        tuple((randint(0, 1000) for _ in range(1000))),
    ),
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
        assert l2[i + 1 : i].is_empty()  # noqa: E203


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


def test_linked_list_split_no_index_empty_list(l0: LinkedList):
    assert isinstance(l0.split(), Tuple)  # type: ignore[arg-type]
    h1, h2 = l0.split()
    assert h1 == h2 == l0


def test_linked_list_split_no_index_one_item(l1: LinkedList):
    assert isinstance(l1.split(), Tuple)  # type: ignore[arg-type]
    h1, h2 = l1.split()
    assert h1 == l1 != h2
    assert h2.is_empty()


@pytest.mark.parametrize(
    "llst",
    (
        LinkedList((i for i in range(200))),
        LinkedList({i: i for i in range(535)}),
        LinkedList(
            tuple((chr(i) for i in (randint(0, 1000) for _ in range(1000))))
        ),
        LinkedList(
            tuple((chr(i) for i in (randint(0, 1000) for _ in range(1001))))
        ),
    ),
)
def test_linked_list_split_no_index_more_than_one_item(llst: LinkedList):
    assert isinstance(llst.split(), Tuple)  # type: ignore[arg-type]
    h1, h2 = llst.split()
    assert h1 != llst != h2
    if llst.size % 2 == 0:
        assert h1.size == h2.size == llst.size // 2
    else:
        assert h1.size == h2.size - 1
        assert h1.size + h2.size == llst.size


@pytest.mark.parametrize(
    "wrong_index",
    ("a", b"abc", [1, 2, 3], {}, bytearray([1, 2, 3]), True, False),
)
def test_linked_list_split_wrong_index_type(l2: LinkedList, wrong_index):
    with pytest.raises(TypeError):
        l2.split(wrong_index)


def test_linked_list_split_with_index_empty_list(l0: LinkedList):
    assert isinstance(l0.split(10), Tuple)  # type: ignore[arg-type]
    h1, h2 = l0.split(10)
    assert h1 == h2 == l0
    assert h1.is_empty() and h2.is_empty()


def test_linked_list_split_with_index_zero(l2: LinkedList):
    h1, h2 = l2.split(0)
    assert h1.is_empty()
    assert h2 == l2


@pytest.mark.parametrize(
    "llst",
    (
        LinkedList((i for i in range(200))),
        LinkedList({i: i for i in range(535)}),
        LinkedList(
            tuple((chr(i) for i in (randint(0, 1000) for _ in range(1000))))
        ),
        LinkedList(
            tuple((chr(i) for i in (randint(0, 1000) for _ in range(1001))))
        ),
    ),
)
def test_linked_list_split_with_max_index(llst: LinkedList):
    index = llst.size - 1
    h1, h2 = llst.split(index)
    assert h1 == llst[:index]
    assert h2.head == llst.tail


@pytest.mark.parametrize(
    "llst",
    (
        LinkedList((i for i in range(200))),
        LinkedList({i: i for i in range(535)}),
        LinkedList(
            tuple((chr(i) for i in (randint(0, 1000) for _ in range(1000))))
        ),
        LinkedList(
            tuple((chr(i) for i in (randint(0, 1000) for _ in range(1001))))
        ),
    ),
)
def test_linked_list_split_with_index_same_or_bigger_than_size(
    llst: LinkedList,
):
    index = randint(llst.size, llst.size + 100)
    with pytest.raises(IndexError):
        llst.split(index)


@pytest.mark.parametrize(
    "llst",
    (
        LinkedList((i for i in range(50))),
        LinkedList({i: i for i in range(335)}),
        LinkedList(
            tuple((chr(i) for i in (randint(0, 1000) for _ in range(500))))
        ),
        LinkedList(
            tuple((chr(i) for i in (randint(0, 1000) for _ in range(501))))
        ),
    ),
)
def test_linked_list_split_with_any_valid_index(llst: LinkedList):
    for i in (randint(0, llst.size - 1) for _ in range(int(llst.size * 0.1))):
        h1, h2 = llst.split(i)
        assert h1 == llst[:i]
        assert h2 == llst[i:]


def test_linked_list_sort_no_key_emtpy_list(l0: LinkedList):
    l_copy = l0.copy()
    l0.sort()
    assert l0 == l_copy


def test_linked_list_sort_no_key_one_item(l1: LinkedList):
    l_copy = l1.copy()
    l1.sort()
    assert l1 == l_copy


@pytest.mark.parametrize(
    "llst",
    (
        LinkedList((choice((int, str))(i) for i in range(20))),
        LinkedList((choice((int, bytes))(i) for i in range(20))),
        LinkedList((choice((str, bytes))(i) for i in range(20))),
    ),
)
def test_linked_list_sort_no_key_mixed_types(llst: LinkedList):
    with pytest.raises(TypeError):
        llst.sort()


@pytest.mark.parametrize(
    "itr",
    [
        [randint(-100, 100) for _ in range(50)],
        {randint(0, 1000): i for i in range(335)},
        tuple((randint(0, 1000) for _ in range(1000))),
    ],
)
def test_linked_list_sort_no_key_ints(itr: Iterable):
    lst = list(itr)
    lst.sort()
    llst = LinkedList(itr)
    llst.sort()

    for i in range(len(itr)):  # type: ignore[arg-type]
        assert llst[i] == lst[i]


@pytest.mark.parametrize(
    "itr",
    [
        [chr(randint(0, 100)) for _ in range(50)],
        {chr(randint(0, 1000)): i for i in range(335)},
        tuple((chr(randint(0, 1000)) for _ in range(1000))),
    ],
)
def test_linked_list_sort_no_key_strs(itr: Iterable):
    lst = list(itr)
    lst.sort()
    llst = LinkedList(itr)
    llst.sort()

    for i in range(len(itr)):  # type: ignore[arg-type]
        assert llst[i] == lst[i]


@pytest.mark.parametrize(
    "itr",
    [
        [bytes(randint(0, 100)) for _ in range(50)],
        {bytes(randint(0, 1000)): i for i in range(335)},
        tuple((bytes(randint(0, 1000)) for _ in range(1000))),
    ],
)
def test_linked_list_sort_no_key_bytes(itr: Iterable):
    lst = list(itr)
    lst.sort()
    llst = LinkedList(itr)
    llst.sort()

    for i in range(len(itr)):  # type: ignore[arg-type]
        assert llst[i] == lst[i]


@pytest.mark.parametrize(
    "index", ("a", b"abc", True, False, [1, 2, 3], {}, type, int, slice)
)
def test_linked_list_setitem_wrong_index_type(l0: LinkedList, index):
    with pytest.raises(TypeError):
        l0[index] = 1


def test_linked_list_setitem_int_index_empty_list(l0: LinkedList):
    with pytest.raises(IndexError):
        l0[0] = 1


@pytest.mark.parametrize("index", (-21, 20, 30))
def test_linked_list_setitem_int_index_out_of_range(l2: LinkedList, index):
    with pytest.raises(IndexError):
        l2[index] = 1


@pytest.mark.parametrize(
    ("index", "value"), [(0, 2), (5, 4), (19, 10), (17, "a"), (13, b"abc")]
)
def test_linked_list_setitem_int_index_inside_range(
    l2: LinkedList, index, value
):
    l2[index] = value
    assert l2[index] == value


@pytest.mark.parametrize("value", (1, type, LinkedList, Tuple))
def test_linked_list_setitem_slice_index_non_iterable_value(
    l2: LinkedList, value
):
    with pytest.raises(TypeError):
        l2[:] = value


def test_linked_list_setitem_slice_index_negative_step(l2: LinkedList):
    with pytest.raises(NotImplementedError):
        l2[::-1] = [1]


@pytest.mark.parametrize(
    ("start", "stop", "value"),
    [(-21, 5, [10]), (15, 22, [5]), (19, 100, [3, 4, 5])],
)
def test_linked_list_setitem_slice_index_single_step_indices_out_of_range(
    l2: LinkedList, start, stop, value
):
    lst = list(l2)
    l2[start:stop] = value
    lst[start:stop] = value
    assert l2 == LinkedList(lst)


@pytest.mark.parametrize(
    ("start", "stop", "value"),
    [(6, 5, [10]), (15, 14, [5]), (19, 19, [3, 4, 5]), (11, 11, [5, 4, 3])],
)
def test_linked_list_setitem_slice_index_single_step_start_ge_stop(
    l2: LinkedList, start, stop, value
):
    lst = list(l2)
    l2[start:stop] = value
    lst[start:stop] = value
    assert l2 == LinkedList(lst)


@pytest.mark.parametrize(
    ("start", "stop", "value"),
    [(3, 5, [10]), (10, 14, [5]), (18, 19, [3, 4, 5]), (0, 19, [5, 4, 3])],
)
def test_linked_list_setitem_slice_index_single_step_start_lt_stop(
    l2: LinkedList, start, stop, value
):
    lst = list(l2)
    l2[start:stop] = value
    lst[start:stop] = value
    assert l2 == LinkedList(lst)


@pytest.mark.parametrize(
    ("start", "stop", "step", "value"),
    [
        (3, 5, 2, [10, 11]),
        (10, 14, 3, [5]),
        (5, 19, 4, [4, 5]),
        (0, 19, 20, [5, 4, 3]),
    ],
)
def test_linked_list_setitem_slice_index_multistep_wrong_iter(
    l2: LinkedList, start, stop, step, value
):
    with pytest.raises(ValueError):
        l2[start:stop:step] = value


@pytest.mark.parametrize(
    ("start", "stop", "step", "value"),
    [(5, 5, 2, [10]), (15, 14, 3, [5]), (10, 8, 4, [4]), (19, 16, 20, [-19])],
)
def test_linked_list_setitem_slice_index_multistep_start_ge_stop(
    l2: LinkedList, start, stop, step, value
):
    with pytest.raises(ValueError):
        l2[start:stop:step] = value


@pytest.mark.parametrize(
    ("start", "stop", "step", "value"),
    [
        (3, 8, 2, [10, 11, 12]),
        (10, 18, 3, [5, 6, 7]),
        (0, 19, 4, [1, 2, 3, 4, 5]),
        (0, 19, 20, [1]),
    ],
)
def test_linked_list_setitem_slice_index_multistep_start_lt_stop(
    l2: LinkedList, start, stop, step, value
):
    lst = list(l2)
    l2[start:stop:step] = value
    lst[start:stop:step] = value
    assert l2 == LinkedList(lst)


@pytest.mark.parametrize(
    "wrong_index", ("a", b"abc", True, False, [1, 2, 3], {}, type, int, slice)
)
def test_linked_list_delitem_wrong_index_type(l1: LinkedList, wrong_index):
    with pytest.raises(TypeError):
        del l1[wrong_index]


def test_linked_list_delitem_empty_list(l0: LinkedList):
    with pytest.raises(IndexError):
        del l0[0]


@pytest.mark.parametrize("index", (-21, 20, 30, -100))
def test_linked_list_delitem_int_index_out_of_range(l2: LinkedList, index):
    with pytest.raises(IndexError):
        del l2[index]


@pytest.mark.parametrize(
    ("itr", "indices"),
    [
        ([i for i in range(10)], (randint(-10, 9) for _ in range(5))),
        ([chr(i) for i in range(20)], (randint(-20, 19) for _ in range(5))),
        ([bytes(i) for i in range(50)], (randint(-50, 49) for _ in range(5))),
    ],
)
def test_linked_list_delitem_int_valid_index(itr: Iterable, indices):
    llst = LinkedList(itr)
    count = 0
    for i in indices:
        i = i - count if i >= 0 else i + count
        deleted_item = llst[i]
        del llst[i]
        count += 1
        assert deleted_item not in llst


@pytest.mark.parametrize(("start", "stop"), [(-22, 5), (10, 100), (19, 21)])
def test_linked_list_delitem_slice_single_step_out_of_range(
    l2: LinkedList, start, stop
):
    lst = list(map(lambda x: x.data, l2))
    deleted_items = map(lambda x: x.data, l2[start:stop])
    del l2[start:stop]
    del lst[start:stop]
    assert l2 == LinkedList(lst)
    for item in deleted_items:
        assert item not in l2


@pytest.mark.parametrize(
    ("itr", "_slice"),
    [
        ([i for i in range(10)], slice(8, 7)),
        ([chr(i) for i in range(20)], slice(10, 4)),
        ([bytes(i) for i in range(50)], slice(49, 30)),
    ],
)
def test_linked_list_delitem_slice_single_step_start_ge_stop(
    itr: Iterable, _slice
):
    lst = list(itr)
    llst = LinkedList(itr)
    deleted_items = tuple(map(lambda x: x.data, llst[_slice]))
    assert len(deleted_items) == 0
    lst_previous_size = len(lst)
    llst_previous_size = len(llst)
    del lst[_slice]
    del llst[_slice]
    assert llst == LinkedList(lst)
    assert len(llst) == llst_previous_size == len(lst) == lst_previous_size


@pytest.mark.parametrize(
    ("itr", "_slice"),
    [
        ([i for i in range(10)], slice(4, 7)),
        ([chr(i) for i in range(20)], slice(1, 16)),
        ([bytes(i) for i in range(50)], slice(15, 38)),
    ],
)
def test_linked_list_delitem_slice_single_step_start_lt_stop(
    itr: Iterable, _slice: slice
):
    lst = list(itr)
    llst = LinkedList(itr)
    deleted_items = tuple(map(lambda x: x.data, llst[_slice]))
    del lst[_slice]
    del llst[_slice]
    assert llst == LinkedList(lst)
    for item in deleted_items:
        assert item not in llst


@pytest.mark.parametrize(
    ("itr", "_slice"),
    [
        ([i for i in range(10)], slice(-11, 7, 2)),
        ([chr(i) for i in range(20)], slice(1, 21, 3)),
        ([bytes(i) for i in range(50)], slice(15, 38, 5)),
    ],
)
def test_linked_list_delitem_slice_multistep_out_of_range(
    itr: Iterable, _slice: slice
):
    slice_size = len(
        range(*(_slice.indices(len(itr))))  # type: ignore[arg-type]
    )
    lst = list(itr)
    llst = LinkedList(itr)
    deleted_items = tuple(map(lambda x: x.data, llst[_slice]))
    assert slice_size == len(deleted_items)
    lst_previous_size = len(lst)
    llst_previous_size = len(llst)
    del lst[_slice]
    del llst[_slice]
    assert llst == LinkedList(lst)
    for item in deleted_items:
        assert item not in llst
    assert (
        len(llst)
        == len(lst)
        == lst_previous_size - slice_size
        == llst_previous_size - slice_size
    )


@pytest.mark.parametrize(
    "_slice", (slice(0, 2, -2), slice(4, 7, -1), slice(15, 19, -10))
)
def test_linked_list_delitem_slice_multistep_negative_step(
    l2: LinkedList, _slice: slice
):
    with pytest.raises(NotImplementedError):
        del l2[_slice]


@pytest.mark.parametrize(
    ("itr", "_slice"),
    [
        ([i for i in range(10)], slice(8, 2, 2)),
        ([chr(i) for i in range(20)], slice(10, 4, 4)),
        ([bytes(i) for i in range(50)], slice(49, 30, 5)),
    ],
)
def test_linked_list_delitem_slice_multistep_start_ge_stop(
    itr: Iterable, _slice
):
    lst = list(itr)
    llst = LinkedList(itr)
    deleted_items = tuple(map(lambda x: x.data, llst[_slice]))
    assert len(deleted_items) == 0
    lst_previous_size = len(lst)
    llst_previous_size = len(llst)
    del lst[_slice]
    del llst[_slice]
    assert llst == LinkedList(lst)
    assert len(llst) == llst_previous_size == len(lst) == lst_previous_size


@pytest.mark.parametrize(
    ("itr", "_slice"),
    [
        ([i for i in range(10)], slice(1, 7, 2)),
        ([chr(i) for i in range(20)], slice(3, 16, 3)),
        ([bytes(i) for i in range(50)], slice(15, 38, 6)),
    ],
)
def test_linked_list_delitem_slice_multistep_start_lt_stop(
    itr: Iterable, _slice: slice
):
    slice_size = len(
        range(*(_slice.indices(len(itr))))  # type: ignore[arg-type]
    )
    lst = list(itr)
    llst = LinkedList(itr)
    deleted_items = tuple(map(lambda x: x.data, llst[_slice]))
    assert slice_size == len(deleted_items)
    lst_previous_size = len(lst)
    llst_previous_size = len(llst)
    del lst[_slice]
    del llst[_slice]
    assert llst == LinkedList(lst)
    for item in deleted_items:
        assert item not in llst
    assert (
        len(llst)
        == len(lst)
        == lst_previous_size - slice_size
        == llst_previous_size - slice_size
    )


def test_linked_list_iter_empty_list(l0: LinkedList):
    _iter = l0.__iter__()
    assert isinstance(_iter, Generator)
    assert len(tuple(_iter)) == l0.size
    for node in l0:
        assert node in l0


def test_linked_list_iter_non_empty_list(l2: LinkedList):
    _iter = l2.__iter__()
    assert isinstance(_iter, Generator)
    assert len(tuple(_iter)) == l2.size
    for node in l2:
        assert node in l2


def test_linked_list_next(l0: LinkedList, l2: LinkedList):
    with pytest.raises(StopIteration):
        next(l0)
    for i in range(l2.size):
        node = next(l2)
        assert node == l2[i]
    with pytest.raises(StopIteration):
        next(l2)
    for i in range(l2.size):
        node = next(l2)
        assert node == l2[i]
    with pytest.raises(StopIteration):
        next(l2)


@pytest.mark.parametrize(
    "value", (1, type, list, range, 1.5, None, True, False)
)
def test_linked_list_extend_wrong_type(l0: LinkedList, value):
    with pytest.raises(TypeError):
        l0.extend(value)


@pytest.mark.parametrize(
    "itr",
    [
        token_bytes(50),
        token_urlsafe(50),
        (i for i in range(10)),
        [chr(i) for i in range(50)],
        {randint(0, 1000) for _ in range(500)},
    ],
)
def test_linked_list_extend_from_linked_list(l2: LinkedList, itr: Iterable):
    new_llst = LinkedList(itr)
    l2_initial = l2.copy()
    l2.extend(new_llst)
    assert l2.size == l2_initial.size + new_llst.size
    for node in l2:
        assert node in l2_initial or node in new_llst
    for node in l2_initial:
        assert node in l2
    for node in new_llst:
        assert node in l2


@pytest.mark.parametrize(
    "itr",
    [
        token_bytes(50),
        token_urlsafe(50),
        tuple((i for i in range(10))),
        [chr(i) for i in range(50)],
        {randint(0, 1000) for _ in range(500)},
    ],
)
def test_linked_list_extend_from_other_iterables(
    l2: LinkedList, itr: Iterable
):
    l2_initial = l2.copy()
    l2_initial_size = l2_initial.size
    assert isinstance(itr, Sized)
    itr_size = len(itr)

    l2.extend(itr)
    assert l2.size == l2_initial.size + itr_size

    count = 0
    for node in l2:
        if count < l2_initial_size:
            assert node in l2_initial
        else:
            assert (
                node.data if isinstance(itr, (str, bytes)) else node
            ) in itr
        count += 1
    for node in l2_initial:
        assert node in l2
    for item in itr:
        assert item in l2


@pytest.mark.parametrize(
    "value", ([1, 2, 3], (1, 2), {}, 1, range, 1.5, None, True, False)
)
def test_linked_list_add_radd_iadd_wrong_type(l0: LinkedList, value):
    with pytest.raises(TypeError):
        l0 + value
    with pytest.raises(TypeError):
        value + l0
    with pytest.raises(TypeError):
        l0 += value


@pytest.mark.parametrize(
    "itr",
    [
        tuple(token_bytes(50)),
        tuple(token_urlsafe(50)),
        tuple((i for i in range(10))),
        [chr(i) for i in range(50)],
        {randint(0, 1000) for _ in range(500)},
    ],
)
def test_linked_list_add_other_linked_list(l2: LinkedList, itr):
    llst = LinkedList(itr)
    l2_size = l2.size
    new_list = l2 + llst
    count = 0
    for node in new_list:
        if count < l2_size:
            assert node in l2
        else:
            assert node in llst
        count += 1


@pytest.mark.parametrize(
    "itr",
    [
        tuple(token_bytes(50)),
        tuple(token_urlsafe(50)),
        tuple((i for i in range(10))),
        [chr(i) for i in range(50)],
        {randint(0, 1000) for _ in range(500)},
    ],
)
def test_linked_list_radd_other_linked_list(l2: LinkedList, itr):
    llst = LinkedList(itr)
    llst_size = llst.size
    new_list = l2.__radd__(llst)
    count = 0
    for node in new_list:
        if count < llst_size:
            assert node in llst
        else:
            assert node in l2
        count += 1


@pytest.mark.parametrize(
    "itr",
    [
        tuple(token_bytes(50)),
        tuple(token_urlsafe(50)),
        tuple((i for i in range(10))),
        [chr(i) for i in range(50)],
        {randint(0, 1000) for _ in range(500)},
    ],
)
def test_linked_list_iadd_other_linked_list(l2: LinkedList, itr):
    llst = LinkedList(itr)
    llst_size = llst.size
    l2_copy = l2.copy()
    l2_initial_size = l2.size
    l2 += llst
    assert l2.size == l2_initial_size + llst_size
    count = 0
    for node in l2:
        if count < l2_initial_size:
            assert node in l2_copy
        else:
            assert node in llst
        count += 1
