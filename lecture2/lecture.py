"""
Lecture 2: The Shell

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

=============================================

Wednesday, Oct 15

Continuing the shell.

Poll:
Which of the following are reasons you might want to use the shell? (Select all that apply)

<Options cut>

https://forms.gle/YrsjyyXe5Ve1aqEM7

-----

Last time we saw: ls, cd, python3

(btw: ls is short for "list")
(cd: . = current folder, .. = parent folder)

(autocomplete; up/down arrow)

Remaining commands:

- pytest <code>.py:
  Run pytest (Python unit testing framework) on a Python program

- conda install <module>:
  Conda = package manager for various data science libaries & frameworks
  This command installs a software package <module> using Conda

- pip3 install <module>:
  Somewhat deprecated nowadays in favor of better package managers
  Install python libraries / packages

  Better?
  + Use conda
  + Use your package manager through your operating system
    brew for macOS
    apt for Linux

  For modern Python projects:
  You should be using venv - makes a virtual package environment per-Python project

  If you ever see a file like .venv in a GitHub repository, that's what that is

What do all of these programs have in common?

Commonalities:
  They all involved working with system resources in some way.

Differences:

- ls: mostly was "informational" command - just figuring out what folder we're
  curently inside

- cd, conda, pip3, python3 - "doing stuff" commands - we're actually modifying the
  state of the system when running these.

Other answers (skip):

- Different programs may have been developed by different people, in different
  teams, in different languages, etc.

- We can't assume someone wrote a nice GUI for us to connect these programs
  or pieces together! (Sadly, often they didn't.)

Some examples of running these:
"""

# Try:
# python3, ls, pytest, conda

# ls: doesn't show hidden folders and files
# On Mac: anything starting with a . is hidden
# Hidden files are used for many important purposes,
# e.g., storing program data, caching information, writing
# configuration for tools like Git, etc.

"""
when submitting code to others:
best to remove hidden files & folders!

These can clutter up a project, resulting in a large
.zip file with lots of extra junk/files.

(Similarly, they can also clutter up a Git repository
- which is why we use .gitignore to tell Git to ignore
certain stuff.)
"""

# To show hidden + other metadata
# ls -alh
# ^^^^^^^ TL;DR use this to show all the stuff in a folder

"""
Observations:

- You can run shell commands in Python

- You can run Python programs from the shell
  (we've already seen how to do this)

Let's see an example
"""

# 1. Using the built-in os library

# os, sys - Python libraries for interacting with
# system resources

# os is how Python interacts with the operating system
import os

def ls_1():
    # Listdir: input a folder, show me all the files
    # and folders inside it
    # The . refers to the current directory
    # Also does not include hidden files/folders.
    print(os.listdir("."))

# ls_1()

# 2. Running general/arbitrary commands

# Library for running other commands
import subprocess

def ls_2():
    subprocess.run(["ls", "-alh"])
    # Equivalent: ls -alh in the shell!

# ls_2()
# ^^^^ same output as if I ran the command line directly

"""
Re: Q in chat
When working with the shell, you are often doing very
platform-specific stuff (platform = operating system, architecture, etc.).

Example differences across platforms:
- syntax for arguments in Mac/Linux vs Windows Powershell
- capitalization of folders
  example: on Mac I run ls Subfolder - not case-sensitive -
  to get the files inside "subfolder"

  Won't work on another platform!

  "Works on my machine"
  But doesn't work on someone else's.

Summary points:

Sometimes in Python we just directly call into
commands, and knowing shell syntax is useful as it
gives a very powerful way for Python programs to interact
with the outside world.

Everything that can be done in the shell can be done in a Python script
(Why?)

Everything that can be done in Python can be done in the shell
(Why?)

So knowing shell stuff might help you with running
systems-level stuff in Python, and vice versa.

===== A model for interacting with the shell: 3 types of command =====

We saw how to run basic commands in the shell and what it means.

Three types of commands:

1. Information
2. Getting help
3. Doing something

=== Informational commands: looking around ===

An analogy:
There used to be a whole genre of text-based adventure games.
the shell is kind of like this.

e.g.
- Zork (1977):
  https://textadventures.co.uk/games/play/5zyoqrsugeopel3ffhz_vq
- Peasant's Quest (2004):
  https://homestarrunner.com/disk4of12

Back in the day you would then open up the game (and be provided no information to help. :-) )
What would you do first?

If you like, play around with Zork offline, it can be a fun game/distraction
(bit of a blast from the past)

https://textadventures.co.uk/games/play/5zyoqrsugeopel3ffhz_vq

If you know how to play Zork then you know how to work with the shell.

Recap:

- We saw some stuff about hidden files/folders (starting with .)

- We talked about running shell commands from Python using subprocess, and Python system libraries

- We talked about platform differences and how these can be an issue when working
  with the shell

- We introduced a 3-category analogy for shell commands: Info commands, Help commands, and "Do something" commands.

********** Where we ended for today **********

=======================================================

Friday, October 17

Discussion Question & Poll:

1. Which of the following are a good use cases for things to list in .gitignore? (Select all that apply)
<options cut>

2. Platform-specific things to be aware of could include... (Select all that apply)
<options cut>

https://forms.gle/HmmT8BjXtiBvferRA

Some notes:

Q1:
- Not all hidden files are unimportant!
  Some, like .gitignore may be important, or may be useful to track
  with the repository.

  Other hidden files, like .DS_Store are not important and can be ignored.

Q2:
- Python is cross-platform (at least for things like a Hello World! program)
  and will work on any operating system

- definition: what is a Platform anyway?

  Platform = The operating system + the architecture + any libraries or other environment packages that are installed

Review poll answers: exams/poll_answers.md

Continuing the shell:

Last time:

I introduced a model for interacting with the shell which I called the
3-part model:
- Informational commands
- Help commands
- Doing stuff commands

Analogy:
I mentioned this is kind of like playing a text-based adventure game
like "Zork" (1970s), many other old games

=== Informational commands ===

Just as in a text-based adventure,
the most important thing you need to know when opening a shell is
how to "look" around. What do you see?

Key features of such commands:
- Don't modify your system state at all
- Might tell you some information about your system and things around you,
  and what you might want to do next.

The same approach to progressing the game in Zork applies to the shell!
Including external tools people have built, and even commands outside of the shell, like
functions in Python:
knowing how to "see" the current
state relevant to your command is often the first step to get more comfortable with the command.

So how do we "look around"?

- ls
  we have already seen - list files/directories in the current location

  "current working directory"

- echo $PWD -- get our current location
  PWD = Print Working Directory
  echo = Repeat whatever I said
  echo "text" -- repeat text

  $VAR - means a variable with name VAR

  These are called "environment variables"

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

  Point:
  There are different shells and terminal implementations.
  The default one on MacOS these days is zsh
  bash is another common/very well-used shell (for example, on Linux systems)

  If you're on Windows I recommend using WSL so that you have access to a
  similar shell (usually bash)

  I can run one shell from another shell. Try:
  - bash
  - zsh
  - Kind of like the Python3 command prompt

  Are there advantages to one shell over another?

  Yes, there are also some advanced/modern shells that you can install

  - maybe with some interesting graphical interface
  - maybe with some interesting color coding
  - maybe with some AI support

  Most shells try to support a similar syntax so that people don't get
  confused going from one shell to another.

  ---- other possible answers (skipped) ----

  Usability: Some modern shells have fancy things like syntax highlighting,
  GUIs that you can click around in, etc.

  Portability: You'll want a shell that sort of behaves as a Unix-like shell
  Avoid: PowerShell (Windows syntax)

  (Mac and Linux systems are Unix-based. Windows is based on a totally different
  OS architecture.)

  A system will come with a built-in shell that you would start out with
  If you want a different one you could use that shell to install another shell.

=== Environment variables ===

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

A:
No, they won't
But there is a way to make things persist and these are the shell config files like
- .bash_profile, .bashrc, .zshrc, ...
- These are files with random code in them that gets executed whenever you open a shell.
  + For zsh, every time I open a shell, .zshrc is executed
- This is why we don't have to keep adding Python, conda, etc. to the $PATH every
  time we open a new shell.

This system - of environment variables and $PATH and .zshrc, etc. is
the precarious fabric on which all software installation is working under the
hood.

In case you need to access similar functionality from a Python script:
"""

# with a built-in Python library
def pwd_1():
    print(os.getcwd())

# pwd_1()

# with subprocess (run an arbitrary command)
# This one is a bit harder
def pwd_2():
    # os.environ is the Python equivalent of the shell $ indicator.
    subprocess.run(["echo", os.environ["PWD"]])

# pwd_2()

# In fact, we could just use this directly as well, and this offers a third way
def pwd_3():
    print(os.environ["PWD"])

# pwd_3()

# Q: What happens when we run this from a different folder?

# It matters what folder you run a program or command from!

"""
Recap:

- We talked about informational commands - ways to get the state of the system

  + Current working directory
  + Files/folders in the system (or in the current woroking directory)
  + The shell that's running

- We talked about environment variables

  $PWD, $PATH

  These are important pieces of system information

- We talked a little bit about .zshrc, .bash_profile, etc. which are
  shell configuration files

  + Lists of shell commands that run when you open a shell.

    BTW, virtual machines and things like Docker also have similar such config files

    Dockerfile -- list of shell commands that gets run.

Next time we will talk about:
- help commands, doing stuff commands

==============================================

Monday, October 20

Continuing with the shell!

Showing two more commands before the discussion question:

- cat <path>:
  Prints out the contents of a file at <path>

- less <path>:
  Show "less" of the contents of the file at <path>
  u to go up, d to go down, q to quit

- open <path>:
  Open the file in your default program for that file.

(Three ways to view/open a file)

Discussion Question & Poll:
Which of the following are "informational" commands?
<Options cut>

https://forms.gle/XkbkUL2QxsLz6dLq7

=====

Informational commands (finishing up)

Information about the current state of our shell includes:
- what folder we are in
- what environment variables (local variables) are set (and to what values)
- other system information and system data
- file contents etc.

A few other commands:

- ls <directory>:

  ls ..
  ls ../lecture2

Examples in Python:
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
This concludes the first part on "looking around"

=== Getting help ===

Recall the three-part model: Looking around, getting help, doing something

Another thing that is fundamentally important -- and perhaps even more important
than the last thing -- is getting help if you *don't* know what to do.

One of the following 3 things usually works:
- `man cmd` or `cmd --help` or `cmd -h`

Examples:
- ls: has a man entry, but no --help or -h
- python3: has all three options

Some ways to get help (examples running these from Python):
"""

def get_help_for_command(cmd):
    subprocess.run([cmd, "--help"])
    subprocess.run([cmd, "-h"])
    subprocess.run(["man", cmd])

# get_help_for_command("python3")

"""
Other ways to get help:

Using Google/StackOverflow/AI can also be really useful for a number of reasons!

- A more recent development:
  AI tools in the shell: e.g. https://github.com/ibigio/shell-ai
  (use at your own risk)

  Example: q make a new git branch -> returns the right git syntax

to determine the right command to run for what you want to do.

Important caveat: you need to know what it is you want to do first!
"""

# Example:
# how to find all files matching a name unix?
# https://www.google.com/search?client=firefox-b-1-d&q=how+to+find+all+files+matching+a+name+unix
# https://stackoverflow.com/questions/3786606/find-all-files-matching-name-on-linux-system-and-search-with-them-for-text
# find ../lecture1 -type f -name lecture.py -exec grep -l "=== Poll ===" {} +

"""
Some observations:
Using AI doesn't obliviate the need to understand things ourselves.
- we still needed to know how to modify the command for your own purposes
- we still needed to know the platform we are on (Unix)
- (for the AI tool) you still need to figure out how to install it (:
  + as some of you have noticed (especially on Windows), installing some software dev tools
    can seem like even more work than using/understanding the program itself.

=== Doing stuff ===

Once we know how to "look around", and how to "get help",
we can make a plan for what to do.

The same advice applies to all commands: knowing how to "modify" the current
state relevant to your command is often the second step to get a grip on how
the command works.
(In the context of a Python library such as Pandas:
 python3 -i to interactively "look around"
 the values of variables, the online documentation to see the
 different functions available, actually write code to do what
 you want.)

(And, once again, this is also exactly what we would do in a text-based adventure :))

So what should we do?
We need a way to move around and modify stuff:

- cd -- change directory
  This modifies the state of the system by changing the current
  working directory

- mkdir -- make a new (empty) directory in the current locaiton
  (current working directory)

- cp -- copy a file from one place to another

(demo: copy folder.txt to ../folder.txt)

(I follow this pattern a lot -- information first, then do something, then information again)

- touch <file or path> -- make a new file

  Create a new empty file at <file or path>

(Another example - creating a new Python module)
- mkdir subfolder
- cd subfolder
- touch mod.py
- open mod.py

- mv <file1> <file2>:
  Move a file from one path to another, or rename it
  from one file name to another.

Examples of how to accomplish similar purposes in Python:
"""

def cd(dir):
    # Sometimes necessary to change the directory from which your
    # script was called
    os.chdir(dir)

def touch(file):
    with open(file, 'w') as fh:
        fh.write("\n")

# touch("mod-2.py")

"""
=== Anatomy of a shell command ===

Commands are given arguments, like this:

cmd -<argument name> <argument value>
cmd --<argument name> <argument value>

Some arguments don't have values:

cmd -<argument flag>

You can chain together any number of arguments:

cmd -<arg1> <val1> -<arg2> <val2> ...

Example:
  git --version to get the version of git
  git -v : equivalent to the above

(Informational commands for git)

This is typical: usually we use a single dash + a single letter
as a shortcut for a double dash plus a long argument name.

We have seen some of these already.

Commands also have "positional" arguments, which don't use - or -- flags

  - cd <val>

  - cp <val1> <val2>

(More examples in Python:)
"""

def run_git_version():
    # Both of these are equivalent
    subprocess.run(["git", "--version"])
    subprocess.run(["git", "-v"])

# run_git_version()

def run_python3_file_interactive(file):
    subprocess.run(["python3", "-i", file])

# run_python3_file_interactive("subfolder/mod.py")

"""
=== I/O & Composing Shell Commands ===

What about I/O?
Remember that one of the primary reasons for the shell's existence is to
"glue" different programs together. What does that mean?

Selected list of important operators
(also called shell combinators):
- |, ||, &&, >, >>, <, <<

Most useful:
- Operator >
  Ends the output into a file.
  (This is called redirection)

- Operator >>
  Instead of replacing the file, append new content to the end of it

- || and &&
  Behave like "or" and "and" in regular programs
  Useful for error handling

  cmd1 || cmd2 -- do cmd1, if it fails, do command 2
  cmd1 && cmd2 -- do cmd1, if it succeeds, do command 2

  These are "shortcircuiting" boolean operations,
  just as in most programming languages, but based
  on whether the command succeeds or fails.

Examples:
  python3 lecture.py || echo "Hello"
  python3 lecture.py && echo "Hello"

===== Skip the following for time =====

- |
  Chains together two commands

Exercises:

- cat followed by ls

  Fixed example from class: cat folder.txt | xargs ls

  Better example (more common):
  Using "grep" to search for a particular pattern

  Example, find all polls in lecture 1:

    cat ../lecture1/lecture.py | grep "forms.gle"

  Find all packages installed with conda that contain the word "data":

    conda list | grep "data"

  Output:

    astropy-iers-data         0.2024.6.3.0.31.14 py312hca03da5_0
    datashader                0.16.2          py312hca03da5_0
    importlib-metadata        7.0.1           py312hca03da5_0
    python-tzdata             2023.3             pyhd3eb1b0_0
    stack_data                0.2.0              pyhd3eb1b0_0
    tzdata                    2024a                h04d1e81_0
    unicodedata2              15.1.0          py312h80987f9_0

- ls followed by cat
  (equivalent to just ls)
- cat followed by cd
  (using xargs)
- ls, save the results to a file
  (using >)
- python3, save the results to a file
  (using >)
- (Hard) cat followed by cd into the first directory of interest

Recap:

Help commands: see a command usage & options

Doing stuff commands:
  various ways of creating files, moving files,
  copying files, etc.

Anatomy of commands:
  cmd <val1> <val2> ... or
  cmd -<option1> <val1> -<option2> <val2> etc.

We saw various ways of combining and composing
different commands, which can be used for
advanced shell programming to write arbitrary
scripts in the shell.

****** Where we ended for today ******

==========================================================

Wednesday, October 22

Poll quesiton:

1. Give an example of a command that uses a positional argument

2. Give an example of a command that uses a named argument

3. Why do you think that commands have both positional and named arguments?

A) There is no reason for this, it's a historical accident
B) Positional arguments are more often optional, named arguments are more often required
C) Named arguments are more often optional, positional arguments are more often required
D) Named arguments can be combined with positional arguments to specify options or modify command behavior
E) Named arguments emphasize the intended purpose of the argument for readability purposes
F) Named arguments allow easily specifying Boolean flags (like turning debug mode on or off)

https://forms.gle/UNCmxWcRE53MkLNv7

Comments:

Analogy:
positional argument
    cd dir
    def cd(dir)

named argument
    python --version
    def python(version=True)

Correct answers: C, D, E, F

Named arguments are more often optional

Named arguments are often used as configuration flags

  python3 -i <--- modifies the "way" that we run Python

Another difference that wasn't mentioned:

Typically the order does not matter in named arguments!

  ls -alh
  ls -lah
  ls -a -l -h

If the user might not want to remember which order to call
the args in, another good use case for named.

===== Git =====

Git follows the same model as other shell commands!

Informational commands:
- git status

Info returned by git status?
  + "On branch" main
  + Whether my branch is up to date
  + Info about modified files
  + Do I have any changes to commit

- git log

  (down arrow, up arrow, q to quit)

  Shows a list of commits that have been made to the repository.

Mental model of git: it's a tree

  root:
  (Instructor initialized the repository)

Every time a change is made to the code, it grows the tip of the tree
After instructor posts lecture 1 and 2,

  root
  |
  lecture1
  |
  lecture2

If the TA simultaneously makes changes to lecture1
Two diverging branches:

  root
  |
  lecture1
  |                               \
  lecture2 (instructor's changes)    lecture1 (TA's changes)

When you check out the code, you're at a particular point in
the tree.

Git is sort of the opposite of keeping everything up to date :-)

  Modern webapp philosophy: everything should sync automatically!

  Git philosophy: nothing should sync automatically!

  That means that everyone opts in to what changes they do/do not
  want for the code.

  Side note: interesting questions about philosophy of collaboration
  and why we may or may not want to share our work/progress with others.

  Imagine two people working on the same branch at once,
  why would that be a problem?
  One person's work could break another person's work :-(

    + This gets more common the more people are working on a shared
      project.

    + Unit tests fail, code fails to compile, etc.

    + In this scenario, Git saves you: it says, you get to "check
      out" your copy of the code and be assured that your copy is
      yours to play around with.

Corollaries:

  - Everyone can be at a different point of the tree

  - Different people can work on different branches

  - If two people try to "push" the code - publishing it
    for others, we need to have some way of determining whose
    code wins the race, or how to combine the different changes
    to the code.

    ===> "merge conflict problem"

  - Each individual working on a branch may not need to see
    the entire tree at once to do their work.

    ======> You need the list of changes up until your point in
            the tree

    ======> You only need a "local view" or local window into
            the tree, which contains a copy of some of the changes.

When you git clone, or "git stash, git pull" the lecture notes,
you are creating an instance of this philosophy - essentially,
you're working on your own little branch of the tree.

In that context:

  First two lines of git status: where I am in the tree

  Changes: changes I've made on my local copy of the tree.

- git log --oneline

  List of changes, one per line

- git branch -v

  More information about the branch you're on

- git diff

  Most useful second to git status -- what changes you've made
  to the code on your local copy.

What about help commands? Try:
- man git
- git status --help
- git log --help
- git add --help
- git commit --help

  BTW: log, add, commit -- "subcommands"
      You can think of them like a special type of positional argument

Finally, doing stuff:

For getting others' changes:
- git pull

  Pull the latest code from the "published" version of the branch

- git push

  Attempt to push your code to the "published" version of the branch

If one branch is behind the other, great! we can just grow that
branch to make it equal to the other one

We're gonna have a problem if they are on diverging or two separate
branches, git does a "merge"
and try to shove the two things together.

  Sometimes it works, sometimes it doesn't and you have to debug.

  Two things could fail:

  1. Git could not know how to merge the changes
     (usually happens if both people modified)
      Results in: "Merge conflict"

  2. Merge succeeds, but the code breaks

     Two conflicting features, one feature breaks someone else's
     unit test, etc.

(Related commands -- not as worried about:)
- git fetch
- git checkout

For sharing/publishing your own changes
(a common sequence of three to run):
- git add .

  After a git add, I usually do a:
  git status
  git diff --staged

  AND:
  Run the code again just to make sure everything looks good

- git commit -m "Commit message"

  Modify what you just did:
  git commit --amend

  Then I would do a git status again

**Most important:**
To publish your code to the main branch

  Magic sequence of 3 commands:
  git add, git commit, git push.

This is a multi-step process because git wants you to
be deliberate about all changes.

  git add = what changes you want

  git commit = why?

  git push = publish it.

git add, git commit = your local branch only

git push = shares it publicly.

=========================================

===== Other miscellaneous things =====

i) Text editors in the shell

Running `git commit` without the `-m` option opens up a text
editor!

Vim: dreaded program for many new command line users

  Get stuck -- don't know how to quit vim!

  :q + enter

The most "accessible" of these is probably nano.

Sometimes files open by default in vim and you have to
know how to close the file.

Use nano (most accessible), don't use vim and emacs.
"""

def edit_file(file):
    subprocess.run(["nano", file])

# Let's edit the lecture file and add something here.
# print("Hello, world!")

"""
Text editors get opened when you run git commands
like git commit without a message.

ii) Variations of git diff

  git diff
  git diff --word-diff (word level diff)
  git diff --word-diff-regex=. (character level diff)

  git diff --staged -- after you do a git add, shows diff from green
  changes

iii) Other git commands (selected most useful):

- git merge -- merge together different conflicting versions of the code
- git rebase
- git rebase -i -- often useful for modifying commit messages
- git branch -- create a new branch, often useful for developing new features.

Just like before, we can also run these commands in Python.
"""

def git_status():
    # TODO
    raise NotImplementedError

"""
Finishing up the shell:

=== Dangers of the shell ===

The shell has something called "ambient authority"
which is a term from computer security basically meaning that
you can do anything that you want to, if you just ask.

Be aware!

- rm -f part1.py -- permanently delete your code (and changes),
  no way to recover
  rm -- remove
    -f: force removal (don't ask first)
    -r: remove all subfiles and subdirectories

- rm -rf "/"

  removes all files on the system.

  Many modern systems will actually complain if you try to do this.
"""

def rm_rf_slash():
    raise RuntimeError("This command is very dangerous! If you are really sure you want to run it, you can comment out this exception first.")

    # Remove the root directory on the system
    subprocess.run(["rm", "-rf", "/"])

# rm_rf_slash()

"""
sudo: run a command in true "admin" mode

  sudo rm -rf /
  ^^^^^^^^^^^^^ Delete the whole system, in administrator mode
"""

"""
Aside: This is part of what makes the shell so useful, but it is also
what makes the shell so dangerous!

All shell commands are assumed to be executed by a "trusted" user.
It's like the admin console for the computer.

Example:
person who gave an LLM agent access to their shell:
https://twitter.com/bshlgrs/status/1840577720465645960

"At this point I was amused enough to just let it continue. Unfortunately, the computer no longer boots."
"""

# sudo rm -rf "/very/important/operating-system/file"

"""
=============== Closing material (discusses advanced topics and recap; feel free to review on your own time!) ===============

=== What is the Shell? (revisited) ===

The shell IS:

- the de facto standard for interacting with real systems,
  including servers, supercomputers, and even your own operating system.

- a way to "glue together" different programs, by chaining them together

The shell is NOT (necessarily):

- a good way to write complex programs or scripts (use Python instead!)

- free from errors (it is often easy to make mistakes in the shell)

- free from security risks (rm -rf /)

=== Q+A ===

Q: How is this useful for data processing?

A: Many possible answers! In decreasing order of importance:

- Interacting with software dev tools (like git, Docker, and package managers)
  -- many tools are built to be accessed through the shell.

- Give us a better understanding of how programs run "under the hood"
  and how the filesystem and operating system work
  (this is where almost all input/output happens!)

- Gives you another option to write more powerful functions in Python
  by directly calling into the shell (subprocess)
  (e.g. fetching data with git; connecting to a
  database implementation or a network API)

- Writing quick-and-dirty data processing scripts direclty in the shell
  (Common but we will not be doing this in this class).

  Example: Input as a CSV, filter out lines that are not relevant, and
  add up the results to sort by most common keywords or labels.

Q: How is the shell similar/different from Python?

A: Both of these are useful "glue" languages -- ways to
   connect together different programs.

   Python is more high-level, and the shell is more like what happens
   under the hood.

   Knowing the shell can improve your Python scripts and vice versa.

=== Some skipped topics ===

Things we didn't cover:

- Using the shell for cleaning, filtering, finding, and modifying files

  + cf.: grep, find, sed, awk

- Regular expressions for pattern matching in text

=== Miscellaneous further resources ===

Future of the shell paper:

- https://dl.acm.org/doi/pdf/10.1145/3458336.3465296

Regular expressions
(for if you are using grep or find):

- Regex debugger: https://regex101.com/

- Regex explainer: https://regexr.com/

  Example to try for a URL: [a-zA-Z]+\\.[a-z]+( |\\.|\n)

End.
"""
