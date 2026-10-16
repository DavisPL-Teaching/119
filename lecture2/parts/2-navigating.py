"""
Wednesday, Oct 14

Part 2: Filesystems and Platform Dependence

Continuing the shell, now talking about one of the main things the shell interacts with:
the filesystem (files/directories) and your other operating system resources.

Poll:
Which of the following are reasons you might want to use the shell? (Select all that apply)

<Options cut>

https://forms.gle/UhQckCFjSP7rQpjF6

-----

Last time we saw: ls, cd, python3

(btw: ls is short for "list")
(cd: . = current folder, .. = parent folder)

    ~ = special character for home folder

Also very useful:

  autocomplete

  command history: up/down arrow

=== A few additional commands ===

Additional commands:

- pytest <code>.py:
  Run pytest (Python unit testing framework) on a Python program

  "Gotcha" when using pytest:

    accidentally naming a non-unit test with test_ will cause it to get run

    accidentally naming a unit test with some other non-test_ name will cause
    it to fail to get run
"""

def test_example():
    assert 1 + 1 == 2

"""
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
    apt for Linux (or WSL)

  For modern Python projects:
  You should be using venv - makes a virtual package environment per-Python project

  If you ever see a file like .venv in a GitHub repository, that's what that is

  (Other modern package managers for Python exist.)

  Don't use pip3
"""

"""
=== Hidden files and folders ===

When running ls -alh: additional rows are present not in ls

  These are hidden files and folders!

  There are 3 rows here - what they have in common:
    They all begin with a .

When submitting code to others:
best to remove hidden files & folders!

These can clutter up a project, resulting in a large
.zip file with lots of extra junk/files.

(Similarly, they can also clutter up a Git repository
- which is why we use .gitignore to tell Git to ignore
certain stuff.)
"""

# To show hidden + other metadata
# ls -alh
# ^^^^^^^ TL;DR use this to show all the stuff in a folder,
#               including hidden files and folders.

"""
=== Platform dependence ===

When working with the shell, you are often doing very
platform-specific stuff.

What is a platform? A platform is 3 things:
  1. operating system (e.g. MacOS, Linux)
  2. architecture of your system (hardware)
  3. installed software/dependencies (e.g. Python)

Example differences across platforms:
- syntax for arguments in Mac/Linux vs Windows Powershell
- capitalization of folders
  example: on Mac I run ls Subfolder - not case-sensitive -
  to get the files inside "subfolder"

  Won't work on another platform!

  "Works on my machine" effect

  ---> the code works when you run it
  ---> But doesn't work when someone else runs it.

As you can imagine, this is a big problem when building and running
pipelines over a large scale that you want to be usable/shareable across
many devices (e.g., different members of a team, different clients/customers,
etc.)

The shell is different between platforms -- raising some of these issues
  -- but it is also what we can use to fix/automatically fix many of these
     issues when sharing software across machines

     Example:

     we write a list of shell commands (via a Python script) that will install
     all required dependencies, and check if the operating system/architecture
     are compatible with a particular data pipeline before running it.

     You'll do a similar exercise on HW1 Part 3.

---------

Quick recap:

- We toured some additional commands available to us in the shell
  (particularly with regard to installing/investigating missing software,
   conda and pip3, as well as ls -alh option for hidden files/folders)

- We talked about hidden files/folders and why they exist, and why you
  should remove them if sharing your code with others

- We talked about platform-dependence

    Platform-dependent means: dependent on either the (1) OS, (2) architecture,
    or (3) specific set of installed libraries/dependencies on a system

- We stated that the shell can be used to diagnose and fix issues surrounding
  installed software and platform dependence.

---------
"""

"""
=== Shell commands vs. Python ===

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

Q: Why know both Python and the shell?

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
"""

"""
=== Recap of Part 2 ===

.
.
.
.
.

- We saw a few more commands

- We talked about hidden files/folders (starting with .)

- We talked about platform differences and how these can be an issue when working
  with the shell

- We talked about running shell commands from Python using subprocess, and Python system libraries.

Next part:

- We will introduce a 3-part model for shell commands: Info commands, Help commands, and "Do something" commands.

"""
