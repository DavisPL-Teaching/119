"""
Part 3: Concurrency and Data Races

=== Poll ===

(Recall definitions)
For each of the following scenarios, select whether it is parallel, concurrent, or distributed (select more than one if applicable, or "none of the above")

https://forms.gle/iiSr5en4fSyNKM336

.
.
.
.
.
.
.
.
.
.

----- Where we ended for Oct 28

=== Outline ===

- Last part: parallel example
- This part: concurrent + distributed examples
- Parallel thinking, types of parallelism, and quantifying
  the amount of parallelism available
- Measuring scaling & types of scaling

=== Concurrent examples ===

Recall our example above average_numbers_in_parallel.

No concurrency! (Why?)

Let's modify our example to add concurrency:
a shared memory data structure to keep track of and combine the two outputs.
"""

### *** IGNORE ***
### Boilerplate from before
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
def worker1(results):
    sum = 0
    count = 0
    for i in range(N // 2):
        sum += i
        count += 1

    print(f"Worker 1 result: {sum} {count}")
    # Save the results in the shared results array
    results[0] = sum + results[0]
    results[1] += count

def worker2(results):
    sum = 0
    count = 0
    for i in range(N // 2, N):
        sum += i
        count += 1

    print(f"Worker 2 result: {sum} {count}")
    # Save the results in the shared results array
    results[2] = sum + results[2]
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
    p1 = Process(target=worker1, args=(results,))
    p2 = Process(target=worker2, args=(results,))
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
# N = 10_000_000
# if __name__ == "__main__":
#     freeze_support()
#     average_numbers_concurrent()

"""
Questions:

What do you think would happen if we modified the example so that both
processes access the same elements of the array?
(Let's try it)

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

If nothing happens: lower N and try again.

.
.
.
.
.

Spoiler: it seems to work! ....
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

(We have the same problem as before and a new problem)

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

    Contention:

    Multiple workers, threads, or processes trying to access the same data at the
    same time causes a vast decline in performance.

    AND
    we have a race condition which, this time (unlike above)
    is actually reliably triggering every time we run the code.

    Observe that not only do some reads/writes not get counted,
    they also corrupt the data and produce completely random
    results.

=== Data races ===

Definition:

    A "data race" is a particular race condition where a read and
    a write happens to the same memory location at the same time.

    On most architectures, a data race results in random/arbitrary/
    nondeterministic behavior.

Moral of the story:
    Don't read and write to the same data at the same time!

Q: Which of the above is the best concurrent solution and why?

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
  The ability of parallel and concurrent code to behave as if it were
  sequential code.
  You want the same answers as if you just ran the code sequentially.

- Nondeterminism:
  Multiple executions of the same code give different answers.

=== Additional exercise (SKIP) ===

Exercise:
Modify the example to add up a shared list instead of an iterator.
Write a version that uses (i) shared reads to the list and (ii) shared writes
to the list (for example popping off elements as they are used).
What happens?

=== Poll ===

(Do the poll - in 4-types.py)

=== Recap from this lecture ===

We saw how code can be concurrent (not just parallel):
shared conflicting operations (typically, a read/write or a write/write)

We saw & defined many of the problems that you can run into with concurrent code

**In this class, we want to avoid all of the above problems and parallelize
in a way that avoids reading/writing to the same memory at the same time.**

Coming up next:
- types of parallelism (in a pipeline)
- quantifying parallelism (in a pipeline)
"""
