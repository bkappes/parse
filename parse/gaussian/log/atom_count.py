from ...core.extractors import RegexExtractor

def get_atom_count(filename, each_step=False, aslist=True):
    """
    Extracts the number of atoms from the Gaussian log file.
    This is reported at each step. Generally, the number of
    atoms is the same; however rare, the number may change.

    If the number is constant, then a single value is returned.
    If not, or if each_step is True, then a list is returned.

    Keywords
    --------
    :each_step, bool: If True, a list of values is returned -- one
            per step. If False (default), then a single value is
            returned if the number of atoms remains constant through
            the calculation.
    :aslist, bool: If True, a list of values is returned, even if
            only one is found. If False and if only one value is
            found, then the value is returned. If more than one
            value is found, this keyword has no affect. (Default: True)

    Returns
    -------
    Number of atoms (list of int)
    """
    # --------------- helper functions --------------- #
    def parse_atom_count(line):
        """
        Converts the text string containing the number of atoms
        Expected format: "NAtoms=\s+\d NActive=..."
        """
        line = line.replace('=', ' ')
        words = line.strip().split()
        return int(words[1])
    # ------------- end helper functions ------------- #
    # open the file, if a string
    if isinstance(filename, str):
        ifs = open(filename, 'r')
    else:
        ifs = filename
    # extract the lines containing atom count
    regex = r'^\s*NAtoms='
    rre = RegexExtractor(regex)
    lines = rre(ifs)
    # close file
    if ifs is not filename:
        ifs.close()
    # get the number of atoms
    natoms = [parse_atom_count(l) for l in lines]
    if (not aslist) and (len(natoms) == 1):
        natoms = natoms[0]
    # should the atom count be reduced
    if not each_step:
        num = list(set(natoms))
        if (len(num) == 1):
            natoms = num[0]
    return natoms
