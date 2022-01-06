from typing import Any, Hashable, Iterable, Sequence, Tuple
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
        root.set_parent(None)
        self._root = root

    @property
    def root(self) -> TreeNode:
        return self._root
    
    @property
    def degree(self) -> int:
        return max(
            (node.degree for node in self if not node.is_leaf_node())
        ) if not self.root.is_leaf_node() else 0

    def get_least_common_ancestor(self, node1: TreeNode, node2: TreeNode):
        if not isinstance(node1, TreeNode) or not isinstance(node2, TreeNode):
            raise TypeError(
                "Nodes must be of TreeNode type. "\
                f"node1 = {node1}; node2 = {node2}"
            )
        # Nodes' ancestors include the nodes themselves
        # in order for us to calculate the distance between
        # child and parent nodes.
        n1_ancestors = set(node1.ancestors+(node1,))
        n2_ancestors = set(node2.ancestors+(node2,))
        common_ancestors = list(n1_ancestors.intersection(n2_ancestors))
        common_ancestors.sort(key=lambda x: x.depth)
        return common_ancestors.pop() if common_ancestors else None

    def get_distance_between(self, node1: TreeNode, node2: TreeNode):
        lca = self.get_least_common_ancestor(node1, node2)
        if not lca:
            raise ValueError(
                f"There are no common ancestors between {node1} and {node2}."
            )
        return node1.depth + node2.depth - 2*lca.depth
    
    def get_nodes_at_level(self, level: int):
        if not isinstance(level, int) or isinstance(level, bool):
            raise TypeError(
                f"Level cannot be a {get_class_name(level)}. "\
                "Must be an int."
            )
        if level < 1:
            raise ValueError("Level must be >= 1.")
        return tuple(filter(lambda x: x.level==level, self))

    def get_level_width(self, level: int):
        return len(self.get_nodes_at_level(level))

    @property
    def breadth(self):
        return self.root.breadth

    @staticmethod
    def _is_node(node) -> bool:
        return isinstance(node, TreeNode)

    def find(self, node: TreeNode) -> TreeNode:
        for _node in self:
            if _node == node:
                return _node
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
    
    def __contains__(self, node: TreeNode):
        if not isinstance(node, TreeNode):
            raise TypeError("Item must be a TreeNode type node.")
        return node in self.root.all_nodes
    
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
    