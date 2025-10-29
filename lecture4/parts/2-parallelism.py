"""
Part 2: Definitions and Parallel/Concurrent Distinction

Parallel computing: speeding up our pipeline by doing more than
one thing at a time!

=== Getting Started ===

Parallel, concurrent, and distributed computing

They're different, but often get (incorrectly) used synonymously!

What is the difference between the three?

Let's make a toy example.

We will forgo Pandas for this lecture
and just work in plain Python for the sake of clarity,
but all of this applies to a data processing pipeline written using
vectorized operations as well (as we will see soon).

Baseline:
(sequential pipeline)

    Sequential means "not parallel", i.e. one thing happening at a time,
    run on a single worker.

(Rule 0 of parallel computing:
Any time we're measuring parallelism we want to start
with a sequential version of the code!)

    Scalability! But at what COST?
    https://www.usenix.org/system/files/conference/hotos15/hotos15-paper-mcsherry.pdf

Q: can I think of sequential computing like a monolithic application,
and parallel computing like microservices?

    That's related to the distibuted computing part - we'll talk more about
    the difference between parallel/distributed soon.

For now think of:

    Sequential baseline = 1 machine, only 1 CPU runs (1 worker)

    Parallel = multiple workers (machines or CPUs)
"""

def average_numbers(N):
    sum = 0
    count = 0
    for i in range(N):
        # Busy loop with some computation in it
        sum += i
        count += 1
    return sum / count

# Uncomment to run:
# N = 200_000_000
# result = average_numbers(N)
# print(f"Result: {result}")

# baseline (Sequential performance) is at 9.07s

# From the command line:
# time python3 lecture.py

# How are we doing on CPU usage:
# Activity Monitor in MacOS (Window -> CPU Usage)

"""
Task gets moved from CPUs from time to time, making it a little difficult to see,
but at any given time one CPU is being used to run our program.

What if we want to do more than one thing at a time?

Let's say we want to make our pipeline twice as fast.

We're adding the numbers from 1 to N... so we could:

- Have worker1 add up the first half of the numbers

- Have worker2 add up the second half

At the end, combine worker1's and worker2's results

Our hope: we take about half the time to complete the computation.

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

# time python3 lecture.py: 5.2s
# CPU usage

"""
New result: roughly half the time! (Twice as fast)

Not exactly twice as fast - why?

    One reason is because of the additional boilerplate required
    to run multiple workers and combine the results.

    We actually didn't combine the results!
    (We should add the results from worker1 and worker2)
    This would also add a small amount of overhead

We've successfully achieved parallelism!
We have two workers running at the same time.

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

    There are multiple workers working at the same time.

The workers could be working on the same conveyor belt
or two different conveyor belts

Worker1 and worker2 are working on separate conveyer belts!

    ==>   | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 |   ==>
    ...   ==========================================  worker1

    ==>   |  | ... | 1000002 | 1000001 | 1000000 |   ==>
    ...   ==========================================  worker2

=== What is concurrency? ===

Concurrency is when there are multiple tasks happening that might overlap or conflict.

- If the workers are working on the same conveyer belt ... then operations might conflict

- If the workers are working on different conveyer belts ... then operations won't conflict!

----- Where we ended for today -----

-----------------------------

Oct 29
(Finishing up a few things)

Recap:

- Once our pipeline is working sequentially, we want to figure
  out how to **scale** to more data and more frequent updates

- We talked about parallelism: multiple workers working at once

- Conveyer belt analogy:
    parallel = multiple workers working at the samt eim.

=== Related definitions and sneak peak ===

Difference between parallelism & concurrency & distribution:

- Parallelism: multiple workers working at the same time
- Concurrency: multiple workers accessing the same data (even at different times) by performing potentially conflicting operations

    For now: think about it as multiple workers modifying or moving items
    on the same conveyer belt.

- Distribution: workers operating over multiple physical devices which are independently controlled and may fail independently.

Good analogy:
    Distributed computing is like multiple warehouses, each with its own
    workers and conveyer belts.

For the purposes of this class: if code is running on multiple devices,
it is distributed; otherwise it's not.

In the conveyor belt analogy, this means...

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

- Both parallelism and concurrency can exist with/without distribution!

    Are the different conveyer belts operated by different computers?
    Do they function and fail independently?

    Are the different workers running on different computers?
    Do they function and fail independently?
"""
