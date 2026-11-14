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

Midterm:

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
