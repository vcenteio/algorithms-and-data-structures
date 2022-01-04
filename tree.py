from typing import Any


class TreeNode:
    def __init__(
        self, data, parent: "TreeNode" = None,
        _children: list["TreeNode"] = None
    ):
        self.data = data
        self._parent: TreeNode = parent
        self._children: list = _children if _children else []
        self.level: int = 0 if parent == None else parent.level+1
    
    def add_child(self, new_child):
        new_child.level = self.level + 1
        new_child._parent = self
        self._children.append(new_child)
    
    def remove_child(self, child):
        children_data = [child.data for child in self._children]
        child_index = children_data.index(child)
        self._children.pop(child_index)
    
    def is_leaf_node(self) -> bool:
        return not self._children
    
    def is_internal_node(self) -> bool:
        return bool(self._children)

    @property
    def descendants(self):
        if self.is_leaf_node():
            return [self]
        else:
            _l = []
            for child in self._children:
                 _l.extend(child.descendants)
            _l.insert(0, self)
            return _l
    
    def __repr__(self):
        return str(self.data)

    def __str__(self):
        return str(self.data)
    
    def __iter__(self):
        return iter(self._children)

    def __contains__(self, item):
        children_data = [child.data for child in self]
        return item in children_data


class Tree:
    def __init__(self, root: TreeNode):
        self.root = root
        if self.root:
            self.root.level = 0    
    
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
        return iter(self.root.descendants)
    
    def __contains__(self, item):
        return item.data in self.root.descendants
    
    def __repr__(self):
        nodes_str = [child.level * '__' + str(child) for child in self]
        return "\n|".join(nodes_str)


# for manual testing purposes
if __name__ == "__main__":
    tn0 = TreeNode("a")
    tn1 = TreeNode("b")
    tn1ch0 = TreeNode("Wolf")
    tn1ch1 = TreeNode("Dog")

    genus = ["Canines", "Bovines", "Felines", "Birds"]
    for species in genus:
        tn1.add_child(TreeNode(species))

    t1 = Tree(tn1)
    