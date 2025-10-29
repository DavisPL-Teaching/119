"""
Wednesday, Oct 15

Part 2: Commands and Platform Dependence

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
"""
