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
- Distribution: spatially distributed workers and data that operate and may fail completely independently.

============================

=== Oct 23 ===

=== Poll ===

Review from definitions last time;
Which of the following scenarios are parallel, concurrent, and distributed?

https://forms.gle/RY4QH5utjLtww6Ur8
https://tinyurl.com/m3pvbdwe

=== Poll Answers ===

The poll wording has been slightly updated.

1. Parallel
2. Parallel + Concurrent
3. Parallel + Concurrent
4. Concurrent + Distributed
5. Parallel + Distributed
6. Parallel + Concurrent + Distributed

=== Lecture outline ===

- Last time: parallel example
- Today: concurrent + distributed examples
- Parallel thinking, types of parallelism, and quantifying
  the amount of parallelism available
- Measuring scaling & types of scaling

=== Concurrent examples ===

Recall our example above average_numbers_in_parallel.

No concurrency! (Why?)

Exercises:
Modify our example to keep track of an output.
"""

# Redefine N -- modify here as needed
N = 1000

# Shared memory between the processes
# Shared list for results
# this has to be a special Array instead of a Python
# list -- don't worry about this (impl detail)
from multiprocessing import Array

# new argument: results array
# results: a shared array of length 4
def worker3(results):
    sum = 0
    count = 0
    for i in range(N // 2):
        sum += i
        count += 1

        # Super race-y version
        # results[0] += i
        # results[1] += 1

    print(f"Worker 3 result: {sum} {count}")
    # Save the results in the shared results array
    results[0] += sum
    results[1] += count

def worker4(results):
    sum = 0
    count = 0
    for i in range(N // 2, N):
        sum += i
        count += 1

        # Super race-y version
        # results[0] += sum
        # results[1] += count

    print(f"Worker 4 result: {sum} {count}")
    # Save the results in the shared results array
    results[2] += sum
    results[3] += count

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
    sum = results[0] + results[2]
    count = results[1] + results[3]
    print(f"Average: {sum} / {count} = {sum / count}")
    print(f"Computation finished")

# Uncomment to run
# if __name__ == "__main__":
#     freeze_support()
#     average_numbers_concurrent()

"""
Now we don't just have parallelism, we have concurrency

Questions:

What do you think would happen if we modified the example so that both
processes access the same elements of the array?
(Let's try it)

Answer: it seems to work!
... But it doesn't actually work in general
... we just get lucky most of the time.
... Very very rarely, worker3 will read the value, worker4 will read it,
    then worker3 will write it, then worker4 will write it,
    and destroy worker3's work.

    This is called a race condition.

What do you think would happen if we modified the example to use the shared
results list directly for each worker's local variables?
(Let's try it)

Does something go wrong?

    Contention:

    Multiple threads or processes trying to access the same data at the
    same time causes a vast decline in performance.

    AND
    we have a race condition which, this time (unlike above)
    is actually reliably triggering every time we run the code.

    Observe that not only do some reads/writes not get counted,
    they also corrupt the data and produce completely random
    results.

    A "data race" is a particular race condition where a read
    and a write happens to the same memory location at the same
    time.

    On most architectures, a data race results in random/arbitrary/
    nondeterministic behavior.

Moral of the story:
    Don't read and write to the same data at the same time!

Which of the above is the best concurrent solution and why?

A: the first solution is best: both workers keep track of their
    results using local variables and write their answers to
    completely different indices in the shared memory array.

When parallelizing pipelines, we want to follow this principle;
generally speaking, we want different workers to be working on
- different portions of the data
- different steps in the pipeline
- producing output in different places or to different output files

So that we avoid any of the above issues.

=== Concepts ===

- Race condition: when the order in which workers complete their task
  (which one completes it first) affects the final outcome

- Data race
  A particular race condition where a read and a write happen at the same
  time and in the same memory location

- Contention
  Reduction in performance due to competing concurrent operations

- Deadlock
  Different threads try to access the same data at the same time in a way
  that prevents any thread from continuing.

- Consistency
  The ability of parallel and concurent code to behave as if it were
  sequential code.
  You want the same answers as if you just ran the code sequentially.

=== Additional exercises ===

(Probably skip)
Exercise:
Modify the example to add up a shared list instead of an iterator.
Write a version that uses (i) shared reads to the list and (ii) shared writes
to the list (for example popping off elements as they are used).
What happens?

=== Recap from today ===

We saw how code can be concurrent (not just parallel)
We saw the main problems that you can run into with concurrent code
In this class, we want to avoid all of the above problems and parallelize
in a way that avoids reading/writing to the same memory at the same time.

Next time: a very short distributed example
and then get into:
- types of parallelism (in a pipeline)
- quantifying parallelism (in a pipeline)

=======================================================

=== Oct 25 ===

=== Poll ===

1.
Two workers, threads, or processes are accessing the same shared memory variable "x". Each worker increments the variable 100 times:

    for i in range(100):
        x += 1

What are possible values of x?

2.
The scenario above exhibits... (select all that apply)
- Concurrency
- Parallelism
- Distribution
- Contention
- Deadlock
- Race condition
- Data race

https://forms.gle/wb8WEUF4fRgGcPVeA
https://tinyurl.com/3k9yeuym

=== What is distribution? ===

Distribution means that we have multiple workers and belts
**in different locations**
can process and fail independently.

The workers must be on different computers or devices.
    (Why does it matter?)

For this one, it's more difficult to simulate in Python directly.
We can imagine that our workers are computed by an external
server, rather than being computed locally on our machine.

To give a simple instance of this, let's use ssh to connect to a remote
server, then use the server to compute the sum of the numbers.

(You won't be able to use this code; it's connecting to my own SSH server!)
"""

# for os.popen to run a shell command (like we did on HW1 part 3)
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
# This won't work on your machine!
# average_numbers_distributed()

"""
Questions:

Q1: can we have distribution without parallelism?

Q2: can we have distribution with parallelism?

Q3: can we have distribution without concurrency?

Q4: can we have distribution with concurrency?

"""

"""
===== Back to parallelism! ======

Now that we know about concurrency and distribution,
at this point in the lecture, let's go back
to simple parallelism.
Also, we will move from thinking about parallelism in general
to how they are most used / most useful in data science.

Goals:

    - We want to think about parallelism at a higher-level than
      individual workers and processes

      Simply: is it parallel? how much parallelism?

    - We want massively parallel computations
      + we want fast results
        (not waiting 2 hours or 2 days to get a query result)
      + we want deployed pipelines to not
        waste money and resources

    - We want to avoid thinking about concurrency
        (why?)
        + we can do this by...

    - We want to distribute data and computations
        (why?)

        + But even when the dataset is distributed, we want to think about
          it using the same abstractions

Of course, priorities are important:

    - We still want to prototype using a sequential implementation first.

    - We still want to test on smaller datasets if needed

    - For prototypting: resort to parallelism...

    - For production: resort to parallelism...

=== Parallel thinking in data science ===

We often think about parallelism by dividing it into three types:

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
What do these types of parallelism look like on a real pipeline
rather than a toy example?

Data parallelism:

Pipeline parallelism:

Task parallelism:

Which of these is most important?
(Hint: it's not a close contest)
A:
"""

"""
=== Quantifying parallelism ===

Another way to think about parallelism:
What amount of parallelism is available in a system?

Amdahl's law:
https://en.wikipedia.org/wiki/Amdahl%27s_law

=== Standard form of the law ===



=== Example with a simple task ===



This applies to distributed computations as well!

=== Alternate form ===



=== Example with two tables ===

Let's start with a simple example:
we have two tables, of employee names and employee salaries.
We want to compute which employees make more than 1 million Euros.
The employee salaries are listed in dollars.

We are given as input the CEO name.
We want to get the salary associated with the CEO,
convert it from USD to Euros, and filter only the rows where the
result is over 1 million.
Assume all basic operations take 1 unit of time per row.

What does Amdahl's law say about our simple
average_numbers pipeline?
"""

"""
Some TODOs:

1. Rephrase in terms of running time

2. Rephrase in terms of throughput

3. Rephrase in terms of latency
"""

"""
=== Parallelizing our code in Pandas? ===

We don't want to parallelize by hand! (why? See problems with concurrency above)

Dask is a simple library that works quite well for parallelizing datasets
on a single machine as a drop-in replacement for Pandas.
"""

# conda install dask or pip3 install dask
# import dask

def dask_example():
    # Example dataset
    df = dask.datasets.timeseries()

    # Dask is lazy -- it only generates data when you ask it to.
    # (More on laziness later).
    print(type(df))
    print(df.head(5))

    # Use a standard Pandas filter access
    df2 = df[df.y > 0]
    print(type(df2))
    print(df2.head(5))

    # Do a group by operation
    df3 = df2.groupby("name").x.mean()
    print(type(df3))
    print(df3.head(5))

    # Compute results -- this processes the whole dataframe
    print(df3.compute())

# Uncomment to run.
# dask_example()

"""
=== End note: vertical vs. horizontal scaling ===

- Vertical: scale "up" resources at a single machine (hardware, parallelism)
- Horizontal: scale "out" resources over multiple machines (distribution)

This lecture, we have only seen *vertical scaling*.
But vertical scaling has a limit!
Remember that we are still limited in the size of the dataset we can
process on a single machine
(recall Wes McKinney estimate of how large a table can be).
Even without Pandas overheads,
we still can't process data if we run out of memory!

So, to really scale we may need to distribute our dataset over many
machines -- which we do using a distributed data processing framework
like Spark.
This also gives us a convenient way to think about data pipelines
in general, and visualize them.
We will tour PySpark in the next lecture.

In addition to scaling even further, distribution can offer an even
more seamless performance compared to parallelism as it can eliminate
many coordination overheads and contention between workers
(see partitioning: different partitions of the database are operated entirely independently by different machines).
"""
