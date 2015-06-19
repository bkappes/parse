from ...core.extractors import RegexRangeExtractor
import numpy as np

def get_apt_charges(filename,
                    hydrogen_summed_into_heavy_atoms=False):
    """
    Get the per-atom Mulliken charges.

    Keywords
    --------
    :hydrogen_summed_into_heavy_atoms, bool: Hydrogen charges summed
            into heavy atoms.

    Returns
    -------
        (np.array(indices), np.array(chemical symbols), np.array(charges))
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
        lines = block.strip().split('\n')
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
        start = r'^\s*APT charges with hydrogens summed into heavy atoms:'
        stop  = r'^\s*Electronic spatial extent'
    else:
        start = r'^\s*APT charges:'
        stop  = r'^\s*Sum of APT charges'
    rre = RegexRangeExtractor(start, stop,
                              include_start=False,
                              include_stop=False)
    block = rre(ifs)[0]
    # close file
    if ifs is not filename:
        ifs.close()
    # parse data
    #+ single values/file
    rval = parse_data(block)
    return rval
