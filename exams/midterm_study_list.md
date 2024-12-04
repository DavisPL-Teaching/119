# Midterm Study List

Study list of topics for the midterm.

**The midterm will cover Lectures 1-4.**

## Lecture 1 (Introduction to data processing)

- Python classes, functions, modules, unit tests

  (know: why/when you might want to use)

- Data validation: know things that can go wrong in your input!

- Latency and throughput and how to measure them

## Lecture 2 (the Shell)

- "Looking around, getting help, doing stuff" model

  + Underlying state of the shell

- Basic command purposes (I won't test you on syntax!)
  ls, cd, cat, git, python3, >, |, echo, man, mkdir, touch, open, rm
  $PATH, $PWD

- shell commands can be run from Python and vice versa

- dangers of the shell

## Lecture 3 (Pandas)

- what a DataFrame is and basic properties

- know: what would you do right after loading in a dataset?
  validation and cleaning steps; getting a feel for the data;
  understanding checks

- SQL operators on DataFrames (I won't test you on syntax!)

- Mutability: not specifics
  for example, know: modifying rows/columns in-place;
  shallow vs deep copy

- Vectorization: what it means; why hardware acceleration matters;
  typically mutch faster than using a for loop

- Space overhead of using Pandas

## Lecture 4 (Parallelization)

- Know major terms:
    + Parallelism, Concurrency, Distribution

    + Multiple of these can exist at a time

    + You should be able to identify, define, or give an example

    + Scalability

    + Speedup

    + Sequential / sequential execution

- Concurrency vocabulary:

    + See "concepts" section

    + Race condition, Data race, Contention, Deadlock, Consistency

    + Multiple of these can exist at a time

    + You should be able to identify, define, or give an example

    + **Simplified data race model:**
      If a read and a write occurs to the same memory location at the same time,
      or two writes, the data gets corrupted and could be anything.

- Parallel thinking in data science:
    + identifying parallelism, quantifying parallelism
      (see below)

    + Drawing a dataflow graph
        * Nothing fancy! One node per task

        * Directly identify types of parallelism from the graph.

- Types of parallelism:
    + Data, task, pipeline

    + Multiple of these can exist at a time

    + You should be able to identify, define, or give an example

- Quantifying parallelism:
    + Amdahl's law

    + Calculating maximum speedup

    + Understand: the model, theoretical basis and limitations

## Notes

Some things you do **not** need to know:
Python syntax / multiprocess; difference between workers, threads, processes; architectural and language details (like whether a data race causes data corruption on a particular machine or particular hardware).
