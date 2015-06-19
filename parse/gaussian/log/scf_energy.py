from ...core.extractors import RegexExtractor

def get_scf_energy(filename, aslist=True):
    """
    Get the self-consistant field (SCF) energy for each step, in kcal/mol.

    Keywords
    --------
    :aslist, bool: If True, a list of values is returned, even if
            only one is found. If False and if only one value is
            found, then the value is returned. If more than one
            value is found, this keyword has no affect. (Default: True)

    Returns
    -------
    SCF energies (list of floats). See `aslist` keyword.
    """
    # --------------- helper functions --------------- #
    def parse_data(line):
        """
        Parse the line(s) to get the data.
        """
        label, values = line.split('=')
        words = values.strip().split()
        try:
            rval = float(words[0])
        except ValueError:
            raise ValueError('The format of {} is not valid for ' \
                             'extracting the SCF energy.'.format(line))
        return rval
    # ------------- end helper functions ------------- #
    # open the file, if a string
    if isinstance(filename, str):
        ifs = open(filename, 'r')
    else:
        ifs = filename
    # extract the relevent lines
    regex = r'^\s*SCF Done:'
    rre = RegexExtractor(regex)
    lines = rre(ifs)
    # close file
    if ifs is not filename:
        ifs.close()
    # parse data
    #+ multiple values/file
    rval = [parse_data(l) for l in lines]
    if (not aslist) and (len(rval) == 1):
       rval = rval[0]
    return rval
