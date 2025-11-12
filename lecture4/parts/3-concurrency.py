"""
Part 3: Concurrency and Data Races

Wednesday, Oct 29

=== Poll ===

(Recall definitions)
Which of the following scenarios are parallel, concurrent, and distributed?

https://forms.gle/h1u9xZwUTndhJWbk9




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

from multiprocessing import Process, freeze_support

def run_in_parallel(*tasks):
    running_tasks = [Process(target=task) for task in tasks]
    for running_task in running_tasks:
        running_task.start()
    for running_task in running_tasks:
        result = running_task.join()

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

    print(f"Worker 3 result: {sum} {count}")
    # Save the results in the shared results array
    results[0] = sum + results[0]
    results[1] += count

def worker4(results):
    sum = 0
    count = 0
    for i in range(N // 2, N):
        sum += i
        count += 1

    print(f"Worker 4 result: {sum} {count}")
    # Save the results in the shared results array
    results[2] = sum + results[0]
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
    # print(f"Worker results: {results[:]}")
    sum = results[0] + results[2]
    count = results[1] + results[3]
    print(f"Average: {sum} / {count} = {sum / count}")
    print(f"Computation finished")

# Uncomment to run
# Define N -- modify here as needed
# N = 1_000_000
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

Definition of a race condition:
    The output of your program depends on the exact order in which different
    potentially conflicting operations occur --
        "who wins the race"

What do you think would happen if we modified the example to use the shared
results list directly for each worker's local variables?
(Let's try it)
"""

# Super race-y version of worker 3 -- don't do this!
def worker3_racey(results):
    for i in range(N // 2):
        # print(f"Worker 3 loop: {i}")
        results[0] += i
        results[1] += 1

    print(f"Worker 3 complete")

# Super race-y version of worker 4
def worker4_racey(results):
    for i in range(N // 2, N):
        # print(f"Worker 4 loop: {i}")
        results[0] += i
        results[1] += 1

    print(f"Worker 4 complete")

# Super race-y version of main process
def average_numbers_racey():
    print(f"N = {N}")

    # Create a shared results array
    # i = integer, d = double (we use d here because the integers suffer from overflow)
    results = Array('d', range(2))

    # Iniitalize our shared array
    results[0] = 0
    results[1] = 0

    # Like run_in_parallel but with added code to handle arguments
    p1 = Process(target=worker3_racey, args=(results,))
    p2 = Process(target=worker4_racey, args=(results,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    # Calculate results
    # print(f"Worker results: {results[:]}")
    sum = results[0]
    count = results[1]
    print(f"Average: {sum} / {count} = {sum / count}")
    print(f"Computation finished")

# Uncomment to run
# Define N -- modify here as needed
# N = 1_000_000
# if __name__ == "__main__":
#     freeze_support()
#     average_numbers_racey()

"""
Does something go wrong?

    Contention:

    Multiple workers, threads, or processes trying to access the same data at the
    same time causes a vast decline in performance.

    AND
    we have a race condition which, this time (unlike above)
    is actually reliably triggering every time we run the code.

    Observe that not only do some reads/writes not get counted,
    they also corrupt the data and produce completely random
    results.

Recap:

    Definitions of parallelism, concurrency, and distribution
    - In terms of workers, memory that they may share, whether the workers
      run at the same time, and whether not the operations to the memory may conflict.
    - We saw multiple concurrent (not just parallel) versions of the code
      from last time, where two workers are now updating memory that they
      share together, and performing operations which may conflict
    - We saw: data races and contention.

    ********** We will end here for today **********

    ================================================

Finishing up a few things:

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

=== Terminology ===

- Race condition: when the order in which workers complete their task
  or certain operations
  (which one completes it first) affects the final outcome

- Data race
  A particular race condition where a read and a write happen at the same
  time and in the same memory location

  (Data races only exist in concurrent applications)

- Undefined Behavior: "Feature" in some programming languages where the existence
  of a data race means that the compiler can do whatever it wants with your
  code (even miscompile it to something else entirely)

- Contention
  Reduction in performance due to competing concurrent operations

- Deadlock
  Different threads try to access the same data at the same time in a way
  that prevents any thread from continuing.

  (Similar to an infinite loop)

- Consistency
  The ability of parallel and concurent code to behave as if it were
  sequential code.
  You want the same answers as if you just ran the code sequentially.

- Nondeterminism:
  Multiple executions of the same code give different answers.

=== Additional exercises (skip for time) ===

Exercise:
Modify the example to add up a shared list instead of an iterator.
Write a version that uses (i) shared reads to the list and (ii) shared writes
to the list (for example popping off elements as they are used).
What happens?

=== Recap from this lecture ===

We saw how code can be concurrent (not just parallel):
shared conflicting operations (typically, a read/write or a write/write)

We saw & defined many of the problems that you can run into with concurrent code

**In this class, we want to avoid all of the above problems and parallelize
in a way that avoids reading/writing to the same memory at the same time.**

Coming up next:
- types of parallelism (in a pipeline)
- quantifying parallelism (in a pipeline)


=== A difficult exercise (discussion & poll from Oct 31) ===

1.
Two workers, threads, or processes are accessing the same shared memory variable "x". Each worker increments the variable 100 times:

    for i in range(100):
        x += 1

What are possible values of x at the end of the program?

If it helps: think of x += 1 as a read followed by a write, i.e.
    temp = x + 1
    x = temp

You may assume that the programming language we are in executes all the workers concurrently (i.e., interleaving the operations in some way).
You may ignore any possible "undefined behavior".
(I will comment on this briefly after the poll how this would look in a language like C or Rust)

2.
The scenario above exhibits... (select all that apply)
- Concurrency
- Parallelism
- Distribution
- Contention
- Deadlock
- Race condition
- Data race

https://forms.gle/Ar4QKXfBmcsiU9iM9

.
.
.
.


Walk through...

Can we get the value 200?
A: Yes, if for example worker1 increments 100 times, then worker 2 increments 100 time (no interleaving)

Can we get the value 100?

Yes:
Idea: worker1 finishes, worker2 hasn't finished yet:
worker1: 0 -> 1, 1 -> 2, ..., 99 -> 100

worker2: 0 ->                           -> 1, 1 -> 2, 2 -> 3,
    ..., 99 -> 100.

Can we get 120?

worker2 reads x when it's at the value 20 instead of 0.
worker1: 0 -> 1, 1 -> 2, ..., 99 -> 100

worker2:                 20             -> 21 -> ... -> 100.

0 to 5 instead of 0 to 100:
worker1: 0 -> 1, 1 -> 2,      2 -> 3, 3 -> 4, 4 -> 5
worker2:                 2 ->                        3, 3 -> 4, 4 -> 5, 5 -> 6, 6 -> 7.

Final boss: Can we get a value between 0 and 100? Like 70?

We should try to construct an execution where both worker1 and worker2
overwrite all of each other's work!

worker1: 0 -> 1, 1 -> 2, 2 -> 3, 3 -> 4,       1                              -> 2
worker2: 0                               -> 1, 1 -> 2, 2 -> 3, 3 -> 4, 4 -> 5

We got 2! with two workers, 0 to 5.

We can generalize this to two workers to get 2 (or any value between 2 and 100)
with 100 increments.

Probably not a way to get 0 or 1.

**Correct answer should be: any value between 2 and 200.**

Very scary!

A simple program with a data race turned out to be extremely counterintuitive
to think about.

Concurrent programming is very hard! It's better if we can write code in a way
that *exposes* parallelism but not concurrency - tasks that are parallel run in parallel,
and we don't have to worry about concurrency and data races.

"""
