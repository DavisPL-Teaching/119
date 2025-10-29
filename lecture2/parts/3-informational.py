"""
Friday, October 17

Part 3: Informational Commands

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
"""
