"""
Part 6: Distribution and concluding thoughts
(Planned for: Nov 9)

=== Introduction ===

at the start of this lecture, we introduced 3 related terms: Parallelism, Concurrency, and Distribution

we have talked about parallelism

we have talked about concurrency

    concurrency is part of the underlying system! but we want to avoid
    thinking about it if possible (use libraries/frameworks that have
    already solved the concurrency problems)

we have talked about how to tell IF parallelism is present and HOW MUCH is present if so.

What about distribution?

Real pipelines are distributed!

    The real world is distributed! The fact we have isolated certain pieces of code and datasets
    to run on individual computers is an artificial limitation

We will move to distributed pipelines in Lecture 5.

-------- Where we stopped for 11/9 --------

=== A distributed code example ===

Recall: Distribution = multiple devices involved.

    (Think of as: multiple workers and belts **in different physical warehouses**
    can operate and fail independently)

Why does this introduce new challenges?

    Running on the same physical device, both workers have
    access to the same resources;
    Running on two different devices, they access different resources, and one worker could crash even if the other
    one doesn't.
    If the workers try to communicate, they may be faced with communication delays,
    out-of-order messages, dropped messages, or different clocks between the two workers.

    It becomes a complex coordination problem between different devices.

BUT:

    It also introduces a huge opportunity:
    because any single physical device (even a huge beefy server machine!) only has
    a finite number of resources, but by scaling many devices,
    we are no longer limited by the amount of resources on one machine.

    Also: coordination and overhead can be reduced to zero.

    Unlocks arbitrary potential for scaling!

To give a simple instance of a distributed pipeline,
and close the loop for this lecture,
let's use ssh to connect to a remote
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
# (Note: I have to be connected to university VPN for this to work.)
# average_numbers_distributed()

# This waits until the first connection finishes before
# starting the next connection; but we could easily modify
# the code to make them both run in parallel.

"""
Questions (REVIEW)

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

=== Recap: Part 6 ===

- We talked about distribution; ran our same running example as a distributed pipeline over ssh

- We talked about vertical vs horizontal scaling

- We contrasted parallelism with distributed scaling - where we will be going next in Lecture 5.
"""

"""
Extra material

There is some extra material about parallelizing DataFrame computations using a library
called dask.
See extras/dask.py.
"""
