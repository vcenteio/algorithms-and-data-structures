import sys
from typing import Any, Union, Tuple, overload
from collections.abc import MutableSequence, Iterable

from .node import INode, Node
from ..tools.tools import get_class_name


class LinkedList(MutableSequence):
    head: Union[INode, None]

    def __init__(self, head: Any = None, node_type=Node):
        self._set_node_type(node_type)
        self._i = None
        if isinstance(head, INode) or head is None:
            self.head = head
        elif isinstance(head, Iterable) and not isinstance(head, (str, bytes)):
            self.head = None
            self._add_from_iterable(head)
        elif head:
            self.head = node_type(head)

    def _set_node_type(self, node_type) -> None:
        if not issubclass(node_type, INode):
            raise TypeError(f"Invalid node type ({type(node_type)}).")
        self._node_type = node_type

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
        tail = current = self.head
        while current:
            tail = current
            current = current.next_node
        return tail

    def is_empty(self):
        return self.head is None

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

    def insert(self, index: int, value: Any) -> None:
        if not isinstance(index, int) or isinstance(index, bool):
            raise TypeError(
                f"Index type should be an int, not {type(index).__name__}."
            )
        if index < 0:
            raise NotImplementedError(
                "Negative sequence indexes are not yet implemented.")
        if index > self.size:
            raise IndexError(f"Sequence index {index} out of range.")
        if index == 0:
            self.prepend(value)
        else:
            new_node = self._create_new_node(value)
            node_before = self[index-1]
            new_node.set_next_node(node_before.next_node)
            node_before.set_next_node(new_node)

    def extend(self, values) -> None:
        self += values

    def search(self, item: Any) -> Union[int, None]:
        current = self.head
        index = 0
        while current:
            if current.data == item:
                return index
            current = current.next_node
            index += 1
        return None

    def index(self, value: Any, start=0, stop=sys.maxsize) -> int:
        index = self.search(value)
        if index is None or index < start or index > stop:
            raise ValueError(f"{value} is not in linked list.")
        return index

    def _pop_head(self):
        item_to_remove = self.head
        self.head = self.head.next_node
        return item_to_remove

    def _remove_by_index(self, index: int):
        if not isinstance(index, int):
            raise TypeError(
                f"Index must be an int, not {get_class_name(index)}"
            )
        item_to_remove = self.__getitem__(index)
        previous = self.__getitem__(index-1)
        previous.set_next_node(item_to_remove.next_node)
        return item_to_remove

    def pop(self, index: int = None) -> Union[Node, None]:
        if self.is_empty():
            raise IndexError("Empty list.")
        if index is None:
            index = self.size-1
        if index == 0 or index + self.size == 0:
            item_to_remove = self._pop_head()
        else:
            item_to_remove = self._remove_by_index(index)
        return item_to_remove

    def remove(self, item: Any) -> None:
        current = self.head
        while self.head and current:
            if self.head.data == item:
                self.head = self.head.next_node
            else:
                previous = self.head
                current = self.head.next_node
                while current:
                    if current.data == item:
                        previous.set_next_node(current.next_node)
                        current = current.next_node
                    else:
                        previous = current
                        current = current.next_node

    def copy(self, _from=0, _until=None) -> "LinkedList":
        new_list = LinkedList()
        if not self.is_empty():
            until = self.size-1 if _until is None else _until
            current = self[_from]
            count = _from
            while current and count <= until:
                new_list.append(current)
                current = current.next_node
                count += 1
        return new_list

    def reverse(self):
        new_list = LinkedList()
        current = self.head
        while current:
            new_list.prepend(current)
            current = current.next_node
        return new_list

    def clear(self) -> None:
        while self.head:
            self.head = self.head.next_node

    def split(self, index=None) -> Tuple["LinkedList", "LinkedList"]:
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
        elif n == 2 and self.head is not None:
            if self.head > self.head._next and self.head._next is not None:
                a, b = self.head._next.data, self.head.data
                self.head.data, self.head._next.data = a, b
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
                        current_A = current_A._next
                    else:
                        new_list.append(current_B)
                        current_B = current_B._next
                while current_A:
                    new_list.append(current_A)
                    current_A = current_A._next
                while current_B:
                    new_list.append(current_B)
                    current_B = current_B._next
            self.clear()
            current = new_list.head
            while current:
                self.append(current)
                current = current._next
            del new_list
            return self

    @staticmethod
    def _is_valid_iterable(itr: Any) -> bool:
        return isinstance(itr, Iterable) and not isinstance(itr, (str, bytes))

    def _add_from_iterable(self, other: Iterable):
        if self._is_valid_iterable(other):
            for i in other:
                self.append(i)

    def _add_item(self, other: Any):
        if self._is_valid_iterable(other):
            self._add_from_iterable(other)
        else:
            self.append(other)
        return self

    def __add__(self, other: Any):
        return self.copy()._add_item(other)

    def __radd__(self, other: Any):
        return self.copy()._add_item(other)

    def __iadd__(self, other: Any):
        return self._add_item(other)

    def _multiply(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                "Can't multiply sequence "
                f"by non-int of type '{get_class_name(value)}'"
            )
        if value < 0:
            raise ValueError(
                "Multiplication of linked lists "
                "by negative numbers is not suported."
            )
        if value == 0:
            self.clear()
            return self
        if value == 1:
            return self
        count = 1
        copy = self.copy()
        while count < value:
            self += copy
            count += 1
        return self

    def __mul__(self, other: int):
        return self.copy()._multiply(other)

    def __rmul__(self, other: int):
        return self.copy()._multiply(other)

    def __imul__(self, other: int):
        return self._multiply(other)

    def __len__(self) -> int:
        return self.size

    def __bool__(self) -> bool:
        return self.size != 0

    def _get_item(self, index: int, start_node: INode = None):
        if self.is_empty():
            raise IndexError("Cannot get item from empty list.")
        n = self.size
        # index + n is considered to accomodate for
        # negative index values.
        if index >= n or index + n < 0:
            raise IndexError(f"Sequence index {index} out of range.")
        if index < 0:
            index += n
        current = start_node if start_node else self.head
        count = 0
        while count < index and current is not None:
            count += 1
            current = current.next_node
        return current

    def __getitem__(self, index: Union[int, slice]):
        if isinstance(index, int) and not isinstance(index, bool):
            return self._get_item(index)
        elif isinstance(index, slice):
            start, stop, step = index.indices(self.size)
            if step < 1:
                raise ValueError("Step value must be >= 1.")
            current = self._get_item(start)
            new_list = LinkedList(self._create_new_node(current))
            count = start + step
            while count < stop:
                count += step
                current = self._get_item(step, current)
                new_list.append(self._create_new_node(current))
            return new_list
        else:
            raise TypeError(
                "Index should be an int or a slice object, "
                f"not {get_class_name(index)}."
            )

    @overload
    def __setitem__(self, index: int, value: Any) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[Any]) -> None:
        ...

    def __setitem__(self, index, value) -> None:
        if isinstance(index, int):
            item = self.__getitem__(index)
            item.data = value
        elif isinstance(index, slice):
            if not isinstance(value, Iterable):
                raise TypeError("Can only assign an iterable.")
            start, stop, step = index.indices(self.size)
            if step < 0:
                raise NotImplementedError(
                    "Negative sequence indexes are not yet implemented."
                )
            if step == 1:
                i = start
                while i < stop:
                    self.pop(start)
                    i += 1
                i = start
                for item in value:
                    self.insert(i, item)
                    i += 1
            else:
                len_of_current_items = len(self[index])
                len_of_new_items = len(value)  # type: ignore[arg-type]
                if len_of_current_items != len_of_new_items:
                    raise ValueError(
                        "Attempt to assign sequence of size "
                        f"{len_of_new_items} "
                        f"to extended slice of size {len_of_current_items}."
                    )
                i = start
                for item in value:
                    self[i] = item
                    i += step
        else:
            raise TypeError(
                f"Wrong type for index: {get_class_name(index)}."
            )

    def _get_indices_from_slice(self, sl: slice):
        start, stop, step = sl.indices(len(self))
        if step < 0:
            raise NotImplementedError(
                "Negative sequence indexes are not yet implemented."
            )
        return tuple(range(start, stop, step))

    def __delitem__(self, index: Union[int, slice]) -> None:
        if isinstance(index, int):
            self.pop(index)
        elif isinstance(index, slice):
            indices = self._get_indices_from_slice(index)
            print("DEBUG indices:", indices)
            counter = 0
            for i in indices:
                i -= counter
                self.pop(i)
                counter += 1
        else:
            raise TypeError(
                f"Wrong type for index: {get_class_name(index)}."
            )

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

    def __contains__(self, item: Any) -> bool:
        return self.search(item) is not None

    def __repr__(self):
        nodes = []
        current = self.head
        while current:
            nodes.append(f"{current.data}")
            current = current.next_node
        return " -> ".join(nodes)


# for manual testing purposes
if __name__ == "__main__":
    from random import randint
    l1 = LinkedList([0, 1, 2])
    l2 = LinkedList([randint(0, 100) for i in range(20)])
    l3 = LinkedList([randint(0, 1000) for i in range(100)])
    g = (i for i in range(10))
