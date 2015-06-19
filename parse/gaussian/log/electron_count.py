from ...core.extractors import RegexExtractor

def get_electron_count(filename, each_step=False):
    """
    Extracts the number of electrons from the Gaussian log
    file.

    Every SCF step reports these values, so there is the
    potential for the electron count to change in the course of the
    calculation; however, this is highly atypical. To better
    serve the typical case, when the electron count remains
    constant through the duration of the calculation, only
    unique values are returned, and as will most often be the
    case, if the number of electrons is constant, then a scalar
    is returned.

    Example:

    ```
    try:
        nelec = get_electron_count('gaussian.log')
        _ = nelec[0]
    except TypeError: # nelec is a scalar
        pass
    else: # code if electron count changes
        nelec = get_electron_count('gaussian.log', each_step=True)
    ```

    Keywords
    --------
    :each_step, bool: report all electron counts, as a list of
            (alpha, beta) tuples. Default: False

    Returns
    -------
    Number of electrons (int). (See above for exceptional cases.)
    """
    # --------------- helper functions --------------- #
    def parse_data(line):
        """
        Parse the line(s) to get the data.
        """
        words = line.strip().split()
        try:
            alpha, beta = int(words[0]), int(words[3])
        except ValueError:
            raise ValueError('Cannot extract the electron count ' \
                             'from "{}"'.format(line))
        return (alpha, beta)
    # ------------- end helper functions ------------- #
    # open the file, if a string
    if isinstance(filename, str):
        ifs = open(filename, 'r')
    else:
        ifs = filename
    # extract the relevent lines
    regex = r'alpha electrons'
    rre = RegexExtractor(regex)
    lines = rre(ifs)
    # close file
    if ifs is not filename:
        ifs.close()
    # parse data
    #+ multiple values/file
    rval = [parse_data(l) for l in lines]
    # typically, this value should be a single int
    if not each_step:
        rval = tuple(set([a+b for a,b in rval]))
        if len(rval) == 1:
            rval = rval[0]
    return rval
