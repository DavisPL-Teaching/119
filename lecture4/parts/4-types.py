"""
Part 4: Parallelism Types

=== Poll ===

1.
Two workers, threads, or processes are accessing the same shared memory variable "x". Each worker increments the variable 100 times:

    for i in range(100):
        x += 1

What are possible values of x?

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

============================================

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
# Redefine N again
# N = 100_000_000
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
# N = 1_000_000
# if __name__ == "__main__":
#     freeze_support()
#     average_numbers_pipeline_parallelism()

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
