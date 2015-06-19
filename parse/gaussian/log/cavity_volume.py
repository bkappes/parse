from ...core.extractors import RegexExtractor

def get_cavity_volume(filename, aslist=True):
    """
    Returns the GePol cavity volume.

    Keywords
    --------
    :aslist, bool: If True, a list of values is returned, even if
            only one is found. If False and if only one value is
            found, then the value is returned. If more than one
            value is found, this keyword has no affect. (Default: True)

    Returns
    -------
    Cavity volume (list of floats, Ang**3). See `aslist` keyword.
    """
    # --------------- helper functions --------------- #
    def parse_data(line):
        """
        Parse the line(s) to get the data.
        Expected format:

            'GePol: Cavity volume      = \d+ Ang**3'
        """
        label, value = line.strip().split('=')
        value, units = value.split()
        return float(value)
    # ------------- end helper functions ------------- #
    # open the file, if a string
    if isinstance(filename, str):
        ifs = open(filename, 'r')
    else:
        ifs = filename
    # extract the relevent lines
    regex = r'^\s*GePol: Cavity volume'
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
