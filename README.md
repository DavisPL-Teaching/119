# ECS 119: Data Processing Pipelines - Fall Quarter 2024

## Welcome and Course Information

Welcome! I am super excited to have you all here.

- **Instructor:** Caleb Stanford
- **TA:** Muhammad Hassnain
- **CRN:** 49704
- **Units:** 4
- **Lectures:** Monday, Wednesday, Friday 3:10-4pm in Teaching and Learning Complex 3215
- **Discussion section:** Mondays at 9am in Olson Hall 206.
- **Final exam:** Wednesday, December 11, 6-8pm.
- [CS department link](https://cs.ucdavis.edu/schedules-classes/ecs-119-data-processing-pipelines)

## Lectures

Most lectures will be live coding, and I will post the code for each lecture in this repository.
To follow along with the lectures:

Clone the repo:
```shell
git clone git@github.com:DavisPL-Teaching/119.git
```

If you make changes to the code after each lecture, you will need to discard them before pulling again.
For example, you can run:
```shell
git stash
git pull
```

## Textbook

There is no required textbook,
but the following textbooks are optional:

- [**Python for Data Analysis.**](https://wesmckinney.com/pages/book.html) Wes McKinney. O'Reilly Media (2012).

- [**Spark: The Definitive Guide : Big Data Processing Made Simple.**](https://www.oreilly.com/library/view/spark-the-definitive/9781491912201/) Bill Chambers and Matei Zaharia. O'Reilly Media (2018).

- [**Big Data: Concepts, Technology, and Architecture.**](https://www.wiley.com/en-us/Big+Data%3A+Concepts%2C+Technology%2C+and+Architecture-p-9781119701828) Nandhini Abirami R, Seifedine Kadry, Amir H. Gandomi, and Balamurugan Balusamy. Wiley; 1st edition (2021).

## Course Description

Introduction to software systems for working with large datasets and managing data processing jobs.
Hands-on experience with scripting, data sources, data parallelism, data streams, software development and deployment infrastructure, and distributed computing.

## Prerequisites

The official prerequisites are ECS 116 or 165A.
I will assume the following prerequisites:
- Some prior exposure to databases
- A basic ability to program (e.g. basic Python or C/C++ code). For example, I will assume the ability to write a program like [FizzBuzz](https://www.hackerrank.com/challenges/fizzbuzz/problem) (ECS 36A/36B/36C or equivalent).

This course is ideal for mid to upper-level undergraduate majors in **data science.**
It is also open to computer science majors.

## Learning Objectives

By the end of the course, students will be able to:

- Use Python and other scripting tools to manage and manipulate data on a single machine.

- Understand the components, techinques, tools, and performance metrics of setting up data processing jobs in Python.

- Understand the concepts of parallelism, types of parallelism, and parallelization mechanisms, via tools like MapReduce, Hadoop and Spark.

- Understand how software engineering tools and configuration are integrated into a data project, via tools like Git and the shell and other orchestration.

- Understand the concepts of distributed computing and distributed data processing, including distributed consistency requirements, and how it manifests in real-world applications.

- Understand advanced topics including programming over real-time and streaming data sources and using cloud platforms such as AWS, Azure, and Google Cloud.

## Course Outline

Here is a rough course outline of what topics we will cover in more detail:

1. Basics of big data processing
- Sources of big data: databases, real-time data
- Scripting in Python
- Other tools: shell, shell scripting (time permitting)
2. Software development tools
- Debugging and IDE
- Version control, eg. Git
- Testing and quality assurance
- Ethics of data collection and big data systems
- Virtualization e.g., Docker (time permitting)
3. Data processing
- Data input sources
- Scraping and collecting data
- Data transformations and operators
- Data outputs
- Interacting with databases
- Important performance metrics
4. Data parallelism
- Parallel algorithms and parallel thinking
- Types of parallelism: pipeline parallelism, task parallelism, data parallelism
- MapReduce/Hadoop
- Distributed files and filesystems (time permitting)
5. Advanced Programming in Spark
- Operator chaining
- Autoparallelization and optimizations
- Data streams (in Python, Spark)
- Communicating between nodes
- Interacting with external state
6. Advanced topics: distributed and cloud programming
- Distributed consistency requirements
- Distributed algorithms
- Communication between nodes
- Distributed data structures, and distributed streaming
- Cloud computing resources (S3, EC2, Lambda)
- Cloud computing providers: AWS, Google Cloud, Azure

## Course Schedule

See `schedule.md`.

## Evaluation Criteria

- **Participation (10%):** via in-class quizzes
- **Homeworks (45%):** 3 assignments, each assignment including a project component, plus homework 0
- **Midterm (15%):** covering the first half and main concepts of the course
- **Final Exam (30%):** covering all topics covered in the course.

## Grade Breakdown

The following are minimum cutoffs: if your grade is above the given percentage, you will definitely receive at least the given grade. However, I reserve the right to lower the cutoffs (i.e. you might get a better grade than what the table says).
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

## Homeworks

Homeworks will consist of programming assignments in Python designed to bring together concepts we learned in class
and to give you practice using all of the tools we cover.
There are 3 homeworks, plus homework 0, which is designed to help you install the relevant software for the course.

Each homework will have a project component. That means that as part of homeworks 1, 2, and 3, you will put
together progress towards data collection, data analysis, and a working pipeline for a project of your choice.
I will provide detailed instructions in class and together with each homework when it is released.

## Homework Grading

**Most important:** Your code must run to get credit!
Frequently running and testing your code during development is an essential part of computer programming that can never be skipped.
You must run Python on your code before each submission to ensure that it works.
The graders do not have time to debug submissions, and code that does not run will generally receive either a 0 or at most 10% of partial credit.

Other than this, your assignments will be graded on the following two broad criteria: correctness and code quality.
The majority of the grade will be based on correctness.
You may expect a rough rubric of 90% of the points for correctness and 10% for code quality.

- **Correctness:** Does you program work? That is, does it have the right output on each input and run within a reasonable amount of time? Are your answers to individual questions correct? Does it do everything that's it's supposed to, are there bugs?

- **Code quality:** Does you program exhibit high code quality standards? That is, modular code, readable, not overly complex, well documents, commented, logically separated modules and functions, and reasonably efficient? Are your free response answers thoughtful?

## Exams

There will be a midterm and a final exam.
Exams are closed-book, but you may bring a cheat sheet (single sided) to each exam.

**The exams may be lightly curved:**
That means, for example, if 100 points are possible, it may be entered as out of a smaller number of points like 95 or 85 for the purposes of calculating your grade, if the average score of the class was low or if there were unexpectedly difficult questions.
However, I will not announce the curving strategy ahead of time.

## GitHub Classroom and Gradescope

Exams will be graded on Gradescope, and homeworks will be submitted through GitHub Clasroom.
I will announce more details on how to set up an account with the first assignment.

## Attendance and Participation

To encourage class attendance, there are in class polls that are worth a small amount of credit.
However, if you miss class, you may make up the in-class quizzes
by watching the lectures or looking at slides and filling out your quiz responses offline.
Quizzes may be made up until the end of the quarter (i.e., the last day of class).

## Lecture Recordings and Zoom

**Disclaimer:** I will be broadcasting and recording lectures on Zoom, but this is a best-effort process; I can make no promises that this will work every time, or that it will be as audible/understandable as the in-person lectures.
In particular, please note the following:

- I will share my screen, but I won't generally check the Zoom chat for interactions/questions

- I will generally try to face the audience, so it may not be as easy to see what I am talking about through Zoom, or to see things like audience interaction, or if we write something on the board.

Despite these caveats, my voice will be audible and you should generally be able to follow along through the slides if you need to.
Zoom recordings will be made available on Canvas.

## AI Policy

AI collaboration is allowed and encouraged for homework assignments.
However, the midterm and final exam will be in-class and closed-book.
I caution that becoming too dependent on AI can prevent you from learning on your own including developing your own critical thinking skills.
Please see also [Prof. Jason Lowe-Power's advice here](https://jlpteaching.github.io/comparch/syllabus/#using-generative-ai-tools).

## Collaboration Policy and Academic Integrity

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

## Late Policy

In-class participation points (polls) as well as HW0 can be made up at any point during the quarter (prior to the last day of class), by submitting the Google form link. The forms will remain open and can be found by viewing the lecture recording or lecture notes for that day.
I will not be able to provide a consolidate list of the form links, as their purpose is to encourage you to attend and
watch the lectures.

Homeworks will generally be due at 11:59pm on the due date.
**I cannot guarantee that late homeworks will be graded.**
However, I encourage you to update your assignments even after the deadline -- GitHub classroom will allow us to see both the state of the code at the time of the deadline as well as any recent changes.
At grading time, we may choose to grade the more recent version at our discretion.

## Disclaimers

Communication from the instructor will only be sent through official UC Davis email addresses and channels. Please be vigilant of job scams impersonating faculty members. For more information, visit [UC Davis Job Scams Prevention](https://icc.ucdavis.edu/find/scams).

**Please be kind to each other!**
UC Davis has [policies against harassment and discrimination](https://hr.ucdavis.edu/departments/elr/preventing-discrimination-harassment).
Be inclusive of your classmates in group discussions and in your questions and answers in class.
If you need to, you may reach me by email to report an issue with a classmate.

## Contact and Office Hours

Please use the Piazza for questions related to course material.
If you send me an email, I will most likely respond to post your question on Piazza :)

Please ask all questions publicly, with one exception, if your post contains a large snippet of code.
I encourage you to ask anonymously if you feel more comfortable.

The instructor and TAs will be available during office hours for additional support on course material and assignments. The schedule of office hours can be found in a pinned post on Piazza.
If you have a question that is more sensitive or unrelated to the course, please email me (at `cdstanford` `ucdavis` `edu`).
