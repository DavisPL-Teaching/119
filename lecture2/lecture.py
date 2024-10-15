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

# less()

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

=== Zork demo ===

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

# Example: q make a new git branch -> returns the right git syntax

to determine the right command to run for what you want to do.

Important caveat: you need to know what it is you want to do first!
"""

# Example:
# how to find all files matching a name unix?
# https://www.google.com/search?client=firefox-b-1-d&q=how+to+find+all+files+matching+a+name+unix
# https://stackoverflow.com/questions/3786606/find-all-files-matching-name-on-linux-system-and-search-with-them-for-text
# find ../lecture1 -type f -name lecture.py -exec grep -l "=== Poll ===" {} +

# Important notes:
# Using Google+AI doesn't obliviate the need to understand things ourselves.
# - we still needed to know how to modify the command for your own purposes
# - we still needed to know the platform we are on (Unix)
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
(In the context of a Python library such as Pandas:
 python3 -i to interactively "look around"
 the values of variables, the online documentation to see the
 different functions available, actually write code to do what
 you want.)

(And, once again, this is also exactly what we would do in a text-based adventure :))

So what should we do?
We need a way to move around and modify stuff:

- cd -- change directory
- mkdir -- make a new directory
- touch -- make a new file

Example:
- mkdir subfolder
- cd subfolder
- touch mod.py
- open mod.py
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

Example:
  git --version to get the version of git
  OR git -v are both equivalent

This is typical: usually we use a single dash + a single letter
as a shortcut for a double dash plus a long argument name.

We have seen some of these already.

How subprocess works:
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
=== I/O ===

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

Examples:
  python3 lecture.py || echo "Hello"
  python3 lecture.py && echo "Hello"

(Skip most of these depending on time)

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

Skipped for time:
- ls followed by cat
  (equivalent to just ls)
- cat followed by cd
  (using xargs)
- ls, save the results to a file
  (using >)
- python3, save the results to a file
  (using >)
- (Hard) cat followed by cd into the first directory of interest

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

- git push

=== Recap ===

We finished the "getting help" part and saw the "doing stuff" part
We saw command arguments and input/output
We saw the basics of git

We will finish the rest of the file next time.

=========================================

=== Oct 14 ===

Three things that came up last time:

i) Text editors in the shell

Running `git commit` without the `-m` option opens up a text
editor!

Vim: dreaded program for many new command line users

  Get stuck -- don't know how to quit vim!

  :q + enter

The most "accessible" of these is probably nano.

Sometimes files open by default in vim and you have to
know how to close the file.
"""

def edit_file(file):
    subprocess.run(["nano", file])

# Let's edit the lecture file and add something here.
print("Hello, world!")

"""
Text editors get opened when you run git commands
like git commit without a message.

ii) Here is a very important "informational" command I missed:

  git diff
  git diff --word-diff (word level diff)
  git diff --word-diff-regex=. (character level diff)

  git diff --staged -- after you do a git add, shows diff from green
  changes

iii) A general principle that we have seen several times:
After doing a "doing stuff" command,
we often want to go back to the informational commands
to see what changed.

Example:
- git status
- git add
- git status
- git commit
- git status
- git push
- git status

=== Finishing up git ===

Other git commands (selected most useful):
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

=== Skipped topics ===

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

"""
