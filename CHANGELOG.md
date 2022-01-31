## Unreleased

### Feat

- **LinkedList**: add detect_and_remove_cycle method
- **LinkedList**: add __str__ method
- **LinkedList**: change __repr__ output
- **LinkedList**: implement __eq__ method
- **LinkedList**: make remove method only remove the first occurrence of value
- **LinkedList**: enable insert to work with negative indexes

### Fix

- **LinkedList-Node**: set _next to None on object creation
- **LinkedList**: __*mull__ methods
- **LinkedList**: __*add__ methods infinite loops
- **LinkedList**: __*add__ methods
- **LinkedList**: make extend accept str and bytes as iterables
- **LinkedList**: fix split
- **LinkedList**: fix __getitem__
- **LinkedList**: fix typo on copy error message
- **LinkedList**: implement proper index type check on pop method
- **LinkedList**: make index method handle unexpected arguments
- **LinkedList**: correct copy method issues
- **LinkedList**: Make linked lists accept 0 as head on initialization
- **LinkedList**: make _add_from_iterable raise error on bad argument type

### BREAKING CHANGE

- Multiplication by negative ints is now possible.
- __*add__ methods will serve the sole purpose of being the interface for concatenating linked lists. For other kinds of iterables, the extend method should be used.
- extend does not rely on __iadd__ anymore; they are
different interfaces now.

### Refactor

- **LinkedList**: delitem
- **LinkedList**: getitem
- **LinkedList**: refactor sort method
- **linkedlist.py**: remove assert and sample lists
- **LinkedList**: refactor pop method
- **LinkedList**: add _convert_indices method
- **LinkedList**: refactor __init__
- **LinkedList**: create _is_valid_node_type method
- **LinkedList**: search -> _get_item
- **LinkedList**: Refactor _add* methods

### Perf

- **LinkedList**: improve clear method algorithm
