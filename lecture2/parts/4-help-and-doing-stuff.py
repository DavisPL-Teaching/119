"""
Monday, October 20

Part 4: Help, Doing Stuff, anatomy of shell commands

-----

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
"""
