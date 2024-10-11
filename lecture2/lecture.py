"""
Lecture 2: The Shell

This lecture will cover the shell (AKA: terminal or command line),
including:

- command line basics: cd, ls, cat, less, touch, text editors

- calling scripts from the command line

- calling command line functions from a Python script

- git basics: status, add, push, commit, pull, rebase, branch

- searching / pattern matching: find, grep, awk, sed

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

# python3 -i lecture.py
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

# ls: doesn't show hidden folders and files
# On Mac: anything starting with a . is hidden

# To show hidden + other metadata
# ls -alh
# ^^^^^^^ TL;DR use this to show all the stuff in a folder

"""
Can we do this in Python?

Sure!
"""

# os is the operating system library
# i.e.: how Python interacts with the operating system
import os

def ls_1():
    # Listdir: input a folder, show me all the files
    # and folders inside it
    # The . refers to the current directory
    # Also includes hidden files/folders.
    print(os.listdir("."))

ls_1()

# What's the . folder?
# That stands for the current, or working directory
# for the program

# In python it's often useful to call into another
# command -- you can think of this as basically calling into the shell from Python.

# Library for running other commands
import subprocess

def ls_2():
    subprocess.run(["ls", "-alh"])

ls_2()
# ^^^^ same output as if I ran the command line directly

# In addition to ., there is another special folder: ..

"""
Common theme:
Everything we can do in the shell, we can also do in Python directly.
But, sometimes in Python we just directly call into
commands, and knowing shell syntax is important as it
gives a very powerful way for Python programs to interact
with the outside world.

=== Recap ===

What we have learned:
1. The shell is a very powerful "glue code" system that is
   how all programs interact on your operating system
2. Knowing the shell is useful for example for configuration,
   input, output, running commands in other languages,
   running and configuring other tools, etc.
   (Basically: if you can't find a library for it, may
    have to resort to using the shell)
3. It's also the main way that we interact with programs
  and run/test/debug our code.
4. We saw how to run basic commands like ls and ls -alh,
   special folders and hidden folders, and what that
   means.

=============================================

=== Oct 9 ===

We saw how to run basic commands in the shell and what it means.
Today: a tour of the shell (looking around, navigating, help, I/O, etc.)

Main 3 sections or categories of command:
- 1. looking around, 2. getting help, 3. doing something

=== Informational commands: looking around ===

An analogy:
There used to be a whole genre of text-based adventure games.
the shell is kind of like this.

e.g.
- Zork (1977):
  https://textadventures.co.uk/games/play/5zyoqrsugeopel3ffhz_vq
- Peasant's Quest (2004):
  https://homestarrunner.com/disk4of12

Just as in a text-based adventure,
the most important thing you need to know when opening a shell is
how to "look around". What do you see?

The same advice applies to all commands!
Including external tools people have built, and even commands outside of the shell, like
functions in Python:
knowing how to "see" the current
state relevant to your command is often the first step to get more comfortable with the command.

So how do we "look around"?

- ls
- echo $PWD -- get our current location
  PWD = Print Working Directory
  echo = Repeat whatever I said
  echo "text" -- repeat text
- echo $PATH -- get other locations where the shell looks for programs
  If you've had any difficulties installing software, you may have heard of
  the path!

  In order for software to actually run, you need to add it to your PATH.
  python3 -- "command not found"???
  conda -- "command not found"???
  It's possible that you need to add something to your PATH.

  When we do something like `python3 --version` -- we're checking that you
  have the software installed, AND that it's been added to your path.

  It's a common source of confusion to have multiple installations of the same
  software on your machine -- this is common, for example, with Python
  You need to add all installations, or, only the most relevant/recent installation
  to your PATH to ensure that that's the one that gets run.

  Programs in $PATH are available both programmatically (to other programs),
  and to the user.

- echo $SHELL -- get the current shell we are using

  There are different shells and terminal implementations
  The default one on MacOS these days is zsh
  bash is another common/very well-used shell (for example, on Linux systems)

  I can run one shell from another shell. Try:
  - bash
  - zsh
  - Kind of like the Python3 command prompt

  Are there advantages to one shell over another?

  Usability: Some modern shells have fancy things like syntax highlighting,
  GUIs that you can click around in, etc.

  Portability: You'll want a shell that sort of behaves as a Unix-like shell
  Avoid: PowerShell (Windows syntax)

  (Mac and Linux systems are Unix-based. Windows is based on a totally different
  OS architecture.)

  A system will come with a built-in shell that you would start out with
  If you want a different one you could use that shell to install another shell.

The $ are called "environment variables" -- there are others!
These represent the current state of our shell environment.

When I write x = 3 in Python, x becomes a local variable assigned to the integer "3"
Similarly, $PATH and $PWD are local variables in the shell.
They're assigned to some values, and when written the shell will expand them out
to whatever values they're assigned to.

When we run `echo $PWD` what's actually happening:
- $PWD gets expanded out to its value (/Users/..../119/lecture2)
- This value gets printed back out to the shell output by `echo`

You can also define and set your own environment variables.

Are environment variables local? Will they persist after the shell session terminates?

No, they won't
But there is a way to make things persist and these are the shell config files ilke
- .bash_profile, .bashrc, .zshrc, ...
- These are files with random code in them that gets executed whenever you open a shell.
- This is why we don't have to keep adding Python, conda, etc. to the $PATH every
  time we open a new shell.
"""

# with a built-in Python library
def pwd_1():
    print(os.getcwd())

pwd_1()

# with subprocess (run an arbitrary command)
# This one is a bit harder
def pwd_2():
    # os.environ is the Python equivalent of the shell $ indicator.
    subprocess.run(["echo", os.environ["PWD"]])

pwd_2()

# In fact, we could just use this directly as well, and this offers a third way
def pwd_3():
    print(os.environ["PWD"])

pwd_3()

# Q: What happens when we run this from a different folder?

# It matters what folder you run a program or command from!

"""
Informational commands

Remember that "looking around" is trying to see or look at the various
information about the current state of our shell.
That state includes:
- what folder we are in
- what environment variables (local variables) are set (and to what values)

We can also look inside files and directories:

- cat
  Print out the entire file to the terminal
  Useful programmatically

- less
  Slightly more helpful if you are a human
  Type 'q' to quit

- open
  Open the file using a GUI application on your computer, if available

- ls inside an existing directory

  ls ..
  ls ../lecture2

"""

def cat_1():
    with open("lecture.py") as f:
        print(f.read())

def cat_2():
    subprocess.run(["cat", "lecture.py"])

def less():
    subprocess.run(["less", "lecture.py"])

cat_1()
cat_2()

less()

"""
This concludes the first part on "looking around"
Next time we'll finish this 3-part model

If you're trying to understand really any system, but in particular the shell,
the three things you're going to need to know is
- looking around: how to view the current state of the system
- help: how to get help with what commands are available
- actually doing something

e.g.: git status is telling you the current state of the system.

=== Getting help ===

Another thing that is fundamentally important -- and perhaps even more important
than the last thing -- is getting help!

One of the following 3 things usually works:
- `man cmd` or `cmd --help` or `cmd -h`

=== Recap ==

We saw looking around
Tutorial on the state of the shell (current working directory, environment variables, file contents)
Next time we will look at getting help + navigating/doing stuff
And we will also talk about Git, dangers of the shell, and other Q+A.

=============================================

=== Oct 11 ===

Shell, continued

Recall the three-part model: Looking around, getting help, doing something

Zork demo:

https://textadventures.co.uk/games/play/5zyoqrsugeopel3ffhz_vq

=== Getting help, continued ===

Let's run our "getting help" commands in Python:
"""

def get_help_for_command(cmd):
    subprocess.run([cmd, "--help"])
    subprocess.run([cmd, "-h"])
    subprocess.run(["man", cmd])

# get_help_for_command("python3")

"""
Other ways to get help?

Some shell experts will tell you that you that you shouldn't be "alt-tab"ing outside of the
shell, and should know how to do everything purely within it by getting help as above.
I don't agree with this advice.
Using Google/AI can be really useful for a number of reasons!

You can usually use:
- Google
- chatGPT
- (new!) AI tools in the shell: e.g. https://github.com/ibigio/shell-ai

to determine the right command to run for what you want to do.

Important caveat: you need to know what it is you want to do first!
"""

# Example:
# how to find all files matching a name unix?
# https://www.google.com/search?client=firefox-b-1-d&q=how+to+find+all+files+matching+a+name+unix
# https://stackoverflow.com/questions/3786606/find-all-files-matching-name-on-linux-system-and-search-with-them-for-text

# Important notes:
# Using Google+AI doesn't obliviate the need to understand things ourselves.
# - we still needed to know the platform we are on (Unix)
# - we still needed to know how to modify the command for your own purposes
# - (for the AI tool) you still need to figure out how to install it (:
#   + as some of you have noticed (especially on Windows), installing some software dev tools
#     can seem like even more work than using/understanding the program itself.

"""
=== Navigation ===

Once we know how to "look around", and how to "get help",
we can make a plan for what to do.

The same advice applies to all commands: knowing how to "modify" the current
state relevant to your command is often the second step to get a grip on how
the command works.

(And, once again, this is also exactly what we would do in a text-based adventure :))

So what should we do?
We need a way to move around and modify stuff:

- cd
- mkdir
- touch
"""

def cd(dir):
    os.chdir(dir)

def touch(file):
    with open(file, 'w') as fh:
        fh.write("\n")

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

def run_python3_file_interactive(file):
    # TODO
    raise NotImplementedError

"""
=== I/O ===

What about I/O?
Remember that one of the primary reasons for the shell's existence is to
"glue" different programs together. What does that mean?

Selected list of important operators
(also called shell combinators):
- |, ||, &&, >, >>, <, <<

(Skip most of these depending on time)

Exercises:

- cat followed by ls
- cat followed by cd
- ls, save the results to a file
- python3, save the results to a file
- (Hard:) ls followed by cd into the first directory of interest

"""

"""
=== Git ===

We can think of git under the same model as other shell commands!

Informational commands:
- git status
- git log
- git log --oneline
- git branch -v

What about help commands? Try:
- man git
- git status --help
- git log --help
- git add --help
- git commit --help

Finally, doing stuff:

For getting others' changes:
- git pull
- git fetch
- git checkout

For sharing/publishing your own changes
(a common sequence of three to run):
- git add
- git commit
- git push

Others (selected most useful):
- git rebase
- git rebase -i
- git merge
- git branch

Just like before, we can also run these commands in Python.
"""

def git_status():
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
=== What is the Shell? (revisited) ===

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

Things we didn't cover:

- Using the shell for cleaning, filtering, finding, and modifying files

  + cf.: grep, find, sed, awk

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

  Example to try for a URL: [a-zA-Z]+\\.[a-z]+( |\\.|\n)

"""
