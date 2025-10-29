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

Throughput always (increases, decreases, is constant) with the size of the dataset
Running time generally increases with the size of the dataset
Latency is often measured using a dataset with only one item
Latency always decreases if more than one item is processed at the same time

https://forms.gle/JE4R1bMU13JAvAE36

Running time generally increases - True

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

===== Introduction =====

=== Scripting and the "Glue code" problem ===

Programs are not very useful on their own.
We need a way for programs to talk to each other!
That is, we need to "glue" programs or program components together.

Examples:

- Our data processing pipeline talks to the operating system when it
  asks for the input file life-expectancy.csv.

- Python module example: If another script wants to use our code, it must import it
  which requires the Python runtime to find the code on the system
  (see `module_test.py` for example)

- Much of Pandas and Numpy are written in C. So we need our Python
  code to call into C code.

What tools do people use to "glue" programs together?

1. Using system libraries (like os and sys in Python)

2. Module systems within a programming language (`import` in Python)

3. Shell: To talk to a a C program from Python, one way would be to run commands through the shell

Other solutions:

4. Scripting languages: Python, others (e.g. Ruby, Perl)

For the most part, we can assume in this class that much of this interaction
happens in Python
(In fact, we will see how to do most things in today's lecture both
in the shell, AND in Python!)
But it is still useful to know how this program
interaction happens "under the hood":

When Python interacts with the operating system and with programming languages other than Python, *internally* a common way to do this is through the shell.

----

Let's open up the shell now.
"""

# Mac: Cmd+Space Terminal
# VSCode: Ctrl+` (backtick)
# GitHub Codespaces: Bottom part of the screen

# Once we have a shell open, we have a "command prompt" where
# we can run arbitrary commands/programs on the computer (so it's
# like an admin window into your machine.)

"""
Questions:

+ If I can run commands from Python (we'll see that you can), then why should I use the shell?

+ If I can use a well-designed GUI app (such as my Git installation), why should I use the shell?

Examples where programmers and data scientists regularly use the shell:

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
"""

# python3 lecture.py
print("Welcome to ECS 119 Lecture 2.")

# python3 -i lecture.py
# Quitting: Ctrl-C, Ctrl-D

"""
=== What is the Shell? ===

The shell is a way to talk to your computer, run arbitrary commands,
and connect those commands together.

Examples we have seen:

- ls (stands for "list")
  Show all files/folders in the current folder

- cd: change directory

(ls/cd often work together)

- python3 <code>.py: Run the python code found in <code>.py

NOTE: tab-autocomplete: very useful
  (saves keystrokes)
  (will cycle through theh options if there's more than one.)

Very quick recap:
We introduced the shell/terminal/command prompt as a way to solve the "glue code" problem

We went through some motivation for when data scientists might need to use the shell (esp. to interact with things like remote servers), and saw some basic commands.

We'll pick this up on Wednesday, and remember that we will be at
11am on Zoom, with discussion section in the usual classroom/class time.

***** Where we ended for today. *****
"""
