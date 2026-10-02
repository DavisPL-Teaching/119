"""
Friday, October 2

Part 4: Properties of Dataflow Graphs

On Friday, I introduced the concept of dataflow graphs.
Recall:
    1. To build a dataflow graph, we divide our pipeline into a series of "stages"
To build the graph, we draw:
    - One node per stage of the pipeline
    - An edge from node A to B (A -> B) if node B directly uses the output of node A.

    2. ETL is a special case of dataflow graphs with 3 nodes and 2 edges.

=== Practice with dataflow graphs ===

At the end of Part 3, we introduced a dataset for life expectancy.
We saw a simple data pipeline for this dataset.
Let's separate it into stages as follows:

(read) = load the CSV input
(max) = compute the max
(min) = compute the min
(avg) = compute the avg
(print) = Print the max, min, and avg
(save) = Save the max, min, and avg in a dataframe to the output CSV file.

=== Discussion Question and Poll ===

Suppose we draw a dataflow graph with the above nodes.

1. What edges will the graph have?
  (draw/fill out all edges)

2. Give an example of two stages A and B, where the output for B depends on A, but there is no edge from A to B.

https://forms.gle/ZhpUziw8XTU5tgwC6

Answer:

    (see blackboard)

           -> (max) ----|--> (print)
    (read) -> (min) ----|
           -> (avg) ----|--> (save)

Key points:

    Two "independent" computations will not have an edge one way or the other
    (printing produces output to the terminal, save produces output to a file,
     neither one is used by the other)

    We can read off dependence information from the graph! If there is a path
    from A to B, then B depends (either directly or indirectly) on A.

    What graph we get depends on the precise details of our stages.
    Ex.: if we load the input three different times, once for the max, once for the min,
    once for the avg (and this is listed in our description of the computation),
    we would get a different graph with 8 nodes instead of 6.

    In order to draw this thing, we should refer to the particular way that we wrote out
    our computation.

=== A few more things ===

A couple of more definitions:

- A node B *depends on* a node A if...
    there is a path of edges from A to B

    point: The dataflow graph reveals exactly which computations depend on which others!

- A *source* is a node without any input edges
    (typically, a node which loads data from an external source)
    (corresponds to the E stage of the ETL model)

- A *sink* is a node without any output edges
    (typically, a node which saves data to an external source)
    (corresponds to the L stage of the ETL model)

- (Small correction to the definition from last time:)
  An *operator* is any node that is not a source or a sink.
  Operators take input data, and produce output data
    (corresponds to the T stage of the ETL model).

Points:

    Every node in the dataflow graph is one of the above 3 types

    The dataflow graph reveals exactly where the I/O operations are for your pipeline.

We can use the dataflow graph to reveal (visually and conceptually) many useful features of our pipeline.

In Python:
We could write each node as a stage, as we have been doing before.

Let's just write one example, in the interest of time
"""

def max_stage(df):
    max_year = df["Year"].max()
    return max_year

"""
If we were to do this for all of the 6 stages, what we would obtain
is then a Python function for each node in our dataflow graph

And, the entire dataflow graph would then be a sequence of these Python
functions that are called.

(Reminders for why this helps:

- Better code re-use
- Better ability to write unit tests
- Separation of concerns between different features, developers, or development efforts
- Makes the software easier to maintain (or modify later)
- Makes the software easier to debug)
"""

"""
=== Data validation ===

We may talk a little more about data validation and failures
at some point (time permitting)

Where in a pipeline is data validation most important?

(There is more than one place where validation could help, but what's the most obvious place to start?)

A: Right before transformations
    (Typically: right after source nodes, before any internal operator nodes)

Why?
    - Most common problem: malformed input
    - I might want to validate that all of my rows have the type that I'm expecting before
      I move to any further processing.
    - This might even simplify or speed up the later stages as in those stages I'm allowed
      to assume that the data is well-formed.

NB: You can validate at any point in the graph. (And it can be useful!)

Validation in a dataflow graph:
we may view each edge as having some "constraints" that are validated by the previous stage,
and assumed by the next.

=== Performance ===

Let's touch on one thing that we can do with dataflow graphs:
we can use them to think about performance.

Dataflow graphs are basically the "data processing" equivalent of programs.

For traditional programs, there are two notions of performance that matter:

- Runtime or time complexity
- Memory usage or space complexity

For data processing programs?

We'll answer this next time.

-------------------------

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

We'll care about the most:
- Running time corresponds to: Throughput & Latency
- Memory usage: you can also measure, we'll talk briefly about ways of thinking about this.

**********

Recap:

We reviewed the definition of dataflow graph
- divided into sources, operators, and sinks
- def of when to draw an edge

We practiced drawing dataflow graphs

We used dataflow graphs to explore various features of a data processing computation

We argued that analogous to regular computer programs for the traditional computing world,
    dataflow graphs are the right notion of computer programs for the data processing world.
"""
