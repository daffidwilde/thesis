""" Generate result directory tree. """

from pathlib import Path

def make_data_tree(inputs, root):
    """ Create a directory tree with a `README.rst` at each leaf if it doesn't
    already exist.

    Parameters
    ----------
    inputs : array-like
        The inputs that will become all subdirectories from the root
    root : str
        The base of the tree
    """

    paths = [Path(f'./{root}/{beta}/{size}/{seed}/{sample_idx}') \
             for beta, size, seed, sample_idx in inputs]

    for path in paths:
        readme_path = Path(f'{path}/README.rst')
        if not readme_path.exists():
            path.mkdir(parents=True, exist_ok=True)
            readme_path.touch()

            beta = path.parts[0]
            sample_idx = path.parts[1]
            seed = path.parts[2]
            size = path.parts[3]

            with readme_path.open('w') as readme_file:
                readme = f'This directory holds the partions for the run with \
                           the following inputs: \n \
                           beta={beta}, size={size}, seed={seed}, \
                           sample_idx={sample_idx}'
                readme_file.write(readme)
