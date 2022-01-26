import pytest
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
