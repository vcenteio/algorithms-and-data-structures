from typing import Union, Iterable
from linked_list import LinkedList
from hashlib import *
from tools import get_class_name


class HashMap:
    def __init__(
            self, _iter: Iterable = None, map_size: int = 10,
            load_factor: float = 0.75
        ):
        self._set_initial_map_size(map_size)
        self._hash_ceiling = map_size
        self._set_load_factor(load_factor)
        self._create_new_list(map_size, _iter)
    
    @property
    def _size(self):
        return len(self.keys())

    @property
    def _capacity(self):
        return len(self._list) 

    @property
    def _load(self):
        return self._size / self._capacity

    def _create_new_list(self, map_size: int, _iter: Iterable = None):
        self._list = [None for i in range(map_size)]
        if not _iter:
            return
        elif isinstance(_iter, Iterable):
            self.update(_iter)
        else:
            raise TypeError("Non-iterable object passed at HashMap creation.")
    
    def _set_initial_map_size(self, map_size: int):
        if not isinstance(map_size, int):
            raise TypeError(
                f"Inappropriate type '{get_class_name(map_size)}' "\
                "for map size. Should be 'int'."
            )
        if map_size < 1:
            raise ValueError("Map size cannot be smaller than 1.")
        self._INITIAL_MAP_SIZE = map_size

    def _set_load_factor(self, load_factor: float):
        if not isinstance(load_factor, float):
            raise TypeError(
                f"Inappropriate type '{get_class_name(load_factor)}' "\
                "for load factor. Should be 'float'."
            )
        if load_factor >= 1 or load_factor <= 0:
            raise ValueError(
                "Load factor value should be between 0 and 1 "\
                "(both ends not included)."
            )
        self._load_factor = load_factor
    
    def _calculate_new_map_size(self, number_of_new_items: int):
        n = number_of_new_items
        double_capacity = self._capacity * 2
        return double_capacity if double_capacity > n else n + int(0.25 * n) 

    def _resize_list(self, number_of_new_items: int):
        print("Resize needed.")
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
        return {bucket[0]:bucket[1] for bucket in self._list if bucket != None}

    def keys(self):
        return tuple((bucket[0] for bucket in self._list if bucket != None))

    def values(self):
        return tuple((bucket[1] for bucket in self._list if bucket != None))
    
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
    
    def pop(self, key, default=None):
        item_to_pop = self.get(key)
        if item_to_pop != None:
            self[key] = None
            return item_to_pop
        else:
            if default != None:
                return default
            else:
                raise KeyError("Mapping key not found.")

    def clear(self):
        for k in self.keys():
            self[k] = None

    def __getitem__(self, key):
        item = self._list[self._hash(key)]
        if item == None:
            raise KeyError("Mapping key not found.")
        return item[1]

    @staticmethod
    def _prehash(key):
        encoded_key = key.encode() if isinstance(key, str) else bytes(key)
        return sum(sha1(encoded_key).digest())

    def _hash(self, key):
        return self._prehash(key) % self._hash_ceiling
    
    def __setitem__(self, key, value):
        new_value = (key, value) if value is not None else None
        self._list[self._hash(key)] = new_value 
    
    def __delitem__(self, key):
        item_to_remove = self[key]
        self[key] = None
        del item_to_remove
    
    def __iter__(self):
        return iter(self.items())
    
    def __contains__(self, key):
        return key in self.keys()
    
    @staticmethod
    def _ensure_its_a_hashmap(other):
        if not isinstance(other, HashMap):
            raise TypeError(
                "Cannot compare HashMap with object of another type "\
                f"({get_class_name(other)})."
            )
    
    def __eq__(self, other: "HashMap"):
        self._ensure_its_a_hashmap(other)
        return self.items() == other.items()
    
    def __ne__(self, other: "HashMap"):
        self._ensure_its_a_hashmap(other)
        return self.items() != other.items()
    
    def __len__(self):
        return self._size
    
    def __repr__(self):
        return f"<LinkedHashMap: {self._list}>"

    def __str__(self):
        return str(self.items())


# for manual testing purposes
if __name__ == "__main__":
    from random import randint
    hm1 = HashMap((100, "a"))
    hm2 = HashMap([(i, chr(i)) for i in range(4)])
    hm3 = HashMap()
    hm3.update({i:i*2 for i in range(8)})
    hm3.update({randint(0,100):randint(0,100) for i in range(10000)})