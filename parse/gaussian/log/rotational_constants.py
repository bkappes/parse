from ...core.extractors import RegexExtractor
import numpy as np

def get_rotational_constants(filename, aslist=True):
    """
    Extracts the rotational constants from a Gaussian log file.

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
    1 x 3 rotational constants OR list of constants.
    See `aslist` keyword.
    """
    # ---------- helper functions ----------- #
    def parse_vector(line):
        """
        Reads the rotational constants from Gaussian 09 output.

        Returns
        -------
        rotational constants as np.ndarray
        """
        labels, values = line.split(':')
        values = [float(v) for v in values.strip().split()]
        return np.array(values)
    # --------- end helper functions --------- #

    # open the file, if a string
    if isinstance(filename, str):
        ifs = open(filename, 'r')
    else:
        ifs = filename
    # extract distance matrices
    regex = r'^\s*Rotational constants'
    rre = RegexExtractor(regex)
    lines = rre(ifs)
    # close file
    if ifs is not filename:
        ifs.close()
    # convert the matrices
    rotational_constants = [parse_vector(l) for l in lines]
    # return as list or single ndarray?
    if (not aslist) and (len(rotational_constants) == 1):
        rotational_constants = rotational_constants[0]
    return rotational_constants
