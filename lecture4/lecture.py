"""
Lecture 4: Parallelism

=== Poll ===

- Definition of a data operator

- (Dis)advantages of Pandas

https://forms.gle/3syqeqUwqTi6LBAP6
https://tinyurl.com/3az4pfx3

===== Introduction =====

So far, we know how to set up a basic working data processing pipeline
for our project:

- We have a prototype of the input, processing, and output stages (Lecture 1)

- We have used scripts and shell commands to download any necessary
  data, dependencies, and set up any other system configuration (Lecture 2)
  (running these automatically if needed, see HW1 part 3)

- We have used a vectorized internal memory representation to represent
  the data in-memory in the processing stage (Lecture 3)
  (for a review on vectorization, see discussion section and HW1 part 2)

The next thing we need to do is **scale** our application.

=== Why scaling? ===

Basically we should scale if we want one of two things:

1. Running on **more** input data
    e.g.:
    + training your ML model on the entire internet instead of a dataset of
      Wikipedia pages you downloaded to a folder)
    + update our population pipeline to calculate some analytics by individual city,
      instead of just at the country or continent level

2. Running **more often** or on **more up-to-date** data
    e.g.:
    + re-running your pipeline once a day on the latest analytics;
    + re-running every hour to ensure the model or results stay fresh; or even
    + putting your application online as part of a live application
      that responds to input from users in real-time
      (more on this later in the quarter!)

Why might you want to do this?

- Biggest difference between a toy project and industry!

- More data ==
    more accurate models
    more precise results
    more insight that can guide decisions

- Example: GPT-4
    + trained on roughly 13 trillion tokens
    + 25 though A100 processors
    + span of 3 months
    + over $100M cost according to Sam Altman
    https://www.kdnuggets.com/2023/07/gpt4-details-leaked.html
    https://en.wikipedia.org/wiki/GPT-4

- Contrast:
    our population dataset is roughly 60,000 lines and roughly 1.6 MB on disk.

=== What is scalability? ===

Scalability is the ability of a computer system to handle an increasing amount of work.

Points:

- We can think of scaling in terms of throughput and latency

    See scaling/ folder for some examples!

- Typically, we talk about "linear scaling" which means the amount of time it will
take your system to proces N input data items is O(N)
(constant throughput!)
When we talk about scaling, we are looking for something better than O(N).

Disdavantage of Pandas: does not scale!

- Wes McKinney, the creator of Pandas:
    "my rule of thumb for pandas is that you should have 5 to 10 times as much RAM as the size of your dataset"

    https://wesmckinney.com/blog/apache-arrow-pandas-internals/

Exercise:

    Check how much RAM your personal laptop has.
    According to McKinney's estimate, how much how large of a dataset in population.csv
    could your laptop handle?

- NVIDIA stock:

    https://www.google.com/finance/quote/NVDA:NASDAQ?window=5Y

===== Getting started: Some Definitions and Examples =====

Parallel, concurrent, and distributed computing

What is the difference between the three?

Let's make a toy example.

We will forgo Pandas for this lecture
and just work in plain Python for the sake of clarity,
but all of this applies to a data processing pipeline written using
vectorized operations as well (as we will see soon).

Baseline:
"""

def average_numbers(N):
    sum = 0
    count = 0
    for i in range(N):
        # TODO
        raise NotImplementedError

# Uncomment to run:
# N = 200_000_000
# result = average_numbers(N)
# print(f"Result: {result}")

# From the command line:
# time python3 lecture.py

# How are we doing on CPU usage:
# Activity Monitor in MacOS (Window -> CPU Usage)

"""
=== What is parallelism? ===

Imagine a conveyor belt, where our numbers are coming in on the belt...

ASCII art:

    ==>   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |   ==>
    ...   ==========================================   ...

Our worker takes the items off the belt and
adds them up as they come by.

Worker:
    (sum, count)
    (0, 0) -> (1, 1) -> (3, 2) -> (6, 3) -> (10, 4) -> ...

Parallelism is when there are **multiple workers working at the same time.**

Example:
"""

# **************************************
# ********** Ignore this part **********
# **************************************

# NOTE: Python has something called a global interpreter lock (GIL)
# which often prevents code from running in parallel (via threads)
# and for this reason, is not a good fit for writing parallel code
# without a good supporting library.
# The following is just for illustration purposes.
# Basically, don't try this at home. :)

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

# TODO delete
def average_numbers(N):
    sum = 0
    count = 0
    for i in range(N):
        sum += i
        count += 1
    return sum / count

N = 200_000_000
result = average_numbers(N)
print(f"Result: {result}")

def worker1():
    sum = 0
    count = 0
    for i in range(N // 2):
        sum += i
        count += 1
    print(f"Worker 1 result: {sum} {count}")
    return (sum, count)

def worker2():
    sum = 0
    count = 0
    for i in range(N // 2, N):
        sum += i
        count += 1
    print(f"Worker 2 result: {sum} {count}")
    return (sum, count)

def average_numbers_parallel():
    results = run_in_parallel(worker1, worker2)
    print(f"Computation finished")

# Uncomment to run
# if __name__ == '__main__':
#     freeze_support()
#     average_numbers_parallel()

# time python3 lecture.py
# CPU usage

"""
Exercise:
Modify our example to compute output
"""

"""
=== What is concurrency? ===

Concurrency is when there are conflicting or out-of-order operations happening.

In a conveyor belt, it means multiple workers are taking items off the belt.

- Concurrency can exist without parallelism!
  (How?)

- Parallelism can exist without concurrency!
  (How?)

Exercise: write a version of the previous example
that accesses values concurrently.

Write a versio of the previous example that
updates values concurrently.

What are potential dangers here?
"""

def average_numbers_concurrent_reads(l):
    # TODO
    pass

def average_numbers_concurrent_writes(l):
    # TODO
    pass

"""
Was there concurrency in our previous example?
"""

"""
=== What is distribution? ===

Distribution means that we have multiple workers and/or belts
**in different locations**
can process and fail independently.

For this one, it's more difficult to simulate in Python directly.
We can imagine that our workers are computed by an external
server, rather than being computed locally on our machine.
"""

def worker1_distributed():
    raise NotImplementedError

def worker2_distributed():
    raise NotImplementedError

def average_numbers_distributed():
    # TODO: pretend to call AWS lambda
    raise NotImplementedError

# average_numbers_distributed()
# TODO:

"""
Questions:

Q1: can we have distribution without parallelism?

Q2: can we have distribution without concurrency?

"""

"""
===== Parallel thinking =====

How do we think about parallelism?

What amount of parallelism is available in a system?

Amdahl's law:
https://en.wikipedia.org/wiki/Amdahl%27s_law

Some TODOs:

1. Rephrase in terms of running time

2. Rephrase in terms of throughput

3. Rephrase in terms of latency
"""
