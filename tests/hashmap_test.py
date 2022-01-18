from typing import Dict, Iterable, List
from secrets import randbelow
import pytest

from src.algoandds.hashmap import HashMap


@pytest.fixture
def hm0():
    return HashMap()


@pytest.mark.parametrize(
    ("value", "error"),
    [(1, TypeError), (True, TypeError), (b"1.3", TypeError)],
)
def test_set_load_factor_wrong_type(hm0: HashMap, value, error):
    with pytest.raises(error):
        hm0._set_load_factor(value)


@pytest.mark.parametrize(
    ("value", "error"),
    [(0.74, ValueError), (-4.0, ValueError), (0.96, ValueError)],
)
def test_set_load_factor_wrong_value(hm0: HashMap, value, error):
    with pytest.raises(error):
        hm0._set_load_factor(value)


@pytest.mark.parametrize(
    ("arg", "expected_result"),
    [(0.75, 0.75), (0.95, 0.95), (0.823, 0.823), (0.9099999, 0.9099999)],
)
def test_set_load_factor_correct_argument(hm0: HashMap, arg, expected_result):
    hm0._set_load_factor(arg)
    assert hm0._load_factor == expected_result


@pytest.mark.parametrize(
    ("value", "error"),
    [(1.0, TypeError), (True, TypeError), (b"1.3", TypeError)],
)
def test_get_size_with_load_margin_wrong_type(hm0: HashMap, value, error):
    with pytest.raises(error):
        hm0._get_size_with_load_margin(value)


@pytest.mark.parametrize(
    ("value", "error"),
    [(-1, ValueError), (-10, ValueError), (-1000, ValueError)],
)
def test_get_size_with_load_margin_wrong_value(hm0: HashMap, value, error):
    with pytest.raises(error):
        hm0._get_size_with_load_margin(value)


@pytest.mark.parametrize(
    ("value", "error"),
    [(1.0, TypeError), (True, TypeError), (b"1.3", TypeError)],
)
def test_set_initial_map_size_wrong_type(hm0: HashMap, value, error):
    with pytest.raises(error):
        hm0._set_initial_map_size(value)


@pytest.mark.parametrize(
    ("load_factor", "number_of_new_items", "expected_size"),
    [(0.75, 20, 20 * 2), (0.75, 3, 10), (0.823, 20, 20 * 2)],
)
def test_set_initial_map_size_correct_argument(
    hm0: HashMap, load_factor, number_of_new_items, expected_size
):
    hm0._load_factor = load_factor
    hm0._set_initial_map_size(number_of_new_items)
    assert hm0._INITIAL_MAP_SIZE == expected_size


@pytest.mark.parametrize(
    ("value", "error"),
    [(1, TypeError), ("abc", TypeError), (bytearray((1, 2, 3)), TypeError)],
)
def test_update_wrong_type(hm0: HashMap, value, error):
    with pytest.raises(error):
        hm0.update(value)


@pytest.mark.parametrize(
    ("value", "error"),
    [(1, TypeError), ("abc", TypeError), (bytearray((1, 2, 3)), TypeError)],
)
def test_add_from_tuple_wrong_type(hm0: HashMap, value, error):
    with pytest.raises(error):
        hm0._add_from_tuple(value)


@pytest.mark.parametrize(
    ("tuple", "error"),
    [((1,), ValueError), ((1, 2, 3), ValueError), ((), ValueError)],
)
def test_add_from_tuple_wrong_tuple_size(hm0: HashMap, tuple, error):
    with pytest.raises(error):
        hm0._add_from_tuple(tuple)


@pytest.mark.parametrize(
    ("key", "value"), [(1, "a"), (b"1", 5), ("&", [1, 2])]
)
def test_add_from_tuple_correct_tuple_size(hm0: HashMap, key, value):
    hm0._add_from_tuple((key, value))
    assert hm0[key] == value


@pytest.mark.parametrize(
    ("value", "error"),
    [(1, TypeError), ("abc", TypeError), (bytearray((1, 2, 3)), TypeError)],
)
def test_add_from_dict_wrong_type(hm0: HashMap, value, error):
    with pytest.raises(error):
        hm0._add_from_dict(value)


@pytest.mark.parametrize("d", [{1: "a", 2: "b", 3: "c"}, {"key": "value"}])
def test_add_from_dict_correct_argument(hm0: HashMap, d: Dict):
    hm0._add_from_dict(d)
    assert hm0.items() == d


@pytest.mark.parametrize(
    ("value", "error"),
    [(1, TypeError), ("abc", TypeError), (bytearray((1, 2, 3)), TypeError)],
)
def test_add_from_list_wrong_type(hm0: HashMap, value, error):
    with pytest.raises(error):
        hm0._add_from_list(value)


@pytest.mark.parametrize(
    "l", ([1, 2, 3], [(1,), (2,)], [(), ()], [(1, 2, 3), (4, 5, 6)])
)
def test_add_from_list_invalid_list(hm0: HashMap, l: List):
    with pytest.raises(ValueError):
        hm0._add_from_list(l)


@pytest.mark.parametrize("l", [[(1, "a"), (2, "b"), (3, "c")]])
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


@pytest.mark.parametrize("value", [True, "a", b"54", [4, 3], (), 3.2])
def test_set_hash_ceiling_wrong_type(hm0: HashMap, value):
    with pytest.raises(TypeError):
        hm0._set_hash_ceiling(value)


@pytest.mark.parametrize("value", [11, 9, 27, 25, 0])
def test_set_hash_ceiling_wrong_value(hm0: HashMap, hm3: HashMap, value):
    with pytest.raises(ValueError):
        hm0._set_hash_ceiling(value)
    with pytest.raises(ValueError):
        hm3._set_hash_ceiling(value)


@pytest.mark.parametrize("value", [10, 20, 90, 1, 0])
def test_set_hash_ceiling_correct_value(hm0: HashMap, value):
    hm0._list = [None for _ in range(value)]
    hm0._set_hash_ceiling(value)
    assert hm0._hash_ceiling == value


@pytest.mark.parametrize(
    "wrong_map_size", [1.2, True, HashMap, sorted, {i for i in range(5)}]
)
def test_create_new_list_wrong_map_size_type(hm0: HashMap, wrong_map_size):
    with pytest.raises(TypeError):
        hm0._create_new_list(wrong_map_size)


@pytest.mark.parametrize("wrong_map_size", [1, 0, -10, 9])
def test_create_new_list_wrong_map_size_value(hm0: HashMap, wrong_map_size):
    with pytest.raises(ValueError):
        hm0._create_new_list(wrong_map_size)


@pytest.mark.parametrize("map_size", [11, 20, 1000])
def test_create_new_list_correct_map_size_type(hm0: HashMap, map_size):
    hm0._create_new_list(map_size)
    assert hm0._capacity == hm0._hash_ceiling == map_size
    assert hm0._size == len(hm0) == 0


def test_create_new_list_no_arguments(hm0: HashMap):
    hm0._create_new_list()
    assert hm0._capacity == hm0._hash_ceiling == hm0._INITIAL_MAP_SIZE
    assert hm0._size == len(hm0) == 0


def test_create_hashmap_with_no_items(hm0: HashMap):
    assert hm0._list == [None for _ in range(HashMap._MINIMUM_MAP_SIZE)]
    assert hm0._load_factor == HashMap._DEFAULT_LOAD_FACTOR
    assert hm0._capacity == HashMap._MINIMUM_MAP_SIZE
    assert hm0._size == len(hm0) == 0


@pytest.mark.parametrize("wrong_iter", [1, 0.34, sorted, Dict, Iterable, dir])
def test_create_hashmap_wrong_iter(wrong_iter):
    error_msg = "Non-iterable object passed at HashMap creation."
    with pytest.raises(TypeError) as exec:
        HashMap(wrong_iter)
    assert error_msg in str(exec.value)


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


@pytest.fixture
def l0():
    return []


@pytest.fixture
def l10():
    return [(i, i * 2) for i in range(10)]


@pytest.fixture
def l20():
    return [(i, i * 2) for i in range(10, 30)]


@pytest.fixture
def d10():
    return {i: i * 2 for i in range(10)}


@pytest.fixture
def d20():
    return {i: i * 2 for i in range(10, 30)}


def test_len(l10, l20, d10, d20):
    hm = HashMap(l10)
    assert len(hm) == sum((1 for _ in l10 if _ is not None))
    hm = HashMap(l20)
    assert len(hm) == sum((1 for _ in l20 if _ is not None))
    hm = HashMap(d10)
    assert len(hm) == sum((1 for _ in d10 if _ is not None))
    hm = HashMap(d20)
    assert len(hm) == sum((1 for _ in d20 if _ is not None))


def test_capacity(l10, l20, d10, d20):
    hm = HashMap(l10)
    assert hm._capacity == len(l10) * 2
    hm = HashMap(l20)
    assert hm._capacity == len(l20) * 2
    hm = HashMap(d10)
    assert hm._capacity == len(d10) * 2
    hm = HashMap(d20)
    assert hm._capacity == len(d20) * 2


def test_load(l10, l20, d10, d20):
    hm = HashMap(l10)
    assert hm._load == hm._size / (len(l10) * 2)
    hm = HashMap(l20)
    assert hm._load == hm._size / (len(l20) * 2)
    hm = HashMap(d10)
    assert hm._load == hm._size / (len(d10) * 2)
    hm = HashMap(d20)
    assert hm._load == hm._size / (len(d20) * 2)


@pytest.mark.parametrize(
    ("number_of_items", "expected"),
    [(0, False), (1, False), (5, False), (6, False), (8, True), (40, True)],
)
def test_is_resize_needed(hm0: HashMap, number_of_items, expected):
    assert hm0._is_resize_needed(number_of_items) == expected


@pytest.mark.parametrize(
    ("number_of_items", "expected"), [(0, 10), (1, 10), (10, 20)]
)
def test_calculate_new_map_size(hm0: HashMap, number_of_items, expected):
    assert hm0._calculate_new_map_size(number_of_items) == expected


@pytest.fixture
def hm4():
    return HashMap([(i, i * 2) for i in range(40)])


@pytest.mark.parametrize(("key"), [41, 42, 43, 500, 1100232])
def test_set_default_non_existent_key_no_default(hm4: HashMap, key):
    assert hm4.setdefault(key) is None


@pytest.mark.parametrize(
    ("key", "default"), [(41, 2), (43, 4), ("a", "b"), (b"123", [5, 9, 6])]
)
def test_set_default_non_existent_key_with_default(hm4: HashMap, key, default):
    assert hm4.setdefault(key, default) == default


@pytest.mark.parametrize(("key", "value"), [(1, 2), (3, 6), (7, 14), (39, 78)])
def test_set_default_existing_key(hm4: HashMap, key, value):
    assert hm4.setdefault(key, "default") == value


def test_items(hm0: HashMap, hm4: HashMap, d10: Dict, d20: Dict):
    assert hm0.items() == {}
    hm0.update(d10)
    assert hm0.items() == d10
    hm0.update(d20)
    dtemp = d10.copy()
    dtemp.update(d20)
    assert hm0.items() == dtemp
    assert hm4.items() == {i: i * 2 for i in range(40)}


def test_keys(hm0: HashMap, hm4: HashMap, d10: Dict, d20: Dict):
    assert hm0.keys() == ()
    hm0.update(d10)
    assert set(hm0.keys()) == set(d10.keys())
    hm0.update(d20)
    dtemp = d10.copy()
    dtemp.update(d20)
    assert set(hm0.keys()) == set(dtemp.keys())
    assert set(hm4.keys()) == set((i for i in range(40)))


def test_values(hm0: HashMap, hm4: HashMap, d10: Dict, d20: Dict):
    assert hm0.values() == ()
    hm0.update(d10)
    assert set(hm0.values()) == set(d10.values())
    hm0.update(d20)
    dtemp = d10.copy()
    dtemp.update(d20)
    assert set(hm0.values()) == set(dtemp.values())
    assert set(hm4.values()) == set((i * 2 for i in range(40)))


@pytest.mark.parametrize(("key", "expected"), [(1, 2), (10, 20), (39, 78)])
def test_get_existing_key(hm4: HashMap, key, expected):
    assert hm4.get(key) == expected


@pytest.mark.parametrize(
    ("key", "default"),
    [(41, "default"), (100, b"123"), (76, bytearray((3, 2, 1)))],
)
def test_get_non_existing_key(hm4: HashMap, key, default):
    assert hm4.get(key, default) == default
    assert hm4.get(key) is None


@pytest.mark.parametrize(
    ("key", "value"), [(1, 2), (10, 20), (39, 78), (20, 40), (15, 30)]
)
def test_pop(hm4: HashMap, key, value):
    assert hm4.pop(key) == value
    assert hm4.pop(key, "default") == "default"
    with pytest.raises(KeyError):
        hm4.pop(key)


def test_clear(hm0: HashMap, hm4: HashMap):
    l = hm0._list
    hm0.clear()
    assert hm0._list == l == [None for _ in range(hm0._MINIMUM_MAP_SIZE)]

    l = hm4._list
    hm4.clear()
    assert hm4._list == [None for _ in range(hm4._INITIAL_MAP_SIZE)] != l


@pytest.mark.parametrize("key", [(1, 2), [1, 2], [], (), {1: "a"}, {}])
def test_getitem_wrong_type_key(hm4: HashMap, key):
    with pytest.raises(TypeError):
        hm4[key]


def test_getitem_wrong_value_key(hm4: HashMap):
    with pytest.raises(ValueError):
        hm4[None]


def test_getitem_non_existing_key(hm4: HashMap):
    keys = [i for i in range(40, 60)]
    for k in keys:
        with pytest.raises(KeyError):
            hm4[k]
    for k in range(10):
        hm4.pop(k)
        with pytest.raises(KeyError):
            hm4[k]


def test_getitem_existing_key(hm4: HashMap):
    keys = [i for i in range(40)]
    for k in keys:
        assert hm4[k] == k * 2

    keys = [randbelow(30000) for _ in range(30000)]
    hmt = HashMap({key: key * 2 for key in keys})
    for k in keys:
        assert hmt[k] == k * 2


def test_setitem_non_existing_key(hm0: HashMap):
    d = {i: i * 5 for i in range(10)}
    for key in d:
        hm0[key] = d[key]
        assert hm0[key] == d[key]

    keys = [randbelow(30000) for _ in range(10000)]
    hmt = HashMap({key: key * 5 for key in keys})
    non_existent_keys = [k for k in range(30000) if k not in keys]
    for key in non_existent_keys:
        with pytest.raises(KeyError):
            hmt[key]
        hmt[key] = key * 5
        assert hmt[key] == key * 5


def test_setitem_existing_key(hm4: HashMap):
    for i in range(40):
        assert hm4[i] == i * 2

    keys = [i for i in range(1, 30000)]
    hmt = HashMap({key: key * 5 for key in keys})
    for key in keys:
        assert hmt[key] != key * 7
        assert hmt[key] == key * 5
        hmt[key] = key * 7
        assert hmt[key] == key * 7


def test_delitem_non_existing_key(hm4: HashMap):
    for k in range(40, 30000):
        with pytest.raises(KeyError):
            del hm4[k]


def test_delitem_existing_key(hm4: HashMap):
    for k in range(40):
        del hm4[k]
        with pytest.raises(KeyError):
            hm4[k]
    # Test item deletion and map resizing when
    # load gets too low.
    keys = [i for i in range(1, 3000)]
    hmt = HashMap({key: key * 5 for key in keys})
    for k in keys:
        previous_capacity = (
            hmt._capacity if hmt._is_resize_needed(-1) else None
        )
        del hmt[k]
        if previous_capacity is not None:
            assert hmt._capacity < previous_capacity
        with pytest.raises(KeyError):
            hmt[k]


@pytest.mark.parametrize(
    "iter",
    [
        [(i, i * 2) for i in range(30000)],
        {chr(c): bytes(c) for c in range(30000)},
    ],
)
def test_iter_non_empty_hashmap(iter: Iterable):
    hmt = HashMap(iter)
    for key in hmt:
        value = iter[key][1] if isinstance(iter, List) else iter[key]
        assert hmt[key] == value


@pytest.mark.xfail
def test_iter_empty_hashmap(hm0: HashMap):
    for k in hm0:
        hm0[k]


@pytest.mark.parametrize(
    "iter",
    [
        [(i, i * 2) for i in range(300)],
    ],
)
def test_contains_non_existing_key(iter: Iterable):
    hmt = HashMap(iter)
    for key in range(300, 600):
        assert key not in hmt


@pytest.mark.parametrize(
    "iter",
    [
        [(i, i * 2) for i in range(300)],
    ],
)
def test_contains_existing_key(iter: Iterable):
    hmt = HashMap(iter)
    for key in range(300):
        assert key in hmt


@pytest.mark.parametrize(
    "wrong_item", (1, "a", {1: "a"}, [], bytearray((1, 2, 3)), set((1, 2, 3)))
)
def test_eq_ne_wrong_type(hm0: HashMap, wrong_item):
    with pytest.raises(TypeError):
        hm0 == wrong_item
    with pytest.raises(TypeError):
        hm0 != wrong_item


@pytest.mark.parametrize(
    "correct_item",
    [
        HashMap((1, "a")),
        HashMap({chr(i): i for i in range(2000)}),
        HashMap([(i, bytes(i)) for i in range(2000)]),
    ],
)
def test_eq_ne_correct_type(correct_item: HashMap):
    hmt = HashMap(correct_item.items())
    assert hmt == correct_item
    assert not hmt != correct_item
    correct_item.clear()
    assert not hmt == correct_item
    assert hmt != correct_item


@pytest.mark.parametrize(
    "hm",
    [
        HashMap(),
        HashMap((1, "a")),
        HashMap({chr(i): i for i in range(2000)}),
        HashMap([(i, bytes(i)) for i in range(2000)]),
    ],
)
def test_str_repr(hm: HashMap):
    l = hm._list
    items = hm.items()
    assert repr(hm) == f"<HashMap: {l}>"
    assert str(hm) == str(items)


@pytest.mark.parametrize(
    "rng",
    [
        range(10),
        range(10, 20),
        range(20, 40),
        range(40, 100),
        range(100, 10000),
    ],
)
def test_integrity_on_increasing_load(hm0: HashMap, rng: range):
    hm0.update({i: i * 2 for i in rng})
    for i in rng:
        assert hm0[i] == i * 2


@pytest.mark.parametrize(
    "hm",
    [
        HashMap(),
        HashMap((1, "a")),
        HashMap({chr(i): i for i in range(2000)}),
        HashMap([(i, bytes(i)) for i in range(2000)]),
    ],
)
def test_copy(hm: HashMap):
    assert set(hm) == set(hm.copy())
