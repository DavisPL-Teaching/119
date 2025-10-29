"""
Wednesday, October 22

Part 5: Git

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
