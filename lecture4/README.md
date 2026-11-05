# Lecture 4: Parallelism

## Monday, October 26

Changing gears today!

Announcements:

- A few details about the midterm (scheduled for Fri, Nov 6):

    Format:

    + Cheat sheet, typed or handwritten, single sided

    + Roughly: 10 questions, 8 MC/short answer, 2 free response

        The free response questions are longer! Each ~1-2 pages

    + Time length is limited to class time

        Please try to arrive early! Try to arrive 10 mins before

    Studying:

    + Review the polls! `exams/poll_answers.md`

    + A sample exam (from a previous year) will be released later today

    + Study guide: `exams/midterm_study_list.md`

        Contains up to Lecture 1, 2, so far

        More topics will be added from Lecture 4:
        Exam will cover Lectures 1, 2, and first 4 days of Lecture 4 (through next Monday Nov. 2)

        I will go over the full list of topics next Monday.

    + Please ask questions at the OHs, discussion sections, and Piazza!

Plan for today:

- Motivation: scaling your application

    - Along the way: activity and poll

- Key definitions: parallel, concurrent, and distributed computing

Questions?

## Wednesday, October 28

Reminders:

- Midterm: Fri, Nov. 6

    Today (and next week) discussion sections will conduct practice questions
    (from the practice midterm) and midterm review!

    Please attend (or if you missed today, take a look at the discussion recording).

    Resources: in `exams/`

Plan:

- Continuing: Part 2: Parallelism

    Parallel code example

    Difference between parallelism, concurrency, and distribution

- Part 3: Concurrency.

    Starting with a practice question on the poll

    Coding example.

Questions?

## Friday, October 30

Announcements:

- HW1 grades released!

    + There were a few mistakes in the autograder, thank you to those of you who pointed these out.
      You may have noticed an update in your autograder score and your scores should be updated in Canvas.

    + A short note about packaging up your code for others

        Why this is important

        Tips:

            Remove unneeded files like .git/, .pytest_cache, __pycache__, etc,

            Keep needed data files like data/2019.csv

            Try downloading your code on a new user account or machine,
            running it locally and seeing if it works.

Reminders:

- Midterm: Fri, Nov. 6

    + Discussion section Weds.: Midterm Review

    + OH: Today 415, Monday 415

      Come prepared with polls/practice midterm questions you would like to go over.

Plan:

- Part 3: Concurrency

    + Programming example

    + Things that can go wrong

    + Vocabulary/terminology to know

- Poll: Strange behavior of concurrent workers/threads

If we have extra time:

- Part 4: Types of Parallelism.

Questions?

## Monday, November 2

Reminders:

- Midterm this Friday!

  Arrive early!

  Today will be the last day of material covered on the midterm.

  Weds. Discussion section: midterm review

  Weds. continue material; however:
  start of class: I will be happy to go over any topics or polls
  people want to review at the start of class, please come
  prepared!
  Wednesday's poll will also be an extra practice question
  (covering today's material).

Plan:

- Go over last time's poll: data race example.

    SEE: `extras/data-race-example.py` and `extras/Data_Race_Poll_Walkthrough.md`

- Last remaining topic - Part 4: Types of parallelism

    + 3 types:

        * Task Parallelism

        * Data Parallelism

        * Pipeline parallelism

    + Last ~20 mins of class: do the poll (separated out in `parts/4-POLLS.md`)

    + There are two of these polls, we will do one of them today and the other Wednesday

    + If there is time, last ~10 mins of class: go over topics for midterm.
      I will post the study list of topics for your own review after class.

      SEE: `exams/midterm_study_list.md`.

Questions?

## Weds., November 4

Reminders:

- Midterm Friday in class!

    Important:
        Arrive 10min early
        bring single-sided cheat sheet (handwritten or typed)
        bring a pen or #2 pencil.

    Study list & Practice midterm:
    https://piazza.com/class/ms5m0v40uh8613/post/65

    Resources:
    exams/midterm_study_list.md
    exams/poll_answers.md

Plan:

- Questions or topics to go over for the midterm

- Finish Part 4: Pipeline parallelism

- Do the poll (this was posted ahead of time)

If time, continue with:

- Part 5: Quantifying parallelism

- Amdahl's Law.

Reminder, **today's topics (pipeline parallelism + Amdahl's Law) will not be covered on midterm.**

#### Questions or topics for the midterm

On Monday, I asked you to come prepared with any topics or poll questions you would like
to go over.
We can spend some time going over these (first ~20 mins of class or so).

Q: Data parallelism vs. task parallelism

    Data parallelism: same task, different data
                      ^^^^^^^^^ tasks in pipeline (dataflow graph)

            Present at a single node

    Task parallelism: different task, same or different data

            Present between a pair of nodes

    Example:

        Load in input dataset students.csv, calculate total number
        of students

        Load in input dataset students.csv
        Load in input dataset classes.csv
