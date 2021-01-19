# New methods for algorithm evaluation and cluster initialisation with applications to healthcare

A repository for my PhD thesis at Cardiff University with the Cwm Taf Morgannwg
University Health Board (UHB).

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
[Anaconda virtual environment][envs].


With Anaconda installed, run the following commands to create and activate the
environment:

```
$ conda env create -f environment.yml
$ source activate thesis
```

## Compiling the thesis

This document has been prepared using LaTeX and can be compiled as intended
with any tool that offers a shell escape flag. Examples include `latexmk` and
`pdflatex`.

However, a number of `invoke` tasks have been [written](tasks.py) to ease the
compilation and testing of this thesis. So, the easiest way to compile the
document is to activate the `thesis` environment and run the following command:

```
$ inv compile
```

## Abstract

This thesis explores three themes related to modern operational research:
evaluating the objective performance of an algorithm, combining clustering with
concepts of mathematical fairness, and developing insightful healthcare models
despite a lack of fine-grained data.

The established evaluation procedure for algorithms --- and particularly machine
learning algorithms --- lacks robustness, potentially inflating the success of
the methods being assessed. To tackle this, the evolutionary dataset
optimisation method is introduced as a supplementary evaluation tool. By
traversing the space in which datasets exist, this method provides the means of
attaining a richer understanding of the algorithm under study.

This method is used to investigate a novel initialisation method for a
centroid-based clustering algorithm, k-modes. The initialisation makes use of a
matching game to allocate the starting centroids in a mathematically fair way.
The subsequent investigation reveals the conditions under which the new
initialisation improves upon two other initialisation methods.

An extension to the k-modes algorithm is utilised to segment an administrative
dataset provided by the co-sponsors of this project, the Cwm Taf Morgannwg UHB.
The dataset corresponds to the patient population presenting a specific chronic
disease, and comprises a high-level summary of their stays in hospital over a
number of years. Despite the relative coarseness of this dataset, the
segmentation provides a useful profiling of its instances. These profiles are
used to inform a multi-class queuing model representing a hypothetical ward for
the affected patients. Following a novel validation process for the queuing
model, actionable insights into the needs of the population are found.

In addition to the research reported in this thesis, several open-source
software packages have been developed to accompany this thesis. These pieces of
software were developed using best practices to ensure the reliability,
reproducibility, and sustainability of the research in this thesis.


## Additional software

Directions for the relevant software packages to accompany this thesis are
listed in the table below.

| Name       | Repository             | Documentation                     |
|------------|------------------------|-----------------------------------|
| `edo`      | [daffidwilde/edo]      | [edo.readthedocs.io][e-docs]      |
| `matching` | [daffidwilde/matching] | [matching.readthedocs.io][m-docs] |
| `edolab`   | [daffidwilde/edolab]   | Repository `README`               |

[envs]: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
[daffidwilde/edo]: https://github.com/daffidwilde/edo
[e-docs]: https://edo.readthedocs.io
[daffidwilde/matching]: https://github.com/daffidwilde/matching
[m-docs]: https://matching.readthedocs.io
[daffidwilde/edolab]: https://github.com/daffidwilde/edolab
