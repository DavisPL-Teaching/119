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
  10 questions: 8 multiple choice/short answer, 2 free response

  In our testing: takes about 35 minutes (so you should have enough time!)

  Study topic list: start of class today.
  Study questions: go over the in-class polls!

  Midterm is o closed-book, on paper!

  You are allowed a one-sided cheat sheet.
  Handwritten or typed is OK.

  No questions that ask you to hand-write code
  (concepts, not syntax)

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

- Start with the poll

- Fundamental properties of RDDs:
  + laziness (transformation/action distinction),
  + partitioning (wide/narrow distinction)

- Recap on distributed pipelines and dataflow graphs

- MapReduce

- DataFrames

We will finish up Lecture 5 today and Monday.
