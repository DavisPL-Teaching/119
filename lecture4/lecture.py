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
**in different physical locations**
can process and fail independently.

The workers must be on different physical computers or physical devices.
    (Why does it matter?)

    Running on the same physical device, both workers have
    access to the same resources;
    Running on two different devices, they access different resources, and one worker could crash even if the other
    one doesn't.
    So, it introduces new challenges.

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

# This waits until the first connection finishes before
# starting the next connection; but we could easily modify
# the code to make them both run in parallel.

"""
Questions:

Q1: can we have distribution without parallelism?

    A: Yes, we just did

Q2: can we have distribution with parallelism?

    A: Yes, we could allow the server to run and compute
    an answer while we continue to compute other stuff,
    or while we run a separate connection to a second
    server.

Q3: can we have distribution without concurrency?

    A: Yes, for example we send a single task to the
    server and let it complete that task

    A: Even simpler: we have two databases or database
    partitions running separately (and they don't interact)

Q4: can we have distribution with concurrency?

    Yes, we often do, for example when distributed workers
    communicate via passing messages to each other
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
        (why?: concurrency comes with lots of pains,
         including data races, contention, etc.)
        + we can do this by relying on libraries that
          others have built to solve concurrent programming
          problems and to parallelize safely.
          + how those libraries work: they avoid
            reading and writing to the same data at the
            same time.

    - We want to distribute data and computations
        (why?)
        parallelization happens on a single machine,
        distributed code enables us to scale even further.

        + But even when the dataset is distributed, we
          don't want to worry about concurrency and implementation
          details.

Of course, priorities are important:

    - We still want to prototype using a sequential implementation first.

    - We still want to test on smaller datasets if needed

    - For prototypting: resort to parallelism
        if you need it for fast query results

    - For production: resort to parallelism
        if it's faster, cheaper, and more efficient

=== Parallel thinking in data science ===

We've written our pipeline:
Q1: Is it parallel?
Q2: How much parallelism?

About Q1:

We often think about parallelism by dividing it into three types:

- Data parallelism

    This is the most important one

    Different parts of your dataset can be processed in parallel.

    Example 1: imagine an SQL query where you need to match
    the employee name with their salary

    Different rows in the input: I can match one employee
    name totally independently from another employee name --
    these tasks can be done in parallel!
    That's data parallelism.

    Example 2: In our running example, we were adding up
    the numbers between 1 and 20,000,000.
    We notice that we can add up the numbers between
    1 and 10,000,000 and the numbers betweeen
    10,000,001 and 20,000,000 separately!
    That's data parallelism.

    ----> i.e. same task, different data points

- Task parallelism

    Different tasks can be done in parallel.

    ----> i.e. different task, potentially same data points

    ----> the two tasks aren't dependent on each other.

    Example 1: You have an SQL query where you want
    to compute the employee with the highest salary
    and the employee with the lowest salary.

    You might realize that you can compute highest
    with one query, and lowest with a separate query,
    and these two queries can be done in parallel.

    Example 2: Going back to our running example,
    avg. of the first 200,000,000 integers
    we could compute the sum with one worker,
    and the count with the other worker.
    That's task parallelism.

- Pipeline parallelism

    (The last type of parallelism is the most strange)
    It's that if two tasks are done in sequence,
    we can still benefit (surprisingly) from parallelism!

    (dataset) --> task 1 --> (output 1) --> task 2 --> (output 2)

    Example: Take our dataset of employees, for each employee
    name, strip the spaces from the name, then extract the first
    name, then extract the last letter of the first name,
    and save that to an output data frame.

    This is a pipeline of tasks:
    -> I have to strip the spaces before I extract the first name
    -> I have to extract the first name before I can get the last letter
    -> I have to get the last letter before I can save it to the output data frame

    (dataset) --> task 1 --> task 2 --> task 3 --> task 4

    It doesn't seem like there's any parallelism here!
    But there is.

              task 1     task 2     task 3     task 4
    input 1:    1          2          3          4
    input 2:    2          3          4          5
    input 3:    3          4          5          6

    That's pipeline parallelism!

***** Ended here for Oct 25 *****

============================================

===== Oct 30 =====

Recap:
We saw some examples (without writing code)
of data parallelism, task parallelism, and pipeline parallelism.

We saw that our original average_numbers computation exploited data parallelism.

Let's do a poll to review.

=== Poll ===

Which types of parallelism are present in the following scenario? (select all that apply)

A Python script needs to:
- load a dataset into Pandas: students.csv, with 100 rows
- calculate a new column which is the total course load for each student
- send an email to each student with their total course load

https://forms.gle/bfbjmwhJHgWqRRux8
https://tinyurl.com/5kvanhwv

Answer: data + pipeline parallelism, no task parallelism in the pipeline as described.

Visual aid (we'll come back to this very soon in lecture 5! Helpful way to think about it:)

    Draw out the tasks your pipeline needs to compute as nodes, and dependencies between them
    as arrows between the nodes

    (load dataset) -> (calculate a new column) -> (send an email to each student)

    (This is something called a dataflow graph)

    Data parallelism exists if a single node in the pipeline can be done in parallel over
    its inputs

    Task parallelism exists if there two nodes that can be run in parallel without an arrow between them

    Pipeline parallelism exists if there are two nodes that can be run in parallel with an arrow between them.

=== Exercises ===

Exercise: Let's write some actual code.

1. Write a version of our average_numbers pipeline that exploits task parallelism.

We will start with a skeleton of our code from the concurrent example.
"""

# Redefine N again
N = 100_000_000

def worker5(results):
    sum = 0
    for i in range(N):
        sum += i

    results[0] = sum

def worker6(results):
    count = 0
    for i in range(N):
        count += 1

    results[1] = count

"""
**pictoral model** (dataflow graph)

    (input) --> (sum)
                         --> (compute average)
    (input) --> (count)
"""
def average_numbers_task_parallelism():
    # Create a shared results array
    # i = integer, d = double (we use d here because the integers suffer from overflow)
    results = Array('d', range(2))

    # Iniitalize our shared array
    results[0] = 0
    results[1] = 0

    # Like run_in_parallel but with added code to handle arguments
    p1 = Process(target=worker5, args=(results,))
    p2 = Process(target=worker6, args=(results,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    # Calculate results
    sum = results[0]
    count = results[1]
    print(f"Average: {sum} / {count} = {sum / count}")
    print(f"Computation finished")

# Uncomment to run
# if __name__ == "__main__":
#     freeze_support()
#     average_numbers_task_parallelism()

"""
2. Write a version of our average_numbers pipeline that exploits pipeline parallelism.
    (This one will be a bit more contrived)

If we want to exploit pipeline parallelism...

    we should have one worker produce as input the integers,
    and one worker process those integers!
"""

# Redefine N again
N = 1_000_000

def worker7(results):
    # Worker 7 is responsible for loading the input
    # (In our toy example, "loading" just means going through
    # a Python range)
    # and putting into a shared array
    for i in range(N):
        results[i] = i

    print("Worker 7 complete")

def worker8(results):
    # We need to read the output from worker 7!

    i = 0
    sum = 0
    count = 0
    while i < N:
        # Wait for the input at index i
        # There are more efficient ways to do this,
        # but let's do what's called a "busy wait" -- means
        # we just keep running through the loop until the input
        # arrives.
        if results[i] == -1:
            # print(f"Worker loop: if case {i}")
            # Worker 7 hasn't gotten us our input yet!
            # pass
            continue
        else:
            # print(f"Worker loop: else case {i}")
            # Worker 7 has given us our input -- we can continue
            sum += results[i]
            count += 1
            # Make progress -- move on to the next item
            i += 1

    print(f"Average: {sum} / {count} = {sum / count}")
    print(f"Worker 8 finished")

def average_numbers_pipeline_parallelism():
    # Create a shared results array
    # i = integer, d = double (we use d here because the integers suffer from overflow)
    results = Array('d', range(N))

    # Iniitalize our shared array
    for i in range(N):
        results[i] = -1

    # Like run_in_parallel but with added code to handle arguments
    p1 = Process(target=worker7, args=(results,))
    p2 = Process(target=worker8, args=(results,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    # Calculate results
    # -- we don't need to do anything here -- we did this logic in Worker 8.
    print("Computation finished.")

# Uncomment to run
if __name__ == "__main__":
    freeze_support()
    average_numbers_pipeline_parallelism()

"""
It works!
And it illustrates the basic idea of pipeline parallelism.

BUT: there is 1 potential problem here, does anyone see it?

Remember that read + a write to the same memory at the same time
is dangerous. (That's called a data race)

It's not clear whether this actually causes a bug in our pipeline,
(it depends on the architecture and the implementation of Array),
but this could potentially cause arbitrary behavior or random data
to be saved into the array, we saw this in a previous example.
"""

"""
(Skip)
What do these types of parallelism look like on a real pipeline
rather than a toy example?

Data parallelism:

Pipeline parallelism:

Task parallelism:

Which of these is most important in the real world?
(Hint: it's not a close contest)

A: Data parallelism.

Example: You may be doing 10-15 different tasks as part of your pipeline,
but if your pipeline is 10 million items large, 10-15 is very small
compared to the size of your pipeline.

For this reason, data parallelism is the main focus of most
parallel and distributed data processing frameworks.
(Again, looking forward to lecture 5).
"""

"""
=== Quantifying parallelism ===

We know how to tell *if* there's parallelism.
What about *how much*?

    i.e.: What amount of parallelism is available in a system?

Definition:
**Speedup** is defined by:
    (running time of sequential code) / (running time of parallel code)

example:
    4.6s for parallel impl
    9.2s for sequential impl

Speedup would be 2x.

Fundamental law of parallelism:
Amdahl's law:
https://en.wikipedia.org/wiki/Amdahl%27s_law

Amdahl's law gives an upper bound on the amount of speedup that is possible for any task.

***** End here for Oct 30. *****
===============================================

=== Standard form of the law ===

Suppose we have a computation that exhibits one or more types of parallelism.
The amount of speedup in a computation is at most

    1 / (1 - p)

where:

    p is ....

=== Example with a simple task ===

We have written a complex combination of C and Python code to train our ML model.
95% of the code can be fully parallelized, however there is a 5% of the time of the code
that is spent parsing the input model file and producing as output an output model file
that we have determined cannot be parallelized.

Q: What is the maximum speedup for our code?

=== Alternate form ===

Here is an alternative form of the law that is equivalent, but sometimes a bit more useful.
Let:
- T be the total amount of time to complete a task
- S be the amount of time to compute some inherently sequential portion of the task

Then the maximum speedup of the task is at most

    (T / S).

Note: this applies to distributed computations as well!

=== More examples ===

1. Let's take our data parallelism example:
- imagine an SQL query where you need to match
  the employee name with their salary and produce a joined table
  (join on name_table and salary_table)

Assume that all operations take 1 unit of time per row.

Q: What is the maximum speedup here?

2. average_numbers example

Our average_numbers example is slightly more complex than above as it involves an aggregation
(group-by).
Aggregation can be parallelized.
    (Why? What type of parallelism?)

For the purposes of Amdahl's law, we can think of aggregation as requiring at least 1 operation
(1 unit of time to compute the total).

Q: What is the maximum speedup here?

3. An extended version of the table join example.
We have two tables, of employee names and employee salaries.
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
Let's also connect Amdahl's law back to throughput & latency.

1. Rephrase in terms of throughput

2. Rephrase in terms of latency
"""

"""
=== Parallelizing our code in Pandas? ===

We don't want to parallelize our code by hand.
(why? See problems with concurrency from last week!)

Dask is a simple library that works quite well for parallelizing datasets
on a single machine as a drop-in replacement for Pandas.
"""

# conda install dask or pip3 install dask
import dask

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
=== A final definition and end note: Vertical vs. horizontal scaling ===

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

Everything we have said about identifying and quantifying parallelism also applies to
distributing the code (for the most part -- we will only see exceptions to this if we cover
distributed consistency issues and faults and crashes, this is an optional topic that we will
get to only if we have time.)
In addition to scaling even further, distribution can offer an even
more seamless performance compared to parallelism as it can eliminate
many coordination overheads and contention between workers
(see partitioning: different partitions of the database are operated entirely independently by different machines).
"""
