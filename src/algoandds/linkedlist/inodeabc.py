from typing import Any, Hashable, Iterator, Union
from abc import ABC, abstractmethod


class INode(ABC):
    data: Hashable = None
    _next: Union["INode", None] = None

    @property
    @abstractmethod
    def next_node(self) -> Union["INode", None]:
        ...

    @abstractmethod
    def set_next_node(self, next_node: Union["INode", None]):
        ...

    @abstractmethod
    def __getitem__(self, key: int) -> Any:
        ...

    @abstractmethod
    def __iter__(self) -> Iterator:
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...

    @abstractmethod
    def __eq__(self, other) -> bool:
        ...

    @abstractmethod
    def __ne__(self, other) -> bool:
        ...

    @abstractmethod
    def __lt__(self, other) -> bool:
        ...

    @abstractmethod
    def __gt__(self, other) -> bool:
        ...

    @abstractmethod
    def __le__(self, other) -> bool:
        ...

    @abstractmethod
    def __ge__(self, other) -> bool:
        ...
