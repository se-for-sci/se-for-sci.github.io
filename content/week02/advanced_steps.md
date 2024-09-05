# More advanced steps with git

## Creating tags

Switching between commits can be made easier using the `git tag` command. Let's
tag the current state (the last version of our repository) using

```console
$ git tag v2
```

Now let's go back to the first version of our repository using

```console
$ git checkout 476b980
```

We now tag this first version using

```console
$ git tag v1
```

It is now really easy to go back to the second version using

```console
$ git checkout v2
```

without using the weird hash key.

We can look at the history of our repository and see:

```console
$ git log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short
* 41f8d80 2022-10-06 | Committing file3 (HEAD -> master, tag: v2) [Romain Teyssier]
* c6e6535 2022-10-06 | Committing file2 [Romain Teyssier]
* 476b980 2022-10-06 | Commit changes (tag: v1) [Romain Teyssier]
* c073d19 2022-10-06 | First commit [Romain Teyssier]
```

You see now the tags `v1` and `v2` in the list of commits. You can also see the
list of all the tags in your repository using the `git tag` command as

```console
$ git tag
v1
v2
```

## Creating branches

Let us say we are not happy with our current version of the code. We would like
to go back to `v1` and start fresh.

We use

```console
$ git checkout v1
$ git log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short
* 476b980 2022-10-06 | Commit changes (HEAD, tag: v1) [Romain Teyssier]
* c073d19 2022-10-06 | First commit [Romain Teyssier]
$ ls
file1.txt
```

Now let's create a new empty file with a new file name

```console
$ touch file4.txt
$ git add file4.txt
$ git commit -m "A better code now?"
$ ls
file1.txt file4.txt
$ git log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short
* 1e19277 2022-10-07 | A better code now? (HEAD) [Romain Teyssier]
* 476b980 2022-10-06 | Commit changes (tag: v1) [Romain Teyssier]
* c073d19 2022-10-06 | First commit [Romain Teyssier]
```

And another one

```console
$ touch file5.txt
$ git add file5.txt
$ git commit -m "Yes it is a better code"
$ ls
file1.txt file4.txt file5.txt
```

Let's go back again to our second version `v2`

```console
$ git checkout v2
Warning: you are leaving 2 commits behind, not connected to
any of your branches:

  6ed6b75 Yes it is a better code
  1e19277 A better code now?

If you want to keep them by creating a new branch, this may be a good time
to do so with:

 git branch <new-branch-name> 6ed6b75

HEAD is now at 41f8d80 Committing file3
```

You see that git is not happy because you didn't create a branch for all these
new commits. Indeed, you have created a new thread of commits that are in
competition with what you did before. You have now 2 diverging code versions.
Let's follow git's advice and create a new branch for these 2 new commits

```console
$ git branch better_code 6ed6b75
```

We can see how many branches we have using the `git branch` command

```console
$ git branch
* (HEAD detached at v2)
  better_code
  master
```

We can now see in the history of our repository all the branches using the
`--all` option as

```console
$ git log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short --all
* 6ed6b75 2022-10-07 | Yes it is a better code (better_code) [Romain Teyssier]
* 1e19277 2022-10-07 | A better code now? [Romain Teyssier]
| * 41f8d80 2022-10-06 | Committing file3 (HEAD, tag: v2, master) [Romain Teyssier]
| * c6e6535 2022-10-06 | Committing file2 [Romain Teyssier]
|/
* 476b980 2022-10-06 | Commit changes (tag: v1) [Romain Teyssier]
* c073d19 2022-10-06 | First commit [Romain Teyssier]
```

If you don't use `--all` you only see the history of the branch you sit on,
namely here the master branch

```console
$ git log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short
* 41f8d80 2022-10-06 | Committing file3 (HEAD, tag: v2, master) [Romain Teyssier]
* c6e6535 2022-10-06 | Committing file2 [Romain Teyssier]
* 476b980 2022-10-06 | Commit changes (tag: v1) [Romain Teyssier]
* c073d19 2022-10-06 | First commit [Romain Teyssier]
```

If you examine the content of your repository, you see only the files in the
`master` branch.

```console
$ ls
file1.txt file2.txt file3.txt
```

Let's go back to the other branch

```console
$ git checkout better_code
Previous HEAD position was 41f8d80 Committing file3
Switched to branch 'better_code'
```

We can check we are on the right branch using

```console
$ git branch
* better_code
  master
```

We only see the files of the second branch (our better version of the code).

```console
$ ls
file1.txt file4.txt file5.txt
```

Without the `--all` option, we also only see the history of this branch.

```console
$ git log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short
* 6ed6b75 2022-10-07 | Yes it is a better code (HEAD -> better_code) [Romain Teyssier]
* 1e19277 2022-10-07 | A better code now? [Romain Teyssier]
* 476b980 2022-10-06 | Commit changes (tag: v1) [Romain Teyssier]
* c073d19 2022-10-06 | First commit [Romain Teyssier]
```

## Merging branches

Now that we have a better code, we want to import in this better branch what was
done in the `master` branch. In other words, we want to merge to work done in
these 2 diverging versions of the code. We can do this using the `git merge`
command.

First, let's check we are in the correct branch using

```console
$ git branch
* better_code
  master
```

Second, let's merge the `master` branch into the `better_code` branch.

```console
$ git merge master -m "Merging previous work in better version of the code"
Merge made by the 'recursive' strategy.
 file2.txt | 0
 file3.txt | 0
 2 files changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 file2.txt
 create mode 100644 file3.txt
```

We can now have a look at the history using the `--all` option.

```console
$ git log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short --all
*   8b3b89f 2022-10-07 | Merge branch 'master' into better_code Merging previous work in better version of the code (HEAD -> better_code) [Romain Teyssier]
|\
| * 41f8d80 2022-10-06 | Committing file3 (tag: v2, master) [Romain Teyssier]
| * c6e6535 2022-10-06 | Committing file2 [Romain Teyssier]
* | 6ed6b75 2022-10-07 | Yes it is a better code [Romain Teyssier]
* | 1e19277 2022-10-07 | A better code now? [Romain Teyssier]
|/
* 476b980 2022-10-06 | Commit changes (tag: v1) [Romain Teyssier]
* c073d19 2022-10-06 | First commit [Romain Teyssier]
```

You can see how the branches are now converging back together. Let's see what we
have in our repository now.

```console
$ ls
file1.txt file2.txt file3.txt file4.txt file5.txt
```

Wow! We have everything now.

Let's now try something more difficult. We go back to the master branch and
modify directly the text inside `file1.txt`.

```console
$ git checkout master
```

Edit file1.txt in order to obtain

```console
$ cat file1.txt
This is my first file but I modified it again to match the better code version.
```

You can check that the file has been modified using

```console
$ git status
```

You can also see the modifications using

```console
$ git diff
```

Let's commit these changes as usual.

```console
$ git add file1.txt
$ git commit -m "Modify file1.txt"
```

Let's go back to the `better_code` branch again and merge these changes from the
`master` branch.

```console
$ git merge master -m "Trying to merge again"
Merge made by the 'recursive' strategy.
 file1.txt | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

Wow! It worked flawlessly.

## Resolving conflicts

Let's try something more complex. Go in the `better_code` branch and edit
file1.txt so that it looks like

```console
$ cat file1.txt
I went crazy!
```

Obviously you decided to make drastic changes here. Commit these changes to the
repository (using `git add` and `git commit` in sequence). Now go back to the
`master` branch. Edit `file1.txt` to make more sensible changes.

```console
$ cat file1.txt
This is my first file but I modified it one more time to match the better code version.
```

Now go back again to the `better_code` branch and try and merge the `master`
branch.

```console
$ git merge master
Auto-merging file1.txt
CONFLICT (content): Merge conflict in file1.txt
Automatic merge failed; fix conflicts and then commit the result.
```

Crap! We have a conflict between the two different commits. `file1.txt` now
looks like this:

```console
$ cat file1.txt
<<<<<<< HEAD
I went crazy!

=======
This is my first file but I modified it one more time to match the better code version.
>>>>>>> master
```

You must now edit yourself this file and decide which version to use. Obviously,
you want to use the correct version that looks like

```console
$ cat file1.txt
This is my first file but I modified it one more time to match the better code version.
```

Now that the file has been properly edited, you can commit the fixed changes
using as usual

```console
$ git add file1.txt
$ git commit -m "Fixed conflict"
[better_code 1243e96] Fixed conflict
```

Pfew! That was stressful but it all went back to normal.

Now that you happy with your better version of the code, you can merge back
everything to the `master` branch.

```console
$ git checkout master
Switched to branch 'master'
$ git merge better_code
Updating abc9ee2..1243e96
Fast-forward
 file4.txt | 0
 file5.txt | 0
 2 files changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 file4.txt
 create mode 100644 file5.txt
$ ls
file1.txt file2.txt file3.txt file4.txt file5.txt
```

Now the `master` and the `better_code` branches are identical. You can check the
history of the `master` branch.

```console
$ git log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short
*   1243e96 2022-10-07 | Fixed conflict (HEAD -> master, better_code) [Romain Teyssier]
|\
| * abc9ee2 2022-10-07 | One more modif to file1 [Romain Teyssier]
* | 1cba3e4 2022-10-07 | I went crazy [Romain Teyssier]
* | ce60f0f 2022-10-07 | Trying to merge again [Romain Teyssier]
|\|
| * 07557d4 2022-10-07 | Modify file1.txt [Romain Teyssier]
* | 8b3b89f 2022-10-07 | Merge branch 'master' into better_code This is necessary. [Romain Teyssier]
|\|
| * 41f8d80 2022-10-06 | Committing file3 (tag: v2) [Romain Teyssier]
| * c6e6535 2022-10-06 | Committing file2 [Romain Teyssier]
* | 6ed6b75 2022-10-07 | Yes it is a better code [Romain Teyssier]
* | 1e19277 2022-10-07 | A better code now? [Romain Teyssier]
|/
* 476b980 2022-10-06 | Commit changes (tag: v1) [Romain Teyssier]
* c073d19 2022-10-06 | First commit [Romain Teyssier]
```

## Cloning a repository

When working in a large team of developers, it might be useful to duplicate the
entire repository across different machines. git is ideally suited for this kind
of collaborative development. For simplicity, we will duplicate the current
repository on your own laptop, but pretend this is in fact a different developer
writing code on a different computer.

First go up one level in your file system to see your directory `mywork`.

```console
$ cd ..
$ ls
mywork
```

Now we will clone the repository using the `git clone` command.

```console
$ git clone mywork cloned_work
Cloning into 'cloned_work'...
done.
$ cd cloned_work
$ ls
file1.txt file2.txt file3.txt file4.txt file5.txt
```

You can see that all the files of the original repository are here. Looking at
the history of the cloned repository, now we get

```console
git log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short
*   1243e96 2022-10-07 | Fixed conflict (HEAD -> master, origin/master, origin/better_code, origin/HEAD) [Romain Teyssier]
|\
| * abc9ee2 2022-10-07 | One more modif to file1 [Romain Teyssier]
* | 1cba3e4 2022-10-07 | I went crazy [Romain Teyssier]
* | ce60f0f 2022-10-07 | Trying to merge again [Romain Teyssier]
|\|
| * 07557d4 2022-10-07 | Modify file1.txt [Romain Teyssier]
* | 8b3b89f 2022-10-07 | Merge branch 'master' into better_code This is necessary. [Romain Teyssier]
|\|
| * 41f8d80 2022-10-06 | Committing file3 (tag: v2) [Romain Teyssier]
| * c6e6535 2022-10-06 | Committing file2 [Romain Teyssier]
* | 6ed6b75 2022-10-07 | Yes it is a better code [Romain Teyssier]
* | 1e19277 2022-10-07 | A better code now? [Romain Teyssier]
|/
* 476b980 2022-10-06 | Commit changes (tag: v1) [Romain Teyssier]
* c073d19 2022-10-06 | First commit [Romain Teyssier]
```

The first line is markedly different than the history of the original
repository, with now 3 new branches `origin/master`, `origin/better_code` and
`origin/HEAD`. These new branches are associated to the remote repository from
which the local one has been cloned. We can get the information regarding the
remote original repository using the `git remote` command.

```console
$ git remote
origin
```

We can learn more about this remote repository named `origin` using

```console
$ git remote show origin
* remote origin
  Fetch URL: /Users/rt3504/mywork
  Push  URL: /Users/rt3504/mywork
  HEAD branch: master
  Remote branches:
    better_code tracked
    master      tracked
  Local branch configured for 'git pull':
    master merges with remote master
  Local ref configured for 'git push':
    master pushes to master (up to date)
```

Let's now make a change in the original repository.

```console
$ cd ../mywork
$ echo "I have changed file5.txt" > file5.txt
$ git add file5.txt
$ git commit -m "Modify file5.txt in origin repository"
```

Let's go back to the cloned repository. `file5.txt` is still empty.

```console
$ cd ../cloned_work
$ cat file5.txt
```

Now let's pull the changes in the remote repository into our cloned one.

```console
$ git pull
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 1), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (3/3), 287 bytes | 287.00 KiB/s, done.
From /Users/rt3504/mywork
   1243e96..1cf5640  master     -> origin/master
Updating 1243e96..1cf5640
Fast-forward
 file5.txt | 1 +
 1 file changed, 1 insertion(+)
```

We can check now that `file5.txt` is now modified as in the original repository.

```console
$ cat file5.txt
I  have changed file5.txt
```

When using `git pull`, you are in fact merging the remote branch with your local branch, using under the hood `git merge`.

## Using GitHub as origin repository

Note that repository `mywork` does not have any `origin` repository. Usually,
true origin repository are located on a remote server, most of the time publicly
available pages like GitHub or BitBucket. Let's first create a new project. Go
to the [GitHub web page](https://github.com) and make sure you are properly
logged in. Then press the button with a `+` sign. Choose `New repository`. Only
specify the name. I suggest you use `se_git`. Leave all other fields empty. Now
go to the repository `mywork` on your laptop and use the command

```console
$ git remote add origin git@github.com:your_login/se_git.git
```

You can now push to the remote GitHub repository all your ongoing work using

```console
$ git push --set-upstream origin master
```

If you now look at the GitHub  website, you can see all your hard work
listed there, including  all the past history. Note that  what we just
did never occurs in practice. You  will always create an empty project
on GitHub or  BitBucket first, and then clone it  to your computer and
start editing files there.

Let's now learn how to change a file in your local repository and push it to the
remote repository.

```console
$ echo "I have changed file4.txt" > file4.txt
$ git add file4.txt
$ git commit -m "Modify file4 on my laptop"
[master ecac23d] Modify file4 on my laptop
 1 file changed, 1 insertion(+)
$ git push
X11 forwarding request failed on channel 0
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 10 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 297 bytes | 297.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To github.com:rteyssier/se_git.git
   1cf5640..ecac23d  master -> master
```

Check now the GitHub webpage. You will see your modifications there. Other
collaborators can now directly clone your GitHub repository and contribute to
your code. You are in business!

## Using git rebase instead of git merge

In large projects with multiple developers, merging different branches can 
result in very cumbersome histories with multiple diverging tracks converging 
back to the master branch with complex patterns. 

`git` offers the `rebase` functionality to combine two branches along the same trunk,
one entire diverging branch after the other. Let's try an example.
Go back to the repository `mywork`. Checkout branch `better_code` and create a new file called `file6.txt`. 
Don't forget to `git add` and `git commit`. Then checkout branch `master` and create a new
file called `file7.txt`. Again, `git add` and `git commit`. 

If you `git log`, you will see now 2 diverging branches like before. 
This time, we will combine these 2 branches using

```console
$ git rebase better_code
Successfully rebased and updated refs/heads/master.
```

If now you type `git log`, you see that the `master` branch has merged the `better_code` branch 
in a single timeline. You don't see any diverging and converging path anymore. 
Commits made in parallel in the `master` branch appear now after the `better_code` commits.

## Example of a complex git repository

Let's now navigate to the BitBucket page of a large collaborative project I
have contributed to, namely the
[RAMSES code](https://bitbucket.org/rteyssie/ramses). You can explore the
different rubrics there, including an automatic test page (more later on this
topic in the course) and a wiki with all the documentation. You can clone the
corresponding repository on your laptop and have fun running hydrodynamics
simulations.

## See also

- [The curious coder’s guide to git](https://matthew-brett.github.io/curious-git/index.html)
