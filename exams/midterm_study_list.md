# Midterm Study List

Study list of topics for the midterm.

**The midterm will cover Lecture 1, Lecture 2, and Lecture 4 up through Data Parallelism (in Part 4).**

You should know all of the following concepts, but I won't test you on syntax.
- For example, you won't be asked to write code on the exam,
  but you might be asked to explain how you might to dome task in words
  or asked to calculate how much time a task would take given some
  assumptions about how long the parts take.

## Lecture 1 (Introduction to data processing)

- Data pipelines: the ETL model

    + Know each stage and why it exists

- Dataflow Graphs

    + Know how to draw a dataflow graph

    + Definition of edges & dependencies

    + Definition and application of: sources, data operators, sinks

    + Definition of an operator

    + Relation between ETL and dataflow graphs

- Coding practices: Python classes, functions, modules, unit tests

- Performance:

  Latency and throughput:
  concepts, definitions, formulas and how to calculate them

- Pandas: what a DataFrame is and basic properties

  (some number of rows and columns)

  (DataFrame = table)

- Also know:

  + Know a little bit about data validation: things that can go wrong in your input!

    (check for null values, check that values are positive)

  + Some things about exploration time vs. development time:
    I might ask you what step(s) you might do to explore a dataset
    after reading it in to Python or Pandas

  + Know the following term: vectorization

## Lecture 2 (the Shell)

- "Looking around, getting help, doing stuff" model

  + 3 types of commands

  + Underlying state of the system

    (current working directory, file system, environment variables)

- Basic command purposes (I won't test you on syntax!)
  ls, cd, cat, git, python3, echo, man, mkdir, touch, open, rm, cp
  $PATH, $PWD

- shell commands can be run from Python and vice versa

- hidden files and folders, environment variables

- platform dependence; definition of a "platform"

  platform = operating system, architecture, any installed software requirements or depdencies

- named arguments vs. positional arguments

- Git, philoslophy of git

- dangers of the shell, file deletion, concept of "ambient authority"

## Lecture 4 (Parallelism)

Part 1:

- Scaling: scaling in input data or # of tasks; Pandas does not scale

Part 2:

- Definitions of parallelism, concurrency, and distribution;
  how to identify these in tasks; conveyer belt analogy

- Should be able to give an example scenario using these terms, or an example
  scenario satisfying soem of parallelism, concurrency, and distribution but not
  the others

- How parallelism speeds up a pipeline; be able to estimate how fast a program would take given some assumptions about how long it takes to process each item and how
it is parallelized

Part 3:

- Know terminology: Concurrency, race condition, data race, undefined behavior, contention, deadlock, consistency, nondeterminism

- "Conflicting operations": for example, a read/write are conflicting, two writes are conflicting, two reads are not conflicting as they can both occur simultaneously (this is also part of the definition of a data race)

- Know possible concurrent executions of a program: you won't be asked a scenario as complex as the poll on Oct 31. However, you might be asked about a simpler program, like one with two workers, one increments x += 1, the other implements x += 1 twice, etc.

- Why we avoid concurrency in data pipelines: difficult to program with; no one
  should write any program with data races in it.

Part 4:

- Motivation: is parallelism present? how much parallelism?
  Want to parallelize without writing concurrent code ourselves

- Types of parallelism: task parallelism, data parallelism

- How to identify each of these in the dataflow graph.
