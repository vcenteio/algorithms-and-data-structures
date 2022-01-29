import sys
from typing import Any, Union, Tuple, Optional
from collections.abc import MutableSequence, Iterable

from .node import INode, Node
from ..tools.tools import get_class_name


MAXSIZE = sys.maxsize


class LinkedList(MutableSequence):
    head: Optional[INode]

    def __init__(self, head: Any = None, node_type=Node):
        self._set_node_type(node_type)
        self._i = None
        self.head = None
        if isinstance(head, INode) or head is None:
            self.head = head
        elif self._is_valid_iterable(head):
            self._add_from_iterable(head)
        else:
            self.head = node_type(head)

    @staticmethod
    def _is_valid_node_type(node_type) -> bool:
        return issubclass(node_type, INode) and node_type is not INode

    def _set_node_type(self, node_type) -> None:
        if not self._is_valid_node_type(node_type):
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

    def count(self, value: Any) -> int:
        """Return the number of occurrences of value."""
        current = self.head
        count = 0
        while current:
            if current.data == value:
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
        if not self._is_valid_int(index):
            raise TypeError(
                f"Index type should be an int, not {type(index).__name__}."
            )
        if abs(index) > self.size:
            raise IndexError(f"Sequence index {index} out of range.")
        index = index + self.size if index < 0 else index
        if index == 0:
            self.prepend(value)
        else:
            new_node = self._create_new_node(value)
            node_before = self[index - 1]
            new_node.set_next_node(node_before.next_node)
            node_before.set_next_node(new_node)

    def extend(self, values) -> None:
        self += values

    def _convert_indices(
        self, start: int, stop: int, step: Optional[int] = None
    ) -> Tuple[int, int, int]:
        return slice(start, stop, step).indices(self.size)

    def _get_index(self, item: Any) -> Union[int, None]:
        current = self.head
        index = 0
        while current:
            if current.data == item:
                return index
            current = current.next_node
            index += 1
        return None

    def index(self, value: Any, start: int = 0, stop: int = MAXSIZE) -> int:
        if not self._is_valid_int(start) or not self._is_valid_int(stop):
            raise TypeError("Start and stop values must be integers.")
        start, stop, _ = self._convert_indices(start, stop)
        index = self._get_index(value)
        if index is None or index < start or index >= stop:
            raise ValueError(f"{value} is not in linked list.")
        return index

    def _pop_head(self) -> INode:
        if self.head is None:
            raise IndexError("pop from empty list")
        item_to_remove = self.head
        self.head = self.head.next_node
        return item_to_remove

    def _pop_at_index(self, index: int) -> INode:
        item_to_remove = self[index]
        previous_item = self[index - 1]
        previous_item.set_next_node(item_to_remove.next_node)
        return item_to_remove

    def _is_head_index(self, index: int) -> bool:
        return index == 0 or index + self.size == 0

    def pop(self, index: int = None) -> INode:
        if self.is_empty():
            raise IndexError("pop from empty list")
        if not self._is_valid_int(index) and index is not None:
            raise TypeError(
                f"index must be an int, not {get_class_name(index)}"
            )
        i = self.size - 1 if index is None else index
        if not self._is_head_index(i):
            item = self._pop_at_index(i)
        else:
            item = self._pop_head()
        return item

    def remove(self, value: Any) -> None:
        """Removes first occurrence of value.

        Raises ValueError if value is not in the list.
        """
        if self.head is not None:
            if self.head.data == value:
                self._pop_head()
                return
            current = self.head.next_node
            previous = self.head
            while current:
                if current.data == value:
                    previous.set_next_node(current.next_node)
                    return
                else:
                    previous = current
                    current = current.next_node
        raise ValueError("value not in list")

    def remove_all(self, value: Any) -> None:
        """Removes all occurrences of value.

        Raises ValueError if value is not in the list.
        """
        try:
            removed_items = 0
            while True:
                self.remove(value)
                removed_items += 1
        except ValueError:
            if removed_items == 0:
                raise ValueError("value not in list")

    @staticmethod
    def _is_valid_int(value) -> bool:
        return isinstance(value, int) and not isinstance(value, bool)

    def copy(
        self, _from: int = 0, _until: Optional[int] = None
    ) -> "LinkedList":
        if not self._is_valid_int(_from):
            raise TypeError(
                f"Wrong type {get_class_name(_from)} for _from parameter."
            )
        if not self._is_valid_int(_until) and _until is not None:
            raise TypeError(
                f"Wrong type {get_class_name(_until)} for _until parameter."
            )
        new_list = LinkedList()
        if self.is_empty():
            return new_list
        start = _from
        stop = self.size if _until is None else _until
        count, until, _ = self._convert_indices(start, stop)
        current = self[count]
        while current and count < until:
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
        self.head = None

    def split(self, index=None) -> Tuple["LinkedList", "LinkedList"]:
        n = self.size
        if n < 2:
            left_half, right_half = self, LinkedList()
        else:
            mid = n // 2 if index is None else index
            left_half, right_half = self.copy(_until=mid), self.copy(mid)
        return left_half, right_half

    def _append_left_over_items(self, currentA, currentB) -> None:
        while currentA:
            self.append(currentA)
            currentA = currentA._next
        while currentB:
            self.append(currentB)
            currentB = currentB._next

    @staticmethod
    def _merge_sorted_lists_into_sorted_list(
        listA: "LinkedList", listB: "LinkedList"
    ) -> "LinkedList":
        if listA.tail < listB.head:
            listA.tail.set_next_node(listB.head)
            sorted_list = LinkedList(listA.head)
        else:
            sorted_list = LinkedList()
            current_A, current_B = listA.head, listB.head
            while current_A and current_B:
                if current_A <= current_B:
                    sorted_list.append(current_A)
                    current_A = current_A._next
                else:
                    sorted_list.append(current_B)
                    current_B = current_B._next
            sorted_list._append_left_over_items(current_A, current_B)
        return sorted_list

    def sort(self) -> None:
        n = self.size
        if n < 2:
            return
        elif n == 2 and self.head is not None:
            if self.head > self.head._next and self.head._next is not None:
                a, b = self.head._next.data, self.head.data
                self.head.data, self.head._next.data = a, b
        else:
            listA, listB = self.split()
            listA.sort()
            listB.sort()
            new_list = self._merge_sorted_lists_into_sorted_list(listA, listB)
            self.head = new_list.head

    @staticmethod
    def _is_valid_iterable(itr: Any) -> bool:
        return isinstance(itr, Iterable) and not isinstance(itr, (str, bytes))

    def _add_from_iterable(self, itr: Iterable):
        if self._is_valid_iterable(itr):
            for i in itr:
                self.append(i)
        else:
            raise TypeError(
                f"Invalid item of type {get_class_name(itr)}"
                "passed as argument."
            )

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

    @staticmethod
    def _is_index_outside_range(index: int, max: int) -> bool:
        # index + n is considered to accomodate for
        # negative index values.
        return index >= max or index + max < 0

    def _get_item_from_index(self, index: int, start_node: INode = None):
        if self.is_empty():
            raise IndexError("get item from empty list")
        n = self.size
        if self._is_index_outside_range(index, n):
            raise IndexError(f"Sequence index {index} out of range.")
        if index < 0:
            index += n
        current = start_node if start_node is not None else self.head
        count = 0
        while count < index and current is not None:
            count += 1
            current = current.next_node
        return current

    def _get_list_from_slice(self, slice: slice):
        if self.is_empty():
            raise IndexError("get item from empty list")
        start, stop, step = slice.indices(self.size)
        if step < 1:
            raise ValueError("Step value must be >= 1.")
        new_list = LinkedList()
        if start < stop:
            current = self._get_item_from_index(start)
            new_list.append(current)
            count = start + step
            while count < stop:
                count += step
                current = self._get_item_from_index(step, current)
                new_list.append(current)
        return new_list

    def __getitem__(self, index: Union[int, slice]):
        if self._is_valid_int(index):
            return self._get_item_from_index(index)  # type: ignore[arg-type]
        elif isinstance(index, slice):
            return self._get_list_from_slice(index)
        else:
            raise TypeError(
                "index should be an int or a slice object, "
                f"not {get_class_name(index)}"
            )

    def _setitem_from_slice_multistep(
        self, _iter: Iterable, _slice: slice
    ) -> None:
        start, stop, step = _slice.indices(self.size)
        len_of_current_slice = len(range(start, stop, step))
        len_of_new_slice = len(_iter)  # type: ignore[arg-type]
        if len_of_current_slice != len_of_new_slice:
            raise ValueError(
                "attempt to assign sequence of size "
                f"{len_of_new_slice} "
                f"to extended slice of size {len_of_current_slice}"
            )
        i = start
        for item in _iter:
            self[i] = item
            i += step

    def _setitem_from_slice_single_step(
        self, _iter: Iterable, start: int, stop: int
    ) -> None:
        i = start
        while i < stop:
            self.pop(start)
            i += 1
        i = start
        for item in _iter:
            self.insert(i, item)
            i += 1

    def _setitem_from_slice(self, _slice: slice, _iter: Iterable) -> None:
        if not isinstance(_iter, Iterable):
            raise TypeError("can only assign an iterable")
        start, stop, step = _slice.indices(self.size)
        if step < 0:
            raise NotImplementedError(
                "negative sequence slices are not implemented"
            )
        if step == 1:
            self._setitem_from_slice_single_step(_iter, start, stop)
        else:
            self._setitem_from_slice_multistep(_iter, _slice)

    def _setitem_from_int(self, index: int, value: Any) -> None:
        item = self.__getitem__(index)
        item.data = value

    def __setitem__(
        self, index: Union[int, slice], value: Union[Any, Iterable[Any]]
    ) -> None:
        if isinstance(index, int):
            self._setitem_from_int(index, value)
        elif isinstance(index, slice):
            self._setitem_from_slice(index, value)
        else:
            raise TypeError(f"wrong type for index: {get_class_name(index)}")

    def _get_range_from_slice(self, _slice: slice) -> range:
        start, stop, step = _slice.indices(len(self))
        if step < 0:
            raise NotImplementedError(
                "negative sequence indexes are not implemented"
            )
        return range(start, stop, step)

    def __delitem__(self, index: Union[int, slice]) -> None:
        if isinstance(index, int):
            self.pop(index)
        elif isinstance(index, slice):
            indices_range = self._get_range_from_slice(index)
            number_of_poped_items = 0
            for i in indices_range:
                i -= number_of_poped_items
                self.pop(i)
                number_of_poped_items += 1
        else:
            raise TypeError(f"wrong type for index: {get_class_name(index)}")

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
        return self._get_index(item) is not None

    def __eq__(self, other) -> bool:
        if not isinstance(other, LinkedList):
            return False
        n = self.size
        if n != other.size:
            return False
        for i in range(n):
            if self[i] != other[i]:
                return False
        return True

    def _get_str_with_nodes_and_separator(self, _repr=False) -> str:
        str_nodes = map(str if not _repr else repr, self)  # type: ignore
        sep = " -> "
        return sep.join(str_nodes)

    def __repr__(self) -> str:
        return f"LinkedList({self._get_str_with_nodes_and_separator(True)})"
