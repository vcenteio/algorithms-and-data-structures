from typing import Any, Hashable
from abc import ABC, abstractmethod
from tools import get_class_name

class INode(ABC):
    data: Hashable = None
    _next: "INode" = None

    @property
    @abstractmethod
    def next_node(self) -> "INode":
        ...

    @abstractmethod
    def set_next_node(self, next_node: "INode"):
        ...


class Node(INode):
    def __init__(self, data: Hashable = None):
        if not isinstance(data, Hashable):
            raise TypeError(
                "Only hashable objects are accepted as node values. "\
                f"'{get_class_name(data).title()}' objects are not hashable."
            )
        self.data = data
    
    def __repr__(self):
        return f"Node({self.data})"

    def __str__(self):
        return f"{self.data}"
    
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.data == other.data
        else:
            return self.data == other
    
    def __ne__(self, other):
        if isinstance(other, Node):
            return self.data != other.data
        else:
            return self.data != other
    
    def __hash__(self):
        return hash(self.data)

    def __gt__(self, other):
        return self.data > other.data

    def __ge__(self, other):
        return self.data >= other.data
    
    def __lt__(self, other):
        return self.data < other.data

    def __le__(self, other):
        return self.data <= other.data

    @property
    def next_node(self) -> "Node":
        return self._next

    def set_next_node(self, next_node: "Node"):
        self._next = next_node