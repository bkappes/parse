from ...core.extractors import RegexExtractor

def get_isotropic_polarizability(filename):
#def get_data(filename, aslist=True):
    """
    Returns the isotropic polarizability for W = 0.0000, in Bohr**3.
    """
    # --------------- helper functions --------------- #
    def parse_data(line):
        """
        Parse the line(s) to get the data.
        """
        label, values = line.split('=')
        W, alpha, units = values.strip().split()
        return float(alpha)
    # ------------- end helper functions ------------- #
    # open the file, if a string
    if isinstance(filename, str):
        ifs = open(filename, 'r')
    else:
        ifs = filename
    # extract the relevent lines
    regex = r'^\s*Isotropic polarizability for W='
    rre = RegexExtractor(regex)
    line = rre(ifs)[0]
    # close file
    if ifs is not filename:
        ifs.close()
    # parse data
    #+ single value/file
    rval = parse_data(line)
    return rval
