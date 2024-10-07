"""
Lecture 2: The Shell

This lecture will cover the shell (AKA: terminal or command line),
including:

- command line basics: cd, ls, cat, less, touch, text editors

- calling scripts from the command line

- calling command line functions from a Python script

- git basics: status, add, push, commit, pull, rebase, branch

- pattern matching: grep, find, awk, sed

Background:
I will assume no background on the shell other than the
one or two basic commands we have been typing in class.
(Like `python3 lecture.py`)

===== Introduction =====

=== Scripting and the "Glue code" problem ===

Programs are not very useful on their own.
We need a way for programs to talk to each other!
That is, we need to "glue" programs or program components together.

Examples:

- Our data processing pipeline talks to the operating system when it
  asks for the input file life-expectancy.csv.

- If another script wants to use our code, it must import it
  which requires the Python runtime to find the code on the system
  (see `module_test.py` for example)

- Much of Pandas and Numpy are written in C. So we need our Python
  code to call into C code.

What tools do people use to "glue" programs together?

1. Module systems within a programming language (`import` in Python)

2. Scripting languages: Python, others (e.g. Ruby, Perl)

3. Shell implementations: Terminal on Mac; Anaconda Prompt; the shell inside VSCode; Windows Terminal; Powershell (not recommended)

For the most part, we can assume in this class that much of this interaction
happens in Python (options 1 and 2).
(In fact, we will see how to do most things in today's lecture both
in the shell, AND in Python!)
But it is still useful to know how this program
interaction happens "under the hood":

1. We still need the command line to call our code in the first place.

2. Under the hood, everything is really interacting through the shell
   (or more directly through calls to operating system built-ins)
   -- so it is sometimes easier and more powerful to interact through
   these interface directly.

   (Like opening up your car hood to look inside the engine)

3. Much of code development, building, configuration, management, input,
   and output happens through the shell in the real world.

Let's open up the shell now.
"""

# Mac: Cmd+Space Terminal
# VSCode: Ctrl+` (backtick)
# GitHub Codespaces: Bottom part of the screen

"""
Examples where programmers and data scientists regularly use the shell:

- You have bought a new server machine from Dell, and you want to connect to
  it to install some software on it.

- You bought a virtual machine instance on AWS, and you want to connect to it
  to run your program.

- You want to set up a Docker container with your application so that anyone
  can run and interact with it. You need to write a Dockerfile to do this.

Or even, simply:

- You have written some code, you want to send it to me so I can try it out.

Or even more simply:

- You have a program, and you want to run it.
"""

# python3 lecture.py
print("Welcome to ECS Lecture 2.")

# Quitting: Ctrl-C, Ctrl-D

"""
=== What is the Shell? ===

The shell is a way to talk to your computer, run arbitrary commands,
and connect those commands together.

Examples we have seen:

- ls: list files in our current directory

- cd: change directories

- python3 <code>.py: run a Python script

- pytest <code>.py: run unit tests

- conda install <module>: install new software with Conda

- pip3 install <module>: install new Python libraries with Pip

What do these programs have in common?

- Different programs may have been developed by different people, in different
  teams, in different languages, etc.

- We can't assume someone wrote a nice GUI for us to connect these programs
  or pieces together! (Sadly, often they didn't.)

Let's try running a couple of these to remind ourselves how these work.
"""

# Try:
# python3, ls, pytest, conda

"""
Can we do this in Python?

Sure!
"""

import os

def ls_1():
    # The . refers to the current directory
    print(os.listdir("."))

import subprocess

def ls_2():
    subprocess.run(["ls", "-alh"])

# ls_1()
# ls_2()

# In addition to ., there is another special output: ..

"""
Common theme:
Everything we can do in the shell, we can also do in Python directly.

=== Getting started: informational commands ===

The most important thing you need to know when opening a shell is
how to "look around". What do you see?

(NOTE:The same applies to all commands, including external tools people have built: knowing how to "see" the current
state relevant to your command is often the first step to get a grip on the command.)

- Aside: this used to be a whole genre of text adventure games.
  e.g. Zork (1977):
  https://textadventures.co.uk/games/play/5zyoqrsugeopel3ffhz_vq

So how do we "look around"?

- ls
- echo $PWD -- get our current location
- echo $PATH -- get other locations where the shell looks for programs
- echo $SHELL -- get the current shell we are using

The $ are called "environment variables" -- there are others!
These represent the current state of our shell environment.
"""

def pwd_1():
    print(os.getcwd())

# This one is a bit harder
def pwd_2():
    # os.environ is the Python equivalent of the shell $ indicator.
    subprocess.run(["echo", os.environ["PWD"]])

# pwd_1()
# pwd_2()

# Q: What happens when we run this from a different folder?

"""
We can also look inside files and directories:

- cat
- less
- ls inside an existing directory
"""

def cat_1():
    with open("lecture.py") as f:
        print(f.read())

def cat_2():
    subprocess.run(["cat", "lecture.py"])

def less():
    subprocess.run(["less", "lecture.py"])

# cat_1()
# cat_2()

# less()

"""
=== Navigation ===

Once we know how to "look around", we can make a plan for what to do.

(NOTE: The same applies to all commands: knowing how to "modify" the current
state relevant to your command is often the second step to get a grip on how
the command works.)

So what should we do?
We need a way to move around and modify stuff:

- cd
- mkdir
- touch
"""

def touch():
    # TODO
    raise NotImplementedError

"""
=== Getting help ===

This may actually be more important than the previous two!

One of the following 3 things usually works:
- `man cmd` or `cmd --help` or `cmd -h`

"""

def get_help_for_command(cmd):
    subprocess.run([cmd, "--help"])
    subprocess.run([cmd, "-h"])
    subprocess.run(["man", cmd])

# get_help_for_command("python3")

"""
=== Anatomy of a shell command ===

Commands are given arguments, like this:

cmd --<argument name> <argument value>

We have seen some of these already.

How subprocess works:
"""

def run_python3_file(file):
    # TODO
    raise NotImplementedError

"""
=== Dangers of the shell ===

Be aware!

- rm -rf "/"
"""

def rm_rf_slash():
    raise RuntimeError("This command is very dangerous! If you are really sure you want to run it, you can comment out this exception first.")

    # Remove the root directory on the system
    subprocess.run(["rm", "-rf", "/"])

# rm_rf_slash()

"""
Aside: This is part of what makes the shell so useful, but it is also
what makes the shell so dangerous!

All shell commands are assumed to be executed by a "trusted" user.
It's like the admin console for the computer.

Person who gave an LLM agent access to their shell:
https://twitter.com/bshlgrs/status/1840577720465645960

"At this point I was amused enough to just let it continue. Unfortunately, the computer no longer boots."

sudo: run a command in true "admin" mode
"""

# sudo rm -rf "/very/important/operating-system/file"

"""
=== What is the Shell? (continued) ===

The shell IS:

- the de facto standard for interacting with real systems,
  including servers, supercomputers, and even your own operating system.

- a way to "glue together" different programs, by chaining them together

The shell is NOT (necessarily):

- a friendly, helpful, usable interface for most beginners

- a good way to write complex programs or scripts (use Python instead!)

- free from errors (it is often easy to make mistakes in the shell)

- free from security risks (rm -rf /)

=== Q+A ===

Q: How is this useful for data processing?

A: Managing input and output: often through the filesystem or through other
  programs on the system (e.g. a database implementation or a network API)

A: Many software tools provide useful interfaces that can only be accessed
   through the shell.

A: Data processing scripts have to interact with these
   external tools all the time.

A: The shell is very useful for software development in general.

Q: How is the shell different from Python?

A: It's not really! Both of these are useful "glue" languages -- ways to
   connect together different programs.

A: In fact, we have seen that anything that can be done in the shell
   can be done directly in a Python script.
   (using subprocess)

=== Where we are going next? ===

Things we want to cover:

- How Git works

- Shell combinators (|| && > < >> <<) -- often useful

- Using the shell for cleaning, filtering, finding, and modifying files

  + cf.: grep, find, sed, awk

We will mention but probably not cover:

- Regular expressions for pattern matching in text

=== Further resources ===

ChatGPT is often very good at generating/explaining shell commands.

Here is a fun tool which lets you see the state modified by a shell command
before executing it:
https://github.com/binpash/try

e.g.: try rm -rf /

Several tools now exist for using AI in the shell to help you come up
with the right syntax for shell commands:
https://github.com/ibigio/shell-ai

Future of the shell:
- https://www.youtube.com/watch?v=dMrfLCjtHM4
- https://dl.acm.org/doi/pdf/10.1145/3458336.3465296

Regular expressions:

- Regex debugger: https://regex101.com/

- Regex explainer: https://regexr.com/

  Example to try for a URL: [a-zA-Z]+\.[a-z]+( |\.|\n)

"""
