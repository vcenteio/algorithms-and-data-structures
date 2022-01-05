import sys
sys.path.append("..")

from tree import TreeNode, Tree
import pytest

@pytest.fixture
def n0():
    return TreeNode("Animal")

@pytest.fixture
def n1():
    node = TreeNode("Animal")
    genera = ["Canines", "Bovines", "Felines", "Birds"]
    for genus in genera:
        node.add_child(TreeNode(genus))
    return node

@pytest.fixture
def n2():
    parent = TreeNode("Living Organisms")
    genera = ["Canines", "Bovines", "Felines", "Birds"]
    children = tuple((TreeNode(genus) for genus in genera))
    return TreeNode("Animal", parent, children)

@pytest.fixture
def n3():
    parent = TreeNode("Living Organisms")
    genera = ["Canines", "Bovines", "Felines", "Birds"]
    canines = list(map(TreeNode, ["Dog", "Wolf"]))
    bovines = list(map(TreeNode, ["Cattle", "Bison"]))
    felines = list(map(TreeNode, ["Cat", "Tiger"]))
    birds = list(map(TreeNode, ["Hawk", "Dove"]))
    subchildren = [canines, bovines, felines, birds]
    children = list()
    for i in range(len(genera)):
        children.append(TreeNode(genera[i], _children=subchildren[i]))
    return TreeNode("Animal", parent, children)

@pytest.fixture
def t1(n1):
    return Tree(n1)

# Node tests
def test_node_instantiation_with_no_data():
    with pytest.raises(TypeError):
        TreeNode()

def test_node_instantiation_with_no_parent_and_no_children(n0: TreeNode):
    assert n0._parent == None
    assert n0._children == []
    assert n0.level == 0

def test_node_instantiation_with_parent_and_no_children():
    parent = TreeNode("a")
    new_node = TreeNode("aa", parent)

    assert new_node._parent not in new_node.all_nodes
    assert new_node.level == new_node._parent.level+1
    assert new_node._parent.level == parent.level
    assert new_node in new_node._parent.descendants

def test_node_instantiation_with_parent_and_children(n2: TreeNode):
    parent = TreeNode("Living Organisms")
    genera = ["Canines", "Bovines", "Felines", "Birds"]
    children = tuple((TreeNode(genus) for genus in genera))
    new_node = n2

    assert new_node._parent not in new_node.all_nodes
    assert new_node.level == new_node._parent.level+1
    assert new_node._parent.level == parent.level
    assert new_node in new_node._parent.descendants

    expected_children = list(children)
    assert new_node._children == expected_children

    expected_children_level = new_node.level+1
    for child in new_node._children: 
        assert child.level == expected_children_level
    
    expected_descendants = set()
    for child in children:
        for node in child.all_nodes:
            expected_descendants.add(node)
    assert set(tuple(new_node.descendants)) == expected_descendants

def test_node_instantiation_with_parent_and_children_with_subchildren(n3: TreeNode):
    parent = TreeNode("Living Organisms")
    genera = ["Canines", "Bovines", "Felines", "Birds"]
    canines = tuple(map(TreeNode, ["Dog", "Wolf"]))
    bovines = tuple(map(TreeNode, ["Cattle", "Bison"]))
    felines = tuple(map(TreeNode, ["Cat", "Tiger"]))
    birds = tuple(map(TreeNode, ["Hawk", "Dove"]))
    subchildren = [canines, bovines, felines, birds]
    children = tuple((TreeNode(genus) for genus in genera))
    new_node = n3

    i = 0
    for child in new_node.children:
        assert child.children == subchildren[i]
        i += 1

    expected_children = {child for child in children}
    expected_subchildren = {subchild for subgenus in subchildren for subchild in subgenus}
    expected_descendants = expected_children | expected_subchildren
    assert set(tuple(n3.descendants)) == expected_descendants

    assert n3.level == 1
    assert n3._parent.level == 0
    for child in n3.children:
        assert child.level == 2
        for subchild in child.children:
            assert subchild.level == 3
    for descendant in n3.descendants:
        assert descendant.level == descendant._parent.level+1
    
    assert n3._parent == parent
    for child in n3.children:
        assert child._parent == n3
        for subchild in child.children:
            assert subchild._parent == child
    
def test_node_add_child_correct_type(n0: TreeNode):
    n0.add_child(child_a := TreeNode("aa"))
    n0.add_child(child_b := TreeNode("ab"))
    assert n0._children == [child_a, child_b]
    assert child_a._parent == child_b._parent == n0
    assert child_a.level == child_b.level == 1

def test_node_add_child_wrong_type(n0: TreeNode):
    with pytest.raises(TypeError):
        n0.add_child("str")

def test_node_pop_child_correct_value(n1: TreeNode):
    genera = ["Canines", "Bovines", "Felines", "Birds"]
    removed_child = n1.pop_child("Canines")
    assert removed_child.data == "Canines"
    assert n1._children == genera[1:]
    assert removed_child._parent == None
    removed_child = n1.pop_child("Felines")
    assert removed_child.data == "Felines"
    assert n1._children == genera[1::2]
    assert removed_child._parent == None

def test_node_pop_child_wrong_value(n1: TreeNode):
    with pytest.raises(ValueError):
        n1.pop_child("Dinosaurs")

def test_node_set_parent_correct_type(n1: TreeNode):
    n1.set_parent(parent := TreeNode("Living Organism"))
    assert n1 in parent
    assert n1._parent == parent
    assert n1.level == parent.level+1 == n1._parent.level+1
    for child in n1.children:
        assert child.level == n1.level+1 == n1.parent.level+2 

    n1.set_parent(None)
    assert n1._parent == None
    assert n1.level == 0
    for child in n1.children:
        assert child.level == 1

def test_node_set_parent_wrong_type(n1: TreeNode):
    with pytest.raises(TypeError):
        n1.set_parent("str")
    with pytest.raises(TypeError):
        n1.set_parent(1)
    with pytest.raises(TypeError):
        n1.set_parent(b"bytes123")
    with pytest.raises(TypeError):
        n1.set_parent([1,2,3])

def test_node_set_level(n3: TreeNode):
    assert n3.level == 1 == n3.parent.level+1
    n3._parent = None
    n3.set_level()
    assert n3.level == 0
    for descendant in n3.descendants:
        assert descendant.level == descendant.parent.level+1
    
def test_node_set_children_with_empty_list(n0: TreeNode, n1: TreeNode):
    n0.set_children([])
    assert n0._children == []
    
    n1_children_copy = n1.children[:]
    n1.set_children([])
    for child in n1_children_copy:
        assert child.level == 0
        assert child.parent == None
    assert n1.children == () and n1._children == []

def test_node_set_children_with_non_empty_list(n0: TreeNode, n1: TreeNode):
    genera = ["Fishes", "Reptiles", "Horses"]
    children = list(map(TreeNode, genera))
    n0.set_children(children)
    for child in n0.children:
        assert child in children
    for child in children:
        assert child in n0
    assert len(n0.children) == len(children)

    n1_children_copy = n1.children[:]
    n1.set_children(children)
    for child in n1_children_copy:
        assert child.level == 0
        assert child.parent == None
        assert child not in n1
    for child in n1.children:
        assert child in children
    for child in children:
        assert child in n1
    assert len(n1.children) == len(children)

def test_node_is_leaf_node(n0: TreeNode, n1: TreeNode, n3: TreeNode):
    assert n0.is_leaf_node()
    assert not n1.is_leaf_node()
    for child in n1.children:
        assert child.is_leaf_node()
    for child in n3.children:
        assert not child.is_leaf_node()

def test_node_is_internal_node(n0: TreeNode, n1: TreeNode, n3: TreeNode):
    assert not n0.is_internal_node()
    assert n1.is_internal_node()
    for child in n1.children:
        assert not child.is_internal_node()
    for child in n3.children:
        assert child.is_internal_node()

def test_node_descendants_list(n1: TreeNode):
    genera = ["Canines", "Bovines", "Felines", "Birds"]
    d = tuple((TreeNode(genus) for genus in genera))
    assert n1.descendants == d

def test_node_descendants_level(n1: TreeNode):
    for descendant in n1.descendants:
        assert descendant.level == descendant._parent.level+1

def test_node_self_not_in_descendants(n1: TreeNode):
    assert n1 not in n1.descendants

def test_node_self_in_all_nodes(n1: TreeNode):
    assert n1 in n1.all_nodes


# Tree tests.
def test_tree_root_level(t1: Tree):
    assert t1.root.level == 0
