# Useful shell tools and tricks

The shell (usually `bash` or `zsh`) is the glue that holds a scientific
computing workflow together. You probably already use it to run scripts and
launch jobs, but a little fluency with a handful of classic tools can save you
from writing throwaway Python scripts for tasks the shell does in one line.

This chapter is a practical tour of the tools worth knowing. None of it is
exhaustive - the goal is to show you what exists so you know what to reach for.

## Pipes and redirection

Every command has three standard streams: standard input (`stdin`), standard
output (`stdout`), and standard error (`stderr`). The shell lets you redirect
these.

```bash
command > out.txt      # stdout to a file (overwrites)
command >> out.txt     # stdout appended to a file
command 2> err.txt     # stderr to a file
command > all.txt 2>&1 # stdout and stderr to the same file
command < in.txt       # read stdin from a file
```

The pipe `|` connects one command's `stdout` to the next command's `stdin`,
which lets you build pipelines:

```bash
cat data.csv | sort | uniq -c | sort -rn | head
```

This reads a file, sorts it, counts unique lines, sorts by count
(reverse-numeric), and shows the top results - no script required. (You can
often drop the leading `cat` and let the first tool read the file directly, e.g.
`sort data.csv`.)

## Searching text: grep and ripgrep

`grep` searches for patterns (regular expressions) in text:

```bash
grep "error" logfile.txt        # lines containing "error"
grep -i "error" logfile.txt     # case-insensitive
grep -n "error" logfile.txt     # show line numbers
grep -r "TODO" src/             # search recursively
grep -v "DEBUG" logfile.txt     # invert: lines NOT matching
grep -c "error" logfile.txt     # count matches
```

For searching codebases, [ripgrep](https://github.com/BurntSushi/ripgrep) (`rg`)
is much faster and respects `.gitignore` by default:

```bash
rg "def main"          # recursive by default, skips .git and ignored files
rg -t py "import numpy" # only Python files
```

## Finding files: find and fd

`find` locates files by name, type, size, or modification time:

```bash
find . -name "*.py"              # all Python files below the current dir
find . -type f -mtime -1         # files modified in the last day
find . -name "*.tmp" -delete     # find and delete temp files
```

[fd](https://github.com/sharkdp/fd) is a friendlier, faster alternative with a
simpler syntax (and, like `rg`, it respects `.gitignore`):

```bash
fd "\.py$"          # find Python files
fd -e csv           # find files with the csv extension
```

## xargs: turning output into arguments

`xargs` takes a list on `stdin` and turns it into command-line arguments. This
is how you connect "find some things" to "do something to each":

```bash
fd -e py | xargs wc -l                 # count lines in every Python file
fd -e py | xargs -I{} cp {} backup/    # {} is replaced by each filename
fd -e py | xargs -P4 -I{} mytool {}    # run 4 jobs in parallel
```

For filenames with spaces, use `fd -0 ... | xargs -0` (or `find ... -print0`) so
entries are separated by null bytes instead of whitespace.

## Stream editing: sed and awk

`sed` edits a stream line by line. The most common use is substitution:

```bash
sed 's/old/new/' file.txt       # replace first match per line
sed 's/old/new/g' file.txt      # replace all matches (global)
sed -i 's/old/new/g' file.txt   # edit the file in place
sed -n '10,20p' file.txt        # print only lines 10-20
```

`awk` is a small language for columnar data. It splits each line into fields
(`$1`, `$2`, ...) automatically:

```bash
awk '{print $1}' data.txt              # print the first column
awk '{sum += $2} END {print sum}' d.txt # sum the second column
awk -F, '{print $3}' data.csv          # use comma as the field separator
```

These can replace surprisingly large Python scripts for quick data munging, but
reach for a real script once the logic stops fitting on one line.

## History and shortcuts

The shell remembers what you typed. A few high-value tricks:

- `Ctrl-r` searches your command history interactively - start typing and it
  finds the last matching command.
- `!!` re-runs the previous command; `sudo !!` re-runs it with `sudo`.
- `!$` expands to the last argument of the previous command (handy for
  `mkdir foo && cd !$`).
- `Ctrl-a` / `Ctrl-e` jump to the start / end of the line; `Ctrl-w` deletes the
  word before the cursor; `Ctrl-u` clears the line.
- `cd -` returns to the previous directory.

## Working on remote machines: ssh, scp, rsync

Scientific work often happens on clusters or remote servers. `ssh` opens a
remote shell:

```bash
ssh user@host
ssh user@host "command"   # run one command remotely and return
```

Copy files with `scp` (simple) or `rsync` (efficient, resumable, only transfers
differences):

```bash
scp local.txt user@host:/path/        # copy a file to the remote
scp user@host:/path/file.txt .        # copy a file from the remote
rsync -avz local_dir/ user@host:dir/  # sync a directory, compressed
rsync -avz --progress big.dat user@host:data/
```

`rsync` is the right choice for large datasets: rerun it and it only sends what
changed. Set up an SSH key (`ssh-keygen`, then `ssh-copy-id user@host`) so you
are not typing passwords, and add host aliases to `~/.ssh/config` to shorten
long connection strings.

## Keeping work alive: jobs, &, nohup, and tmux

If you start a long-running job and your connection drops, the job usually dies
with it. There are a few ways to avoid that.

Background a command in the current shell:

```bash
mytraining_run &     # start in the background
jobs                 # list background jobs
fg                   # bring the most recent job to the foreground
```

Press `Ctrl-z` to suspend a running foreground job, then `bg` to resume it in
the background.

To survive logout, prefix with `nohup` (and redirect output):

```bash
nohup ./long_job.sh > job.log 2>&1 &
```

The most robust option is a terminal multiplexer like
[tmux](https://github.com/tmux/tmux/wiki) (or the older `screen`). It keeps your
session running on the remote machine even after you disconnect:

```bash
tmux                 # start a new session
# ... run your jobs ...
# press Ctrl-b then d to detach; the session keeps running
tmux attach          # reattach later, even after logging out and back in
```

tmux also gives you split panes and multiple windows in a single terminal, which
is invaluable when juggling an editor, a running job, and a log tail.

## Where to learn more

You do not need to memorize every flag. Two tools make the shell much
friendlier:

- [explainshell.com](https://explainshell.com) - paste any command and it
  annotates each piece (flags, pipes, arguments) with the relevant manual text.
- [tldr](https://tldr.sh) - community-maintained cheat sheets with practical
  examples; run `tldr tar` instead of reading the full `man tar`.

And of course, `man <command>` and `<command> --help` are always available.
