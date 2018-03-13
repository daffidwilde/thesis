"""
Script for the collection and manipulation of similar pairs in a given
dataset, using dask to parallelise the work needed.
"""

import sys
import time
import dask
import dask.dataframe as dd
import pandas as pd
import numpy as np

from sampling import get_sample, dissim, build_matrices, build_dataframe
from write_results import write_results

if __name__ == '__main__':

    processes = int(sys.argv[1])
    if len(sys.argv) == 2:
        root = 'results'
    else:
        root = str(sys.argv[2])
