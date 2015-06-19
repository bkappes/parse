from ...core.extractors import RegexRangeExtractor

def get_dipole_moment(filename, aslist=True):
    """
    Returns the magnitude of the field-independent dipole moment.

    Keywords
    --------
    :aslist, bool: If True, a list of values is returned, even if
            only one is found. If False and if only one value is
            found, then the value is returned. If more than one
            value is found, this keyword has no affect. (Default: True)

    Returns
    -------
    Dipole moment (list of float, in Debye). See `aslist` keyword.
    """
    # --------------- helper functions --------------- #
    def parse_data(line):
        """
        Parse the line(s) to get the data.

        Expected format:

            'X= \d+ Y= \d+ Z= \d+ Tot= \d+'
        """
        words = line.strip().split('=')
        return float(words[-1])
    # ------------- end helper functions ------------- #
    # open the file, if a string
    if isinstance(filename, str):
        ifs = open(filename, 'r')
    else:
        ifs = filename
    # extract the relevent lines
    start = '^\s*Dipole moment'
    stop  = '.*'
    rre = RegexRangeExtractor(start, stop,
                              include_start=False,
                              include_stop=True)
    lines = rre(ifs)
    # close file
    if ifs is not filename:
        ifs.close()
    #+ multiple values/file
    rval = [parse_data(l) for l in lines]
    if (not aslist) and (len(rval) == 1):
       rval = rval[0]
    return rval
