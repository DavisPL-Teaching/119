"""
Part 4: Parallelism Types

=== A difficult question & Poll ===

1.
Two workers, threads, or processes are accessing the same shared memory variable "x". Each worker increments the variable 100 times:

    for i in range(100):
        x += 1

What are possible values of x at the end of the program?

If it helps: think of x += 1 as a read followed by a write, i.e.
    temp = x + 1
    x = temp

You may assume that the programming language we are working in
executes all the workers concurrently (i.e., interleaving the operations in some way).
You may ignore any possible "undefined behavior".
(I will comment on this briefly after the poll how this would look in a language like C or Rust)

2.
The scenario above exhibits... (select all that apply)
- Concurrency
- Parallelism
- Distribution
- Contention
- Deadlock
- Race condition
- Data race

https://forms.gle/J3QUq9Eeeeuy1WiN7

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

Walk through...
see extras/Data_Race_Poll_Walkthrough.md
and data-race-example.py for executable code for this example.

===== Back to parallelism! ======

Now that we have learned about concurrency, our focus will move
back to simple parallelism.
(We will return to Distribution in Lecture 5!)

Also, we will move from thinking about parallelism *in general*
to how parallelism is most useful in data science:
how to identify and exploit parallelism in your own pipelines and projects.

Goals:

    - We want the benefits from parallelism (fast results and more efficient computations)
      + we want fast results
        (not waiting 2 hours or 2 days to get a query result)
      + we want deployed pipelines to not
        crash due to overloading, causing permanently lost data or resources

    - We want to think about parallelism at a higher-level than
      individual workers and processes

      Simply: is it parallel? how much parallelism?

    - We want to avoid thinking about concurrency

        (why?: concurrency comes with lots of pains,
         including data races, contention, etc.)
        + we can do this by relying on libraries that
          others have built to solve concurrent programming
          problems and to parallelize safely.
          + how those libraries work: they avoid
            reading and writing to the same data at the
            same time.

We should still keep in mind the lessons from parts/1-motivation.py and 2-parallelism.py:

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

We can understand parallelism by dividing it into three types:

If you want to know if a program is parallel, you should be looking
for one of three types.
I'll also demonstrate that all three can be viewed directly by
looking at the dataflow graph.

For each type of parallelism we will go over:

1. The definition
2. Example of a pipeline where it is present
3. Example code
4. How to identify it in the dataflow graph.

===== 1. Task parallelism =====

A pipeline has *task parallelism* if
different tasks can be done in parallel.

----> i.e. different task, same or different data points

----> the two tasks aren't dependent on each other.

Example 1: You have an SQL query where you want
to compute the employee with the highest salary
and the employee with the lowest salary.

You might realize that you can compute highest
with one query, and lowest with a separate query,
and these two queries can be done in parallel.

Dataflow graph (DFG):

                            ---> Find Highest Salary
    Load Employee Salaries
                            ---> Find Lowest Salary

Example 2: Going back to our running example,
avg. of the first 200,000,000 integers
we could compute the sum with one worker,
and the count with the other worker.
That's task parallelism!

DFG:

    (input1) --> (sum)
                         --> (compute average)
    (input2) --> (count)

Exercise:
Write a version of our average_numbers pipeline that exploits task parallelism,
based on the above dataflow graph.

(The code is based off of a skeleton of our concurrent code example)
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
N = 200_000_000
if __name__ == "__main__":
    freeze_support()
    average_numbers_task_parallelism()

"""
### IN THE DATAFLOW GRAPH:

        ---> (Task1) --->


                        ---> (Task2) ---->

Any time there are two nodes which don't depend on each other, there is
**task parallelism** between these two nodes.
"""

"""
===== 2. Data parallelism =====

This is the most important one.

A pipeline has *data parallelism* if
the same task can be done in parallel on different
parts of your dataset.

Example 1: imagine an task where you need to match
the employee name with their salary.
Tasks:
1. Load employee salaries
2. Load employee names
3. Match salaries to names

DFG:

    (load input employee database) ->
                                        (match employee to salary)
    (load salary database)         ->

Different rows in the input: I can match one employee
name totally independently from another employee name --
these tasks can be done in parallel!
That's data parallelism.

But how can we see this in the dataflow graph?

    (load input employee database) ->
                                        (match employee to salary)
    (load salary database)         ->

Data parallelism is present at the level of an individual node (task) in the
graph: it tells me that different inputs to that node can be processed in parallel.

In this case, it is present at:

    (match employee to salary) node

It is also present at all other nodes!

Example 2: In our running example, we were adding up
the numbers between 1 and 20,000,000.
We notice that we can add up the numbers between
1 and 10,000,000 and the numbers betweeen
10,000,001 and 20,000,000 separately!
That's data parallelism.

We can add up different numbers from the input dataset in parallel.

----> i.e. same task, different data points

Summary so far:
Task parallelism = different tasks on same/different data points
Data parallelism = same task on different data points.

Do we need another example for data parallelism?

No, because we had a data parallelism example in part 2 (2-parallelism.py).
"""

def average_numbers_task_parallelism():
    #  We already saw an example of this
    pass

"""
### IN THE DATAFLOW GRAPH:

Data parallelism is present at an individual node (task),
**if** that task can be done in parallel on different chunks or sections of its input.

        ---[input]---> (Task) ---[output] --->

===== 3. Pipeline parallelism (SKIP) =====

The last type of parallelism, and also the strangest!

Imagine that two tasks are done in sequence,
so there's no task parallelism between them - and there's
no data parallelism.

I claim that even in this case,
we can still benefit (surprisingly) from parallelism!

Example: Take our dataset of employees, for each employee
name, strip the spaces from the name, then extract the first
name, then extract the last letter of the first name,
and save that to an output data frame.

DFG:

    (load dataset) --> (strip spaces) --> (extract first name) --> (extract last letter) --> (save output)

This is a pipeline of tasks:
    -> I have to strip the spaces before I extract the first name
    -> I have to extract the first name before I can get the last letter
    -> I have to get the last letter before I can save it to the output data frame

More abstractly:

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

Side note: this is also how your CPU works to make code go super fast :-)
https://en.wikipedia.org/wiki/Instruction_pipelining

That's pipeline parallelism!

Coding example: SKIP (will revisit below).

### IN THE DATAFLOW GRAPH:

Pipeline parallelism is present any time there are two tasks, connected by an edge;
and the second task can begin computing before the first task has completed.

        .... ----> (TASK1) ----> (TASK2) ----> ....

====== Review: Identifying parallelism in the dataflow graph =====

You can use the dataflow graph reliably to identify all types of parallelism!

Review: How?

    Draw out the tasks your pipeline as a dataflow graph
    (recall how we did this in Lecture 1 and above examples)
    (make sure you have 1 node in your dataflow graph per task!)

    (load dataset) -> (calculate a new column) -> (send an email to each student)

Then:

    Data parallelism exists if a single node in the pipeline can
    be done in parallel over its inputs

    Task parallelism exists if there two nodes that can be run in parallel without any path from one to the other

    Pipeline parallelism exists if there are two nodes that can be run in parallel with an arrow between them.

Summary:
    1 node with processing different inputs in parallel = data par.
    2 nodes without any path = task parallelism
    2 nodes with an edge = pipeline parallelism, as long as the second task can begin
    processing the outputs as soon as they are produced, before the first task completes.

-----------------
#### POLL -- do the poll here (if not done yet).
See 4-POLLS.md
-----------------

Finishing the pipeline parallelism example:
Just to give example code.

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
=== Additional practice question ===

SKIP in class; I will ask the TA to do it as a practice question in discussion section

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

Q: Which of the 3 types of parallelism is most important in the real world?
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

=== Recap ===

----
(TODO: UPDATE)
In the poll, we talked about how programs with concurrency can have many different
wildly different behaviors due to interleaved reads and writes

We'd like to write programs which avoid this issue and benefit from parallelism,
but we don't want to write any concurrent code ourselves

We talked about three types of parallelism with examples and how to identify them in
the dataflow graph:

1. Task Parallelism -- exists between two nodes when there is a path from one to the other

2. Data Parallelism -- exists at a single node when that task can be performed on different elements of the input data set (or sets) at that node in parallel.

3. Pipeline Parallelism - exists between a pair of nodes connected by an edge,
where multiple data items are passed between the nodes.
"""
