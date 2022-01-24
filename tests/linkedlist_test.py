import pytest
from src.algoandds.linkedlist import LinkedList, Node, INode


@pytest.fixture
def l0():
    return LinkedList()


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

