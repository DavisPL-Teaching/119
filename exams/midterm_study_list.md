# Midterm Study List

**Please note: this will be updated again next week with additional topics.**

Study list of topics for the midterm.

Only Lecture 1 and Lecture 2 parts for now.

Some notes:
  concepts, not syntax - you won't be tested on syntax
  no questions which ask you to write actual code.

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
