from abc import ABC, abstractmethod
from typing import Any, Container, Generator, Iterable, MutableSequence, Sequence, Union


class INode(ABC):
    data: Any = None
    _next: "INode" = None

    @property
    @abstractmethod
    def next_node(self) -> "INode":
        ...

    @abstractmethod
    def set_next_node(self, next_node: "INode"):
        ...


class Node(INode):
    def __init__(self, data: Any = None):
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


class LinkedList:
    def __init__(self, head: Any = None, node_type: INode = Node):
        if not issubclass(node_type, INode):
            raise TypeError(f"Invalid node type ({type(node_type)}).")
        self._i = None
        self._node_type = node_type
        if isinstance(head, Iterable):
            self.head = None
            self._add_from_iterable(head)
        elif isinstance(head, INode) or head == None:
            self.head = head
        elif head:
            self.head = node_type(head)
    
    @property
    def size(self):
        current = self.head
        count = 0
        while current:
            count += 1
            current = current.next_node
        return count
    
    @property
    def tail(self):
        current = self.head
        tail = current
        while current:
            tail = current
            current = current.next_node
        return tail
    
    def is_empty(self):
        return self.head == None
    
    def count(self, item) -> int:
        current = self.head
        count = 0
        while current:
            if current.data == item:
                count += 1
            current = current.next_node
        return count
    
    def _create_new_node(self, item: Any) -> INode:
        new_node_data = item.data if isinstance(item, INode) else item
        return self._node_type(new_node_data)
    
    def append(self, new_item: Any) -> None:
        new_node = self._create_new_node(new_item)
        if self.is_empty():
            self.head = new_node
        else:
            self.tail.set_next_node(new_node)

    def prepend(self, new_item: Any) -> None:
        new_node = self._create_new_node(new_item)
        new_node.set_next_node(self.head)
        self.head = new_node
    
    def insert(self, new_item: Any, index = 0) -> None:
        if not isinstance(index, int) or isinstance(index, bool):
            raise TypeError(
                f"Index type should be an int, not {type(index).__name__}."
            )
        if index < 0:
            raise NotImplementedError(
                f"Negative sequence indexes are not yet implemented.")
        if index > self.size:
            raise IndexError(f"Sequence index {index} out of range.")
        if index == 0:
            self.prepend(new_item)
        else:
            new_node = self._create_new_node(new_item)
            node_before = self[index-1]
            new_node.set_next_node(node_before.next_node)
            node_before.set_next_node(new_node)

    def search(self, item: Any) -> Union[int, None]:
        current = self.head
        index = 0
        while current:
            if current.data == item:
                return index 
            current = current.next_node
            index += 1
        return None

    def pop(self) -> Union[Node, None]:
        item = None
        if not self.is_empty():
            n = self.size
            if n > 1:
                new_tail = self[n-2]
                item = new_tail.next_node
                new_tail.set_next_node(None)
            else:
                item, self.head = self.head, None
        return item
    
    def remove(self, item: Any) -> int:
        current = self.head
        count = 0
        while self.head and current:
            if self.head.data == item:
                self.head = self.head.next_node
                count += 1
            else:
                previous = self.head 
                current = self.head.next_node
                while current:
                    if current.data == item:
                        previous.set_next_node(current.next_node)
                        current = current.next_node
                        count += 1
                    else:
                        previous = current
                        current = current.next_node
        return count
    
    def copy(self, _from=0, _until=None) -> "LinkedList":
        new_list = LinkedList()
        if not self.is_empty():
            until = self.size-1 if _until == None else _until
            current = self[_from]
            count = _from
            while current and count <= until:
                new_list.append(current)
                current = current.next_node
                count += 1
        return new_list
        
    def clear(self) -> None:
        while self.head:
            self.head = self.head.next_node
    
    def split(self, index=None) -> tuple["LinkedList", "LinkedList"]:
        n = self.size
        if n < 2:
            left_half, right_half = self, LinkedList()
        else:
            mid = n // 2 if not index else index
            left_half, right_half = self.copy(_until=mid-1), self.copy(mid)
        return left_half, right_half

    def sort(self) -> "LinkedList":
        n = self.size
        if n < 2:
            return self
        elif n == 2:
            if self.head > self.head.next_node:
                a, b = self.head.next_node.data, self.head.data
                self.head.data, self.head.next_node.data = a, b
            return self
        else:
            left_half, right_half = self.split()
            list_A, list_B = left_half.sort(), right_half.sort()
            if list_A.tail < list_B.head:
                new_list = list_A + list_B
            else:
                new_list = LinkedList()
                current_A, current_B = list_A.head, list_B.head
                while current_A and current_B:
                    if current_A <= current_B:
                        new_list.append(current_A)
                        current_A = current_A.next_node
                    else:
                        new_list.append(current_B)
                        current_B = current_B.next_node
                while current_A:
                    new_list.append(current_A)
                    current_A = current_A.next_node
                while current_B:
                    new_list.append(current_B)
                    current_B = current_B.next_node
            self.clear()
            current = new_list.head
            while current:
                self.append(current)
                current = current.next_node
            del new_list
            return self

    def _add_from_iterable(self, other):
        for i in other:
            self.append(i)
    
    def _add(self, other: Any):
        if isinstance(other, LinkedList):
            current = other.head
            while current:
                self.append(current.data)
                current = current.next_node
        elif isinstance(other, Iterable):
            self._add_from_iterable(other)
        else:
            self.append(other)
        return self
    
    def __add__(self, other: Any):
        return self.copy()._add(other)

    def __iadd__(self, other: Any):
        return self._add(other)

    def __len__(self) -> int:
        return self.size
    
    def _get_item(self, index: int, start_node: INode = None) -> INode:
        if self.is_empty():
            raise IndexError("Cannot get an item from an empty list.")
        if index >= len(self):
            raise IndexError(f"Sequence index {index} out of range.")
        if index < 0:
            raise ValueError("Index cannot be negative.")
        current = start_node if start_node else self.head
        count = 0
        while count < index:
            count += 1
            current = current.next_node
        return current

    def __getitem__(self, index: Union[int, slice]):
        if not isinstance(index, (int, slice)):
            raise TypeError(
                f"Index should be an int or a slice object, not {type(index)}."
            )
        if isinstance(index, int):
            return self._get_item(index)
        elif isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            current = self._get_item(start)
            new_list = LinkedList(self._create_new_node(current))
            count = start + step
            while count < stop:
                count += step
                current = self._get_item(step, current)
                new_list.append(self._create_new_node(current))
            return new_list
    
    def _generator(self):
        current = self.head
        while current:
            yield current
            current = current.next_node
        self._i = None
    
    def __iter__(self):
        return self._generator()

    def __next__(self):
        if not self._i:
            self._i = self._generator()
        return next(self._i)

    def __repr__(self):
        nodes = []
        current = self.head
        while current:
            nodes.append(f"{current.data}")
            current = current.next_node
        return " -> ".join(nodes)


if __name__ == "__main__":
    from random import randint
    l1 = LinkedList()
    l2 = LinkedList([randint(0, 100) for i in range(20)])
    l3 = LinkedList([randint(0, 1000) for i in range(100)])
    g = (i for i in range(10))
