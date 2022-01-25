import pytest
from src.algoandds.linkedlist import LinkedList, Node, INode


@pytest.fixture
def l0():
    return LinkedList()

@pytest.fixture
def l1():
    return LinkedList(1)


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
    assert l0.tail == None
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


@pytest.mark.parametrize(
    "wrong_type",
    ("abc", b"abc", 1, LinkedList, list)
)
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
        {i for i in range(20)}
    )
)
def test_linked_list_add_from_iterable_correct_type(l0: LinkedList, _iter):
    l0._add_from_iterable(_iter)
    for item in _iter:
        assert item in l0


def test_linked_list_create_no_arguments(l0: LinkedList):
    assert l0.head == None
    assert l0.size == 0


@pytest.mark.parametrize(
    "wrong_type",
    ("a", 1, type, INode, str, LinkedList, Node(1))
)
def test_linked_list_create_wrong_node_type(wrong_type):
    with pytest.raises(TypeError):
        LinkedList(node_type=wrong_type)


@pytest.mark.parametrize(
    "head",
    (Node(2), Node(None), Node((1, 2)))
)
def test_linked_list_create_single_item_node_type(head):
    lt = LinkedList(head)
    assert lt.head == Node(head) == head


@pytest.mark.parametrize(
    "head",
    (2, "a", b"abc", 0)
)
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
        {i for i in range(20)}
    )
)
def test_linked_list_create_from_iterable(itr):
    lt = LinkedList(itr)
    for item in itr:
        assert item in lt
