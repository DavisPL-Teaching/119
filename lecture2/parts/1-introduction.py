"""
Lecture 2: The Shell

Part 1: Introduction and Motivation

This lecture will cover the shell (AKA: terminal or command line),
including:

- command line basics: cd, ls, cat, less, touch, text editors

- calling scripts from the command line

- calling command line functions from a Python script

- git basics: status, add, push, commit, pull, rebase, branch

- (if time) searching / pattern matching: find, grep, awk, sed

Background:
I will assume no background on the shell other than the
one or two basic commands we have been typing in class.
(Like `python3 lecture.py`)

=== Discussion Question & Poll ===

Review from last time

1. Which of the following are valid units of latency?
Hours
Items / second
Milliseconds
Nanoseconds
Rows / item
Rows / minute
Seconds
Seconds / item

2. True or false?

- Throughput always (increases, decreases, is constant) with the size of the dataset
- Running time generally increases with the size of the dataset
- Latency is often measured using a dataset with only one item
- Latency always decreases if more than one item is processed at the same time

The poll will also ask you a couple of questions to get feedback on how the course is going so far.

https://forms.gle/B7oYUk3zfnH3qAf66

For throughput:

    Throughput = N / T

    Generally, as a rule, throughput T is linearly related to
    (or proportional to) the size of the dataset, meaning that
    T = constant * N <-- first approximation

    Throughput = N / (constant * N) = 1 / constant

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

  ==== Some notes about running time and throughput (optional) (SKIP) ===

  Throughput = N / T

  N = number of input items
  T = total running time

  Sometimes throughput goes up, sometimes it goes down

  N / T - often roughly linear, but not exactly linear!

  - if N = 1, often the system can't benefit from "scale",
    so throughput will be quite low

  - is N increases (10, 100, 1000, ...) the system will start to
    benefit from scale, so throughput will increase

  - if N -> infinity (more data than the laptop/machine can handle at all), throughput will again tank because the system will
  just completely crash or lag / be unable to do things.

.
.
.
.
.

===== Introduction =====

=== What is the Shell? ===

The shell is how commands are run on most systems - it is the "root user" interface to your computer.

The shell is a way to talk to your computer, run arbitrary commands,
and connect those commands together.

It solves the "glue code problem".

=== Why learn about the shell? ===

Questions:

- If I can run commands from Python (we'll see that you can), then why should I use the shell?

- If I can use a well-designed GUI app (such as my Git installation), why should I use the shell?

- If I can use my AI to generate shell commands or have it interface with a computer directly,
  why should I know about the shell?

Answers:

- The shell tells us what is happening "under the hood"

- The shell is used very commonly in data engineering practice.
  Data engineers and ML engineers often have to reach under the hood to see what's happening with
  a data processing job, or to diagnose why it might be failing, or to set up software/installation/frameworks/etc.
  surrounding data processing jobs

- To understand what AI is doing "under the hood", or even to audit it/correct it/
  provide our own expertise and input on top, we should understand how it works.

- It's fun!

=== What is glue code? ===

The "glue code problem" is that we have some programs or components
in different languages or frameworks, and we need a way to "glue" programs
or program components together.

Examples:

- Our data processing pipeline talks to the operating system when it
  asks for the input file life-expectancy.csv.

- Much of Pandas and Numpy are written in C. So we need our Python
  code to call into C code.

 + So, we can write a shell command to call the C code from Python, or vice versa

 + OR, we can write a shell script that executes the entire job, and calls both C and Python

What other tools do people use to "glue" programs together?

1. Using system libraries (like os and sys in Python)

2. Module systems within a programming language (`import` in Python)

3. Scripting languages: Python, others (e.g. Ruby, Perl)

  (---> We can call shell commands from Python)

For the most part, we can assume in this class that much of this interaction
happens in Python
(In fact, we will see how to do most things in today's lecture both
in the shell, AND in Python!)
But it is still useful to know how this program
interaction happens "under the hood".

- (See reasons above)

- When Python interacts with the operating system and with programming languages other than Python, *internally* a common way to do this is through the shell.

----

Let's open up the shell now.
"""

# Mac: Cmd+Space Terminal
# VSCode: Ctrl+` (backtick)
# GitHub Codespaces: Bottom part of the screen

# You can use any shell you prefer, with the caveat that on Windows I do NOT recommend
# using Windows Powershell - use WSL

# Once we have a shell open, we have a "command prompt" where
# we can run arbitrary commands/programs on the computer (so it's
# like an admin window into your machine.)

# python3 lecture.py
print("Welcome to ECS 119 Lecture 2.")

# python3 -i lecture.py
# Quitting: Ctrl-C, Ctrl-D

"""
=== Using the shell -- examples ===

Examples we have seen:

- ls (stands for "list")
  Show all files/folders in the current folder

- cd: change directory

(ls/cd often work together)

- python3 <code>.py: Run the python code found in <code>.py

  if python3 doesn't work: try python

NOTE: tab-autocomplete: very useful
  (saves keystrokes)
  (will cycle through theh options if there's more than one.)

=== Additional Examples where programmers and data scientists regularly use the shell (SKIP) ===

- You have bought a new server machine from Dell, and you want to connect to
  it to install some software on it.

- You bought a virtual machine instance on AWS, and you want to connect to it
  to run your program.

- You want to set up a Docker container with your application so that anyone
  can run and interact with it. You need to write a Dockerfile to do this.

- Debugging software installations - missing dependencies, missing libraries

  (I have Python3 installed, but my program isn't recognizing it)
  Where is the software? Where is it expected to be?
  ---> move it to the correct location

- You want to compile and run an experimental tool that was published on GitHub

Or even, simply:

- You have written some code, you want to send it to me so I can try it out.

Shell on different operating systems?

- Mac, Linux: Terminal app
- Windows is a bit different, commands by default are very different
  option 1:
  recommend the most: WSL (Windows Subsystem for Linux)
  dropdown next to your shell window -> choose which type of
  shell you want
  With WSL, should be able to select a Ubuntu shell.

  option 2:
  Use the shell built into VSCode

(don't recommend powershell)

=== Recap ===

- On the poll,
  We reviewed throughput/latency -- units; how to apply the formula N / T to make conclusions
  about how throughput/latency change with N and with T
  and other T/F questions

- We introduced the shell, covering:

  + Why learn about the shell? Why is it useful and important, and why is it used in data science
    and data/ML engineering practice

  + Motivation for the shell and the "glue code" problem - how to put together different pieces of
    software written in or provided in various languages or frameworks

  + We opened up a shell and ran a few basic commands to practice, covering

    ls, cd, python/python3 and tab-autocomplete.
"""
