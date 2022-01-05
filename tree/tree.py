from typing import Any, Hashable, Sequence, Tuple
from .treenode import TreeNode

class Tree:
    def __init__(self, root: TreeNode):
        self.root = root
    
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
    