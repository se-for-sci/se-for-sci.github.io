# Unix setup and tools

## Operating System

In this course, we'll assume basic access to a UNIX-like system and shell.

On Linux, that's default.

On macOS, it's close enough. I'd recommend homebrew and a few things, see [Intel](https://iscinumpy.dev/post/setup-a-new-mac)/[AS](https://iscinumpy.dev/post/setup-apple-silicon/) recommendations, but it's optional.

On Windows, you should be on a recent version, and you'll probably want to use WSL2 (Linux subsystem for Windows). This is an integrated way to enjoy a UNIX system on Windows. You can get Ubuntu from the Windows store and use it via WSL2.

From this point on, we should all be on nearly the same page.

## Shell

The UNIX shell is Bash (or a Bashwards compatible shell like Zsh). We'll be using that (though you might see the Fish shell occasionally, but we will attempt to point out if there's a difference that matters). Fish is a nicer shell than Bash, but not as commonly used.

## Version control

We'll cover this in the next section in more detail, but the VCS of choice is Git. It's wildly popular and very fast, capable of handling millions of lines of code (it was designed for the Linux kernel).

## Python

For Python, we'll use a recent version of Python (3.10 highly recommended, 3.8+ _probably_ okay). One way to get Python is via Conda (like anaconda, miniconda, etc). Another way is to use homebrew (often on Linux). If you are using Ubuntu 22.04, the system Python will be fine.

## Compiler

We'll be using CMake and a moderately recent system compiler. GCC or Clang should be fine. We won't need these till later in the course.

## Editor

You should have an editor you like. I'll be using a VI interface, either natively or in VS Code. You can pick EMacs, or something else.
