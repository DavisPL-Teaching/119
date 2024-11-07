"""
This is the data race example from the Oct 25
in-class poll, since some of you have asked about it,
and it is worth going into in more detail:

https://forms.gle/NnC2EF5mNBaisHPF6

This is a subtle topic!
TL;DR: The following are both correct:

- x will always between 100 and 200 in Python using multiprocess (multiprocess.Array and multiprocess.Value)

- x could be any integer value making no assumptions about the programming language implementation of += or the underlying architecture.

The latter bullet (any value) is also the technically correct answer in C/C++, where data races are something called "undefined behavior", meaning that the compiler is allowed to compile your code to do something entirely different than what you said.
(And it may depend on the compiler!)

This is why I want you to think about this is with the following simplified view:

    *if there is a read and a write concurrently to the same data (or two concurrent writes), the value of that data is indeterminate.*

Longer discussion:

Try running the example! What happens?

As some of you suspected, in our Python implementation (using multiprocess), it happens to be the case that:

- when run, the result is a value between 100 and 200 in all test runs
  (often 10 or 20 for the N = 10 case -- sometimes some value in between!)

- we do observe a data race
  (if there were no data race, all += 1s would happen, and the value would always end up at 200)

So why did I say that x can be *any* value?

This has to do with what assumptions we are making about how Python represents integers
-- for example, assuming that it consistently handles reads and writes to integers (+= consistently).
This assumption is very dangerous! It is generally *not* true when using operations that aren't designed to be safely called in a concurrent programming context,
such as big integers. (A Python integer is not just a single byte, it contains multiple bytes! That makes it something called a big integer. It may be the case that a read and a write to a Python integer at the same time don't just execute one after the other, but actually completely invalidate that integer, by modifying the different bytes in different ways -- or even, moving the integer somewhere else in memory.
If there is time or during a make-up lecture, I will do an example of this in more detail.)

This actually occurs and is not just a hypothetical:

    - It will occur in Python when using data structures more than just a single byte

    - It will occur in any data structure implementation in C, C++, or Java or any implementation that stores raw pointers in memory.

That's why the way I want you to think about data races in this class
is with the "simplified view" above.
That is, data races cause data to be invalidated and it could represent any value after the race occurs.

Further reading:

- Why += 1 is so-called "undefined behavior" (UB) in C: https://stackoverflow.com/a/39396999/2038713

- More on "undefined behavior" and why:
  https://news.ycombinator.com/item?id=16247958
  https://davmac.wordpress.com/2018/01/28/understanding-the-c-c-memory-model/

- Data races in Python: https://verdagon.dev/blog/python-data-races
  which does not discuss the UB issue.
"""

import ctypes
from multiprocessing import RawValue, Process, freeze_support

N = 100

# Comment out other examples to try:
# N = 1
# N = 10
# N = 10_000_000

def worker1(x):
    for i in range(N):
        x.value += 1

def worker2(x):
    for i in range(N):
        x.value += 1

if __name__ == "__main__":
    # Guard to ensure only one worker runs the main code
    freeze_support()

    # Set up the shared memory
    start = 0
    x = RawValue(ctypes.c_uint64, start)
    print(f"Start value: {x.value}")

    # Run the two workers
    p1 = Process(target=worker1, args=(x,))
    p2 = Process(target=worker2, args=(x,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    # Get the result
    print(f"Final result: x = {x.value}")
