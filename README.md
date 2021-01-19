# New methods for algorithm evaluation and cluster initialisation with
# applications to healthcare

A repository for my PhD thesis at Cardiff University with the Cwm Taf Morgannwg
University Health Board

## Cloning the repo

To clone the repository locally run the following command:

```
$ git clone --recurse-submodules https://github.com/daffidwilde/thesis.git
```

Note that command includes the option `--recurse-submodules`. This is because
there are several submodules to this repository.

## Environment and requirements

All the code for this thesis is written in Python, with all necessary versions
specified in `environment.yml`. This file configures an
[Anaconda virtual environment](https://docs.conda.io/projects/conda/en/latest/
user-guide/tasks/manage-environments.html).

With Anaconda installed, run the following commands to create and activate the
environment:

```
$ conda env create -f environment.yml
$ source activate thesis
```

## Compiling the thesis

This document has been prepared using LaTeX and can be compiled as intended
using any tool that offers a shell escape flag. Examples include `latexmk` and
`pdflatex`.

However, a number of `invoke` tasks have been [written](tasks.py) to ease
compilation and to test this thesis. So, the easiest way is to activate the
`thesis` environment and run the following command:

```
$ inv compile
```
