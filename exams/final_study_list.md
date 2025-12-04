# Final Study List

Study list of topics for the final.

**The final will cover Lectures 1-6.**

## Lectures 1-4

For Lectures 1-4, please refer to the midterm study list `midterm_study_list.md`.

## Review topics from the midterm

Suggested review topics based on the midterm:

- How to draw and interpret a dataflow graph

    + I'm looking for a conceptual understanding of what happens when
      you "run" the pipeline, what tasks need to be completed in what order.

- Understanding throughput and latency conceptually given a dataflow graph

    + Estimating running time in the sequential case, parallel cases; applying formulas

- Concurrency problems: two concurrent executions like (x += 1; x += 1) vs. x += 1

- Data validation: put the concepts in context:
    If asked about what you would do on a dataset or a specific
    real-world example, we're really looking for things specific to that
    dataset or real-world example.

- Not covered on the midterm, but will be covered on the final:
    Amdahl's law (throughput <= T / S) and maximum speedup case (S)

## Lecture 5

- Scalable collection types

    + Differences from normal Python collections
    + Types of scaling - vertical & horizontal scaling
    + Benefits/drawbacks
    + Examples (RDDs, PySpark DataFrames) and their properties

- Operators

    + Map
    + Filter
    + Reduce

- Operator concepts

    + Immutability
    + Evaluation: Lazy vs. not-lazy (transormation vs. action)
        - why laziness matters / why it is useful
    + Partitoning: Wide vs. narrow
        - What operators should be wide vs narrow
    + How partitioning works, what it means, how it affects performance
    + Key-based partitioning (see MapReduce, HW2)

- MapReduce

    + For the purposes of the final, we will use either
        the simple version of MapReduce from class,
        or the generalized one from HW2
        (I will remind you of the type of map/reduce for the exam)

    + simplified model (map and reduce, conceptually)
    + general model (that we saw on HW2) assuming I give you
      the actual types for map and reduce for reference
    + you may be asked to describe how to do a computation as a MapReduce
      pipeline - describe the precise function

        for map: function that takes 1 input row, produces 1 output row
        for reduce: function that takes 2 output rows, returns 1 output row

- Implementation details: In general, you do not need to know implementation details of Spark, but you should know:
    + Number of partitions and how it affects performance
        * too low, too high
    + Running on a local cluster, running on a distributed computing cluster
    + Fault tolerance: you may assume that Spark tolerates node failures (RDDs can recover from a computer or worker crash)

- Drawing a PySpark or MapReduce computation as a dataflow graph

- Limitations of Spark

## Lecture 6

- Understanding latency

    + Intuitive: for example, given 10 orders in a 1 s time interval are
      processed, what can you say about the latency of each order

    + Refined def of latency:
        latency of item X = (end or exit time X) - (start or arrival time X)

- List of summary points:
    + Latency = Response Time
    + Latency can only be measured by focusing on a single item or row. (response time on that row)
    + Latency-critical, real-time, or streaming applications are those for which we are looking for low latency (typically, sub-second or even millisecond response times).
    + Latency is NOT the same as 1 / Throughput
        * If it were, we wouldn't need two different words!
    + Latency is NOT the same as processing time
        * It's processing time for a specific event
    + If throughput is about quantity (how many orders processed), latency is about quality (how fast individual orders processed).

- Batch vs. streaming pipelines

    + When streaming is useful (application scenarios)

    + Latency in both cases

    + How to derive latency given the dataflow graph

    + Batch/stream analogy

- Implementation details of streaming pipelines:

    + Microbatching and possible microbatching strategies

    + Spark timestamp (assigned to all members of a microbatch)

- Time

    + Why it matters: measuring latency, measuring progress in the system, assigning microbatches

    + Reasons that time is complicated (time zones, clock resets)

    + Kinds of time: Real time, event time, system time, logical time

    + Monotonic time
        * which of the above or monotonic

    + Measuring time: entrance time, processing time, exit time (These are all versions of system time.)

## Lecture 7

Will not be covered on the final.

TBD: the lecture is very brief and the last 1-2 days of class.

Example multiple choice question:

  Match each of the following cloud provider services to its use case.

  Major AWS cloud services: S3, EC2, Lambda.

  S3: useful for data storage

  EC2: useful for purchasing compute (basically, cloud computers that you can log into and run via the terminal)

  Lambda: useful for triggering events and running asynchronous code.

## Notes

Some things you do **not** need to know:
Python, Pandas, and PySpark syntax.
Implementation details of PySpark and Spark Streaming, except where mentioned above.
Lecture 7.
