from typing import Any, Tuple, Sequence, Hashable

class TreeNode:
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
            if parent == self:
                raise ValueError("A node cannot be its own parent.")
            parent.add_child(self)
        elif parent == None:
            self._parent = None
        else:
            raise TypeError("Inappropriate type for parent.")
    
    @property
    def parent(self) -> "TreeNode":
        return self._parent

    @property
    def ancestors(self) -> Tuple["TreeNode"]:
        current = self.parent
        ancestors = []
        while current:
            ancestors.append(current)
            current = current.parent
        return tuple(ancestors)

    @property
    def depth(self) -> int:
        current = self.parent
        depth = 0
        while current:
            current = current.parent
            depth += 1
        return depth 
    
    @property
    def siblings(self) -> Tuple["TreeNode"]:
        if not self.parent:
            return ()
        return tuple(
                (child for child in self.parent.children if child != self)
            )
    
    @property
    def neighbours(self) -> Tuple["TreeNode"]:
        parent_and_children = (self.parent,) + self.children
        return parent_and_children if self.parent else self.children
    
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
    
    @property
    def children(self):
        return tuple(self._children) if self._children else ()
    
    @property
    def degree(self):
        return len(self.children)

    @property
    def level(self):
        return self.depth + 1
    
    @property
    def height(self):
        if not self.children:
            return 0
        return 1 + max([child.height for child in self.children])
    
    def distance_from_descendant(self, node: "TreeNode") -> int:
        if not isinstance(node, TreeNode):
            raise TypeError(f"Node must be of type TreeNode.")
        for descendant in self.descendants:
            if node == descendant:
                return descendant.level - self.level
        raise ValueError(f"{node} is not a descendant of {self}.")
    
    def is_leaf_node(self) -> bool:
        return not self._children
    
    def is_internal_node(self) -> bool:
        return bool(self._children)
    
    @property
    def leaves(self) -> tuple["TreeNode"]:
        return tuple((node for node in self.descendants if node.is_leaf_node()))

    @property
    def breadth(self) -> int:
        return len(self.leaves)

    @property
    def all_nodes(self) -> Tuple["TreeNode"]:
        if self.is_leaf_node():
            return (self,)
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