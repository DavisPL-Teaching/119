"""
Part 6: Distribution and concluding thoughts

=== Distributed computing: some examples ===

=== What is distribution? ===

Distribution means that we have multiple workers and belts
**in different physical warehouses**
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
average_numbers_distributed()

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

    A: Yes, for example: we have two databases or database
    partitions running separately (and they don't interact)

Q4: can we have distribution with concurrency?

    Yes, we often do, for example when distributed workers
    communicate via passing messages to each other
"""

"""
=== Parallelizing our code in Pandas? (Skip) ===

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

    # Dask is "lazy" -- it only generates data when you ask it to.
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

# If you just want parallelism on a single machine,
# Dask is a great lightweight solution.

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

In addition to scaling even further, distribution + parallelism can offer an even
more seamless performance compared to parallelism alone as it can eliminate
many coordination overheads and contention between workers
(see partitioning: different partitions of the database are operated entirely independently by different machines).

Recap:

- Finished Amdahl's law, did an example, and a practice example with the poll

- Connected Amdahl's law back to latency & throughput (with two formulas)

- We talked about distribution; ran our same running example as a distributed pipeline over ssh

- We talked about vertical vs horizontal scaling

- We contrasted parallelism with distributed scaling - where we will be going next in Lecture 5.
"""
