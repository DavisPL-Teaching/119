"""
Lecture 4: Parallelism

(Oct 21)

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

=== What is scaling? ===

Scalability is the ability of a computer system to handle an increasing amount of work.

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
    + 25,000 A100 processors
    + span of 3 months
    + over $100M cost according to Sam Altman
    https://www.kdnuggets.com/2023/07/gpt4-details-leaked.html
    https://en.wikipedia.org/wiki/GPT-4

- Contrast:
    our population dataset is roughly 60,000 lines and roughly 1.6 MB on disk.

=== Thinking about scalability ===

Points:

- We can think of scaling in terms of throughput and latency

    See scaling/ folder for some examples!

    If your application is scaling successfully,
    double the # of processors => double the throughput
    (best case scenario)

- Sequential (non-parallel) applications exhibit
"linear scaling" which means the amount of time it will
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

Amount of RAM: 16GB (x4), 8GB (x2), 18GB,

Mode answer: 16GB
We can process: 1.6GB-3.2GB of data

    population.csv was 1.6MB

roughly, we can process like a 1000X as much data
and then we'll a bottleneck.

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
(sequential pipeline)

(Rule 0 of parallel computing:
Any time we're measuring parallelism we want to start
with a sequential version of the code!
Scalability! But at what COST?
https://www.usenix.org/system/files/conference/hotos15/hotos15-paper-mcsherry.pdf
)
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

Parallelism is when there are **multiple workers working at the same time.**

The workers could be working on the same conveyor belt
or two different conveyor belts

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

N = 200_000_000

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
# if __name__ == '__main__':
#     freeze_support() # another boilerplate line to ignore
#     average_numbers_parallel()

# time python3 lecture.py
# CPU usage

"""
=== What is concurrency? ===

Concurrency is when there are conflicting or out-of-order operations happening.

In a conveyor belt, it means multiple workers are taking items off the belt.

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
- Distribution: spatially distributed workers and belts that operate and may fail completely independently.

============================

=== Oct 23 ===

=== Poll ===

Review from definitions last time;
Which of the following scenarios are parallel, concurrent, and distributed?

https://forms.gle/RY4QH5utjLtww6Ur8
https://tinyurl.com/m3pvbdwe

=== Lecture outline ===

- Last time: parallel example
- Today: concurrent + distributed examples
- Parallel thinking and Amdahl's Law
- Measuring scaling & types of scaling

=== Concurrent examples ===

Recall our example above average_numbers_in_parallel.

No concurrency! (Why?)

Exercises:
Modify our example to keep track of an output.
"""

# Redefine N -- modify here as needed
N = 200_000_000

# Shared list for results
from multiprocessing import Array

# new argument: results array
# results: a shared array of length 4
def worker3(results):
    sum = 0
    count = 0
    for i in range(N // 2):
        sum += i
        count += 1
    print(f"Worker 3 result: {sum} {count}")
    # TODO: modify for concurrent implementation

def worker4(results):
    sum = 0
    count = 0
    for i in range(N // 2, N):
        sum += i
        count += 1
    print(f"Worker 4 result: {sum} {count}")
    # TODO: modify for concurrent implementation

def average_numbers_concurrent():
    # Create a shared results array
    # i = integer, d = double (we use d here because the integers suffer from overflow)
    results = Array('d', range(4))

    # Iniitalize our shared array
    results[0] = 0
    results[1] = 0
    results[2] = 0
    results[3] = 0

    # Like run_in_parallel but with added code to handle arguments
    p1 = Process(target=worker3, args=(results,))
    p2 = Process(target=worker4, args=(results,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    # Calculate results
    print(f"Thread results: {results[:]}")
    # TODO: fill in
    # print(f"Result: {sum} / {count} = {sum / count}")
    print(f"Computation finished")

# Uncomment to run
# if __name__ == "__main__":
#     freeze_support()
#     average_numbers_concurrent()

"""
Questions:

What do you think would happen if we modified the example so that both
processes access the same variables?
(Let's try it)

What do you think would happen if we modified the example to use the shared
results list directly for each worker's local variables?
(Let's try it)

Does something go wrong?

Which of the above is the best concurrent solution and why?

=== Concepts ===

- Race condition
- Data race
- Contention
- Deadlock
- Consistency

=== Additional exercises ===

(Probably skip)
Exercise:
Modify the example to add up a shared list instead of an iterator.
Write a version that uses (i) shared reads to the list and (ii) shared writes
to the list (for example popping off elements as they are used).
What happens?
"""

"""
=== What is distribution? ===

Distribution means that we have multiple workers and/or belts
**in different locations**
can process and fail independently.

For this one, it's more difficult to simulate in Python directly.
We can imagine that our workers are computed by an external
server, rather than being computed locally on our machine.

To give a simple instance of this, let's use ssh to connect to a remote
server, then use the server to compute the sum of the numbers.

(You won't be able to use this code; it's connecting to my own SSH server!)
"""

import os

def ssh_run_command(cmd):
    result = os.popen("ssh cdstanfo@set.cs.ucdavis.edu " + cmd).read()
    # Just print the result for now
    print(f"result: {result.strip()}")

def worker1_distributed():
    ssh_run_command("seq 1 1000000 | awk '{s+=$1} END {print s}'")
    print("Worker 1 finished")

def worker2_distributed():
    ssh_run_command("seq 1000001 2000000 | awk '{s+=$1} END {print s}'")
    print("Worker 2 finished")

def average_numbers_distributed():
    worker1_distributed()
    worker2_distributed()
    print("Distributed computation complete")

# Uncomment to run
# average_numbers_distributed()

"""
Questions:

Q1: can we have distribution without parallelism?

Q2: can we have distribution with parallelism?

Q3: can we have distribution without concurrency?

Q4: can we have distribution with concurrency?

"""

"""
===== Parallel thinking =====

At this point in the lecture, we will
move from thinking about parallel, concurrent, and distributed programming in general
to how they are most used / most useful in data science.

- Higher-level viewpoint & what matters
- Thinking about parallelism in your pipeline
- Quantifying parallelism in your pipeline

=== Higher-level viewpoint ===

In the context of data pipelines and data science,
we're often thinking in terms of data sets

    - We want massively parallel computations

    - We want to avoid thinking about concurrency
        (how?)

    - We are often forced to distribute computations
        (why?)

        + But even when the dataset is distributed, we want to think about
          it using the same abstractions

We care the most about parallelism!

Of course, priorities are important:

    - We want to prototype using a sequential implementation first.

    - We may want to test on smaller datasets if needed

    - For prototypting: resort to parallelism...

    - For production: resort to parallelism...

How do we think about parallelism?

=== Parallel thinking in data science ===

Types of parallelism:

- Data parallelism

- Task parallelism

- Pipeline parallelism

Which of these is our average_numbers computation?

Exercise:
Write an example of each of the others.
"""

def average_numbers_task_parallelism():
    # TODO
    raise NotImplementedError

def average_numbers_pipeline_parallelism():
    # TODO
    # This is harder!
    raise NotImplementedError

"""
=== Quantifying parallelism ===

What amount of parallelism is available in a system?

Amdahl's law:
https://en.wikipedia.org/wiki/Amdahl%27s_law

Some TODOs:

1. Rephrase in terms of running time

2. Rephrase in terms of throughput

3. Rephrase in terms of latency
"""
