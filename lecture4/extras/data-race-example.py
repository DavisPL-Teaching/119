"""
Data race example:
Runnable code for the example from the Oct 30 in-class poll.

Also discusses the relationship between data races and UB.

This is a subtle topic!
TL;DR:

- In Python, x could be a value between 2 and 200 using multiprocess or multiprocessing libraries (see below). This is the case that was asked about on the poll. You can try running the code below and see that values under 200 are possible.

- In general - making no assumptions about the programming language implementation of += or the underlying architecture - data races are often considered "undefined behavior". Accounting for this undefined behavior, x could be any integer value. In a language with undefined behavior: *if there is a read and a write concurrently to the same data (or two concurrent writes), the value of that data is indeterminate.*

Longer discussion:

Try running the example! What happens?

- We generally get a value between 100 and 200 in all test runs
  (often 10 or 20 for the N = 10 case -- sometimes some value in between!)

- However! Values between 2 and 100 are also technically possible. It's very rare
  to see these on a test run for statistical reasons - in fact I ran this code
  dozens of times and I still have not been able to observe this behavior on a real
  run. However, it is still technically possible.

- We do observe a data race in this code
  (if there were no data race, all += 1s would happen, and the value would always end up at 200).

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
