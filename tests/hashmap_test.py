import pytest

try:
    from ..src.algoandds.hashmap import HashMap
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
    from src.algoandds.hashmap import HashMap


@pytest.fixture
def hm0():
    return HashMap()

@pytest.fixture
def hm1():
    return  HashMap([(1, "a"), (2, "b"), (3, "c")])


def test_hashmap_creation_from_tuples(hm1: HashMap):
    hm1_dict = {1: "a", 2: "b", 3: "c"}
    assert hm1.items() == hm1_dict

def test_load_factor():
    with pytest.raises(TypeError):
        HashMap(load_factor=2)
    with pytest.raises(TypeError):
        HashMap(load_factor="a")
    with pytest.raises(TypeError):
        HashMap(load_factor=True)

    with pytest.raises(ValueError):
        HashMap(load_factor=7.4)
    with pytest.raises(ValueError):
        HashMap(load_factor=9.6)

    hm1 = HashMap()
    hm2 = HashMap(load_factor=0.80)

    assert hm1._load_factor == 0.75
    assert hm2._load_factor == 0.80

def test_set_initial_map_size():
    with pytest.raises(TypeError):
        HashMap(map_size="a")
    with pytest.raises(TypeError):
        HashMap(map_size=True)
    with pytest.raises(TypeError):
        HashMap(map_size=6.3)

    with pytest.raises(ValueError):
        HashMap(map_size=HashMap._DEFAULT_MAP_SIZE-1)

    l1 = [(i,i*2) for i in range(20)]
    hm1 = HashMap(_iter=l1, map_size=15)
    assert hm1._INITIAL_MAP_SIZE == hm1._get_size_with_load_margin(20)

    l2 = [(i,i*2) for i in range(5)]
    hm2 = HashMap(_iter=l2, map_size=15)
    assert hm2._INITIAL_MAP_SIZE == hm2._get_size_with_load_margin(15)

def test_create_hashmap_with_no_arguments(hm0: HashMap):
    assert hm0._list == [None for _ in range(HashMap._DEFAULT_MAP_SIZE)]
    assert hm0._load_factor == HashMap._DEFAULT_LOAD_FACTOR
    assert hm0._capacity == HashMap._DEFAULT_MAP_SIZE
    assert hm0._size == 0
    assert len(hm0) == 0

def test_create_new_list(hm0: HashMap):
    l1 = [(i,i*2) for i in range(20)]
    hm0._create_new_list(20, l1)
    assert hm0.items() == dict(l1)
