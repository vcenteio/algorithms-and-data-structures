from typing import Hashable, Union, Iterable
from linked_list import LinkedList
from tools import get_class_name


class HashMap:
    _DEFAULT_MAP_SIZE = 10
    _DEFAULT_LOAD_FACTOR = 0.75
    
    def __init__(
            self, _iter: Iterable = None, map_size: int = 10,
            load_factor: float = 0.75
        ):
        self._set_load_factor(load_factor)
        self._set_initial_map_size(map_size, len(_iter) if _iter else 0)
        self._hash_ceiling = self._INITIAL_MAP_SIZE
        self._create_new_list(map_size, _iter)
    
    @property
    def _size(self):
        return sum([1 for item in self._list if item != None])

    @property
    def _capacity(self):
        return len(self._list) 

    @property
    def _load(self):
        return self._size / self._capacity

    def _set_load_factor(self, load_factor: float):
        if not isinstance(load_factor, float):
            raise TypeError(
                f"Inappropriate type '{get_class_name(load_factor)}' "\
                "for load factor. Should be 'float'."
            )
        if load_factor > 0.95 or load_factor < 0.05:
            raise ValueError(
                "Load factor value should be between 0.05 and 0.95 "\
                "(both ends included)."
            )
        self._load_factor = load_factor
    
    def _get_size_with_load_margin(self, n):
        margin_ratio = 1 - self._load_factor
        return n + int(margin_ratio * n)

    def _set_initial_map_size(self, map_size: int, number_of_new_items: int):
        if not isinstance(map_size, int) or isinstance(map_size, bool):
            raise TypeError(
                f"Inappropriate type '{get_class_name(map_size)}' "\
                "for map size. Should be 'int'."
            )
        if map_size < (dmz := self._DEFAULT_MAP_SIZE):
            raise ValueError(f"Map size cannot be smaller than {dmz}.")
        n = number_of_new_items
        if map_size < n:
            self._INITIAL_MAP_SIZE = self._get_size_with_load_margin(n)
        else:
            self._INITIAL_MAP_SIZE = self._get_size_with_load_margin(map_size)

    def _create_new_list(self, map_size: int, _iter: Iterable = None):
        self._list = [None for i in range(map_size)]
        self._hash_ceiling = map_size
        if not _iter:
            return
        elif isinstance(_iter, Iterable):
            self.update(_iter)
        else:
            raise TypeError("Non-iterable object passed at HashMap creation.")
    
    def _calculate_new_map_size(self, number_of_new_items: int):
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
        if self._is_resize_needed(n): self._resize_list(n)

    @staticmethod 
    def _is_valid_tuple(t: tuple):
        return len(t) == 2

    def _add_from_tuple(self, t: tuple):
        if self._is_valid_tuple(t):
            self._manage_current_load()
            key, value = t
            self[key] = value
        else:
            raise ValueError("Tuple should have a length of 2.")

    def _add_from_dict(self, d: dict):
        self._manage_current_load(len(d))
        for key in d:
            self[key] = d[key]
        
    @staticmethod
    def _is_valid_list(l: list):
        try:
            [(key, value) for (key, value) in l]
            return True
        except (TypeError, ValueError):
            return False

    def _add_from_list(self, l: list):
        if self._is_valid_list(l):
            self._manage_current_load(len(l))
            for (key, value) in l:
                self[key] = value
        else:
            raise ValueError(
                "List items should be key-value pair iterables."
            )

    def update(self, _iterable: Union[tuple, dict, list]):
        if not isinstance(_iterable, Iterable):
            raise TypeError(
                "Item should be a 2-item tuple, a list with 2-item "\
                "tuples or a dict."
            )
        if isinstance(_iterable, tuple):
            self._add_from_tuple(_iterable)
        elif isinstance(_iterable, dict):
            self._add_from_dict(_iterable)
        elif isinstance(_iterable, list):
            self._add_from_list(_iterable)
        else:
            raise TypeError(
                f"Iterables of type {get_class_name(_iterable)} "\
                "are not supported."
            )
    
    def setdefault(self, key, default=None):
        if key in self.keys():
            return self[key]
        else:
            self.update((key, default))
            return default
    
    def items(self):
        return {key:value for key, value in self}

    def keys(self):
        return tuple((key for key, _ in self))

    def values(self):
        return tuple((value for _, value in self))
    
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
    
    def pop(self, key, default=None):
        item_to_pop = self.get(key)
        if item_to_pop != None:
            del self[key] 
            return item_to_pop
        else:
            if default != None:
                return default
            else:
                raise KeyError("Mapping key not found.")

    def clear(self):
        del self._list
        self._create_new_list(self._INITIAL_MAP_SIZE)

    @staticmethod
    def _prehash(key):
        return abs(hash(key)) 

    def _hash(self, key):
        # Although a tuple can be hashable if its values are hashable,
        # in this specification I want to prevent users from using
        # tuples for the keys. It may be reconsidered in the future.
        if not isinstance(key, Hashable) or isinstance(key, tuple):
            raise TypeError(
                f"Key be {get_class_name(key)} type. "\
                "Must be hashable and cannot be a tuple or NoneType."
            )
        # Since None is always hashable, for the sake of correctness,
        # I consider it a ValueError.
        if key is None:
            raise ValueError(f"Key cannot be {get_class_name(key)}.")
        return self._prehash(key) % self._hash_ceiling

    def __getitem__(self, key):
        bucket = self._list[self._hash(key)]
        if bucket == None:
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
    def _is_empty_bucket(bucket):
        return bucket == None
    
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
            if index != None:
                bucket[index] = new_bucket
            else:
                bucket.append(new_bucket)
    
    def __delitem__(self, key):
        hash_code = self._hash(key)
        bucket = self._list[hash_code]
        if bucket == None:
            raise KeyError("Mapping key not found.")
        if isinstance(bucket, tuple):
            item_to_remove, self._list[hash_code] = bucket, None
            del item_to_remove
        elif isinstance(bucket, LinkedList):
            bucket: LinkedList
            index = self._get_from_linked_list(key, bucket)
            if index == None:
                raise KeyError("Mapping key not found.")
            else:
                item_to_remove = bucket.pop(index)
                del item_to_remove
    
    def __iter__(self):
        for bucket in self._list:
            if isinstance(bucket, LinkedList):
                for node in bucket:
                    yield node
            elif isinstance(bucket, tuple):
                yield bucket
    
    def __contains__(self, key):
        for existing_key, _ in self:
            if existing_key == key:
                return True
        return False
    
    def _ensure_its_a_hashmap(func):
        def wrapper(self, other):
            if not isinstance(other, HashMap):
                raise TypeError(
                    "Cannot compare HashMap with object of another type "\
                    f"({get_class_name(other)})."
                )
            return func(self, other)
        return wrapper
    
    @_ensure_its_a_hashmap
    def __eq__(self, other: "HashMap"):
        return self.items() == other.items()
    
    @_ensure_its_a_hashmap
    def __ne__(self, other: "HashMap"):
        return self.items() != other.items()
    
    def __len__(self):
        return sum((1 for item in self))
    
    def __repr__(self):
        return f"<HashMap: {self._list}>"

    def __str__(self):
        return str(self.items())


# for manual testing purposes
if __name__ == "__main__":
    from random import randint
    hm1 = HashMap((100, "a"))
    hm2 = HashMap([(i, chr(i)) for i in range(4)])
    hm3 = HashMap()
    hm3.update({i:i*2 for i in range(8)})
    hm3.update({randint(0,100):randint(0,100) for i in range(100)})
    hm4 = HashMap({randint(0, 500):i*2 for i in range(1000)})
    hm4.update({i:i*2 for i in range(1000, 2000)})
    hm5 = HashMap({i:i*2 for i in range(100000)})