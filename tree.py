﻿from typing import Any, Hashable, Sequence, Tuple


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
        if not isinstance(new_child, TreeNode):
            raise TypeError("Child must be of TreeNode type.")
        new_child._parent = self
        new_child.set_level()
        self._children.append(new_child)
    
    def pop_child(self, child_data: Any):
        index = 0
        for child in self._children:
            if child.data == child_data:
                child_to_remove = self._children.pop(index)
                child_to_remove.set_parent(None)
                return child_to_remove
            index += 1
        raise ValueError(f"No child node with data '{child_data}'")
    
    def set_parent(self, parent: "TreeNode"):
        if isinstance(parent, TreeNode):
            parent.add_child(self)
        elif parent == None:
            self._parent = None
            self.set_level()
        else:
            raise TypeError("Inappropriate type for parent.")
    
    @property
    def parent(self) -> "TreeNode":
        return self._parent

    def set_level(self):
        self._level = self._parent.level+1 if self._parent else 0
        for descendant in self.descendants:
            descendant.set_level()
    
    def _release_current_children(self):
        for child in self._children:
            child.set_parent(None)
        self._children = []

    def set_children(self, children: Sequence["TreeNode"]):
        self._release_current_children()
        if not children:
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
    def all_nodes(self) -> Tuple["TreeNode"]:
        if self.is_leaf_node():
            return [self]
        else:
            l = []
            for child in self._children:
                 l.extend(child.all_nodes)
            l.insert(0, self)
            return tuple(l)

    @property
    def descendants(self) -> Tuple["TreeNode"]:
        index_excluding_self = 1
        return self.all_nodes[index_excluding_self:]
    
    def __repr__(self):
        return str(self.data)

    def __str__(self):
        return str(self.data)
    
    def __iter__(self):
        return iter(self._children)

    def __contains__(self, item):
        if not isinstance(item, TreeNode):
            raise TypeError("Item is not of TreeNode type.")
        return item in self._children
    
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
    