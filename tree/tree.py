from typing import Any, Hashable, Iterable, Sequence, Tuple, Union
if __name__ == "__main__":
    from treenode import TreeNode
else:
    from .treenode import TreeNode
import sys
sys.path.append("..")
from tools import get_class_name


class Tree:
    def __init__(self, root: TreeNode):
        self.set_root(root)
    
    def set_root(self, root: TreeNode):
        """
        Sets the root node of the tree.

        The argument must be of a valid node type.
        """
        if not self._is_node(root):
            raise TypeError(
                "Root must be of a valid node type."
            )
        root.set_parent(None)
        self._root = root

    @property
    def root(self) -> TreeNode:
        """The root node of the tree."""
        return self._root
    
    @property
    def degree(self) -> int:
        """The degree of the node(s) with the highest degree in the tree."""
        return max(
            (node.degree for node in self if not node.is_leaf_node())
        ) if not self.root.is_leaf_node() else 0

    def get_common_ancestors(self, node1: TreeNode, node2: TreeNode) -> list:
        """
        Returns a list with the common ancestors between the nodes.

        Any of the two nodes can be considered an ancestor of the other.

        TypeError is raised if any of the items is not of a valid node type.
        """
        if not isinstance(node1, TreeNode) or not isinstance(node2, TreeNode):
            raise TypeError(
                "Nodes must be of TreeNode type. "\
                f"node1 = {node1}; node2 = {node2}"
            )
        # The two considered sets include the nodes themselves and
        # not only their common ancestors, since, to obtain 
        # the lowest common ancestor, nodes must be regarded as
        # descendants of themselves.
        # This way, it's possible to encompass the possibility
        # of one of the nodes being an ancestor of the other, in which
        # case we're able us to calculate the distance between
        # child and parent nodes (which is 1).
        n1_ancestors = set(node1.ancestors+(node1,))
        n2_ancestors = set(node2.ancestors+(node2,))
        return list(n1_ancestors.intersection(n2_ancestors))

    def get_lowest_common_ancestor(self, node1: TreeNode, node2: TreeNode) -> Union[TreeNode, None]:
        """
        Returns the lowest common ancestor (LCA) between the nodes.

        If no common ancestor is found, returns None.

        TypeError is raised if any of the items is not of a valid node type.

        If a given node is a parent (direct ancestor) of the other,
        the former is the LCA.

        Depth is used to measure how close the ancestor is from the nodes. The
        higher the depth, the closer it is.
        """
        common_ancestors = self.get_common_ancestors(node1, node2)
        common_ancestors.sort(key=lambda x: x.depth)
        return common_ancestors.pop() if common_ancestors else None

    def get_distance_between(self, node1: TreeNode, node2: TreeNode) -> int:
        """
        Returns the number of edges along
        the shortest path between the two nodes.

        If no path is found, raise ValueError.
        """
        lca = self.get_lowest_common_ancestor(node1, node2)
        if not lca:
            raise ValueError(
                f"There is no path between nodes {node1} and {node2}."
            )
        return node1.depth + node2.depth - 2*lca.depth
    
    def get_nodes_at_level(self, level: int):
        """
        Returns all nodes at a given level.
        
        Level must be an integer and >= 1, else TypeError or ValueError
        is raised, respectively.
        """
        if not isinstance(level, int) or isinstance(level, bool):
            raise TypeError(
                f"Level cannot be a {get_class_name(level)}. "\
                "Must be an int."
            )
        if level < 1:
            raise ValueError("Level must be >= 1.")
        return tuple(filter(lambda x: x.level==level, self))

    def get_level_width(self, level: int):
        """
        Return the number of nodes at a given level.

        Level must be an integer and >= 1, else TypeError or ValueError
        is raised, respectively.
        """
        return len(self.get_nodes_at_level(level))

    @property
    def breadth(self):
        """The number of leaves on the tree."""
        return self.root.breadth
    
    @property
    def size(self):
        """The number of nodes on the tree, including the root."""
        return len(self.root.all_nodes)
    
    @property
    def height(self):
        """
        The number of edges of the longest downward path
        from the root to a leaf.
        """
        return self.root.height

    @staticmethod
    def _is_node(node) -> bool:
        return isinstance(node, TreeNode)

    def find(self, node: TreeNode) -> TreeNode:
        """
        Searches for the node in the tree and returns it if found.
        
        Returns None if not found.

        Raises TypeError if the argument is not of a valid node type.
        """
        if not self._is_node(node):
            raise TypeError("Argument must be of valid node type.")
        for existing_node in self:
            if existing_node == node:
                return existing_node
        return None

    def _find_parent_node(self, parent_node: TreeNode) -> TreeNode:
        parent = self.find(parent_node)
        if parent == None:
            raise ValueError("Parent node not found.")
        return parent

    def add(self, new_node: TreeNode, parent_node: TreeNode = None):
        """
        Add a node as a child of an existing node in the tree.

        All child nodes of the new node are maintained.
        If no parent node is given, it adds the new node as a child
        of the root node.
        """
        if not self._is_node(new_node):
            raise TypeError("New item must be of TreeNode type.")
        if not self._is_node(parent_node) and parent_node != None:
            raise TypeError("Parent must be of TreeNode type.")
        if parent_node != None:
            parent = self._find_parent_node(parent_node)
            parent.add_child(new_node)
        else:
            self.root.add_child(new_node)

    def remove(self, node: TreeNode) -> TreeNode:
        """
        Removes a node along with its children - if it has any - 
        and returns it.

        TypeError is raised if argument is not of a valid node type.

        ValueError is raised if the argument is the root node or
        if it's not found in the tree.
        """
        if not self._is_node(node):
            raise TypeError("Item must be of TreeNode type.")
        if node == self.root:
            raise ValueError(f"Cannot remove root node.")
        _node = self.find(node)
        if _node == None:
            raise ValueError(f"Node {node} not found.")
        # If the node was found and it's not the root,
        # it must have a parent.
        return _node.parent.pop_child(node)

    def __iter__(self):
        return iter(self.root.all_nodes)
    
    def __contains__(self, node: TreeNode):
        if not isinstance(node, TreeNode):
            raise TypeError("Item must be a TreeNode type node.")
        return node in self.root.all_nodes
    
    def __len__(self) -> int:
        return self.size
    
    def __repr__(self):
        return str({node:(f"lvl={node.level}", f"parent={node.parent}") for node in self})

    def __str__(self):
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
    