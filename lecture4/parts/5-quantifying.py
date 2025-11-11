
"""
Part 5: Quantifying Parallelism and Amdahl's Law.

Content from Nov 7 poll was moved to end of Part 4 lecture.

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
(We can run 2-parallelism.py to check; and we might get different numbers
on different platforms or machines, for example, if your machine has only one CPU
you might not see any speedup.)

Re-running:
Speedup = 9.6 / 5.2 = 1.84x speedup.

You could run with four workers, and get up to a 4x speedup
... or with 8 workers, and get up to an 8x speedup ...

You might wonder, how much can I keep speeding up this computation,
won't this stop working at some point?

At some point ... we hit a bottleneck

Fundamental law of parallelism:
Amdahl's law:
https://en.wikipedia.org/wiki/Amdahl%27s_law

Amdahl's law gives a theoretical upper bound on the amount of speedup that is possible for any task (in arbitrary code, but also applying specifically
to data processing code).

It's a useful way to quantify parallelism & see how useful it would be.

=== Amdahl's Law ===

We're interested in knowing: how much speedup is possible?

Standard form of the law:

Suppose we have a computation that I think could benefit from one or more types of parallelism.
The amount of speedup in a computation is at most

    Speedup <= 1 / (1 - p)

where:

    p is the percentage of the task (in running time) that can be parallelized.

=== Example with a simple task ===

We have written a complex combination of C and Python code to train our ML model.
Based on profiling the code (callgrind or some other profiling tool), we believe that
95% of the code can be fully parallelized, however there is a 5% of the time of the code
that is spent parsing the input model file and producing as output an output model file
that we have determined cannot be parallelized.

Q: What is the maximum speedup for our code?

Applying Amdahl's law:

    p = .95

    Speedup <= 1 / (1 - .95) = 1 / .05 = 20x.

Pretty good - but not infinite!

Example: the best we can get is from 100 hours to 5 hours, a 20x speedup.

How to apply this knowledge?
I was considering purchasing a supercomputer server machine with 160 cores.
Based on the above calculation, I realize that I'm only going to effectively
be able to make use of an at most 20x speedup,
so I think my 160 cores may not be useful, and I buy a smaller machine
with 24 cores.

=== Alternate form ===

Here is an alternative form of the law that is equivalent, but sometimes a bit more useful.
Let:
- T be the total amount of time to complete a task sequentially
  (without any parallelism)
  (in our example: 100 hours)

- S be the amount of time to compute some inherently sequential bottleneck
    --> We don't believe it's possible to do any part of S in parallel
  (in our example: 5 hours)

Then the maximum speedup of the task is at most

    speedup <= (T / S) = 100 hours / 5 hours = 20x.

Note: this applies to distributed computations as well!

This is giving a theoretical upper bound, not taking into account
other overheads (for example, it doesn't take into account
communication overhead between threads, processes or distributed devices).

So it's not an actual number on what speedup we will get, but it still can be a
useful upper bound.

Recap:

- We reviewed 3 type of parallelism in dataflow graphs

- We define speedup

- We talked about estimating the "maximum speedup" in a pipeline, using
  a law called Amdahl's Law

- We saw two forms of the law:

    Speedup <= 1 / (1 - p)

    Speedup <= T / S

    where:
        T is running time of sequential code
        S is running time of a bottleneck that can't be parallelized
        p is % of code that can be parallelized

        p = (T - S) / T.

---- where we ended for Nov 7 ----

Recall formulas from last time

=== Example ===

1. SQL query example

- imagine an SQL query where you need to match
  the employee name with their salary and produce a joined table
  (join on name_table and salary_table)

Assume that all operations take 1 ms per row:
    - 1 ms to load each input row from name_table
    - 1 ms to load each input row from salary_table
    - 1 ms to join -- per row in the joined table

Also assume that there are 100 employees in name_table,
100 in salary_table, and 100 in the joined table.

Q: What is the maximum speedup here?

Dataflow graph:

    (load name_table) ----|
                          |---> (join tables)
    (load salary_table) --|

    speedup <= (T / S)

    What are T and S?

    T = ?
        300ms =
            100ms to load first table
            100ms to load second table,
            100ms to calculate joined table.

    with no parallelism!

    S = what cannot be parallelized?

        Idea: view at the level of input rows!

        Let's identify what needs to happen for some specific employee

        - I need to load the employee name before I produce the particular output row in joined table for that employee

        - I need to load the employee salary before I produce the particular output row in joined table for that employee

        x I need to load the employee name, then load the employee salary, then produce the particular output row

          ^^^ not really a sequential bottleneck

    Minimum "sequential bottleneck" is 2 ms!

    Therefore:

        Speedup <= T / S = 300 ms / 2 ms = 150x.

=== Poll ===

Use Amdahl's law to estimate the maximum speedup in the following scenario.

As in last Monday's poll, a Python script needs to:
- load a dataset into Pandas: students.csv, with 100 rows
- calculate a new column which is the total course load for each student
- send an email to each student with their total course load

Assume that it takes 1 ms (per row) to read in each input row, 1 ms (per row) to calculate the new column, and 1 ms (per row) to send an email.

Q: What is the theoretical bound on the maximum speedup in the pipeline?

https://forms.gle/W5NpbuZGs4Se45VCA

DFG:

    (load) -> (calculate col) -> (send email)
    100 ms         100 ms           100ms

    T = 100 + 100 + 100 = 300 ms

S = 3ms -- need to perform 3 actions in sequence for a single student - can't be parallelized!

    300 ms / 3 ms = 100x.

=== More examples and exercises ===
(Skip - may do in discussion section)

2. Let's take our data parallelism example:

    We had an employee database, and tasks:

    1. load employee dataset

    2. strip the spaces from employee names

    3. extract the first/given name

    with dataflow graph:

        (1) -> (2) -> (3)

Again assume 1ms for each task per input row.
What are T and S here?

3. An extended version of the table join example.
We have two tables, of employee names and employee salaries.
We want to compute which employees make more than 1 million Euros.
The employee salaries are listed in dollars.

We are given as input the CEO name.
We want to get the salary associated with the CEO,
convert it from USD to Euros, and filter only the rows where the
result is over 1 million.
Assume all basic operations take 1 unit of time per row.

=== Additional notes ===

Note 1:
You can think of this as the limit as number of cores/processes
goes to infinity.

T = time it takes to complete with 1 worker
S = time it takes to complete the task with a theoretically infinite number of workers and no cost of overhead when communicating between workers.

**Advanced topics note:**
There's a version of the law that takes the number of processes into account.

    - basically the law would take the portion of the pipeline that *can* be parallelized, and divide it by
      # of processors

      S portion - cannot be parallelized
      T - S - can be parallelized

    - Don't need to know this for this class.

Note 2:
How Amdahl's law applies to aggregation cases.

average_numbers example

Our average_numbers example is slightly more complex than above as it involves an aggregation
(group-by).
Aggregation can be parallelized.
    (Why? What type of parallelism?)

For the purposes of Amdahl's law, let's think of aggregation as requiring at least 1 operation
(1 unit of time to compute the total).

Q: What does Amdahl's law say the maximum speedup for our simple average_numbers pipeline?

=== Connection to throughput & latency ===

Let's also connect Amdahl's law back to throughput & latency.

Given T and S...

1. Rephrase in terms of throughput:

    If there are N input items, then the _maximum_ throughput is

    throughput <= (N / S)

    (Num input items) / (running time of pipeline)

    Amdahl's law is just assuming that the minimum running time of the pipeline is S - "maximum speedup" case.

2. Rephrase in terms of latency:

    Observation:
    In the above examples the "sequential bottleneck" we chose
    is essentially the latency of a single item!

    Therefore we have:

    latency >= S,

    if S is computed in the way that we have computed above.
"""
