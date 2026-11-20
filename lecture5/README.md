# Lecture 5: Distributed Pipelines

## Friday, Nov 13

(Happy Friday the 13th!)

Announcements:

- Midterm grades released!

    See https://piazza.com/class/ms5m0v40uh8613/post/77

    Curve: set to 80.5. (This was set to the 3rd highest score, which means a couple of you get extra credit, and it raises the median from a 76% to an 80%.)

    If you did not do as well as you hoped, don't worry!
    Please focus on studying the questions you missed and hopefully you will be able to do better
    on the final.

    Please come to office hours, come after class, etc. to get help with studying or do go over questions that you missed.

    Some of you are very behind on the in-class polls. I will sync these again after today's class.
    Please go back and make up the in-class polls, this will help some of your grades.

    Grading notes: We generally tried to be very generous with partial credit,
    especially in Q10. Some questions are a little less generous with partial credit.

    Regrade requests:
    Open for 1 week (until Wednesday 11:59pm).

- HW2 now available (Early release)

    https://github.com/DavisPL-Teaching/119-hw2

    Due: Monday, Nov 23, 11:59pm

    Covers material from Lecture 5, you are welcome to get started early.

- OH today: postponed to 430pm-530pm.

Plan:

- Loose ends in Lecture 4: part 6

    + One remaining definition: Vertical vs. Horizontal scaling

- Lecture 5, Part 1:
    Introduction to distributed pipelines

    + Poll

    + Scalable collection types

    + RDDs.

Questions

- Any questions about HW2
    or you would like to go over from the midterm?
    (or plan for today)

###### Going over midterm questions

Q9c

    1. Not re-running the pipeline frequently

    2. # rows: roughly around (bounded by) 50*50 = 2500

        Very small dataset

        No exact cutoff. Thousands of data items is usually very fast
        to run. Hundreds of millions, parallelism will start to be useful.

Q9d

    Two good answers here:

    - "Officially recognized name" is present only if different from other
      names, so we would expect fewer than 50 officially recognized names.

    - country names are complicated (politically etc.), so may appear
      under different names. There are also often idiosynchrasies
      (as we saw with the population.csv dataset of Lecture 1/HW1).

    Either way, answer is no, this is not a good validation step

Q7

    Distributed: multiple sensor devices (+ laptop)

    Parallel: each device is a worker; devices running at the same time

    Concurrent: because of communication, the devices are sending their data to the central laptop, we assume that if there is communication between
    nodes then there is a possibility of conflicting or overlapping operations.

## Monday, November 16

week 9 of the quarter! There are only 3 weeks left of classes.

(It's hailing outside! Hope everyone is staying dry.)

Looking ahead:

- HW2 due in 1 week, 11/23 11:59pm

- There will be no further HWs (following HW2).

- All in-class polls due by last day of class (Friday, Dec 4 11:59pm)

- Final exam: Friday December 11, 10:30am-12:30pm
  (Last day of finals period)

Reminders:

- TA OH today, 415-6pm

- Reviewing the midterm questions -
  BTW, I put the questions we reviewed at the start of last time above,
  so that you can review the answers there.

  Some notes:
  The hardest questions were Q9(c) and Q10(c).
  Only 42% of you got 9c and only 2 fully correct solutions to 10c.

Plan:

- Finish part 1 on RDDs:

    + Note on PySpark and distributed deployment

    + Further coding examples Python types vs. scalable collection types

    + RDDs = data parallelism

- Part 2: Properties of RDDs:

    + Poll

    + Properties:
      RDDs are *scalable, (data-)parallel, lazy, immutable, partitioned, and fault-tolerant.*
      (What do these mean)

    + Chemistry dataset: New dataset for our running examples.

Questions?

## Wednesday, November 18

(It's raining again... (-: )

Announcements:

- HW2 deadline extension: I will move to Tuesday 11:59pm.

  We will talk about MapReduce today.

Reminders:

- Final exam: Friday December 11, 10:30am-12:30pm
  (Last day of finals period)

Plan:

- We will start today with Part 3: MapReduce

- Return back to Part 2: Properties of RDDs

    + Laziness: Transformations vs. actions

    + Immutability, partitioning, fault-tolerant

- Then come back to the poll question: an exercise on laziness.

Questions?

## Friday, November 20

Reminders:

- HW2 deadline is now Tuesday 11:59pm.

- Final exam: Friday December 11, 10:30am-12:30pm
  (Last day of finals period)

Plan:

- Loose ends on Part 2

    + Go over poll from last time

    + Laziness

    + Immutability

    + Fault tolerance (brief)

- No loose ends on Part 3 (however, please see extra practice questions in `extras/exercises.py`.)

    + Also: poll today will be a practice question on MapReduce

- Part 4, Data Partitioning:

    + Why do RDDs work? data partitioning

    + Problems with data partitioning (and an anecdote)

    + Example code for our chem dataset

    + Wide vs. Narrow operators.
