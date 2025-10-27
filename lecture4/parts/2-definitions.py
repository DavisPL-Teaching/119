"""
Part 2: Definitions and Parallel/Concurrent Distinction

=== Getting Started ===

Parallel, concurrent, and distributed computing

What is the difference between the three?

Let's make a toy example.

We will forgo Pandas for this lecture
and just work in plain Python for the sake of clarity,
but all of this applies to a data processing pipeline written using
vectorized operations as well (as we will see soon).

Baseline:
(sequential pipeline)

(Rule 0 of parallel computing:
Any time we're measuring parallelism we want to start
with a sequential version of the code!)

    Scalability! But at what COST?
    https://www.usenix.org/system/files/conference/hotos15/hotos15-paper-mcsherry.pdf
"""

def average_numbers(N):
    sum = 0
    count = 0
    for i in range(N):
        sum += i
        count += 1
    return sum / count

# Uncomment to run:
# N = 200_000_000
# result = average_numbers(N)
# print(f"Result: {result}")

# baseline (Sequential performance) is at 6.7s

# From the command line:
# time python3 lecture.py

# How are we doing on CPU usage:
# Activity Monitor in MacOS (Window -> CPU Usage)

"""
=== What is parallelism? ===

Imagine a conveyor belt, where our numbers are coming in on the belt...

ASCII art:

    ==>   | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 |   ==>
    ...   ==========================================  worker1
                                                      worker2

Our worker takes the items off the belt and
adds them up as they come by.

Worker:
    (sum, count)
    (0, 0) -> (1, 1) -> (3, 2) -> (6, 3) -> (10, 4) -> ...

When is this parallel?



The workers could be working on the same conveyor belt
or two different conveyor belts

Example:
"""

# **************************************
# ********** Ignore this part **********
# **************************************

# NOTE: Python has something called a global interpreter lock (GIL)
# which often prevents code from running in parallel (via threads)
# We are using this purely for illustration, but Python is generally
# not a good fit for parallel and concurrent code.

from multiprocessing import Process, freeze_support

def run_in_parallel(*tasks):
    running_tasks = [Process(target=task) for task in tasks]
    for running_task in running_tasks:
        running_task.start()
    for running_task in running_tasks:
        result = running_task.join()

# **************************************
# **************************************
# **************************************

def worker1():
    sum = 0
    count = 0
    for i in range(N // 2):
        sum += i
        count += 1
    print(f"Worker 1 result: {sum} {count}")
    # return (sum, count)

def worker2():
    sum = 0
    count = 0
    for i in range(N // 2, N):
        sum += i
        count += 1
    print(f"Worker 2 result: {sum} {count}")
    # return (sum, count)

def average_numbers_parallel():
    results = run_in_parallel(worker1, worker2)
    print(f"Computation finished")

# Uncomment to run
# N = 200_000_000
# if __name__ == '__main__':
#     freeze_support() # another boilerplate line to ignore
#     average_numbers_parallel()

# time python3 lecture.py
# CPU usage

"""
=== What is concurrency? ===

Concurrency is when there are multiple tasks happening that might overlap or conflict.

In a conveyor belt, this means...




- Parallelism can exist without concurrency!
  (How?)

    Multiple belts, each worker has its own belt

- Concurrency can exist without parallelism!
  (How?)

    Operations can conflict even if the two workers
    are not working at the same time!

    Worker1 takes an item off the belt
    Worker1 makes some modifications and puts it back
    Then Worker 1 goes on break
    Worker2 comes to the belt
    Doesn't realize that worker 1 was doing anything here
    Takes the item off the belt
    Worker 2 tries to make the same modifications.

    We have a conflict!

    In fact, this is what happens in Python if you
    use threads.
    (Threads vs. processes)

    Multiple workers working concurrently, only one
    active at a given time.

=== Recap and sneak peak ===

Once our pipeline is working sequentially, we want to figure
out how to **scale** to more data and more frequent updates

We talked about parallelism: multiple workers working at once

Difference between parallelism & concurrency & distribution:
- Parallelism: multiple workers working at the same time
- Concurrency: multiple workers accessing the same data or performing potentially conflicting operations
- Distribution: spatially distributed workers and data that operate and may fail completely independently.

=======================================================
"""
