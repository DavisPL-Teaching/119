# Lecture 5: Distributed Pipelines

## Nov 4

Announcements:

- Mid-quarter survey is now available:
  https://forms.gle/pMLRBJbMWuXUSSFF9

  Worth 1 point of extra credit if completed.
  (Make sure you fill out the second form, link available after the first one is completed, to get the extra credit.)

  Due Thursday.

  Please do fill it out! I appreciate all of your feedback and
  use it to make changes (both this year and next year).
  This is especially helpful as this is a new course and much
  of the content is still in flux as to what is most important
  to cover.

- Midterm on Friday.

  **Details on the midterm:**
  See exams/midterm.md

Questions?

Plan:

- Go over midterm study list

- Recap on dataflow graphs and poll

- Scalable collection types

- Programming over collection types with distributed data pipelines.

## Nov 6

Announcements:

- Midterm on Friday

    + My office hours are moved to tomorrow, Thursday 430-530pm.

    + I will reserve 5-10 minutes at the start of class to help with any study/review questions.

    + Poll question answers: poll_answers.md

- Thank you to those of you who have filled out the mid-quarter survey so far!
    Your answers have been super helpful.
    If you haven't yet, please fill it out!
    Survey (+EC) open through EOD tomorrow.

Plan:

- Start with the poll

- Recap on scalable collection types

    + comparison between Python collections and scalable collections

- RDD fundamentals: laziness, wide/narrow operators, partitioning

- A second scalable collectoin type: DataFrames

- MapReduce and how Spark works under the hood.

## Nov 15

Welcome back!

Announcements:

- Midterm is graded, and grades will be released after class today

  I am happy with how everyone did overall!
  There were a couple of questions I noticed we could have spent more time in class going over
  the techniques, which I will spend more time on going forward.

- Piazza thread for Wednesday's makeup reading: https://piazza.com/class/m12ef423uj5p5/post/119

- Thank you for the feedback from the mid-quarter survey:

  + Some of you noted that HW1 was long and would prefer shorter assignments released at larger time intervals

  + Stay tuned for an announcement about this on Monday.

Lecture plan:

Continue with RDDs, MapReduce:

- Start with the poll

- Fundamental properties of RDDs:
  + laziness (transformation/action distinction),
  + partitioning (wide/narrow distinction)

- Recap on distributed pipelines and dataflow graphs

- MapReduce

- DataFrames

We will finish up Lecture 5 today and Monday.

Questions?

## Nov 18

Announcements:

- Midterm grades released on Friday

- HW plan and poll (vote requested by EOD tomorrow): https://piazza.com/class/m12ef423uj5p5/post/124

- HW1 grades in progress, will be released as soon as possible!

Plan:

- Start with the poll (a small exercise on lazy operators)

- Last property of RDDs: Partitioning

- MapReduce and DataFrames -- A lower-level abstraction and a higher-level abstraction.

- Endnote on Spark (benefits and drawbacks)

Questions?

## Nov 20

Announcements:

- HW1 grades released and makeup option

  + HW1 makeup option: 80% of the points back (for points below 90).

- HW2/3 poll results: 26 votes for, 1 against

  + We will have only 1 more HW (HW2), and no final project.

  + HW will be only 40% of the grade (participation up to 20%)

  + HW2 will be incrementally released starting on Friday.

  + Additionally, there will be a makeup option for HW1. See above.

- Regrade requests (midterm and HW1): deadline in one week, EOD on Wed, Nov 27.

Plan:

- In-class poll, wrap up wide/narrow

- DataFrames -- a useful higher-level abstraction

- MapReduce -- a useful lower-level abstraction

- Endnote on Spark (benefits and drawbacks)

Questions?
