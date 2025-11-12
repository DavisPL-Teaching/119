"""
Part 4: Parallelism Types

===== Back to parallelism! ======

Now that we know about concurrency and distribution,
at this point in the lecture, let's go back
to simple parallelism.
Also, we will move from thinking about parallelism in general
to how they are most used / most useful in data science.

Goals:

    - We want to think about parallelism at a higher-level than
      individual workers and processes

      Simply: is it parallel? how much parallelism?

    - We want massively parallel computations
      + we want fast results
        (not waiting 2 hours or 2 days to get a query result)
      + we want deployed pipelines to not
        waste money and resources

    - We want to avoid thinking about concurrency
        (why?: concurrency comes with lots of pains,
         including data races, contention, etc.)
        + we can do this by relying on libraries that
          others have built to solve concurrent programming
          problems and to parallelize safely.
          + how those libraries work: they avoid
            reading and writing to the same data at the
            same time.

    - We want to distribute data and computations
        (why?)
        parallelization happens on a single machine,
        distributed code enables us to scale even further.

        + But even when the dataset is distributed, we
          don't want to worry about concurrency and implementation
          details.

Of course, priorities are important:

    - We still want to prototype using a sequential implementation first.

    - We still want to test on smaller datasets if needed

    - For prototypting: resort to parallelism
        if you need it for fast query results

    - For production: resort to parallelism
        if it's faster, cheaper, and more efficient

=== Parallel thinking in data science ===

We've written our pipeline:
Q1: Is it parallel?
Q2: How much parallelism?

About Q1:

We often think about parallelism by dividing it into three types:

If you want to know if a program is parallel, you should be looking
for one of three types of parallelism; I'll show that all three can
be viewed by looking at the dataflow graph.

1. Task parallelism

    Different tasks can be done in parallel.

    ----> i.e. different task, potentially same data points

    ----> the two tasks aren't dependent on each other.

    Example 1: You have an SQL query where you want
    to compute the employee with the highest salary
    and the employee with the lowest salary.

    You might realize that you can compute highest
    with one query, and lowest with a separate query,
    and these two queries can be done in parallel.

    Example 2: Going back to our running example,
    avg. of the first 200,000,000 integers
    we could compute the sum with one worker,
    and the count with the other worker.
    That's task parallelism.

Exercise:
Write a version of our average_numbers pipeline that exploits task parallelism.

We will start with a skeleton of our code from the concurrent example.
"""

from multiprocessing import Process, freeze_support

def run_in_parallel(*tasks):
    running_tasks = [Process(target=task) for task in tasks]
    for running_task in running_tasks:
        running_task.start()
    for running_task in running_tasks:
        result = running_task.join()

from multiprocessing import Array

def worker5(results):
    sum = 0
    for i in range(N):
        sum += i

    results[0] = sum

def worker6(results):
    count = 0
    for i in range(N):
        count += 1

    results[1] = count

def average_numbers_task_parallelism():
    # Create a shared results array
    # i = integer, d = double (we use d here because the integers suffer from overflow)
    results = Array('d', range(2))

    # Iniitalize our shared array
    results[0] = 0
    results[1] = 0

    # Like run_in_parallel but with added code to handle arguments
    p1 = Process(target=worker5, args=(results,))
    p2 = Process(target=worker6, args=(results,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    # Calculate results
    sum = results[0]
    count = results[1]
    print(f"Average: {sum} / {count} = {sum / count}")
    print(f"Computation finished")

# Uncomment to run
# Redefine N again
# N = 100_000_000
# if __name__ == "__main__":
#     freeze_support()
#     average_numbers_task_parallelism()

"""
**pictoral model** (dataflow graph)

    (input1) --> (sum)
                         --> (compute average)
    (input2) --> (count)

Any time there are two nodes which don't depend on each other, that's task parallelism.
"""

"""
2. Data parallelism

    This is the most important one

    Different parts of your dataset can be processed in parallel.

    Example 1: imagine an SQL query where you need to match
    the employee name with their salary

    Different rows in the input: I can match one employee
    name totally independently from another employee name --
    these tasks can be done in parallel!
    That's data parallelism.

    But I claim that this is not yet visible in the dataflow graph!

    (load input employee database) ->
                                      (match employee to salary) -> (print output)
    (load salary database)         ->

    Data parallelism is present at the level of an individual node (task) in the
    graph: it tells me that different inputs to that node can be processed in parallel.

    The (match employee to salary) node in our case can benefit from data parallelism.

    Example 2: In our running example, we were adding up
    the numbers between 1 and 20,000,000.
    We notice that we can add up the numbers between
    1 and 10,000,000 and the numbers betweeen
    10,000,001 and 20,000,000 separately!
    That's data parallelism.

    We can add up different numbers from the input dataset in parallel.

    ----> i.e. same task, different data points

    Summarize here:
    Task parallelism = different tasks on same/different data points
    Data parallelism = same task on different data points.

----

Recap:

(I will post on Piazza about midterm topics / plan)

In the poll, we talked about how programs with concurrency can have many different
wildly different behaviors due to interleaved reads and writes

We'd like to write programs which avoid this issue and benefit from parallelism,
but we don't want to write any concurrent code ourselves

We talked about two types of parallelism with examples and how to identify them in
the dataflow graph:

1. Task Parallelism -- exists between two nodes when there is a path from one to the other

2. Data Parallelism -- exists at a single node when that task can be performed on different elements of the input data set (or sets) at that node in parallel.

----

***** Resuming here for Monday, Nov 3 *****

Recall example so far:
task parallelism

Do we need another example for data parallelism?

No, because we had a data parallelism example in part 2 (2-parallelism.py).

"""

def average_numbers_task_parallelism():
    #  We already saw an example of this
    pass

"""
3. Pipeline parallelism

    (The last type of parallelism is the most strange)
    It's that if two tasks are done in sequence,
    we can still benefit (surprisingly) from parallelism!

    (load dataset) --> (task 1) ---[interm output 1]---> (task 2) ---[interm output 2]---> (save output)

    Example: Take our dataset of employees, for each employee
    name, strip the spaces from the name, then extract the first
    name, then extract the last letter of the first name,
    and save that to an output data frame.

    This is a pipeline of tasks:
    -> I have to strip the spaces before I extract the first name
    -> I have to extract the first name before I can get the last letter
    -> I have to get the last letter before I can save it to the output data frame

    (dataset) --> task 1 --> task 2 --> task 3 --> task 4

    It doesn't seem like there's any parallelism here!
    But there is.

                  task 1     task 2     task 3     task 4
    input/row 1:    1          2          3          4
    input/row 2:    2          3          4          5
    input/row 3:    3          4          5          6

    Overall:
        If we had done this sequentially, would have required 3 * 4 = 12 timesteps

        But! we were able to do it in 6 timesteps

        And we were able to do that all while doing all 4 tasks in order.

    That's pipeline parallelism!

Visual aid!

How do we identify pipeline parallelism in a dataflow graph?

    Draw out the tasks your pipeline as a dataflow graph
    (recall how we did this in Lecture 1):

    (load dataset) -> (calculate a new column) -> (send an email to each student)

    Data parallelism exists if a single node in the pipeline can
    be done in parallel over its inputs

    Task parallelism exists if there two nodes that can be run in parallel without any path from one to the other

    Pipeline parallelism exists if there are two nodes that can be run in parallel with an arrow between them.

Summary:
    two nodes without any path = task parallelism
    1 node with processing different inputs in parallel = data par.
    two nodes with an edge = pipeline parallelism, as long as the second task can begin
    processing the outputs as soon as they are produced, before the first task completes.

=== Discussion Question & Poll ===

https://forms.gle/RWw7i4o5UX1xquhx7

Which types of parallelism are present in the following scenario? (select all that apply)

A Python script is written to complete the following 3 tasks:
1. load a dataset into Pandas: students.csv, with 100 rows
2. calculate a new column which is the total course load for each student; this is the sum of several other columns
3. send an email to each student with their total course load

A. Data parallelism
B. Task parallelism
C. Pipeline parallelism (please note: will not appear on the midterm)

(For each one: be specific about which of task(s) 1-3 is has parallelism)

Answers:
There is data parallelism + pipeline parallelism, but no task parallelism

Let's draw our dataflow graph:

We are given an example with 3 tasks, so we should have three nodes

(1) Load the dataset
(2) Calculate the new column
(3) Send the email

Edges:
(1) -> (2)
and from (2) -> (3)

    Dataflow graph:
    (1) -> (2) -> (3)

    Task parallelism requires two nodes that don't have a path from one to
    the other.

    Pipeline parallelism is present - from (1) -> (2) and from (2) -> (3)

    Data parallelism is present at nodes (1), (2), and (3).

.
.
.
.
.

--------------------

Back to pipeline parallelism example:

Exercise:
Write a version of our average_numbers pipeline that exploits pipeline parallelism.
(This one will be a bit more contrived)

If we want to exploit pipeline parallelism...

    we should have one worker produce as input the integers,
    and one worker process those integers!
"""

def worker7(results):
    # Worker 7 is responsible for loading the input
    # (In our toy example, "loading" just means going through
    # a Python range)
    # and putting into a shared array
    for i in range(N):
        results[i] = i

    print("Worker 7 complete")

def worker8(results):
    # We need to read the output from worker 7!

    i = 0
    sum = 0
    count = 0
    while i < N:
        # Wait for the input at index i
        # There are more efficient ways to do this,
        # but let's do what's called a "busy wait" -- means
        # we just keep running through the loop until the input
        # arrives.
        if results[i] == -1:
            # print(f"Worker loop: if case {i}")
            # Worker 7 hasn't gotten us our input yet!
            # pass
            continue
        else:
            # print(f"Worker loop: else case {i}")
            # Worker 7 has given us our input -- we can continue
            sum += results[i]
            count += 1
            # Make progress -- move on to the next item
            i += 1

    print(f"Average: {sum} / {count} = {sum / count}")
    print(f"Worker 8 finished")

def average_numbers_pipeline_parallelism():
    # Create a shared results array
    # i = integer, d = double (we use d here because the integers suffer from overflow)
    results = Array('d', range(N))

    # Iniitalize our shared array
    for i in range(N):
        results[i] = -1

    # Like run_in_parallel but with added code to handle arguments
    p1 = Process(target=worker7, args=(results,))
    p2 = Process(target=worker8, args=(results,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    # Calculate results
    # -- we don't need to do anything here -- we did this logic in Worker 8.
    print("Computation finished.")

# Uncomment to run
# N = 1_000_000
# if __name__ == "__main__":
#     freeze_support()
#     average_numbers_pipeline_parallelism()

"""
It works!
And it illustrates the basic idea of pipeline parallelism.

--------------------

BUT: there is 1 potential problem here, does anyone see it?

Remember that read + a write to the same memory at the same time
is dangerous. (That's called a data race)

It's not clear whether this actually causes a bug in our pipeline,
(it depends on the architecture and the implementation of Array),
but this could potentially cause arbitrary behavior or random data
to be saved into the array, we saw this in a previous example.
"""

"""
(Skip)
What do these types of parallelism look like on a real pipeline
rather than a toy example?

Data parallelism:

Pipeline parallelism:

Task parallelism:

=== Additional practice question ===

(We can do this in class if time, if not I will ask the TA to do it as a practice question in discussion section)

A second practice question:

In `extras/dataflow-graph-example.png`
you will find a picture of a dataflow graph.

You don't need to know what all the individual stages are!

(Recall from Lecture 1: Each node represents a task. Arrows --> mean that one task depends on the previous one.)

Assume that yellow nodes mean tasks that load input datasets.
Blue nodes (Map, Semijoin, and Distinct) mean to perform some data transformation or other data operator.

1.
Based on the dataflow graph above, give an example of two tasks that would exhibit task parallelism, or state N/A if no task parallelism is present.

2.
Based on the dataflow graph above, give an example of two tasks that would exhibit pipeline parallelism, or state N/A if no pipeline parallelism is present.

3.
Based on the dataflow graph above, give an example of a task that would exhibit data parallelism, or state N/A if no data parallelism is present.

For this one, you might have to guess a bit as to what "Map", "Semijoin", and "Distinct" mean. Use your best intuition.

.
.
.
.
.

=== Finishing up ===

Q: Which of these is most important in the real world?
(Hint: it's not a close contest)

A:

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

Example: You may be doing 10-15 different tasks as part of your pipeline,
but if your pipeline is 10 million items large, 10-15 is very small
compared to the size of your pipeline.

For this reason, data parallelism is the main focus of most
parallel and distributed data processing frameworks.
(Again, looking forward to lecture 5).

=== Poll and an important note about dataflow graphs ===

(Nov 7 poll)

An important note about identifying parallelism in dataflow graphs!

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

"""
