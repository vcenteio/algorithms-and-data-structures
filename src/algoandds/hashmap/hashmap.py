﻿from typing import Callable, Hashable, Type, Union, Iterable, Tuple, Dict, List
from hashlib import sha1

from ..linkedlist import LinkedList
from ..tools.tools import get_class_name


class HashMap:
    _DEFAULT_MAP_SIZE = 10
    _DEFAULT_LOAD_FACTOR = 0.75

    def __init__(
        self,
        _iter: Union[Tuple, Dict, List] = None,
        map_size: int = 10,
        load_factor: float = 0.75,
    ):
        self._set_load_factor(load_factor)
        self._set_initial_map_size(map_size, len(_iter) if _iter else 0)
        self._create_new_list(map_size, _iter)

    @property
    def _size(self) -> int:
        return sum([1 for item in self._list if item is not None])

    @property
    def _capacity(self) -> int:
        return len(self._list)

    @property
    def _load(self) -> float:
        return self._size / self._capacity

    def _enforce_valid_hash_ceiling(self, ceiling: int):
        if not isinstance(ceiling, int) or isinstance(ceiling, bool):
            raise TypeError("Hash ceiling hash to be an int.")
        if ceiling != self._capacity:
            raise ValueError("Invalid hash ceiling value.")
        
    def _set_hash_ceiling(self, ceiling: int):
        self._enforce_valid_hash_ceiling(ceiling)
        self._hash_ceiling = ceiling

    def _enforce_valid_load_factor(self, load_factor: float):
        if not isinstance(load_factor, float):
            raise TypeError(
                f"Inappropriate type '{get_class_name(load_factor)}' "
                "for load factor. Should be 'float'."
            )
        if load_factor < 0.75 or load_factor > 0.95:
            raise ValueError(
                "Load factor value should be between 0.75 and 0.95 "
                "(both ends included)."
            )

    def _set_load_factor(self, load_factor: float):
        self._enforce_valid_load_factor(load_factor)
        self._load_factor = load_factor

    @staticmethod
    def _enforce_valid_number_of_new_items(n: int):
        if not isinstance(n, int) or isinstance(n, bool):
            raise TypeError(f"Inappropriate type '{get_class_name(n)}' "
                "for number of items. Should be 'int'."
                )
        if n < 0:
            raise ValueError(f"Number of new items should be >= 0.")

    def _get_size_with_load_margin(self, n: int) -> int:
        self._enforce_valid_load_factor(self._load_factor)
        self._enforce_valid_number_of_new_items(n)
        margin_ratio = 1 - self._load_factor
        return n + int(margin_ratio * n)

    def _enforce_valid_map_size(self, map_size: int):
        if not isinstance(map_size, int) or isinstance(map_size, bool):
            raise TypeError(
                f"Inappropriate type '{get_class_name(map_size)}' "
                "for map size. Should be 'int'."
            )
        if map_size < (DMS := self._DEFAULT_MAP_SIZE):
            raise ValueError(f"Map size cannot be smaller than {DMS}.")

    def _set_initial_map_size(self, map_size: int, number_of_new_items: int):
        self._enforce_valid_map_size(map_size)
        n = number_of_new_items if number_of_new_items > map_size else map_size
        self._INITIAL_MAP_SIZE = self._get_size_with_load_margin(n)

    def _reset_list(self, map_size: int = None):
        if map_size is not None:
            self._enforce_valid_map_size(map_size)
            n = map_size
        else:
            n = self._INITIAL_MAP_SIZE
        self._list = [None for _ in range(n)]
        self._set_hash_ceiling(n)

    def _create_new_list(
        self, map_size: int, _iter: Union[Tuple, List, Dict] = None
    ):
        if _iter is None:
            self._reset_list(map_size)
        elif isinstance(_iter, Iterable):
            iter_length = len(_iter)
            n = map_size if map_size > iter_length else iter_length 
            self._reset_list(n)
            self.update(_iter)

        else:
            raise TypeError("Non-iterable object passed at HashMap creation.")

    def _calculate_new_map_size(self, number_of_new_items: int) -> int:
        n = number_of_new_items
        doublecap = self._capacity * 2
        size_with_margin = self._get_size_with_load_margin(n)
        return doublecap if doublecap > size_with_margin else size_with_margin

    def _resize_list(self, number_of_new_items: int):
        new_map_size = self._calculate_new_map_size(number_of_new_items)
        self._hash_ceiling = new_map_size
        self._create_new_list(new_map_size, self.items())

    def _is_resize_needed(self, number_of_new_items: int):
        new_size = self._size + number_of_new_items
        new_load = new_size / self._capacity
        return new_load >= self._load_factor

    def _manage_current_load(self, number_of_new_items: int = 1):
        n = number_of_new_items
        if self._is_resize_needed(n):
            self._resize_list(n)

    @staticmethod
    def _is_valid_tuple(t: tuple):
        return len(t) == 2

    def _add_from_tuple(self, t: Tuple):
        if not isinstance(t, Tuple):
            raise TypeError(
                "Requested update from tuple with non-tuple type object."
            )
        if self._is_valid_tuple(t):
            self._manage_current_load()
            key, value = t
            self[key] = value
        else:
            raise ValueError("Tuple should have a length of 2.")

    def _add_from_dict(self, d: Dict):
        if not isinstance(d, Dict):
            raise TypeError(
                "Requested update from dict with non-dict type object."
            )
        self._manage_current_load(len(d))
        for key in d:
            self[key] = d[key]

    @staticmethod
    def _is_valid_list(l: List) -> bool:
        try:
            [(key, value) for (key, value) in l]
            return True
        except (TypeError, ValueError):
            return False

    def _add_from_list(self, l: List):
        if not isinstance(l, List):
            raise TypeError(
                "Requested update from list with non-list type object."
            )
        if self._is_valid_list(l):
            self._manage_current_load(len(l))
            for (key, value) in l:
                self[key] = value
        else:
            raise ValueError("List items should be key-value pair iterables.")

    def update(self, _iterable: Union[Tuple, Dict, List]):
        """Updates hashmap from dict/iterable.

        Item should be a tuple with a key-value pair,
        a list of tuples with key-value pairs
        or a dict.
        """
        if not isinstance(_iterable, Iterable):
            raise TypeError(
                "Item should be a tuple with a key-value pair, "
                "a list of tuples with key-value pairs "
                "or a dict."
            )
        if isinstance(_iterable, Tuple):
            self._add_from_tuple(_iterable)
        elif isinstance(_iterable, Dict):
            self._add_from_dict(_iterable)
        elif isinstance(_iterable, List):
            self._add_from_list(_iterable)
        else:
            raise TypeError(
                f"Iterables of type {get_class_name(_iterable)} "
                "are not supported."
            )

    def setdefault(self, key, default=None):
        """Insert key with the value of default if
        the key is not in the hashmap.

        Returns the value for key if the latter exists
        in the hashmap.
        """
        if key not in self.keys():
            self.update((key, default))
            return default
        else:
            return self[key]

    def items(self) -> Dict:
        """Returns a dictionary with all the key-value pairs of the hashmap."""
        return {key: value for key, value in self}

    def keys(self) -> Tuple:
        """Returns a tuple with all the keys of the hashmap."""
        return tuple((key for key, _ in self))

    def values(self) -> Tuple:
        """Returns a tuple with all the values of the hashmap."""
        return tuple((value for _, value in self))

    def get(self, key, default=None):
        """Returns the value for key if the latter exists in the hashmap,
        else default.
        """
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key, default=None):
        """Removes the specified key from the hashmap
        and returns the associated value.

        If key does not exists in the hashmap,
        returns default value if one was given,
        otherwise KeyError is raised.
        """
        item_to_pop = self.get(key)
        if item_to_pop is not None:
            del self[key]
            return item_to_pop
        else:
            if default is not None:
                return default
            else:
                raise KeyError("Mapping key not found.")

    def clear(self):
        """Removes all items from the hashmap."""
        self._reset_list()

    @staticmethod
    def _salt(key) -> int:
        encoded_key = key.encode() if isinstance(key, str) else bytes(key)
        return sum(sha1(encoded_key, usedforsecurity=True).digest())

    def _prehash(self, key):
        return abs(hash(key) + self._salt(key))

    def _hash(self, key) -> int:
        # Although a tuple can be hashable if its values are hashable,
        # in this specification I want to prevent users from using
        # tuples for the keys. It may be reconsidered in the future.
        if not isinstance(key, Hashable) or isinstance(key, tuple):
            raise TypeError(
                f"Key be {get_class_name(key)} type. "
                "Must be hashable and cannot be a tuple or NoneType."
            )
        # Since None is always hashable, for the sake of correctness,
        # I consider it a ValueError.
        if key is None:
            raise ValueError(f"Key cannot be {get_class_name(key)}.")
        return self._prehash(key) % self._hash_ceiling

    def __getitem__(self, key):
        bucket = self._list[self._hash(key)]
        if bucket is None:
            raise KeyError("Mapping key not found.")
        if isinstance(bucket, tuple):
            if bucket[0] == key:
                return bucket[1]
            raise KeyError("Mapping key not found.")
        if isinstance(bucket, LinkedList):
            for existing_key, value in bucket:
                if existing_key == key:
                    return value
            raise KeyError("Mapping key not found.")

    @staticmethod
    def _is_empty_bucket(bucket) -> bool:
        return bucket is None

    @staticmethod
    def _get_from_linked_list(key, linked_list):
        index = 0
        for existing_key, _ in linked_list:
            if existing_key == key:
                return index
            index += 1
        return None

    def __setitem__(self, key, value):
        hash_code = self._hash(key)
        bucket = self._list[hash_code]
        new_bucket = (key, value)
        if self._is_empty_bucket(bucket):
            self._list[hash_code] = new_bucket
        elif isinstance(bucket, tuple):
            if bucket[0] == key:
                self._list[hash_code] = new_bucket
            else:
                new_bucket = (key, value)
                self._list[hash_code] = LinkedList([bucket, new_bucket])
        elif isinstance(bucket, LinkedList):
            index = self._get_from_linked_list(key, bucket)
            bucket: LinkedList
            if index is not None:
                bucket[index] = new_bucket
            else:
                bucket.append(new_bucket)

    def __delitem__(self, key):
        hash_code = self._hash(key)
        bucket = self._list[hash_code]
        if bucket is None:
            raise KeyError("Mapping key not found.")
        if isinstance(bucket, tuple):
            _, self._list[hash_code] = bucket, None
            del _
        elif isinstance(bucket, LinkedList):
            bucket: LinkedList
            index = self._get_from_linked_list(key, bucket)
            if index is None:
                raise KeyError("Mapping key not found.")
            else:
                _ = bucket.pop(index)
                del _

    def __iter__(self):
        for bucket in self._list:
            if isinstance(bucket, LinkedList):
                for node in bucket:
                    yield node
            elif isinstance(bucket, Tuple):
                yield bucket

    def __contains__(self, key) -> bool:
        for existing_key, _ in self:
            if existing_key == key:
                return True
        return False

    def _ensure_its_a_hashmap(  # type: ignore
        func: Callable[["HashMap", "HashMap"], bool]
    ):
        def wrapper(self, other):
            if not isinstance(other, HashMap):
                raise TypeError(
                    "Cannot compare HashMap with object of another type "
                    f"({get_class_name(other)})."
                )
            return func(self, other)

        return wrapper

    @_ensure_its_a_hashmap
    def __eq__(self, other: "HashMap") -> bool:
        return self.items() == other.items()

    @_ensure_its_a_hashmap
    def __ne__(self, other: "HashMap") -> bool:
        return self.items() != other.items()

    def __len__(self) -> int:
        return sum((1 for _ in self))

    def __repr__(self) -> str:
        return f"<HashMap: {self._list}>"

    def __str__(self) -> str:
        return str(self.items())