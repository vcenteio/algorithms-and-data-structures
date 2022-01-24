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