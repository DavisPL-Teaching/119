# ECS 119: Data Processing Pipelines - Fall Quarter 2024

[CS department link](https://cs.ucdavis.edu/schedules-classes/ecs-119-data-processing-pipelines)

## Lectures

To follow along with lectures:

Clone the repo:
```shell
git clone git@github.com:DavisPL-Teaching/119.git
```

If you have local changes, but haven't committed them, you can stash and then pull
```shell
git stash
git pull
```

Altneratively, if you want to save your work, you can back up your local changes and pull the latest version:
```shell
git fetch --all
git branch backup-changes
git reset --hard origin/main
```

## Course Information

- **Instructor:** Caleb Stanford
- **TA:** Muhammad Hassnain
- **CRN:** 49704
- **Units:** 4
- **Lectures:** Monday, Wednesday, Friday 3:10-4pm in Teaching and Learning Complex 3215
- **Discussion section:** Mondays at 9am in Olson Hall 206.
- **Final exam:** Wednesday, December 11, 6-8pm.

## Textbook

There is no required textbook.
The following textbooks are optional:

- TBD

## Course Description

Introduction to software systems for processing large datasets.  Hands-on experience with scripting, data streams, distributed computing, and software development and deployment infrastructure.

## Prerequisites

The official prerequisites are ECS 116 or 165A.
Some prior exposure to databases, and ability to program (e.g. basic Python or C/C++ code) are assumed.
For example, I will assume the ability to write a program like [FizzBuzz](https://www.hackerrank.com/challenges/fizzbuzz/problem) (ECS 36A/36B/36C or equivalent).

This course is ideal for mid to upper-level undergraduate majors in **data science.**
I believe it is also open to computer science majors.

## Learning Objectives

By the end of the course, students will be able to:

TBD

## Course Topics

Summary of course contents include the following:

1. Basics of big data processing
- Sources of big data: databases, real-time data
- Pipelining in Unix
- Scripting in Python
2.  Software engineering tools
- Debugging and IDE
- Version control, eg. Git
- Virtualization e.g., Docker
- Orchestration, e.g., Puppet, Salt.
3. Organizing teams for Big Data Systems.
- Deciding Goals & Requirements
- Ethics of Big Data Systems
- Testing and Quality assurance
4.  Programming for streaming data
- Data streams in Python
- Data streams in R
5. Distributed processing
- Parallel algorithms and parallel thinking
- MapReduce/Hadoop processing model
- Distributed files and the Hadoop Distributed Filesystem
- Communication between nodes
- Distributed data structures, and distributed streaming, e.g. SPARK, Yarn
- Cloud programming: e.g. AWS S3, EC2, Lambda

## Course Schedule

See `schedule.md`.

## Evaluation Criteria

TBD: Update

- **Homeworks (55%):** 5 assignments (due bi-weekly), plus homework 0
- **Participation (10%):** via in-class quizzes
- **Final Exam (35%):** covering all topics covered in the course.

## Grade Breakdown

The following are minimum cutoffs: if your grade is above the given percentage, you will definitely receive at least the given grade. However, I reserve the right to lower the cutoffs (i.e. you might get a better grade than what the table says).
This will be used to correct for if assignments or the final were harder than expected.

| Percentage | Minimum Grade |
| --- | --- |
| 93 | A  |
| 90 | A- |
| 87 | B+ |
| 83 | B  |
| 80 | B- |
| 77 | C+ |
| 73 | C  |
| 70 | C- |
| 67 | D+ |
| 63 | D  |
| 60 | D- |

## Grading

For homeworks, your assignments will be graded on the following two broad criteria: correctness and code quality.
The majority of the grade will be based on correctness.
You may expect a rough rubric of 90% of the points for correctness and 10% for code quality.

- **Correctness:** Does you program work? That is, does it have the right output on each input and run within a reasonable amount of time? Are your answers to individual questions correct? Does it do everything that's it's supposed to, are there bugs?

- **Code quality:** Does you program exhibit high code quality standards? That is, modular code, readable, not overly complex, well documents, commented, logically separated modules and functions, and reasonably efficient? Are your free response answers thoughtful?

**The final exam may be lightly curved:**
That means, for example, if 100 points are possible, it may be entered as out of a smaller number of points like 90 or 80 for the purposes of calculating your grade, if the average score of the class was low or if there were unexpectedly difficult questions.
However, I will not announce the curving strategy ahead of time.

## Exams

There will be a midterm and a final exam.

## Homeworks and Gradescope

Programming cannot be learned by merely watching or reading, it must be done!
Homeworks will consist of programming assignments designed to bring together concepts we learned in class.

I plan to have homeworks submitted through Gradescope.
I will announce more details on how to set up an account with the first assignment.

## Attendance and Participation

To encourage class attendance, there are in class polls that are worth a small amount of credit.
However, if you miss class, you may make up the in-class quizzes
by watching the lectures or looking at slides and filling out your quiz responses offline.

## Lecture Recordings and Zoom

**Disclaimer:** I will be broadcasting and recording lectures on Zoom, but this is a best-effort process; I can make no promises that this will work every time, or that it will be as audible/understandable as the in-person lectures.
In particular, please note the following:

- I will share screen, but I won't generally check the Zoom chat for interactions/questions

- I will generally try to face the audience, so it may not be as easy to see what I am talking about through Zoom, or to see things like audience interaction, if we write something on the board, etc.

Despite these caveats, my voice will be audible and you should generally be able to follow along through the slides if you need to.
Zoom recordings will be made available on Canvas.

## AI Policy

AI collaboration is allowed and encouraged for homework assignments. However, the midterm and final exam will be in-class and closed-book.
Please see also [Prof. Jason Lowe-Power's advice here](https://jlpteaching.github.io/comparch/syllabus/#using-generative-ai-tools).

## Collaboration Policy and Academic Integrity

This class will encourage collaboration; however, each person should complete their own version of the assignment. **You should not directly copy code from someone else, even within your study group,** but you can receive help and give help on individual parts of an assignment.

You may complete homework assignments in groups of up to 3 people, as long as everyone is working on their own copy of the code. If you do this, please list the names of your collaborators at the top of your submission.

Here are some examples of good (allowed) collaboration:

- Sharing of resources
- Sharing of inspiration
- Sharing questions about the assignment on Piazza
- Helping out classmates on Piazza
- Collaboration at a low level (E.g., hey, what's the syntax for X, again? Why does this code print Y?)
- Collaboration at a high level (Why did they tell us to do this in that way?)
- As in most CS courses, the internet is your friend!

And here are examples of disallowed collaboration:

- Sharing large amounts of code with others within your group or others in the course.
- Sharing the exact solution to a specific mid-level programming problem.
- Asking a stranger to finish your work for you or copying and pasting what you find online for submission.

In other words, please use common sense!
This course strictly follows the [UC Davis Code of Academic Integrity](https://ossja.ucdavis.edu/academic-integrity).

## Late Policy

In-class participation points (polls) as well as HW0 can be made up at any point during the quarter, by submitting the Google form link. The forms will remain open and can be found by viewing the lecture recording or lecture notes for that day.

Homeworks will generally be due at 11:59pm on the due date.

For homeworks, I cannot guarantee that late work will be graded.
However, I encourage you to update your assignments even after the deadline -- GitHub classroom will allow us to see both the state of the code at the time of the deadline as well as any recent changes.
At grading time, we may choose to grade the more recent version at our discretion.

Also, near the end of the quarter, you will be given the opportunity to go back and pick one assignment that you missed points on, and make up the points (up to 50% of the points back that you missed).

## Disclaimers

Communication from the instructor will only be sent through official UC Davis email addresses and channels. Please be vigilant of job scams impersonating faculty members. For more information, visit [UC Davis Job Scams Prevention](https://icc.ucdavis.edu/find/scams).

Please be nice to each other.
UC Davis has [policies against harassment and discrimination](https://hr.ucdavis.edu/departments/elr/preventing-discrimination-harassment).
Be inclusive of your classmates in group discussions.
If you need to, you may reach me by email to report an issue with a classmate.

## Contact and Office Hours

Please use the Piazza for questions related to course material.
I encourage you to ask anonymously if you feel more comfortable.
Also, please ask publicly unless there is a good reason not to.
If you have a question that is more sensitive or unrelated to the course, please email me (at `cdstanford` `ucdavis` `edu`).

The instructor and TAs will be available during office hours for additional support on course material and assignments. The schedule of office hours can be found in a pinned post on Piazza.
