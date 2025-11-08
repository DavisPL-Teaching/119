"""
Part 6: Dangers of the Shell (and a few Loose Ends)

We covered this part briefly at the end of Wednesday, October 22.

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

- bash fork bomb :-)

    :(){ :|:& };:

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
