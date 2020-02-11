SOURCE CODE
===========

This directory contains all of the source code to generate the data and plots
used in the paper "Evolutionary Dataset Optimisation: learning algorithm quality
through evolution".

At the top level of this directory is an ``environment.yml`` file used to create
a virtual ``conda`` environment. This environment will ensure that the code
herein will reproduce the data and plots used in the paper exactly. Instructions
on how to create, use and otherwise manage ``conda`` environments can be found
at the following link:

https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

The top-level directory contains two ZIP archives that should be uncompressed.
The ``src`` directory contains a package that should be installed locally. To
do so, ensure you have activated the ``conda`` environment and then run the
following command: ``python setup.py install``. The ``edo_exp`` package will now
be installed within this environment.

The source code for the ``edo_exp`` package can be found in the ``src/edo_exp/``
directory -- this contains the functions used by all of the experiments.

The experiment-specific source code used in the paper is stored in the
``experiments`` ZIP archive that should be uncompressed. Each directory within
``experiments`` corresponds to a different experiment from the case study
presented in the work. Each experiment directory contains two files:

- ``data.py``: a script used to generate the data for a given trial. The
  parameters of the trial must be given at runtime to specify the number of
  cores to be used (for parallelisation), population size, selection proportion,
  mutation probability, and seed. For instance, the command for the first trial
  for each experiment in the paper was of the form:
  ``python data.py 4 100 0.2 0.01 0``.
- ``plots.py``: a script used to generate and save the plots for the experiment.
  Uses trial 0 by default. This script assumes that the data is available in the
  directory structure defined in ``data.py``. For instance, for trial 0 of
  ``kmeans_over_dbscan``, this script looks for data in
  ``../../../data/kmeans_over_dbscan/0/data/``.
