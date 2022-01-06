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
        """
        Adds new child to the node forest.

        New child node must be of a valid node type, else
        TypeError is raised.
        """
        if not isinstance(new_child, TreeNode):
            raise TypeError("Child must be of TreeNode type.")
        new_child._parent = self
        self._children.append(new_child)
    
    def pop_child(self, child: "TreeNode"):
        """
        Removes the child node from the node forest.

        Raises ValueError if the node is not found.

        Child node must be of a valid node type, else
        TypeError is raised.
        """
        if not isinstance(child, TreeNode):
            raise TypeError("Item to remove must be of TreeNode type.")
        children = self.children
        for i in range(len(children)):
            if children[i] == child:
                child_to_remove = self._children.pop(i)
                child_to_remove.set_parent(None)
                return child_to_remove
        raise ValueError(f"Node '{self}' has no child node '{child}'.")
    
    def set_parent(self, parent: "TreeNode"):
        """
        Sets the parent node.

        A node cannot be its own parent. ValueError is raised in case
        the node itself is passed as an argument.

        Parent node must be of a valid node type or of NoneType, else
        TypeError is raised.
        """
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
        """
        The direct ancestor of the node.
        
        A node can only have one parent node.
        """
        return self._parent

    @property
    def ancestors(self) -> Tuple["TreeNode"]:
        """All the nodes in the path from the node parent to the root."""
        current = self.parent
        ancestors = []
        while current:
            ancestors.append(current)
            current = current.parent
        return tuple(ancestors)

    @property
    def depth(self) -> int:
        """
        A measure of how distant the node is from the root.

        It's the number of edges along the unique path between the node
        and the root.
        
        The root node has 0 depth.
        """
        current = self.parent
        depth = 0
        while current:
            current = current.parent
            depth += 1
        return depth 
    
    @property
    def siblings(self) -> Tuple["TreeNode"]:
        """
        Tuple containing all the children from the node's parent,
        excluding the node itself.
        """
        if not self.parent:
            return ()
        return tuple(
                (child for child in self.parent.children if child != self)
            )
    
    @property
    def neighbours(self) -> Tuple["TreeNode"]:
        """Tuple containing node's parent and children, if any exists."""
        parent_and_children = (self.parent,) + self.children
        return parent_and_children if self.parent else self.children
    
    def _release_current_children(self):
        for child in self._children:
            child.set_parent(None)
        self._children = []

    def set_children(self, children: Sequence["TreeNode"]):
        """
        Substitutes the current node's children.
        
        The argument must be a sequence containg nodes of a valid node type.
        """
        self._release_current_children()
        if not children:
            return
        for child in children:
            self.add_child(child)
    
    @property
    def children(self):
        """The direct descendants of the node."""
        return tuple(self._children) if self._children else ()
    
    @property
    def degree(self):
        """The number of children the node has."""
        return len(self.children)

    @property
    def level(self):
        """
        A way of enumerating the generations of the tree.
        
        The root node has level 1.

        Level = depth + 1
        """
        return self.depth + 1
    
    @property
    def height(self):
        """
        The number of edges of the longest downward path
        from the node to a leaf.
        """
        if not self.children:
            return 0
        return 1 + max([child.height for child in self.children])
    
    def get_distance_from_descendant(self, node: "TreeNode") -> int:
        """
        Calculate the distance between the node and a descendant node.
        
        If it's not a descendant from the node, ValueError is raised.
        
        The node must be of a valid node type, else
        TypeError is raised.
        """
        if not isinstance(node, TreeNode):
            raise TypeError(f"Node must be of type TreeNode.")
        for descendant in self.descendants:
            if node == descendant:
                return descendant.level - self.level
        raise ValueError(f"{node} is not a descendant of {self}.")
    
    def is_leaf_node(self) -> bool:
        """Returns True if the node has any children, else False."""
        return not self._children
    
    def is_internal_node(self) -> bool:
        """Returns False if the node has any children, else True."""
        return bool(self._children)
    
    @property
    def leaves(self) -> tuple["TreeNode"]:
        """A tuple with all the leaf nodes, if any exist."""
        return tuple((node for node in self.all_nodes if node.is_leaf_node()))

    @property
    def breadth(self) -> int:
        """The number of leaves the node has."""
        return len(self.leaves)

    @property
    def all_nodes(self) -> Tuple["TreeNode"]:
        """A tuple containing all descendant nodes and the node itself."""
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
        """A tuple containing all nodes excluding self."""
        all_nodes = self.all_nodes
        self_position = 0
        range_excluding_self = slice(self_position+1, len(all_nodes))
        return all_nodes[range_excluding_self]
    
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