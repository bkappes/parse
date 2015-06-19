from __future__ import print_function
from ...core.extractors import RegexRangeExtractor
import numpy as np

def get_atom_positions(filename, aslist=True):
    """
    Extracts the atom positions from a Gaussian log file.

    Parameters
    ----------
    :filename, {str|file-like}: filename/filestream from which to
            extract the distance matrix/matrices.

    Keywords
    --------
    :aslist, bool: If True, a list of matrices is returned, even if
            only one is found. If False and if only one matrix is
            found, then the matrix is returned as an np.array object.
            If more than one matrix is found, this keyword has no
            affect. (Default: True)

    Returns
    -------
    N x N distance matrix OR list of matrices. See `aslist` keyword.
    """
    # ---------- helper functions ----------- #
    def parse_coordinates(table):
        """
        Reads the atom positions from the coordinates blocks
        found in Gaussian 09 output.

        Returns
        -------
        distance matrix as np.ndarray
        """
        positions = []
        # skip the first 3 lines
        lines = table.splitlines()
        for line in lines[3:]:
            words = line.split()
            try:
                positions.append([float(x) for x in words[3:]])
            except ValueError:
                import sys
                print(sys.stderr, table)
                raise
        positions = np.array(positions)
        return positions
    # --------- end helper functions --------- #

    # open the file, if a string
    if isinstance(filename, str):
        ifs = open(filename, 'r')
    else:
        ifs = filename
    # extract distance matrices
    start = r'Coordinates \(Angstroms\)'
    stop = r'^\s*-{5,}'
    rre = RegexRangeExtractor(start, stop,
                              skip=2,
                              include_start=True,
                              include_stop=False)
    blocks = rre(ifs)
    # close file
    if ifs is not filename:
        ifs.close()
    # convert the matrices
    positions = [parse_coordinates(b) for b in blocks]
    # return as list or single ndarray?
    if (not aslist) and (len(positions) == 1):
        positions = positions[0]
    return positions
