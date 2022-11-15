# Debugging

Debugging is one of the most painful and addictive activity in software engineering. One could compare it to running or sudoku. You suffer for hours trying to understand why your code is crashing, and when you find the bug, the prize is a dopamine rush and a working code.

In this lecture, we will:

- give an overview of the debugging process

- learn tips and tricks from a lifelong experience in debugging

- gain pratical knowledge in

  - simple debugging techniques using compilers
  - simple debuggers for C/ C++ and Fortran
  - more advanced graphical debuggers

## Overview of the debugging process

### Debugging is not easy

When a code crashes it usually writes out a cryptic error message

- The cpu processes machine instructions, not the C or Fortran source code that you wrote...

- Instructions in the final executable program have probably been rearranged for optimization purposes

- You are in luck if the error happens at the beginning of the execution... usually it does not!

- In a large parallel code, how many processes triggered the problem? 1, 2, all of them? Was it related to inter-process communication?

### Typical error messages

-  ``SIGFPE``: floating point exception
   -  Often controlled by compiler options
   -  division by zero
   -  square root of a negative number
   -  log of a number less or equal to zero

- Does not always crash your code! (unless compiled to do so...)
- The code can keep going for a long time with ``NaN`` values

-  ``SIGSEGV``: segmentation violation (see “man 7 signal”)
   - invalid memory reference!e.g. trying to access an array element
outside the dimensions of an array

Example:
```c
double x[100];
x[345] = 0 ! SIGSEGV
```
- Make sure your shell “stack size limit” and "core size limit" are both set to “unlimited”
  - ``ulimit -c unlimited`` set stack memory to unlimited
  - ``ulimit -s unlimited`` set core file size to unlimited
  - ``ulimit -a`` show all limits

- I/O errors
  - File already exists
  - File doesn't exist
  - No space left on disk
    - ``checkquota`` will check for memory and inodea overflow

```
[rt3504@stellar-intel ~]$ checkquota
          Storage/size quota filesystem report for user: rt3504
Filesystem             Mount              Used   Limit  MaxLim Comment
Stellar home           /home             4.8GB    93GB   100GB
Stellar scratch GPFS   /scratch/gpfs    29.1TB  34.2TB    35TB
Tigress GPFS           /tigress          3.8TB   9.8TB    10TB

Fileset/project space            Mount                Used by ALL By rt3504  MaxLim Comment
Projects GPFS fileset TEYSSIER   /projects/TEYSSIER           0KB         0     5TB

          Storage number of files used report for user: rt3504
Filesystem             Mount              Used   Limit  MaxLim Comment
Stellar home           /home             54.8K    952K    1.0M
Stellar scratch GPFS   /scratch/gpfs      2.3M    3.0M      3M
Tigress GPFS           /tigress         364.7K       0       0

Fileset/project space            Mount                Used by ALL By rt3504  MaxLim Comment
Projects GPFS fileset TEYSSIER   /projects/TEYSSIER             2         1    None

For quota increase requests please use this website:

         https://forms.rc.princeton.edu/quota
```

- NO ERROR MESSAGE AT ALL!
  - The code just hangs
  - Usually points to a communication deadlock in a parallel code
  - The results are just plain wrong
    - can be your fault (bug, race condition)
    - can be the system fault (MPI communication failure)

### Take advantage of the compiler options

- Take the time to go through all the options of the compiler that you use

- Pay particular attention to the diagnostics options under sections with names such as “debugging”, “optimization”, “target-specific”, “warnings”

- Using ``man gcc`` or ``man gfortran`` is a good start although most compilers now have detailed online documentation! Just check the company’s web site under “support” or “documentation”. For example, the documentation for ``gcc`` (GNU Compiler Collection) can be found [here](https://gcc.gnu.org).

```
[rt3504@stellar-intel ~]$ man gfortran
GFORTRAN(1)                                                   GNU                                                   GFORTRAN(1)

NAME
       gfortran - GNU Fortran compiler

SYNOPSIS
       gfortran [-c|-S|-E]
                [-g] [-pg] [-Olevel]
                [-Wwarn...] [-pedantic]
                [-Idir...] [-Ldir...]
                [-Dmacro[=defn]...] [-Umacro]
                [-foption...]
                [-mmachine-option...]
                [-o outfile] infile...

       Only the most useful options are listed here; see below for the remainder.

DESCRIPTION
       The gfortran command supports all the options supported by the gcc command.  Only options specific to GNU Fortran are
       documented here.

       All GCC and GNU Fortran options are accepted both by gfortran and by gcc (as well as any other drivers built at the same
       time, such as g++), since adding GNU Fortran to the GCC distribution enables acceptance of GNU Fortran options by all of
       the relevant drivers.

       In some cases, options have positive and negative forms; the negative form of -ffoo would be -fno-foo.  This manual
       documents only one of these two forms, whichever one is not the default.

OPTIONS
       Here is a summary of all the options specific to GNU Fortran, grouped by type.  Explanations are in the following
       sections.
       
       Error and Warning Options
           -Waliasing -Wall -Wampersand -Wargument-mismatch -Warray-bounds -Wc-binding-type -Wcharacter-truncation -Wconversion
           -Wdo-subscript -Wfunction-elimination -Wimplicit-interface -Wimplicit-procedure -Wintrinsic-shadow
           -Wuse-without-only -Wintrinsics-std -Wline-truncation -Wno-align-commons -Wno-tabs -Wreal-q-constant -Wsurprising
           -Wunderflow -Wunused-parameter -Wrealloc-lhs -Wrealloc-lhs-all -Wfrontend-loop-interchange -Wtarget-lifetime
           -fmax-errors=n -fsyntax-only -pedantic -pedantic-errors

       Debugging Options
           -fbacktrace -fdump-fortran-optimized -fdump-fortran-original -fdump-parse-tree -ffpe-trap=list -ffpe-summary=list
```

- [see Intel C, C++ and Fortran compiler debugging and optimization pages here](https://www.intel.com/content/www/us/en/develop/documentation/fortran-compiler-oneapi-dev-guide-and-reference/top/compilation/debugging/debugging-and-optimizations.html)

### The ``-g`` compiler option

All compilers accept the ``-g`` option.

- It links the source code to the executed machine language code.

- The ``-g`` option is necessary when using a debugger unless you are REALLY good at deciphering machine language.

- However, using ``-g`` slows down the code significantly

- Removes optimizations (unless one uses ``–gopt`` or ``–g –O3``)

- Start with ``-g –O0`` (no optimization) for most accurate correspondence between executable instructions and source code line

- Inserts a lot of extra information in the executable to help the debugging process

- Running with ``-g`` is sometimes sufficient to find a bug. The code crashes and indicates where the error occurred

### The ``-g`` option makes the bug go away!

- Sometimes, the fact of using the ``-g`` option makes the bug go away

- This does not necessarily mean that the optimized code generated by the compiler is wrong, although it could be...

- It can point to a memory issue, such as a pointer accessing a bad memory address when the optimized code is executed

- Look at your compiler’s documentation for how you can use the ``-g`` option while keeping most of the optimizations intact, such as ``-gopt`` for the PGI compiler (Portland Group), or simply ``-g –O2`` for Intel
  - caveat: these solutions can sometimes point you to the wrong location in the source code

### Examples of useful compiler options

- All compilers have options that try to detect potential bugs in the code
  - Array bounds check (Fortran: –C, -Mbounds, -check bounds)
    - Check for array subscripts and substrings out of bounds
    - Should be done on unoptimized code (-O0)
  - Easier for Fortran than C/C++ due to the way pointers are treated
    - In C, it is the responsibility of the programmer to make sure that a pointer always points to a valid address and number

- Enable runtime error traceback capability
  - --trace, -trace, -traceback

- Make sure that Floating Point Exceptions (FPE) are turned on
  - e.g. -fpe0 for Intel and -Ktrap=fp for PGI compiler

### Warning options in ``gcc`` and ``gfortran``

- The gcc compiler has a large number of options that will produce a warning at compile time
  - They all start with ``-W...``
  - Example: ``-Wuninitialized`` warns if an automatic variable is used before being initialized
  - ``-Wall`` turns on most of the gcc warning options
  - ``-Werror`` makes all warnings into errors
  - Different levels of debugging information with ``–g1``, ``–g2``, and ``–g3``
  - See ``man gcc``

### Try different compilers if you can

- Whenever you can, it is always a good idea to try different compilers if you have access to different plavorms or different compilers on the same plavorm

- Some compilers are a lot stricter than others and can catch potential problems at compile time

- See [this page](https://www.fortran.uk/fortran-compiler-comparisons/intellinux-fortran-compiler-diagnostic-capabilities/) for comparison between Fortran compilers in terms of available diagnostics

- See [this page](https://gcc.gnu.org/wiki/ClangDiagnosticsComparison) for comparison between GCC and Clang compilers in term of available diagnostics


### The code crashes... now what?!

- The first thing that you need to know is **where** the code stopped and **how** it got there

- Each time a program performs a function call, information about the call is generated. That information includes the location of the call in the program, the arguments of the call, and the local variables of the function being called

- This information is saved in a block of data called *stack frame*

- The stack frames are stored in a region of memory called the **call stack**

### Saving the stack in ``core`` files

- How can one view the stack if the code crashed?

- When a code crashes, the system (normally) saves the last call stack of the code in files named ``core`` (or ``core.#``, where ``#`` is the rank number of an MPI task in a parallel code)

- No ``core`` file?
  - Check your shell limits: ``ulimit –a`` (bash) or ``limit`` (csh)
  - Look for ``core file size`` (bash) or ``coredumpsize`` (csh) > 0

- These files are binary files meant to be read by debuggers

- Of limited use if the code was not compiled with –g option that links machine language code to high-level source code

### Examining the call stack

- All debuggers should allow you to view the call stack, or simply stack

- Commands to look for in the debuggers
  - backtrace (gdb)
  - where
  - info stack

```
[rt3504@stellar-intel ~]$ apropos debug
__after_morecore_hook (3) - malloc debugging variables
__free_hook (3)      - malloc debugging variables
__malloc_hook (3)    - malloc debugging variables
__malloc_initialize_hook (3) - malloc debugging variables
__memalign_hook (3)  - malloc debugging variables
__realloc_hook (3)   - malloc debugging variables
_nc_tracebits (3x)   - curses debugging routines
_traceattr (3x)      - curses debugging routines
_traceattr2 (3x)     - curses debugging routines
_tracecchar_t (3x)   - curses debugging routines
_tracecchar_t2 (3x)  - curses debugging routines
_tracechar (3x)      - curses debugging routines
_tracechtype (3x)    - curses debugging routines
_tracechtype2 (3x)   - curses debugging routines
_tracedump (3x)      - curses debugging routines
_tracef (3x)         - curses debugging routines
_tracemouse (3x)     - curses debugging routines
backtrace (3)        - support for application self-debugging
backtrace_symbols (3) - support for application self-debugging
backtrace_symbols_fd (3) - support for application self-debugging
BIO_debug_callback (3ssl) - BIO callback functions
CPAN::Debug (3pm)    - internal debugging for CPAN.pm
CRYPTO_mem_debug_pop (3ssl) - Memory allocation functions
CRYPTO_mem_debug_push (3ssl) - Memory allocation functions
CRYPTO_set_mem_debug (3ssl) - Memory allocation functions
CURLOPT_DEBUGDATA (3) - custom pointer for debug callback
CURLOPT_DEBUGFUNCTION (3) - debug callback
curs_trace (3x)      - curses debugging routines
DB (3pm)             - programmatic interface to the Perl debugging API
dbus-monitor (1)     - debug probe to print message bus messages
debugfs (8)          - ext2/ext3/ext4 file system debugger
debuginfod-client-config (7) - debuginfod client environment variables, cache...
debuginfod-find (1)  - request debuginfo-related data
dftest (1)           - Shows display filter byte-code, for debugging dfilter ...
dnf-debug (8)        - DNF debug Plugin
dnf-debuginfo-install (8) - DNF debuginfo-install Plugin
error::dwarf (7stap) - dwarf debuginfo quality problems
gnutls-cli-debug (1) - GnuTLS debug client
FcPatternPrint (3)   - Print a pattern for debugging
gdb (1)              - The GNU Debugger
```

- Use the ``apropos debug`` command on your UNIX-based plavorm to find out which debugger is available

- If working on Linux (most cases), ``gdb`` should be available

### The ``gdb`` debugger

- Official GNU debugger available under Linux

- Widely used for C and C++ code debugging

- Can also be used with Fortran codes

- Online manual for gdb at ``info gdb``

- Can be used within the ``emacs`` editor
  - Can run gdb commands within the emacs source code window (e.g. C-x SPC to set a breakpoint)

- See also Visual Studio

- Online manual can be found [here](https://www.sourceware.org/gdb/current/).

- If code was compiled with –g and *dumped core files* when it crashed, the first thing to try is the following:

```sh
$ gdb executable core.#
(gdb) where (or backtrace, or bt)
```

- The ``where`` command prints out the call stack

- You can also use the DDT advanced debugger to open the core file and view the call stack...

### Using ``gdb``

- Compile with ``-g -O0`` to get accurate binary-to-source correspondence

- Start gdb: ``gdb a.out``

- You get the (gdb) prompt, where you can type the commands:

| Command | Abbrev. | Description |
| :----------- | :----------- | :----------- |
| ``help`` |   | List gdb command topics|
| ``run`` |  ``r``  | Start program execution |
| ``break`` |   | Suspend execution at specific location (line number, function, instruction address, etc.)
| ``step`` | ``s``  | Step to next line of code. Will step into a function if necessary|
| ``next`` |  ``n`` | Execute next line of code. Will NOT enter functions|
| ``until`` |   | Continue processing until it reaches a specified line|
| ``list`` |  ``l`` | List source code with current position of execution|
| ``print`` | ``p``  | Print value stored in a variable|

### The ``gdb`` debugger: a demo

Here is a simple example program in Fortran:
- homework: do the samne in C and C++

```c
program bug

  real(kind=8),dimension(10)::table
  integer::i
  real(kind=8)::x

  i=40
  x=0
  table(i)=2/x
  write(*,*)table(i)

end program bug
```

Now let's compile it and run it on stellar:

```
$ gfortran bug.f90 -o bug
$ ./bug
                  Infinity
```
OK, the compiler managed to deal quite elegantly with the divide by zero.
It didn't care about the array index overflow.

Let's now compile with some more debugging options:
```sh
$ gfortran -g -fbounds-check -ffpe-trap=zero bug.f90 -o bug
$ ./bug

At line 9 of file bug.f90
Fortran runtime error: Index '40' of dimension 1 of array 'table' above upper bound of 10

Error termination. Backtrace:
#0  0x152331025171 in ???
#1  0x152331025d19 in ???
#2  0x1523310260fb in ???
#3  0x400878 in bug
	at /home/rt3504/bug.f90:9
#4  0x400986 in main
	at /home/rt3504/bug.f90:12
```
Let's correct the bug by modifying the program as follows:
```c
program bug

  real(kind=8),dimension(10)::table
  integer::i
  real(kind=8)::x

  i=4
  x=0
  table(i)=2/x
  write(*,*)table(i)

end program bug
```
and compile it again:
```sh
$ gfortran -g -fbounds-check -ffpe-trap=zero bug.f90 -o bug
$ ./bug

Program received signal SIGFPE: Floating-point exception - erroneous arithmetic operation.

Backtrace for this error:
#0  0x154be604c171 in ???
#1  0x154be604b313 in ???
#2  0x154be54dbb1f in ???
#3  0x400885 in bug
	at /home/rt3504/bug.f90:9
#4  0x400986 in main
	at /home/rt3504/bug.f90:12
Floating point exception (core dumped)
```
Now we can fix the last bug:
```c
program bug

  real(kind=8),dimension(10)::table
  integer::i
  real(kind=8)::x

  i=4
  x=0.1
  table(i)=2/x
  write(*,*)table(i)

end program bug
```
and try again:
```sh
$ gfortran -g -fbounds-check -ffpe-trap=zero bug.f90 -o bug
$ ./bug
   19.999999701976780
```
That's much better. We still need to fix the precision of the division by changing:
```c
program bug

  real(kind=8),dimension(10)::table
  integer::i
  real(kind=8)::x

  i=4
  x=0.1d0
  table(i)=2/x
  write(*,*)table(i)

end program bug
```
and try one last time:
```sh
$ gfortran -g -fbounds-check -ffpe-trap=zero bug.f90 -o bug
$ ./bug
   20.000000000000000
```
Ah now it is good!

Let's now use ``gdb``:
```sh
$ gfortran -g -fbounds-check -ffpe-trap=zero -fbacktrace bug.f90 -o bug
$ gdb ./bug
Reading symbols from ./bug...done.
(gdb) b 6
Breakpoint 1 at 0x400821: file bug.f90, line 7.
(gdb) r
Starting program: /home/rt3504/bug

Breakpoint 1, bug () at bug.f90:7
7	  i=4
(gdb) p i
$1 = -2030981413
(gdb) s
8	  x=0.1d0
(gdb) p i
$2 = 4
(gdb) p x
$3 = 1.602534106313551e-310
(gdb) s
9	  table(i)=2/x
(gdb) p x
$4 = 0.10000000000000001
(gdb) s
10	  write(*,*)table(i)
(gdb) p table
$5 = (8.4038908174475465e-315, 6.9533558073037849e-310, 1.158892633800178e-310, 20, 6.9533558072958799e-310, 6.9533558072950894e-310, 0, -3.1921319842597682e-275, 3.1124515152680173e-317, -3.192130481461112e-275)
(gdb) s
   20.000000000000000
12	end program bug
```

### I know where the code crashed... what's next?

- Detective work starts

- Try reducing the problem size and see if the error is still there
  - The smaller the better
  - Running with only 2 processes is ideal if your code is parallel

- Start your code in a debugger (gdb or other) and set a breakpoint on a line executed before the crash

- Examine the values of variables and arrays by printing them out or visualizing them (advanced debuggers)

- Step through your code line by line until you find the problem

- Set other breakpoints to jump over long sections of code, such as
loops

- If you know which variable goes bad, use a conditional breakpoint
to run ``until`` (gdb) the variable changes to a given value

- Visualizing the results coming out of the code may help detect problems
  - Grid problems are often detected by visual inspection of images and movies

### Python debugger

- The ``pdb`` debugger is part of Python

- Just insert the following at any point in your Python code:
```python
import pdb
pdb.set_trace()
```

- The execution will stop after these lines and will put you under ``pdb`` (you will have the (Pdb) prompt)

- Use ``help`` to see the commands
```
(base) ➜  ~ ./map2deb.py Work/tom/velx_00001.map
Reading Work/tom/velx_00001.map
> /Users/rt3504/map2deb.py(21)<module>()
-> with FortranFile(path_to_output, 'r') as f:
(Pdb) help

Documented commands (type help <topic>):
========================================
EOF    c          d        h         list      q        rv       undisplay
a      cl         debug    help      ll        quit     s        unt
alias  clear      disable  ignore    longlist  r        source   until
args   commands   display  interact  n         restart  step     up
b      condition  down     j         next      return   tbreak   w
break  cont       enable   jump      p         retval   u        whatis
bt     continue   exit     l         pp        run      unalias  where

Miscellaneous help topics:
==========================
exec  pdb
```

Let's see another example
```
(base) ➜  ~ ./map2deb.py Work/tom/velx_00001.map
Reading Work/tom/velx_00001.map
> /Users/rt3504/map2deb.py(21)<module>()
-> with FortranFile(path_to_output, 'r') as f:
(Pdb) help p
p expression
        Print the value of the expression.
(Pdb) p path_to_output
'Work/tom/velx_00001.map'
(Pdb)
```

### Please use checkpoint-restart!

- Checkpoint = write out to files **all the information** that you need to restart a simulation from that point

- Extremely important for codes that have long runtimes (> 1 hour)
  - Allows you to restart your simulation at the point of the latest checkpoint
  - Avoid losing hours of precious computer time
  - Especially important for parallel codes

- Extremely important when you need to debug a code that crashes after a few hours!!
  - You can recompile the code with ``–g`` and start from the last checkpoint
  - Remember... ``-g`` slows down the code dramatically so you want to be as close to the crash as possible

- When restarting a simulation from a checkpointed state, reproducibility is very important
  - Test by running the code to a certain point and saving its state at that point
  - Rerun the same case but split in 2 steps where the 2nd step uses restart files generated by the first step
  - Compare the end results of the 2 simulations: they should be **bitwise** identical

- The restart files need to be BINARY files

- When dealing with random numbers, use a reproducible random number generator for which you can save the state for restart purposes like [SPRNG](http://www.cs.fsu.edu/~mascagni/SPRNG_KAUST.pdf).

### Using ``printf`` for monitoring and debugging

- Many serious developers still use old school ``printf`` or ``write`` statements to monitor and debug their codes

- May be the only recourse when running a code at very large concurrencies (100,000+ processors)

- The idea is simple:
  - Insert ``printf`` or ``write`` statements at strategic locations in the code to gather information and try to pinpoint the faulty code line
  - Advantages over other forms of debugging:
    - Easy to use and always works
    - Low overhead
    - Works on optimized code!
  - Caveat:
    - may change or prevent optimization of a section of the code.
    - don't put inside loops!

- For optimization purposes, all code output is buffered before being written to disk unless directed otherwise

- If the code crashes before the memory buffers get written to disk, the information is lost

- It makes it difficult to pinpoint the exact location of the failing statement

- This is the case when using “printf” or “write(6,*)” which redirects to the **standard output**

- Write to **standard error** as much as possible since it is not buffered
  - ``printf(stderr,...)`` in C/C++
  - ``cerr <<`` in C++
  - ``write(0,*)`` in Fortran
  - redirect output: ``mpirun –np 1024 ./a.out 1> output.out 2> output.err``

- Explicit flushing of I/O buffers with ``fflush()`` (C) or ``call flush(unit)`` (Fortran)

### Debugging memory leaks

```c
program memleak

  integer::i

  do i=1,20
     if(mod(i,10)==0)write(*,*)i
     call compute_nothing
  end do

end program memleak

subroutine compute_nothing

  integer,dimension(:),allocatable,target::array
  integer,dimension(:),pointer::p
  integer::i
  integer::n=100000000
  real::outmem

  allocate(array(n))
  allocate(p(n))
  do i=1,n
     array(i)=i*2
  end do
  p=>array
  deallocate(array)

end subroutine compute_nothing
```

```
$ gfortran -g memleak.f90 -o ml
$ ./ml
```
```
[rt3504@stellar-intel ~]$ top -n 1 | grep -B1 ml
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
3092916 rt3504    20   0 4316088  81436   2232 R  94.4   0.0   0:02.29 ml
[rt3504@stellar-intel ~]$ top -n 1 | grep -B1 ml
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
3092916 rt3504    20   0 6269228 314928   2232 R 100.0   0.1   0:03.69 ml
[rt3504@stellar-intel ~]$ top -n 1 | grep -B1 ml
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
3092916 rt3504    20   0 9937.0m  87640   2232 R 100.0   0.0   0:06.04 ml
[rt3504@stellar-intel ~]$ top -n 1 | grep -B1 ml
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
3092916 rt3504    20   0   11.9g 343664   2232 R 100.0   0.1   0:07.70 ml
[rt3504@stellar-intel ~]$ top -n 1 | grep -B1 ml
    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
3092916 rt3504    20   0   14.5g 298636   2232 R  94.4   0.1   0:09.42 ml
```
```
[rt3504@stellar-intel ~]$ valgrind --leak-check=full ./ml
==3093274== Memcheck, a memory error detector
==3093274== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==3093274== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==3093274== Command: ./ml
==3093274==
==3093274== Warning: set address range perms: large range [0x35f70028, 0x4dce8458) (noaccess)
          10
==3093274== Warning: set address range perms: large range [0x100cf0040, 0x118a68440) (undefined)
	  20
==3093274== Warning: set address range perms: large range [0x1ef3aa040, 0x207122440) (undefined)
==3093274== Warning: set address range perms: large range [0x1d7631040, 0x1ef3a9440) (undefined)
==3093274== Warning: set address range perms: large range [0x1ef3aa028, 0x207122458) (noaccess)
==3093274==
==3093274== HEAP SUMMARY:
==3093274==     in use at exit: 8,000,000,000 bytes in 20 blocks
==3093274==   total heap usage: 61 allocs, 41 frees, 16,000,013,520 bytes allocated
==3093274==
==3093274== 2,000,000,000 bytes in 5 blocks are possibly lost in loss record 1 of 2
==3093274==    at 0x4C37135: malloc (vg_replace_malloc.c:381)
==3093274==    by 0x400B19: compute_nothing_ (memleak.f90:21)
==3093274==    by 0x400CF6: MAIN__ (memleak.f90:7)
==3093274==    by 0x400D3C: main (memleak.f90:10)
==3093274==
==3093274== 6,000,000,000 bytes in 15 blocks are definitely lost in loss record 2 of 2
==3093274==    at 0x4C37135: malloc (vg_replace_malloc.c:381)
==3093274==    by 0x400B19: compute_nothing_ (memleak.f90:21)
==3093274==    by 0x400CF6: MAIN__ (memleak.f90:7)
==3093274==    by 0x400D3C: main (memleak.f90:10)
==3093274==
==3093274== LEAK SUMMARY:
==3093274==    definitely lost: 6,000,000,000 bytes in 15 blocks
==3093274==    indirectly lost: 0 bytes in 0 blocks
==3093274==      possibly lost: 2,000,000,000 bytes in 5 blocks
==3093274==    still reachable: 0 bytes in 0 blocks
==3093274==         suppressed: 0 bytes in 0 blocks
==3093274==
==3093274== For lists of detected and suppressed errors, rerun with: -s
==3093274== ERROR SUMMARY: 2 errors from 2 contexts (suppressed: 0 from 0)~

```



