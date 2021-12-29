from typing import Mapping, MutableMapping, Tuple, Any
from linked_list import LinkedList
from hashlib import *

from tools import get_class_name


class HashMap:
    def __init__(self, map_size: int = 100):
        if not isinstance(map_size, int):
            raise TypeError(
                f"Inappropriate type for map_size ({get_class_name(map_size)})"
            )
        if map_size < 1:
            raise ValueError("map_size cannot be smaller than 1.")
        self._list = [None for i in range(map_size)]
        self._HASH_CEILING = map_size
    
    @property
    def _size(self):
        return len(self.keys())

    @property
    def map_size(self):
        return len(self._list) 

    @property
    def load_factor(self):
        return self._size / self.map_size 
    
    @staticmethod
    def _prehash(key):
        encoded_key = key.encode() if isinstance(key, str) else bytes(key)
        return sha1(encoded_key).digest()

    def _hash(self, key):
        sum = 0
        for i in self._prehash(key):
            sum += i
        return sum % self._HASH_CEILING

    def update(self, kvpair: Tuple):
        new_value = kvpair if kvpair[1] is not None else kvpair[1]
        self._list[self._hash(kvpair[0])] = new_value 
    
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
    
    def __setitem__(self, key, value):
        self.update((key, value))
    
    def __delitem__(self, key):
        item_to_remove = self[key]
        self[key] = None
        del item_to_remove
    
    def __iter__(self):
        return iter(self.items())
    
    def __contains__(self, value):
        return value in self.values()
    
    @staticmethod
    def _compare_type_guard(other):
        if not isinstance(other, HashMap):
            raise TypeError(
                "Cannot compare HashMap with object of another type "\
                f"({get_class_name(other)})."
                )
    
    def __eq__(self, other: "HashMap"):
        self._compare_type_guard(other)
        return self.items() == other.items()
    
    def __ne__(self, other: "HashMap"):
        self._compare_type_guard(other)
        return self.items() != other.items()
    
    def __len__(self):
        return self._size
    
    def __repr__(self):
        return f"<LinkedHashMap: {self._list}>"

    def __str__(self):
        return str(self.items())


if __name__ == "__main__":
    hm1 = HashMap()
    hm1.update((100, "a"))
    hm1.update((101, "b"))
    hm2 = HashMap()
    hm2.update((100, "a"))
    hm2.update((102, "c"))