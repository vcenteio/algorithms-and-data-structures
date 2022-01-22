from typing import Any, Hashable, Iterator, Union
from collections.abc import Iterable

from .inodeabc import INode
from ..tools.tools import get_class_name


class Node(INode):
    def __init__(self, data: Hashable = None):
        if not isinstance(data, Hashable):
            raise TypeError(
                "Only hashable objects are accepted as node values. "
                f"'{get_class_name(data).title()}' objects are not hashable."
            )
        self.data = data

    def __getitem__(self, key: int) -> Any:
        return self.data[key]  # type: ignore[index]

    def __iter__(self) -> Iterator:
        if isinstance(self.data, Iterable):
            return iter(self.data)
        else:
            raise TypeError("Node data is not iterable.")

    def __repr__(self) -> str:
        return f"Node({self.data})"

    def __str__(self) -> str:
        return f"{self.data}"

    def __eq__(self, other) -> bool:
        if isinstance(other, Node):
            return self.data == other.data
        else:
            return self.data == other

    def __ne__(self, other) -> bool:
        if isinstance(other, Node):
            return self.data != other.data
        else:
            return self.data != other

    def __hash__(self) -> int:
        return hash(self.data)

    def __gt__(self, other) -> bool:
        return self.data > other.data

    def __ge__(self, other) -> bool:
        return self.data >= other.data

    def __lt__(self, other) -> bool:
        return self.data < other.data

    def __le__(self, other) -> bool:
        return self.data <= other.data

    @property
    def next_node(self) -> Union["INode", None]:
        return self._next

    def set_next_node(self, next_node: Union["INode", None]) -> None:
        self._next = next_node
