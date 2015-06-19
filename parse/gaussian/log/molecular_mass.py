from ...core.extractors import RegexExtractor

def get_molecular_mass(filename):
    """
    Extracts the dipoles (output for each step)
    from a Gaussian log file.

    Returns
    -------
    molecular mass (float, amu)
    """
    # --------------- helper functions --------------- #
    def parse_molecular_mass(line):
        """
        Converts the text string containing the molecular mass.
        """
        words = line.strip().split()
        return float(words[2])
    # ------------- end helper functions ------------- #

    # open the file, if a string
    if isinstance(filename, str):
        ifs = open(filename, 'r')
    else:
        ifs = filename
    # extract the polarizability
    regex = r'^\s*Molecular mass:'
    rre = RegexExtractor(regex)
    lines = rre(ifs)
    # close file
    if ifs is not filename:
        ifs.close()
    # convert the molecular mass
    mmol = parse_molecular_mass(lines[0])
    return mmol
