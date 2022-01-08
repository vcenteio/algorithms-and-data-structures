try:
    from .treenode import TreeNode
except ImportError:
    from treenode import TreeNode


def is_node(node) -> bool:
    return isinstance(node, TreeNode)
