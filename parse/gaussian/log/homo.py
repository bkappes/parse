from ...core.extractors import RegexRangeExtractor

def get_HOMO(filename, aslist=True):
#def get_data(filename, aslist=True):
    """
    Extracts the highest occupied molecular orbital (HOMO).

    Keywords
    --------
    :aslist, bool: If True, a list of values is returned, even if
            only one is found. If False and if only one value is
            found, then the value is returned. If more than one
            value is found, this keyword has no affect. (Default: True)

    Returns
    -------
    Highest occupied molecular orbital (list of floats).
    See `aslist` option.
    """
    # --------------- helper functions --------------- #
    def parse_HOMO(lines):
        """
        Parse the lines to get the data.
        """
        lines = lines.strip().split('\n')
        eigenvalues = []
        for line in lines:
            label, values = line.split('--')
            eigenvalues.extend([float(x) for x in values.split()])
        return eigenvalues[-1]
    # ------------- end helper functions ------------- #
    # open the file, if a string
    if isinstance(filename, str):
        ifs = open(filename, 'r')
    else:
        ifs = filename
    # extract the relevent lines
    start = r'^\s*Alpha\s+occ\.\s+eigenvalues'
    stop  = r'^\s*Alpha\s+virt\.\s+eigenvalues'
    rre = RegexRangeExtractor(start, stop,
                              include_start=True,
                              include_stop=False)
    blocks = rre(ifs)
    # close file
    if ifs is not filename:
        ifs.close()
    #+ multiple values/file
    rval = [parse_HOMO(b) for b in blocks]
    if (not aslist) and (len(rval) == 1):
       rval = rval[0]
    return rval
