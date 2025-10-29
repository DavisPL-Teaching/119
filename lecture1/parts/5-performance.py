"""
October 8

Part 5: Performance

Let's talk about performance!

But first, the poll.

=== Poll / discussion question ===

True or false:

1. Two different ways of writing the same overall computation can have two different dataflow graphs.

2. Operators always take longer to run than sources and sinks.

3. Typically, every node in a dataflow graph takes the same amount of time to run.

https://forms.gle/wAAyXqbJaCkEzyZP9

Correct answers: T, F, F

For 1:
Max and min?
Say I have a dataset in a dataframe df with fields x and y
And I want to do df["x"].max()
and df["x"].min()
"""

# df = load_input_dataset()
# min = df["x"].min()
# max = df["x"].max()

"""
Dataflow graph with nodes
(load_input_dataset) node
(max) node
(min) node

       --> (max)
(load)
       --> (min)

       --> (min)
(load)
       --> (max)

Same graph! Has the same nodes, and has the same edges.

This is actually a great example of a slightly different phenomenon:

1b. Two different ways of writing the same overall computation can have *the same* dataflow graph.

A different example?

If one operator does depend on the other, BUT the answer doesn't depend on the order, you could rearrange them to get an example where
- the overall computation was the same, but
- the dataflow graph was different

example:
- Get row with values x, y, and z
- First, we compute a = x + y
- Then we compute a + z = x + y + z.

OR, we could
- First, compute b = x + z
- Then we compute b + y = x + y + z.

We could get the same answer in two different ways.

And in this example, the dataflow graph is also different:

(input) -> (compute x + y) => (compute a + z)
(input) -> (compute x + z) => (compute b + z).

An easier example is .describe() from last time.
"""

"""
Last time, we reviewed the notions of performance for traditional programs.

There's two types of performance that matter: time & space.

For data processing programs?

===== Running time for data processing programs =====

Running time has two analogs. We will see how these are importantly different!

- Throughput

    What is throughput?

    Most pipelines run slower the more input items you have!

    Think about how long it will take to run an application that
    processes a dataset of university rankings, and finds the top 10
    universities by ranking.

    You will find that if measuring the running time of such an application,
    a single variable dominates ...
    the number of rows in your dataset.

    Example:
    1000 rows => 1 ms
    10,000 rows => ~10 ms
    100,000 rows => ~100 ms

    - Often linear: the more input items, the longer it will take to run

    So it makes sense to measure the performance in a way that takes this
    into account:

        running time = (number of input items) * (running time per item)

        (running time per item) = (running time) / (number of input items)

    Throughput is the inverse of this:
    Definition / formula:
        (Number of input items) / (Total running time).

    Intuitively: how many rows my pipeline is capable of processing,
    per unit time

    There's many real-world examples of this concept:

        -> the number of electrons passing through a wire per second

        -> the number of drops of water passing through a stream per second

        -> the number of orders processed by a restaurant per hour

    "number of things done per unit time"

Is this the only way to measure performance?

We also care about the individual level view: how long it takes to process
a *specific* item or order.

We also might measure, for an individual order, how long it takes for
results for that order to come out of our pipeline.

    Latency =
    (time at which output is produced) - (time at which input is received)

This is called latency.

It almost seems like we've defined the same thing twice?

But these are not the same.
Simplest way to see this is that we might process more than one item at
the same time.

Ex:
    Restaurant processes 60 orders per hour

    Scenario I:
        Process 5 orders every 5 minutes, get those done, and move on to
        the next batch

    Scenario II:
        Process 1 order every 1 minute, get it done, and then move on to
        the next order.

In either case, at the end of the hour, I've processed all 60 orders!

Throughput in Scenario I? In Scenario II?
    I:
        Throughput = (Number of items processed) / (Total running time)

        60 orders / 60 minutes = 1 order / minute.
    II:
        Throughput = (Number of items processed) / (Total running time)

        60 orders / 60 minutes = 1 order / minute

What about latency?

    I:
        (time at which output is produced) - (time at which input is received)

        = roughly 5 minutes

    II:
        (time at which output is produced) - (time at which input is received)

        = roughly 1 minutes

Both measures of running time at a "per item" or "per row" level,
but they can be very different.

It is NOT always the case that Throughput = 1 / Latency
or that Throughput and Latency are directly correlated (or inversely correlated).

===== Recap =====

We talked about how computations are represented as dataflow graphs
to illustrate some important points:
- The same computation (computed in different ways) can have two different dataflow graphs
- The same computation (computed in different ways) could have two of the same dataflow graph

We introduced throughput + latency
- Restaurant analogy
- We saw formulas for each
- Both measures of performance in terms of running time at an "individual row" level, but throughput is an aggregate measure and latency is viewed at the level of an individual row.

********** Where we ended for today **********
"""
