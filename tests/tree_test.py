from tree import Tree, TreeNode
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

# Node tests
def test_node_instantiation_with_no_data():
    with pytest.raises(TypeError):
        TreeNode()

def test_node_instantiation_with_no_parent_and_no_children(n0: TreeNode):
    assert n0._parent == None
    assert n0._children == []
    assert n0.level == 1

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

    i = 0
    for child in n3.children:
        assert child.children == subchildren[i]
        i += 1

    expected_children = {child for child in children}
    expected_subchildren = {subchild for subgenus in subchildren for subchild in subgenus}
    expected_descendants = expected_children | expected_subchildren
    assert set(tuple(n3.descendants)) == expected_descendants

    assert n3.level == 2
    assert n3.parent.level == 1
    for child in n3.children:
        assert child.level == 3
        for subchild in child.children:
            assert subchild.level == 4
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
    assert child_a.level == child_b.level == 2

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
    with pytest.raises(ValueError):
        n1.set_parent(n1)

    n1.set_parent(parent := TreeNode("Living Organism"))
    assert n1 in parent
    assert n1._parent == parent
    assert n1.level == parent.level+1 == n1._parent.level+1
    for child in n1.children:
        assert child.level == n1.level+1 == n1.parent.level+2 

    n1.set_parent(None)
    assert n1._parent == None
    assert n1.level == 1
    for child in n1.children:
        assert child.level == 2

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
    assert n3.level == 2 == n3.parent.level+1
    n3._parent = None
    assert n3.level == 1
    for descendant in n3.descendants:
        assert descendant.level == descendant.parent.level+1
    
def test_node_set_children_with_empty_list(n0: TreeNode, n1: TreeNode):
    n0.set_children([])
    assert n0._children == []
    
    n1_children_copy = n1.children[:]
    n1.set_children([])
    for child in n1_children_copy:
        assert child.level == 1
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
        assert child.level == 1
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

def test_node_ancestors(n0: TreeNode, n1: TreeNode, n2: TreeNode):
    assert n0.ancestors == ()
    assert n1.ancestors == ()
    for child in n1.children:
        assert child.ancestors == (n1,)

    expected_ancestors = (TreeNode("Animal"), TreeNode("Living Organisms"))
    for child in n2.children:
        assert child.ancestors == expected_ancestors

def test_node_siblings(n0: TreeNode, n1: TreeNode):
    assert n0.siblings == ()
    assert n1.siblings == ()
    
    children = tuple(map(TreeNode, ["Canines", "Bovines", "Felines", "Birds"]))

    i = 0
    for child in n1.children:
        assert child.siblings == tuple((child for child in children if child != children[i]))
        i += 1

def test_node_height(n0: TreeNode, n1: TreeNode, n2: TreeNode, n3: TreeNode):
    assert n0.height == 0    

    assert n1.height == 1
    for child in n1.children:
        assert child.height == 0

    assert n2.height == 1
    assert n2.parent.height == 2
    for child in n2.children:
        assert child.height == 0
    
    assert n3.parent.height == 3
    for descendant in n3.descendants:
        if descendant.is_leaf_node():
            assert descendant.height == 0
        if not descendant.height:
            assert descendant.is_leaf_node()
    
    n3.children[0].pop_child("Wolf")
    n3.children[0].pop_child("Dog")
    assert n3.parent.height == 3
    assert n3.height == 2
    n3.children[2].pop_child("Cat")
    n3.children[2].pop_child("Tiger")
    assert n3.parent.height == 3
    assert n3.height == 2
    n3.pop_child("Canines")
    n3.pop_child("Felines")
    n3.pop_child("Bovines")
    assert n3.parent.height == 3
    assert n3.height == 2

def test_node_depth(n0: TreeNode, n1: TreeNode, n2: TreeNode, n3: TreeNode):
    assert n0.depth == 0

    assert n1.depth == 0
    for child in n1.children:
        assert child.depth == 1

    assert n2.depth == 1
    assert n2.parent.depth == 0
    for child in n2.children:
        assert child.depth == 2
    
    for descendant in n3.descendants:
        if descendant.is_leaf_node():
            assert descendant.depth == 3
        elif descendant.is_internal_node():
            assert not descendant.depth == 3
            assert descendant.depth == descendant.parent.depth+1

def test_node_neighbours(n0: TreeNode, n1: TreeNode, n2: TreeNode, n3: TreeNode):
    assert n0.neighbours == ()
    assert n1.neighbours == n1.children
    assert n2.neighbours == (n2.parent,) + n2.children
    assert n2.parent.neighbours == (n2,)
    assert n3.neighbours == (n3.parent,) + n3.children
    for descendant in n3.descendants:
        assert descendant not in n3.neighbours if descendant.level >= n3.level+2 else descendant in n3.neighbours

def test_node_degree(n0: TreeNode, n1: TreeNode, n2: TreeNode, n3: TreeNode):
    assert n0.degree == 0 == len(n0.children)
    assert n1.degree == n2.degree == 4
    assert n2.parent.degree == 1
    n2.parent.add_child(TreeNode("new child"))
    assert n2.parent.degree == 2
    for child in n3.children:
        assert child.degree == 2
        for subchild in child.children:
            assert subchild.degree == 0
    for node in (n0, n1, n2, n3):
        for subnode in node.all_nodes:
            assert subnode.degree == len(subnode.children)
            assert subnode.degree == 0 if subnode.is_leaf_node() else subnode.degree > 0

def test_node_distance_from_descendant_wrong_type(n0: TreeNode):
    with pytest.raises(TypeError):
        n0.distance_from_descendant("str")
    with pytest.raises(TypeError):
        n0.distance_from_descendant(1)

def test_node_distance_from_descendant_correct_type(n0: TreeNode, n1: TreeNode, n2: TreeNode, n3: TreeNode):
    with pytest.raises(ValueError):
        n0.distance_from_descendant(n1)
    with pytest.raises(ValueError):
        n1.distance_from_descendant(n1)
    
    for child in n1.children:
        assert n1.distance_from_descendant(child) == 1
    for child in n2.children:
        for subchild in child:
            assert n2.distance_from_descendant(subchild) == 2 == n2.distance_from_descendant(child)+1
    
    for node in n3.parent.descendants:
        assert n3.parent.distance_from_descendant(node) == node.level - n3.parent.level

def test_node_leaves(n0: TreeNode, n1: TreeNode, n2: TreeNode, n3: TreeNode):
    assert n0.leaves == (TreeNode("Animal"),)

    expected_n1_leaves = tuple(map(TreeNode, ["Canines", "Bovines", "Felines", "Birds"]))
    assert n1.leaves == expected_n1_leaves
    assert n2.leaves == n1.leaves

    canines = list(map(TreeNode, ["Dog", "Wolf"]))
    bovines = list(map(TreeNode, ["Cattle", "Bison"]))
    felines = list(map(TreeNode, ["Cat", "Tiger"]))
    birds = list(map(TreeNode, ["Hawk", "Dove"]))
    expected_n3_leaves = tuple([*canines, *bovines, *felines, *birds])
    assert n3.leaves == expected_n3_leaves

def test_node_breadth(n0: TreeNode, n1: TreeNode, n2:TreeNode, n3: TreeNode):
    assert n0.breadth == 1
    assert n1.breadth == 4 == n2.breadth
    assert n3.breadth == 8


@pytest.fixture
def t0(n0):
    return Tree(n0)

@pytest.fixture
def t1(n1):
    return Tree(n1)

@pytest.fixture
def t2(n2):
    return Tree(n2)

@pytest.fixture
def t3(n3):
    return Tree(n3)

# Tree tests.

def test_tree_contains_wrong_type(t1: Tree):
    with pytest.raises(TypeError):
        1 in t1
    with pytest.raises(TypeError):
        True in t1
    with pytest.raises(TypeError):
        "str" in t1
    with pytest.raises(TypeError):
        [1,2,3] in t1

def test_tree_contains_correct_type(t1: Tree, t2):
    node1 = TreeNode("Animal")
    node2 = TreeNode("Dinosaurs")
    assert node1 in t1
    assert node1 in t2
    assert node2 not in t1
    assert node2 not in t2

def test_tree_root_level(t1: Tree, t2: Tree):
    assert t1.root.level == 1
    assert t2.root.level == 1

def test_tree_degree(t0: Tree, t1: Tree, t2: Tree, t3: Tree):
    assert t0.degree == 0
    assert t1.degree == t2.degree == t3.degree == 4

    t3.root.children[2].add_child(TreeNode("Cheetah"))
    t3.root.children[2].add_child(TreeNode("Cougar"))
    t3.root.children[2].add_child(TreeNode("Leopard"))
    assert t3.degree == 5
    t3.root.children[3].add_child(TreeNode("Chimney Swift"))
    t3.root.children[3].add_child(TreeNode("Red Knot"))
    t3.root.children[3].add_child(TreeNode("Wood Duck"))
    t3.root.children[3].add_child(TreeNode("Virginia Rail"))
    assert t3.degree == 6

def test_tree_least_common_ancestor_wrong_types(t3: Tree):
    with pytest.raises(TypeError):
        assert t3.get_least_common_ancestor("123", 2)

def test_tree_least_common_ancestor_nodes_of_the_same_tree(t3: Tree):
    node1 = t3.find(TreeNode("Wolf"))
    node2 = t3.find(TreeNode("Dog"))
    assert t3.get_least_common_ancestor(node1, node2) == TreeNode("Canines")
    node2 = t3.find(TreeNode("Canines"))
    assert t3.get_least_common_ancestor(node1, node2) == TreeNode("Canines")
    node2 = t3.find(TreeNode("Felines"))
    assert t3.get_least_common_ancestor(node1, node2) == TreeNode("Animal")
    
    t3.root.children[2].add_child(TreeNode("Cheetah"))
    node2 = t3.find(TreeNode("Cheetah"))
    assert t3.get_least_common_ancestor(node1, node2) == TreeNode("Animal")

def test_tree_least_common_ancestor_nodes_of_the_different_trees(t0: Tree, t1: Tree, t2: Tree, t3: Tree):
    node1 = t3.find(TreeNode("Wolf"))
    node2 = t3.find(TreeNode("Living Organisms"))
    with pytest.raises(TypeError):
        t3.get_least_common_ancestor(node1, node2)

    assert t3.get_least_common_ancestor(node1, TreeNode("Dinosaur")) == None

def test_tree_distance_between_nodes_with_lca(t3: Tree):
    node1 = node2 = t3.find(TreeNode("Wolf"))
    assert t3.get_distance_between(node1, node2) == 0
    node2 = t3.find(TreeNode("Dog"))
    assert t3.get_distance_between(node1, node2) == 2
    node2 = t3.find(TreeNode("Canines"))
    assert t3.get_distance_between(node1, node2) == 1
    node2 = t3.find(TreeNode("Animal"))
    assert t3.get_distance_between(node1, node2) == 2
    node2 = t3.find(TreeNode("Felines"))
    assert t3.get_distance_between(node1, node2) == 3
    node2 = t3.find(TreeNode("Cat"))
    assert t3.get_distance_between(node1, node2) == 4
    node2.add_child(TreeNode("Persian"))
    node2 = t3.find(TreeNode("Persian"))
    assert t3.get_distance_between(node1, node2) == 5

def test_tree_get_level_width_wrong_type(t3: Tree):
    with pytest.raises(TypeError):
        t3.get_level_width("as")
    with pytest.raises(TypeError):
        t3.get_level_width(True)
    with pytest.raises(TypeError):
        t3.get_level_width(False)
    with pytest.raises(TypeError):
        t3.get_level_width([1,2,3])

def test_tree_get_level_width_correct_type(t3: Tree):
    with pytest.raises(ValueError):
        t3.get_level_width(0)
    with pytest.raises(ValueError):
        t3.get_level_width(-1)
    assert t3.get_level_width(1) == 1
    assert t3.get_level_width(2) == 4
    assert t3.get_level_width(3) == 8
    assert t3.get_level_width(4) == 0
    assert t3.get_level_width(4) == 0

def test_tree_breadth(t0: Tree, t1: Tree, t3: Tree):
    assert t0.breadth == 1
    assert t1.breadth == 4
    assert t3.breadth == 8
    t3.find(TreeNode("Felines")).add_child(TreeNode("Cougar"))
    assert t3.breadth == 9