# ECS 119: Data Processing Pipelines - Fall Quarter 2025

## Contents

1. [Welcome and Course Information](#welcome-and-course-information)
2. [Lectures](#lectures)
3. [Course Description](#course-description)
4. [Schedule](#schedule)
5. [Grade Breakdown](#grade-breakdown)
6. [Policies](#policies)
7. [Contact and Office Hours](#contact-and-office-hours)

## Welcome and Course Information

Welcome to ECS 119! I look forward to teaching you this quarter!

**Lectures (in `lecture` folders) and other materials are from a previous iteration of the course, and have not yet been updated. These will be updated and posted as we go along this quarter.**

- **Instructor:** Caleb Stanford
- **TA:** Muhammad Hassnain
- **CRN:** 29022
- **Units:** 4
- **Lectures:** Monday, Wednesday, Friday 3:10-4pm in Walker Hall 1330
- **Discussion section:** Wednesdays at 11:00am in Young Hall 194
- **Office hours:** See Piazza
- **Final exam:** Thursday, December 11, 8:00am
- **[Piazza](https://piazza.com/class/mfvn4ov0kuc731)**

## Lectures

To give you a hands-on experience working with programming tools, I typically lecture via live coding.
I will post the code for each lecture in this repository.
To follow along with the lectures, clone the repository:
```shell
git clone git@github.com:DavisPL-Teaching/119.git
```

If you make changes to the code after each lecture, you will need to discard them before pulling again.
For example, you can run:
```shell
git stash
git pull
```

### Lecture Recordings and Zoom

If you miss class, you can make up the lectures (and class polls) at any time
prior to the last day of class.
All lectures will be broadcast and recorded on Zoom.
However, this is a best-effort process, so please keep in mind that occasional technical
difficulties are possible (e.g., lost video recording, poor audio).
Zoom recordings will be made available on Canvas.

## Course Description

Introduction to software systems for working with large datasets and managing data processing jobs.
Hands-on experience with scripting, data sources, data parallelism, data streams, software development and deployment infrastructure, and distributed and cloud computing.

### Prerequisites

I will assume the following prerequisites:
- Some prior exposure to databases (ECS 116 or 165A)
- A basic ability to program (ECS 32A/32B or equivalent). For example, you should be able to write a program like [FizzBuzz](https://www.hackerrank.com/challenges/fizzbuzz/problem).

This course is ideal for mid to upper-level undergraduate majors in **data science.**
It is also open to computer science majors.

### Textbook

There is no required textbook.
If you would like to pick up a textbook, I recommend the following:

- [**Python for Data Analysis.**](https://wesmckinney.com/pages/book.html) Wes McKinney. O'Reilly Media (2012).

- [**Spark: The Definitive Guide: Big Data Processing Made Simple.**](https://www.oreilly.com/library/view/spark-the-definitive/9781491912201/) Bill Chambers and Matei Zaharia. O'Reilly Media (2018).

- [**Big Data: Concepts, Technology, and Architecture.**](https://www.wiley.com/en-us/Big+Data%3A+Concepts%2C+Technology%2C+and+Architecture-p-9781119701828) Nandhini Abirami R, Seifedine Kadry, Amir H. Gandomi, and Balamurugan Balusamy. Wiley; 1st edition (2021).

### Learning Objectives

By the end of the course, students will be able to:

- Use Python and other scripting tools to manage data processing jobs on a single machine, and understand their components, techniques, tools, and performance metrics.

- Understand how software engineering tools and configuration are integrated into a data project, via tools like Git and the shell and other orchestration.

- Understand the concepts of parallelism, types of parallelism, and parallelization mechanisms, via tools like MapReduce, Hadoop and Spark.

- Understand the concepts of distributed computing and distributed data processing, including distributed consistency requirements, and how it manifests in real-world applications.

- Understand advanced topics including programming over real-time and streaming data sources and using cloud platforms such as AWS, Azure, and Google Cloud.

## Schedule

See `schedule.md`.

## Grade Breakdown

**Please note: this section is subject to change but will be finalized on the first day of class.**

Your grade is evaluated based on the following.

- **Participation (10%):** via in-class polls
- **Homeworks (30%):** I plan to assign about 3 homeworks, plus homework 0
- **Midterm (20%):** covering the first half and main concepts of the course
- **Final Exam (40%):** covering all topics covered in the course.

### Attendance and Participation (10%)

To encourage class attendance, there are in-class polls that are worth a small amount of credit.
However, if you miss class, you may make up the polls
by watching the lectures and filling out your responses offline.
Polls may be made up at any time prior to the last day of class.

The discussion section is recommended, but not mandatory.
It will be led by the TA and will also be recorded for those who cannot attend.

### Homeworks (30%)

Homeworks will consist of programming assignments in Python designed to bring together concepts we learned in class
and to give you practice using all of the tools we cover.
I plan to assign about 3 homeworks, plus homework 0, which is designed to help you install the relevant software for the course.

**Important: your code must run to get credit!**
Frequently running and testing your code during development is an essential part of computer programming that can never be skipped.
You must run Python on your code before each submission to ensure that it works.
The graders will not be able to debug submissions, and code that does not run may receive a 0 or at most 50% of partial credit.

Homeworks will be graded primarily for correctness and completion.
There will also be a small number of points reserved for code quality - this will be allocated as either at most 10% of each assignment, OR at most 30% of one assignment, and 0% for the others.
These points will consider: does you program exhibit high code quality standards?
Is it readable, shareable, well-documented, well-commented, logically separated into modules and functions, and reasonably efficient?
Are your free response answers thoughtful?
We will be using Gradescope for homework submissions and grading.

### Exams (60%)

There will be a midterm and a final exam.
Exams are closed-book, but you may bring a single-sided cheat sheet to each exam.
Exams will be graded on Gradescope.

I may choose to curve exams to a lower maximum score.
That means, for example, if 100 points are possible, it may be entered as out of a smaller number of points like 95 or 85 for the purposes of calculating your grade, if the average score of the class was low or if there were unexpectedly difficult questions.

### Final Grade

For the final (letter) grade, the following are minimum cutoffs. That is, if your grade is above the given percentage, you will definitely receive at least the given grade. However, I reserve the right to lower the cutoffs (i.e. you might get a better grade than what the table says).
This will be used to correct for the case that the assignments, midterm, and/or final were harder than expected.

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

## Policies

### AI Policy

AI collaboration is allowed and encouraged for homework assignments.
However, the midterm and final exam will be in-class and closed-book.
I encourage you to use AI responsibly and in a way that helps you learn, rather than replacing your own critical thinking skills!
Please see also [Prof. Jason Lowe-Power's advice here](https://jlpteaching.github.io/comparch/syllabus/#using-generative-ai-tools).

### Collaboration Policy and Academic Integrity

This class will encourage collaboration; however, each person should complete their own version of the assignment. **You should not directly copy code from someone else, even within your study group,** but you can receive help and give help on individual parts of an assignment.
In a real software development or data scientist job, it is common to seek and get help; this class will be no different!

You may work on homework assignments in groups of up to 3 people, as long as everyone is working on their own copy of the code. If you do this, please list the names of your collaborators at the top of your submission.

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

### Late Policy

In-class participation points (polls) as well as HW0 can be made up at any point during the quarter (prior to the last day of class), by submitting the Google form link. The forms will remain open and can be found by viewing the lecture recording or lecture notes for that day.
I will not be able to provide a consolidate list of the form links, as their purpose is to encourage you to attend and
watch the lectures.

Homeworks will generally be due at 11:59pm on the due date.
**I cannot guarantee that late homeworks will be graded.**
However, I encourage you to update your assignments even after the deadline -- Gradescope will allow you to upload late work up to a few days after the assignment deadline.
At grading time, we may choose to grade the more recent version at our discretion.

### Job Scams

Communication from the instructor will only be sent through official UC Davis email addresses and channels. Please be vigilant of job scams impersonating faculty members. For more information, visit [UC Davis Job Scams Prevention](https://careercenter.ucdavis.edu/job-and-internship-search/job-scams).

### Be Nice!

Finally: **please be kind to each other!**
UC Davis has [policies against harassment and discrimination](https://hr.ucdavis.edu/departments/elr/preventing-discrimination-harassment).
Be inclusive of your classmates in group discussions and in your questions and answers in class.
If you need to, you may reach me by email to report an issue with a classmate.

## Contact and Office Hours

Please use the Piazza for questions related to course material.
If you send me an email, I will most likely respond to post your question on Piazza :)

Please ask all questions publicly, with only one exception: if your post contains a large snippet of code then make it private.
I encourage you to ask anonymously if you feel more comfortable.

The instructor and TAs will be available during office hours for additional support on course material and assignments. The schedule of office hours can be found in a pinned post on Piazza.

If you have a question that is more sensitive or unrelated to the course, please email me (at `cdstanford` `ucdavis` `edu`).
