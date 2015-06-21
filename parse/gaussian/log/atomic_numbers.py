from ...core.extractors import RegexRangeExtractor
import numpy as np

def get_atomic_numbers(filename, each_step=False):
    """
    Extracts the atomic numbers of the atoms in the simulation.

    The atomic numbers are recorded for every step, so
    they may be subject to change during the calculation.
    However, this is very rarely the case; therefore, a check
    is made, and if the atomic numbers do not change in the
    course of the simulation, then only one ndarray is returned.
    This array contains the atomic numbers of each atom.

    Keywords
    --------
    :each_step, bool: If True, then the atomic numbers for
            each step are returned as a list, regardless of
            whether they are constant through the duration
            of the calculation. If False (default), they a
            list is only returned if the atomic numbers
            change in the course of the simulation.

    Returns
    -------
    ndarray of atomic numbers (int). See `each_step` and
    the summary for exceptional behavior.
    """
    # --------------- helper functions --------------- #
    def parse_data(block):
        """
        Parse the line(s) to get the data.
        """
        lines = block.strip().splitlines()
        anum = []
        for line in lines[3:]:
            words = line.split()
            anum.append(int(words[1]))
        return np.array(anum)
    # ------------- end helper functions ------------- #
    # open the file, if a string
    if isinstance(filename, str):
        ifs = open(filename, 'r')
    else:
        ifs = filename
    # extract the relevent lines
    start = r'Coordinates \(Angstroms\)'
    stop  = r'^\s*-{5,}'
    rre = RegexRangeExtractor(start, stop,
                              skip=2,
                              include_start=True,
                              include_stop=False)
    blocks = rre(ifs)
    # close file
    if ifs is not filename:
        ifs.close()
    # parse data
    #+ multiple values/file
    rval = [parse_data(b) for b in blocks]
    # check if each step should be returned
    if each_step:
        return rval
    else:
        a = rval[0]
        identical = [np.all(a == b) for b in rval]
        if np.all(identical):
            return a
        else:
            return rval
