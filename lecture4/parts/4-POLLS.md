# Part 4 In-class polls

This file contains the in-class polls planned for Monday (Nov 2) and Wednesday (Nov 4).
These accompany the Part 4 lecture on types of parallelism.

### Discussion Question & Poll #1 (Nov. 2)

https://forms.gle/1sWwWtH4msGTAvdU9

Which types of parallelism are present in the following scenario? (select all that apply)

A Python script is written to complete the following 3 tasks:
1. load a dataset into Pandas: students.csv, with 100 rows
2. calculate a new column which is the total course load for each student; this is the sum of several other columns
3. send an email to each student with their total course load

A. Data parallelism
B. Task parallelism

For each type of parallelism present:
Give a specific example node/task or pair of nodes/tasks(s) for which the parallelism is present.

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

Answers:

Data parallelism - yes, at tasks 1, 2, and 3 (any of them works)
Task parallelism - no

Based on this set of three tasks -
let's start by drawing the DFG -

    (1) --> (2) --> (3)

    no task parallelism - no pair of tasks where there is no path frmo one to the other

    data parallelism - examine at each individual node.

--------------------

### Discussion Question & Poll #2 (Planned for Nov. 4)

An important note about identifying parallelism in dataflow graphs!

- Data parallelism:

    Running the same task on different data points

- Task parallelism

    Running two different tasks on same or different data points

- Pipeline parallelism (Not covered on midterm)

    When feeding the output of one task to another, having the second
    task process the partial results of the first task while the first
    task is still running.

How do we connect these types of parallelism to this concept of
dataflow graphs?

    Note: the word "task" as referring to a node in the dataflow graph.

    Different nodes in the graph = different tasks

#### Poll

For this poll, you may find it helpful to review the dataflow graph example that is drawn at:
lecture4/extras/dataflow-graph-example.png

1. For each type of parallelism that can be present in a dataflow graph, does it occur at a single node, or between a pair of two nodes?

2. For two different ways of drawing a dataflow graph (with different delineations of tasks as nodes), could we get different types of parallelism present, based on the above? Briefly comment on why or why not.

https://forms.gle/uvW8BxdD2nACy9Sk7

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

If you don't want to remember the discussion above, just remember:

    1. Data parallelism always exists at a single node, and I can identify
    it by checking if that particular node/task can be run in parallel over
    different chunks/batches of the input

    2. Task parallelism always exists between any two different nodes that are
    independent of one another

    3. Pipeline parallelism always exists between any
    two different nodes which are connected by an edge.
