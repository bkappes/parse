from ...core.extractors import RegexExtractor

def get_ZPE(filename):
    """
    Extracts the zero-point vibrational energy, in J/mol.
    """
    # --------------- helper functions --------------- #
    def parse_data(line):
        """
        Parse the line(s) to get the data.
        """
        words = line.strip().split()
        try:
            rval = float(words[3])
        except ValueError:
            raise ValueError('Improperly formatted ZPE line ' \
                             'in Gaussian09 output')
        return rval
    # ------------- end helper functions ------------- #
    # open the file, if a string
    if isinstance(filename, str):
        ifs = open(filename, 'r')
    else:
        ifs = filename
    # extract the relevent lines
    regex = r'^\s*Zero-point vibrational energy'
    rre = RegexExtractor(regex)
    line = rre(ifs)[0]
    # close file
    if ifs is not filename:
        ifs.close()
    # parse data
    #+ single value/file
    rval = parse_data(line)
    return rval
