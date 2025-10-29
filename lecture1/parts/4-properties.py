"""
Monday, October 6

Part 4: Proeprties of Dataflow Graphs

On Friday, I introduced the concept of dataflow graphs.
Recall:
    To build a dataflow graph, we divide our pipeline into a series of "stages"
To build the graph, we draw:
    - One node per stage of the pipeline
    - An edge from node A to B (A -> B) if node B directly uses the output of node A.

=== Practice with dataflow graphs ===

At the end of last class period, we introduced a dataset for life expectancy.
We saw a simple data pipeline for this dataset.
Let's separate it into stages as follows:

(read) = load the CSV input
(max) = compute the max
(min) = compute the min
(avg) = compute the avg
(print) = Print the max, min, and avg
(save) = Save the max, min, and avg in a dataframe to a file

=== Discussion Question and Poll ===

Suppose we draw a dataflow graph with the above nodes.

1. What edges will the graph have?
  (draw/write all edges)

2. Give an example of two stages A and B, where the output for B depends on A, but there is no edge from A to B.

https://forms.gle/6FB5hhwKpokTHhit9

Answer:

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

- A stage B *depends on* a stage A if...

    there is a path from A to B

    point: The dataflow graph reveals exactly which computations depend on which others!

- A *source* is a node without any input edges
    (typically, a node which loads data from an external source)
    (corresponds to the E stage of the ETL model)

- A *sink* is a node without any output edges
    (typically, a node which saves data to an external source)
    (corresponds to the L stage of the ETL model)

- A small correction from last time: let's define
  an *operator* is any node that is not a source or a sink.
  Operators take input data, and produce output data
    (corresponds to the T stage of the ETL model)

Points:

    Every node in the dataflow graph is one of the above 3 types

    The dataflow graph reveals exactly where the I/O operations are for your pipeline.

We can use the dataflow graph to reveal (visually and conceptually) many useful features of our pipeline.

In Python:
We could write each node as a stage, as we have been doing before.

Let's just write one example, in the interest of time
"""

def max_stage(df):
    return df["Year"].max()

"""
Reminders for why this helps:

(Maybe it's overkill for a one-liner example like this)

- Better code re-use
- Better ability to write unit tests
- Separation of concerns between different features, developers, or development efforts
- Makes the software easier to maintain (or modify later)
- Makes the software easier to debug

Zooming in on one of these...
(pick one)

Q: How does this correspond to ETL model?

ETL is basically a dataflow graph with 3 nodes.
"""

"""
=== Data validation ===

We will talk more about data validation at some point, most likely as part of Lecture 3.
(See failures.py for a further discussion)

Where in a pipeline is data validation most important?

(There is more than one place where validation could help, but what's the most obvious place to start?)

A: Right before transformations
    (After sources)

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

Let's touch on one other thing that we can do with dataflow graphs:
we can use them to think about performance.

Dataflow graphs are basically the "data processing" equivalent of programs.

For traditional programs, there are two notions of performance that matter:

- Runtime or time complexity
- Memory usage or space complexity

For data processing programs?

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

We argued that analagous to regular computer programs for the traditional computing world,
    dataflow graphs are the right notion of computer programs for the data processing world.

********** where we ended for today **********
"""
