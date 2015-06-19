from ...core.extractors import RegexRangeExtractor
import numpy as np

def get_mulliken_charges(filename,
                         hydrogen_summed_into_heavy_atoms=False,
                         aslist=True):
    """
    Get the per-atom Mulliken charges.

    Keywords
    --------
    :hydrogen_summed_into_heavy_atoms, bool: Hydrogen charges summed
            into heavy atoms.
    :aslist, bool: If True, a list of arrays is returned, even if
            only one is found. If False and if only one array is
            found, then the array is returned. If more than one
            value is found, this keyword has no affect. (Default: True)

    Returns
    -------
    tuple, or list of tuples, e.g.
        (np.array(indices), np.array(chemical symbols), np.array(charges))
    See `aslist` keyword.
    """
    # --------------- helper functions --------------- #
    def parse_data(block):
        """
        Parse the line(s) to get the data.
        Expected format:

            '       1
             1 sym  \d+
             2 sym  \d+
             ...
             N sym  \d+'
        """
        lines = block.strip().splitlines()
        indices = []
        symbols = []
        charges = []
        for line in lines[1:]:
            words = line.split()
            indices.append(int(words[0]))
            symbols.append(words[1])
            charges.append(float(words[2]))
        return (np.array(indices), np.array(symbols), np.array(charges))
    # ------------- end helper functions ------------- #
    # open the file, if a string
    if isinstance(filename, str):
        ifs = open(filename, 'r')
    else:
        ifs = filename
    # extract the relevent lines
    if hydrogen_summed_into_heavy_atoms:
        start = r'^\s*Mulliken charges with hydrogens summed into heavy atoms:'
        stop  = r'^\s*(Electronic spatial extent)|(APT charges:)'
    else:
        start = r'^\s*Mulliken charges:'
        stop  = r'^\s*Sum of Mulliken charges'
    rre = RegexRangeExtractor(start, stop,
                              include_start=False,
                              include_stop=False)
    blocks = rre(ifs)
    # close file
    if ifs is not filename:
        ifs.close()
    # parse data
    #+ multiple values/file
    rval = [parse_data(b) for b in blocks]
    if (not aslist) and (len(rval) == 1):
       rval = rval[0]
    return rval
