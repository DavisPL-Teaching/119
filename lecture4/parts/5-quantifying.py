
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

===============================================

Continuing: quantifying parallelism in your pipeline

We're interested in knowing: how much speedup is possible?

Amdahl's law gives us a theoretical upper bound on the amount of speedup
that is possible (in arbitrary code, but also applying specifically
to data processing code).

=== Standard form of the law ===

Suppose we have a computation that exhibits one or more types of parallelism.
The amount of speedup in a computation is at most

    Speedup <= 1 / (1 - p)

where:

    p is the percentage of the task (in running time) that can be parallelized.

=== Example with a simple task ===

We have written a complex combination of C and Python code to train our ML model.
Based on profiling the code, we believe that
95% of the code can be fully parallelized, however there is a 5% of the time of the code
that is spent parsing the input model file and producing as output an output model file
that we have determined cannot be parallelized.

Q: What is the maximum speedup for our code?

Applying Amdahl's law:

    p = .95

    Speedup <= 1 / (1 - .95) = 1 / .05 = 20x.

Example: the best we can get is from 100 hours to 5 hours, a 20x speedup.

=== Alternate form ===

Here is an alternative form of the law that is equivalent, but sometimes a bit more useful.
Let:
- T be the total amount of time to complete a task sequentially
  (without any parallelism)
  (in our example: 100 hours)

- S be the amount of time to compute some inherently sequential portion of the task
    --> We don't believe it's possible to do any part of S in parallel
  (in our example: 5 hours)

Then the maximum speedup of the task is at most

    speedup <= (T / S) = 100 hours / 5 hours = 20x.

Note: this applies to distributed computations as well!

This is giving a theoretical upper bound, not taking into account
other overheads (for example, it doesn't take into account
communication overhead between threads, processes or distributed devices).

=== Example ===

1. Let's take our data parallelism example:
- imagine an SQL query where you need to match
  the employee name with their salary and produce a joined table
  (join on name_table and salary_table)

Assume that all operations take 1 second per row:
    - 1 second to load each input row rom name_table
    - 1 second to load each input row from salary_table
    - 1 second to join -- per row in the joined table

Also assume that there are 100 employees in name_table,
100 in salary_table, and 100 in the joined table.

Q: What is the maximum speedup here?

    speedup <= (T / S)

    What are T and S?

    T = ?
        201?
        300s =
            100s to load first table
            100s to load second table,
            100s to calculate joined table.

    with no parallelism!

    S = what cannot be parallelized?
        Joining the two tables?
        How can we take into account data parallelism?
        Idea: Once both tables are loaded, I should be able to join
            different rows in parallel.

            If I have all the computational resources in the world,
            I could send each employee to its own worker.
            I should then be able to join all the values associated
            with each worker individually -- different
            employees are processed in parallel.

    Let's draw a data flow graph again of our tasks:

    (load table 1)
                    --> (join tables)
    (load table 2)

    What's the minimum bundle of computation that I can't process in
    parallel?

    Imagine a specific employee A:

    - I have to load table 1, row corresponding to A (1s)
    - I have to load table 2, row corresponding to A (1s)
    - I have to compute joined table, row corresponding to A (1s)

    Minimum time is 2 seconds!

    Therefore:

        Speedup <= T / S = 300 / 2 = 150x.


    Note:
    You can think of this as the limit as number of cores/processes
    goes to infinity.

    There's a version of the law that takes this into account.

    T = time it takes to complete with 1 worker
    S = time it takes to complete the task with a theoretically infinite number of workers and no cost of overhead when communicating between workers.

=== Poll ===

Use Amdahl's law to estimate the maximum speedup in the following scenario.

As in Wednesday's poll, a Python script needs to:
- load a dataset into Pandas: students.csv, with 100 rows
- calculate a new column which is the total course load for each student
- send an email to each student with their total course load

Assume that it takes 1 ms (per row) to read in each input row, 1 ms (per row) to calculate the new column, and 1 ms (per row) to send an email.

Q: What is the theoretical bound on the maximum speedup in the pipeline?


    T = 300 ms
    S = 3 ms

    Speedup <= 100x

=== More examples ===

(Skip)
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

Given T and S...

1. Rephrase in terms of throughput:

    If there are N input items, then the _maximum_ throughput is

    throughput <= (N / S)

2. Rephrase in terms of latency:

    Assuming we care about latency for the whole task
    (not just a single item), the _minimum_ latency is

    latency >= S.

"""
