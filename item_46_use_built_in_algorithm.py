# Item 46: Use built-in algorithms and data structures
from collections import deque
import random
from collections import OrderedDict
from collections import defaultdict
from heapq import heappush
from heapq import heappop
from heapq import nsmallest
from bisect import bisect_left


# When you're implementing Python programs that handle a non-trivial amount of
# data, you'll eventually see slowdowns caused by the algorithmic complexity
# of your code. This usually isn't the result of Python's speed as a language
# (see Item 41: "Consider concurrent.futures for true parallelism" if it is).
# The issue, more likely, is that you are not using the best algorithms and
# data structures for your problem.

# Luckily, the Python standard library has many of the algorithms and data
# structures you'll need to use built in. Besides speed, using these common
# algorithms and data structures can make your life easier. Some of the most
# valuable tools you may want to use are tricky to implement correctly.
# Avoiding reimplementation of common functionality will save you time and
# headaches.


# Double-ended Queue

# The deque class from the collections module is a double-ended queue. It
# provides constant time operations for inserting or removing items from its
# beginning or end. This makes it ideal fro first-in-first-out (FIFO) queues.

fifo = deque()
fifo.append(1)      # Producer
fifo.append(2)      # Producer
fifo.append(3)      # Producer
fifo.append(5)      # Producer
print(fifo)
x = fifo.popleft()  # Consumer
y = fifo.pop()  # Consumer
print(x)
print(y)
print(fifo)
# deque([1, 2, 3, 5])
# 1
# 5
# deque([2, 3])

# The list built-in type also contains an ordered sequence of items like a
# queue. You can insert or remove items from the end of a list in constant
# time. But inserting or removing items from the head of a list takes linear
# time, which is much slower than the constant time of a deque.


# Ordered Dictionary

# Standard dictionaries are unordered. That means a dict with the same keys
# and values can result in different orders of iteration. This behavior is a
# surprising byproduct of the way the dictionary's fast hash table is
# implemented.

a = {}
a['foo'] = 1
a['bar'] = 2
print(a)
# {'foo': 1, 'bar': 2}

# Randomly populate 'b' to cause hash conflicts
while True:
    z = random.randint(99, 1013)
    b = {}
    for i in range(z):
        b[i] = i
    b['foo'] = 1
    b['bar'] = 2
    for i in range(z):
        del b[i]
    if str(b) != str(a):
        break

print(a)
print(b)
print('Equal?', a == b)
# {'foo': 1, 'bar': 2}
# {'bar': 2, 'foo': 1}
# Equal? True
# 这两个dict其实是相等的，但是由于iterate的顺序不同，它们的__str__()结果也不同

"""
Python dictionaries are implemented as hash tables.
Hash tables must allow for hash collisions i.e. even if two keys have same hash value, the implementation of the table must have a strategy to insert and 
retrieve the key and value pairs unambiguously.
Python dict uses open addressing to resolve hash collisions (explained below) (see dictobject.c:296-297).
Python hash table is just a continguous block of memory (sort of like an array, so you can do O(1) lookup by index).
Each slot in the table can store one and only one entry. This is important.
Each entry in the table actually a combination of the three values - . This is implemented as a C struct (see dictobject.h:51-56)
The figure below is a logical representation of a python hash table. In the figure below, 0, 1, ..., i, ... on the left are indices of the slots 
in the hash table (they are just for illustrative purposes and are not stored along with the table obviously!).

Logical model of Python Hash table
-+-----------------+
0| <hash|key|value>|
-+-----------------+
1|      ...        |
-+-----------------+
.|      ...        |
-+-----------------+
i|      ...        |
-+-----------------+
.|      ...        |
-+-----------------+
n|      ...        |
-+-----------------+
When a new dict is initialized it starts with 8 slots. (see dictobject.h:49)

When adding entries to the table, we start with some slot, i that is based on the hash of the key. CPython uses initial i = hash(key) & mask. 
Where mask = PyDictMINSIZE - 1, but that's not really important). Just note that the initial slot, i, that is checked depends on the hash of the key.
If that slot is empty, the entry is added to the slot (by entry, I mean, <hash|key|value>). But what if that slot is occupied!? 
Most likely because another entry has the same hash (hash collision!)
If the slot is occupied, CPython (and even PyPy) compares the the hash AND the key (by compare I mean == comparison not the is comparison) of the entry 
in the slot against the key of the current entry to be inserted (dictobject.c:337,344-345). If both match, then it thinks the entry already exists. 
If either hash or the key don't match, it starts probing.
Probing just means it searches the slots by slot to find an empty slot. Technically we could just go one by one, i+1, i+2, ... and use the first available
one (that's linear probing). But for reasons explained beautifully in the comments (see dictobject.c:33-126), CPython uses random probing. 
In random probing, the next slot is picked in a pseudo random order. The entry is added to the first empty slot. 
For this discussion, the actual algorithm used to pick the next slot is not really important (see dictobject.c:33-126 for the algorithm for probing). 
What is important is that the slots are probed until first empty slot is found.
The same thing happens for lookups, just starts with the initial slot i (where i depends on the hash of the key). 
If the hash and the key both don't match the entry in the slot, it starts probing, until it finds a slot with a match. 
If all slots are exhausted, it reports a fail.
BTW, the dict will be resized if it is two-thirds full. This avoids slowing down lookups. (see dictobject.h:64-65)
"""

# The OrderedDict class from the collections module is a special type of
# dictionary that keeps track of the order in which its keys were inserted.
# Iterating the keys of an OrderedDict has predictable behavior. This can
# vastly simplify testing and debugging by making all code deterministic.

a = OrderedDict()
a['foo'] = 1
a['bar'] = 2

b = OrderedDict()
b['foo'] = 'red'
b['bar'] = 'blue'

for value1, value2 in zip(a.values(), b.values()):
    print(value1, value2)
# 1 red
# 2 blue


# Default Dictionary

# Dictionaries are useful for bookkeeping and tracking statistics. One problem
# with dictionaries is that you can't assume any keys are already present.
# That makes it clumsy to do simple things like increment a counter stored in a
# dictionary.

stats = {}
key = 'my_computer'
if key not in stats:
    stats[key] = 0
stats[key] += 1

# The defaultdict class from the collections module simplifies this by
# automatically storing a default value when a key doesn't exist. All you have
# to do is provide a function that will return the default value each time a
# key is missing. In this example, the int built-in function returns 0 (see
# Item 23: "Accept functions for simple interfaces instead of classes" for
# another example). Now, incrementing a counter is simple.

stats = defaultdict(int)
stats['my_counter'] += 1


# Heap Queue

# Heaps are useful data structures for maintaining a priority queue. The heapq
# module provides functions for creating heaps in standard list types with
# functions like heappush, heappop, and nsmallest.

# Items of any priority can be inserted into the heap in any other.

a = []
heappush(a, 5)
heappush(a, 3)
heappush(a, 7)
heappush(a, 4)

# Items are always by highest priority (lowest number) first.

print(heappop(a), heappop(a), heappop(a), heappop(a))
# 3 4 5 7

# The result list is easy to use outside of heapq. Accessing the 0 index of
# the heap will always return the smallest item.

a = []
heappush(a, 5)
heappush(a, 3)
heappush(a, 7)
heappush(a, 4)
assert a[0] == nsmallest(1, a)[0] == 3

# Calling the sort method on the list maintains the heap invariant.

print('Before:', a)
a.sort()
print('After: ', a)
# Before: [3, 4, 7, 5]
# After:  [3, 4, 5, 7]

# Each of these heapq operations takes logarithmic time in proportion to the
# length of the list. Doing the same work with a standard Python list would
# scale linearly.


# Bisection

# Searching for an item in a list takes linear time proportional to its length
# when you call the index method.

x = list(range(10**6))
i = x.index(991234)

# The bisect module's functions, such as bisect_left, provide an efficient
# binary search through a sequence of sorted items. The index it returns is
# the insertion point of the value into the sequence.

i = bisect_left(x, 991234)

# The complexity of a binary search is logarithmic. That means using bisect to
# search a list of 1 million items takes roughly the same amount of time as
# using index to linearly search a list of 14 items. It's way faster!


# Iterator Tools

# The itertools built-in module contains a large number of functions that are
# useful for organizing and interacting with iterators (see Item 16:
# "Consider generator instead of returning lists" and Item 17: "Be defensive
# when iterating over arguments" for background). Not all these are available
# in Python 2, but they can easily be built using simple recipes documented in
# the module. See help(itertools) in an interactive Python session for more
# details

# The itertools functions fall into three main categories:
# 1. Linking iterations together
#    a. chain: combines multiple iterators into a single sequential iterator.
#    b. cycle: repeats an iterator's items forever.
#    c. tree: splits a single iterator into multiple parallel iterators.
#    d. zip_longest: a variant of the zip built-in function that works well
#       with iterators of different lengths.
# 2. Filtering items from an iterator
#    a. islice: slices an iterator by numerical indexes without copying.
#    b. takewhile: returns items from an iterator while a predicate function
#       returns True.
#    c. dropwhile: returns all items from an iterator once the predicate
#       function returns False for the first time.
#    d. filterfalse: returns all items from an iterator where a predicate
#       function return False. The opposite of the filter built-in function.
# 3. Combinations of items from iterators
#    a. product: returns the Cartesian product of items from an iterator,
#       which is a nice alternative to deeply nested list comprehensions.
#    b. permutations: returns ordered permutations of length N with items
#       from an iterator.
#    c. combination: returns the unordered combinations of length N with
#       unrepeated items from an iterator.

# These are even more functions and recipes available in the itertools module
# that I don't mention here. Whenever you find yourself dealing with some
# tricky iteration code, it's worth looking at the itertools documentation
# again to see whether there's anything there for you to see.


# Things to remember

# 1. Use Python's built-in modules for algorithms and data structures.
# 2. Don't re-implement this functionality yourself. It's hard to get right.
