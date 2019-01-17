"""
Script for the collection and manipulation of similar pairs in a given
dataset, using dask to parallelise the work needed.
"""

import sys
import itertools
import dask.dataframe as dd
import numpy as np

from generate_dir_tree import make_data_tree
from write_results import write_dataframes

if __name__ == '__main__':

    if len(sys.argv) == 1:
        root = 'results'
    else:
        root = str(sys.argv[2])

df = dd.read_csv('data/zoo.csv')

x_bar = df[df['catsize'] == 1]
x_til = df[df['catsize'] != 1]

betas = np.linspace(0, 0.5, 51)
sizes = [x for x in range(1, max(len(x_bar), len(x_til)))]
seeds = np.arange(25)
sample_idxs = np.arange(25)

inputs = itertools.product(betas, sizes, seeds, sample_idxs)
make_data_tree(inputs, root)

results = [write_dataframes(root, x_bar, x_til, beta, size, seed, sample_idx) \
           for beta, size, seed, sample_idx in inputs]
