
"""
Part 5: Quantifying Parallelism and Amdahl's Law.

=== Poll ===

Review:
Identifying parallelism in dataflow graphs!

- Data parallelism:

    Running the same task on different data points

- Task parallelism

    Running two different tasks on same or different data points

- Pipeline parallelism

    When feeding the output of one task to another, having the second
    task process the partial results of the first task while the first
    task is still running.

How do we connect these types of parallelism to this concept of
dataflow graphs?

    Note: the word "task" as referring to a node in the dataflow graph.

    Different nodes in the graph = different tasks

For this poll, you may find it helpful to review the dataflow graph example that is drawn at:
lecture4/extras/dataflow-graph-example.png

1. For each type of parallelism that can be present in a dataflow graph, does it occur at a single node, or between a pair of two nodes?

2. For two different ways of drawing a dataflow graph (with different delineations of tasks as nodes), could we get different types of parallelism present, based on the above? Briefly comment on why or why not.

https://forms.gle/arFaFVM7DhBpuVqSA

examples:

    1. load employee dataset

    2. strip the spaces from employee names, followed by extracting the first/given name

    grouping both parts of task 2 as a single task as numbered above:

    (load) -> (strip and extract)

    then (strip and extract) has data parallelism,
    but no pipeline parallelism; but, if I group it as two different tasks

    (there is pipeline parallelism between "load" and "strip and extract")

    1. load employee dataset

    2. strip the spaces from employee names

    3. extract the first/given name

    (load) -> (strip) -> (extract)

    Now there is pipeline parallelism between (strip) and (extract)
    and data parallelism at (strip) and data parallelism at (extract)

    I can also modify my graph to turn data parallelism into task parallelism

    My dataset got too large, so I split into two halves

    (load dataset1) -> (strip and extract dataset1)

    (load dataset2) -> (strip and extract dataset2)

    Now I have four nodes!

    Now there is task parallelism between "strip and extract dataset1"
    and "strip and extract dataset2"

This was tricky point

If you don't want to remember the discussion above, just remember:

    1. Data parallelism always exists at a single node, and I can identify
    it by checking if that particular node/task can be run in parallel over
    different chunks/batches of the input

    2. Task parallelism always exists between any two different nodes that are
    independent of one another

    3. Pipeline parallelism always exists between any
    two different nodes which are connected by an edge.

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

---- where we ended for today ----

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

=== Poll (For next time) ===

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

"""
