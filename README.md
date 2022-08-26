# Software Engineering for Scientific Computing

A course by Henry Schreiner & Romain Teyssier. Some material written by Gabriel
Perez-Giz for previous iterations of this course.

This material is rendered into a website at
<https://henryiii.github.io/se-for-sci>. A WebAssembly version of some
notebooks is available at <https://henryiii.github.io/se-for-sci/live>.


## Running locally

First, install the provided environment with conda or better, mamba:

```bash
mamba env create
```

If you've already done this, you can update your environment with:


```bash
mamba env update
```


You then should activate the environment:

```bash
conda activate se-for-sci
```


You can then enter Jupyter Lab:

```bash
jupyter lab .
```

Or build the Jupyter Book:

```bash
jupyter book build .
```

