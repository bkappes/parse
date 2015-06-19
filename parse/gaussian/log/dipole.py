from ...core.extractors import RegexExtractor
import numpy as np
import re

def get_dipole(filename, aslist=True):
    """
    Extracts the dipoles (output for each step)
    from a Gaussian log file.

    Keywords
    --------
    :aslist, bool: If True, a list of matrices is returned, even if
            only one is found. If False and if only one matrix is
            found, then the matrix is returned as an np.array object.
            If more than one matrix is found, this keyword has no
            affect. (Default: True)

    Returns
    -------
    1 x 3 dipole, or list of 1 x 3 dipoles.
    See `aslist` keyword.
    """
    # --------------- helper functions --------------- #
    def parse_dipole(line):
        """
        Converts the text string of the dipole values.
        """
        # Expected format:
        # Dipole         =% 10.8D+2% 10.8D+2% 10.8D+2"
        # grab vector
        line = line.split('=')[1]
        # the Gaussian file is not careful to separate
        # the numbers, so we must assume that the number
        # format is fixed, i.e.
        # x.x{1,}D+yy
        dipole = re.split('([^D]+D\+..)', line)
        # cast these as floats -- must first replace
        # D with E.
        dipole = [float(v.replace('D', 'E')) for v in dipole if v]
        return np.array(dipole)
    # ------------- end helper functions ------------- #

    # open the file, if a string
    if isinstance(filename, str):
        ifs = open(filename, 'r')
    else:
        ifs = filename
    # extract the dipole
    regex = r'^\s*Dipole\s+='
    rre = RegexExtractor(regex)
    lines = rre(ifs)
    # close file
    if ifs is not filename:
        ifs.close()
    # convert the dipoles
    dipoles = [parse_dipole(l) for l in lines]
    # return as list or single ndarray?
    if (not aslist) and (len(dipoles) == 1):
        dipoles = dipoles[0]
    return dipoles
