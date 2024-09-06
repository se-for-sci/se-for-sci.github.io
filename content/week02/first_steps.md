# First steps with git

## Getting started with git

Setting up your git environment. On your Terminal window, type the following
commands.

```console
$ git config --global user.name 'Romain Teyssier'
$ git config --global user.email 'teyssier@princeton.edu'
```

Create a new directory.

```console
$ mkdir mywork
$ cd mywork
```

Create a new git project.

```console
$ git init
Initialized empty Git repository in /Users/rt3504/mywork/.git/
```

Now edit your first file.

```console
$ echo "This is my first file" > file1.txt
```

Add this file to the staging area and commit your first change.

```console
$ git add file1.txt
$ git commit -m "First commit"
[master (root-commit) c073d19] First commit
 1 file changed, 1 insertion(+)
 create mode 100644 file1.txt
```

What is the staging area? This is where you put your modifications in the queue,
one after the other, using the `git add` command. git tracks only differences
between successive versions. You can then commit these changes to the repository
with the `git commit` command.

## Checking the status of your repository

We can now check the status of our repository using the command

```console
$ git status
On branch master
nothing to commit, working tree clean
```

Let's now make our first change.

```console
$ echo "This is my first file but I modified it." > file1.txt
```

Let see now the status of our repository.

```console
$ git status
On branch master
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   file1.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

Let's add these changes to the staging area.

```console
$ git add file1.txt
$ git status
On branch master
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   file1.txt
```

Let's commit those changes.

```console
$ git commit -m "Commit changes"
[master 476b980] Commit changes
 1 file changed, 1 insertion(+), 1 deletion(-)
$ git status
On branch master
nothing to commit, working tree clean
```

When you commit changes, using `git commit -m` allows you to give a commit
message on the command line. Without the `-m` options, git will launch an editor
(default is usually `vim`). To set your own editor, use:

```console
$ export GIT_EDITOR='emacs -nw'
```

Try and see what happens if you commit another change without the `-m` option.
Just follow the instruction, add your message in your favorite text editor and
save the file.

## View the history of your project

To see the past history of your project, type:

```console
$ git log
commit 476b9801a6fb1efefdcd6c4d1bc82bff43686f9e (HEAD -> master)
Author: Romain Teyssier <romain.teyssier@gmail.com>
Date:   Thu Oct 6 09:48:30 2022 -0400

    Commit changes

commit c073d19d60ca399ab70e9a9b720cefeaa36c84a6
Author: Romain Teyssier <romain.teyssier@gmail.com>
Date:   Thu Oct 6 09:37:43 2022 -0400

    First commit
```

A nicer way of looking at the history of your repository:

```console
$ git log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short
* 476b980 2022-10-06 | Commit changes (HEAD -> master) [Romain Teyssier]
* c073d19 2022-10-06 | First commit [Romain Teyssier]
```

## Manipulating history

Now, we will create two new files `file2.txt` and `file3.txt`, each time staging
and committing the new file. Your history must now look like this:

```console
$ git log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short
* 41f8d80 2022-10-06 | Committing file3 (HEAD -> master) [Romain Teyssier]
* c6e6535 2022-10-06 | Committing file2 [Romain Teyssier]
* 476b980 2022-10-06 | Commit changes [Romain Teyssier]
* c073d19 2022-10-06 | First commit [Romain Teyssier]
```

Inside our repository, we have the following files:

```console
$ ls
file1.txt file2.txt file3.txt
```

Let's now move back in time and put the pointer of our time coordinate back to
when we only had `file1.txt`.

For this, we use the command `git checkout HASH` where `HASH` is the hash key (7
digits) corresponding to the previous commit are targeting. In our example, we
will type

```console
$ git checkout 476b980
Note: switching to '476b980'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

Turn off this advice by setting config variable advice.detachedHead to false

HEAD is now at 476b980 Commit changes
```

Inside our repository, we are back to the previous state with only one file:

```console
$ ls
file1.txt
```

If we check our past history, we only see the old version of it.

```console
$ git log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short
* 476b980 2022-10-06 | Commit changes (HEAD) [Romain Teyssier]
* c073d19 2022-10-06 | First commit [Romain Teyssier]
```

We can go back to the last version using

```console
$ git checkout master
Previous HEAD position was 476b980 Commit changes
Switched to branch 'master'
$ ls
file1.txt file2.txt file3.txt
```
