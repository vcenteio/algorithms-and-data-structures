import sys
from typing import Any, Hashable, Iterable, Sequence


class TreeNode:
    _level: int = 0
    _parent: "TreeNode" = None

    def __init__(
        self, data, parent: "TreeNode" = None,
        _children: list["TreeNode"] = None
    ):
        self.data: Any = data
        self._children: list["TreeNode"] = []
        self.set_parent(parent)
        self.set_children(_children)
    
    def add_child(self, new_child: "TreeNode"):
        new_child._parent = self
        new_child.set_level()
        self._children.append(new_child)
    
    def remove_child(self, child):
        children_data = [child.data for child in self._children]
        child_index = children_data.index(child)
        self._children.pop(child_index)
    
    def set_parent(self, parent: "TreeNode"):
        if isinstance(parent, TreeNode):
            parent.add_child(self)
        elif parent == None:
            self._parent == None
        else:
            raise TypeError("Inappropriate type for parent.")
    
    @property
    def parent(self):
        return self._parent

    def set_level(self):
        self._level = self._parent.level+1 if self._parent else 0
        for descendant in self.descendants:
            descendant.set_level()

    def set_children(self, children: Sequence["TreeNode"]):
        if not children:
            self._children = []
            return
        for child in children:
            self.add_child(child)
            for descendant in child.descendants:
                descendant.set_level()
    
    @property
    def children(self):
        return tuple(self._children)

    @property
    def level(self):
        return self._level
    
    def is_leaf_node(self) -> bool:
        return not self._children
    
    def is_internal_node(self) -> bool:
        return bool(self._children)

    @property
    def all_nodes(self) -> list["TreeNode"]:
        if self.is_leaf_node():
            return [self]
        else:
            _l = []
            for child in self._children:
                 _l.extend(child.all_nodes)
            _l.insert(0, self)
            return tuple(_l)

    @property
    def descendants(self) -> list["TreeNode"]:
        index_excluding_self = 1
        return self.all_nodes[index_excluding_self:]
    
    def __repr__(self):
        return str(self.data)

    def __str__(self):
        return str(self.data)
    
    def __iter__(self):
        return iter(self._children)

    def __contains__(self, item):
        children_data = [child.data for child in self]
        return item in children_data
    
    def __hash__(self):
        return hash(self.data)
    
    def __eq__(self, other: "TreeNode"):
        return hash(self) == hash(other) if isinstance(other, Hashable) else False


class Tree:
    def __init__(self, root: TreeNode):
        self.root = root
        if self.root:
            self.root._level = 0    
    
    @staticmethod
    def _is_node(node) -> bool:
        return isinstance(node, TreeNode)

    def find(self, data) -> TreeNode:
        for node in self:
            if node.data == data:
                return node
        return None

    def _find_parent_node(self, parent_data):
        parent = self.find(parent_data)
        if parent == None:
            raise ValueError("Parent node not found.")
        return parent

    def add(self, new_node: TreeNode, parent_data):
        parent = self._find_parent_node(parent_data)
        parent.add_child(new_node)

    def remove(self, node, parent_data):
        parent = self._find_parent_node(parent_data)
        parent.remove_child(node)

    def __iter__(self):
        return iter(self.root.all_nodes)
    
    def __contains__(self, item):
        return item.data in self.root.all_nodes
    
    def __repr__(self):
        nodes_str = [child.level * '__' + str(child) for child in self]
        return "\n|".join(nodes_str)


# for manual testing purposes
if __name__ == "__main__":
    tn0 = TreeNode("a")
    tn1 = TreeNode("b")
    tn1ch0 = TreeNode("Wolf")
    tn1ch1 = TreeNode("Dog")

    genera = ["Canines", "Bovines", "Felines", "Birds"]
    for genus in genera:
        tn1.add_child(TreeNode(genus))

    t1 = Tree(tn1)
    