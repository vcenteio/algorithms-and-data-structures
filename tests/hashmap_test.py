from typing import Dict, List
import pytest

from src.algoandds.hashmap import HashMap
from src.algoandds.linkedlist import LinkedList


@pytest.fixture
def hm0():
    return HashMap()


@pytest.mark.parametrize(
    ("value", "error"),
    [(1, TypeError), (True, TypeError), (b"1.3", TypeError)]
)
def test_set_load_factor_wrong_type(hm0: HashMap, value, error):
    with pytest.raises(error):
        hm0._set_load_factor(value)


@pytest.mark.parametrize(
    ("value", "error"),
    [(0.74, ValueError), (-4.0, ValueError), (0.96, ValueError)]
)
def test_set_load_factor_wrong_value(hm0: HashMap, value, error):
    with pytest.raises(error):
        hm0._set_load_factor(value)


@pytest.mark.parametrize(
    ("arg", "expected_result"),
    [(0.75, 0.75), (0.95, 0.95), (0.823, 0.823), (0.9099999, 0.9099999)]
)
def test_set_load_factor_correct_argument(hm0: HashMap, arg, expected_result):
    hm0._set_load_factor(arg)
    assert hm0._load_factor == expected_result


@pytest.mark.parametrize(
    ("value", "error"),
    [(1.0, TypeError), (True, TypeError), (b"1.3", TypeError)]
)
def test_get_size_with_load_margin_wrong_type(hm0: HashMap, value, error):
    with pytest.raises(error):
        hm0._get_size_with_load_margin(value)


@pytest.mark.parametrize(
    ("value", "error"),
    [(-1, ValueError), (-10, ValueError), (-1000, ValueError)]
)
def test_get_size_with_load_margin_wrong_value(hm0: HashMap, value, error):
    with pytest.raises(error):
        hm0._get_size_with_load_margin(value)


@pytest.mark.parametrize(
    ("value", "error"),
    [(1.0, TypeError), (True, TypeError), (b"1.3", TypeError)]
)
def test_set_initial_map_size_wrong_type(hm0: HashMap, value, error):
    with pytest.raises(error):
        hm0._set_initial_map_size(value)


@pytest.mark.parametrize(
    ("load_factor", "number_of_new_items", "expected_size"),
    [(0.75, 20, 20 * 2), (0.75, 3, 10), (0.823, 20, 20 * 2)]
)
def test_set_initial_map_size_correct_argument(
    hm0: HashMap, load_factor, number_of_new_items, expected_size
    ):
    hm0._load_factor = load_factor
    hm0._set_initial_map_size(number_of_new_items)
    assert hm0._INITIAL_MAP_SIZE == expected_size


@pytest.mark.parametrize(
    ("value", "error"),
    [(1, TypeError), ("abc", TypeError), (bytearray((1,2,3)), TypeError)]
)
def test_update_wrong_type(hm0: HashMap, value, error):
    with pytest.raises(error):
        hm0.update(value)


@pytest.mark.parametrize(
    ("value", "error"),
    [(1, TypeError), ("abc", TypeError), (bytearray((1,2,3)), TypeError)]
)
def test_add_from_tuple_wrong_type(hm0: HashMap, value, error):
    with pytest.raises(error):
        hm0._add_from_tuple(value)


@pytest.mark.parametrize(
    ("tuple", "error"),
    [((1,), ValueError), ((1,2,3), ValueError), ((), ValueError)]
)
def test_add_from_tuple_wrong_tuple_size(hm0: HashMap, tuple, error):
    with pytest.raises(error):
        hm0._add_from_tuple(tuple)


@pytest.mark.parametrize(
    ("key", "value"),
    [(1, "a"), (b"1", 5), ("&", [1, 2])]
)
def test_add_from_tuple_correct_tuple_size(hm0: HashMap, key, value):
    hm0._add_from_tuple((key, value))
    assert hm0[key] == value


@pytest.mark.parametrize(
    ("value", "error"),
    [(1, TypeError), ("abc", TypeError), (bytearray((1,2,3)), TypeError)]
)
def test_add_from_dict_wrong_type(hm0: HashMap, value, error):
    with pytest.raises(error):
        hm0._add_from_dict(value)


@pytest.mark.parametrize(
    "d",
    [{1: "a", 2: "b", 3: "c"}, {"key": "value"}]
)
def test_add_from_dict_correct_argument(hm0: HashMap, d: Dict):
    hm0._add_from_dict(d)
    assert hm0.items() == d


@pytest.mark.parametrize(
    ("value", "error"),
    [(1, TypeError), ("abc", TypeError), (bytearray((1,2,3)), TypeError)]
)
def test_add_from_list_wrong_type(hm0: HashMap, value, error):
    with pytest.raises(error):
        hm0._add_from_list(value)


@pytest.mark.parametrize(
    "l",
    ([1,2,3], [(1,), (2,)], [(), ()], [(1,2,3), (4,5,6)])
)
def test_add_from_list_invalid_list(hm0: HashMap, l: List):
    with pytest.raises(ValueError):
        hm0._add_from_list(l)


@pytest.mark.parametrize(
    "l",
    [[(1, "a"), (2, "b"), (3, "c")]]
)
def test_add_from_list_correct_argument(hm0: HashMap, l: List):
    hm0._add_from_list(l)
    assert hm0.items() == dict(l)


@pytest.fixture
def hm1():
    return HashMap([(1, "a"), (2, "b"), (3, "c")])


@pytest.fixture
def hm2():
    return HashMap({1: "a", 2: "b", 3: "c"})


@pytest.fixture
def hm3():
    return HashMap({i: chr(i) for i in range(97, 123)})


@pytest.mark.parametrize(
    "value",
    [True, "a", b"54", [4, 3], (), 3.2]
)
def test_set_hash_ceiling_wrong_type(hm0: HashMap, value):
    with pytest.raises(TypeError):
        hm0._set_hash_ceiling(value)

@pytest.mark.parametrize(
    "value",
    [11, 9, 27, 25, 0]
)
def test_set_hash_ceiling_wrong_value(
    hm0: HashMap, hm3: HashMap, value
    ):
    with pytest.raises(ValueError):
        hm0._set_hash_ceiling(value)
    with pytest.raises(ValueError):
        hm3._set_hash_ceiling(value)

@pytest.mark.parametrize(
    "value",
    [10, 20, 90, 1, 0]
)
def test_set_hash_ceiling_correct_value(hm0: HashMap, value):
    hm0._list = [None for _ in range(value)]
    hm0._set_hash_ceiling(value)
    assert hm0._hash_ceiling == value


@pytest.mark.parametrize(
    "wrong_map_size",
    [1.2, True, HashMap, sorted, {i for i in range(20)}]
)
def test_create_new_list_wrong_map_size_type(hm0: HashMap, wrong_map_size):
    with pytest.raises(TypeError):
        hm0._create_new_list(wrong_map_size)


@pytest.mark.parametrize(
    "wrong_map_size",
    [1, 0, -1, 9, -1000]
)
def test_create_new_list_wrong_map_size_value(hm0: HashMap, wrong_map_size):
    with pytest.raises(ValueError):
        hm0._create_new_list(wrong_map_size)


@pytest.mark.parametrize(
    "map_size",
    [11, 20, 1000]
)
def test_create_new_list_correct_iter_type(hm0: HashMap, map_size):
    hm0._create_new_list(map_size)
    assert hm0._capacity == hm0._hash_ceiling == map_size
    assert hm0._size == len(hm0) == 0


def test_create_new_list_no_arguments(hm0: HashMap):
    hm0._create_new_list()
    assert hm0._capacity == hm0._hash_ceiling == hm0._INITIAL_MAP_SIZE
    assert hm0._size == len(hm0) == 0


def test_create_hashmap_with_no_items(hm0: HashMap):
    assert hm0._list == [None for _ in range(HashMap._DEFAULT_MAP_SIZE)]
    assert hm0._load_factor == HashMap._DEFAULT_LOAD_FACTOR
    assert hm0._capacity == HashMap._DEFAULT_MAP_SIZE
    assert hm0._size == len(hm0) == 0


def test_create_hashmap_from_single_tuple():
    hm = HashMap((1, "a"))
    assert hm.items() == {1: "a"}
    assert len(hm) == 1


def test_create_hashmap_from_list_of_tuples(hm1: HashMap):
    hm1_dict = {1: "a", 2: "b", 3: "c"}
    assert hm1.items() == hm1_dict


def test_create_hashmap_from_dict(hm2: HashMap):
    hm1_dict = {1: "a", 2: "b", 3: "c"}
    assert hm2.items() == hm1_dict


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
