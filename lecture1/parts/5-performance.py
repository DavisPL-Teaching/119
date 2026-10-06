"""
October 5

Part 5: Performance

Let's talk about performance!

But first, the poll.

=== Poll / discussion question ===

True or false:

1. Two different ways of writing the same overall computation can have two different dataflow graphs.

Answers:
- Well, there's usually more than one way to write a valid program, so it would
  make sense if that's also true for dataflow graphs.
- Two operators that are independent of one another? we don't care about the
  order between them, so they would result in the same dataflow graph
  no matter which order we do those operations in.
- One program might be more efficient than the other
- Could get a different graph depending on how you divide your pipeline into
  "stages" or "nodes".

Can we give an example?

    df0 = pd.DataFrame("my-dataset.csv")
    df1 = df0["x"].max()
    df2 = df0["y"].min()

    I need to divide my pipeline into tasks!

    At least two ways:

    One way of doing it:
    1. load input data
    2. calculate max of x
    3. calculate min of y

        ----> (2)
    (1)
        ----> (3)

    Another way:
    1. load input data
    2. calculate max of x and the min of y.

    (1) ----> (2)

    If we were to write:

    df0 = pd.DataFrame("my-dataset.csv")
    df2 = df0["y"].min()
    df1 = df0["x"].max()

    ^^^^^ Different way of writing the computation

    In one case, we get:

        ----> (2)
    (1)
        ----> (3)

    In the other case, we get:

        ----> (3)
    (1)
        ----> (2)

    These are really the same dataflow graph! Same nodes and edges.
    So, this is an example of a different phenomenon:

    - Two different ways of writing the same computation can have
      the *same* dataflow graph.

2. Operators always take longer to run than sources and sinks.

3. It is usually most useful to insert data validation steps at the end of a dataflow graph, right
   before the sinks.

https://forms.gle/gJ7d2CuAqqntoB5g6

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

For 1:
An example?

What about the opposite phenomenon:
1b. Two different ways of writing the same overall computation can have *the same* dataflow graph?

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

Examples (as needed)
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

Returning to:

1. Two different ways of writing the same overall computation can have *two different* dataflow graphs.

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

(input) --> (describe)

vs.

        --> (min)
(input) --> (max)
        --> (avg)

Main points:
    - different ways of writing a computation can result in the same dataflow graph
    - different ways of writing a computation can result in a different dataflow graph
    - the dataflow graph we get depends on the delineation of the computation into
      nodes or "stages"
    - the dataflow graph and the program represent the computation in structurally
      or conceptually different ways.

--------------------------------------------------------------------------------

Last time, we reviewed the notions of performance for traditional programs.

There's two types of performance that matter: time & space.

For data processing programs?

It turns out, there are actually two different notions of running time.
We will see how they are importantly different.

.
.
.
.
.

===== Running time for data processing programs =====

Motivation:

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

"This job is running very slow (4+ hours)" --> Probably just has a lot of data to process

"This job terminates in a few seconds" --> Probably just not a lot of data involved! :-)

    (Like our Alice, Charlie dataset from part 1, with only two users and 3 rows)

BUT:
This isn't very useful.
dataset size changes!

    --> we may run on only a few rows in testing, and then scale up to a huge dataset in
        production

So how do we measure running time in a way that isn't simply a reflection of the
size of our dataset?

===== Throughput =====

What is throughput?

Revisting our example above:

Example:
1000 rows => 1 ms
10,000 rows => ~10 ms
100,000 rows => ~100 ms

- Often linear!

    Even if it's not linear: "linear" is almost always a better
    approximation than "constant".

- The more input items, the longer it will take to run

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

No - we will get to the other, "latency", next time.

Recap:

- Poll covered some T/F on dataflow graphs

We saw that different ways of writing a computation (for example in Python)
may or may not yield the same dataflow graph, depending on the computation
and on how we divide into stages

We defined throughput, which we argued is a better model of performance
for dataflow graphs compared to running time

We saw the formula:

    Throughput = (total # of input rows processed)
                    /
                    (total running time of the pipeline).

---------

Starting here 10/5.

===== Latency =====

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
"""
