from ...core.extractors import RegexRangeExtractor
import re

def get_polarizability(filename):
    """
    Extracts the polarizability from a Gaussian log file.
    This is stored (in the G09 log file) as the six elements
    in a lower-triangular polarizability matrix:

        a_{xx}, a_{xy}, a_{yy}, a_{xz}, a_{yz}, a_{zz}

    Returns
    -------
    :polarizability, tuple: (axx, axy, ayy, axz, ayz, azz)
    """
    # --------------- helper functions --------------- #
    def parse_polarizability(lines):
        """
        Converts the text string (lines) from Gaussian
        to the polarizability values.
        """
        # Expected format:
        # "Polarizability= % 10.8D+2%10.8D+2%10.8D+2\n"
        # "                % 10.8D+2%10.8D+2%10.8D+2\n"
        lines = lines.splitlines()
        # drop "Polarizability="
        lines[0] = lines[0].split('=')[1]
        alpha = []
        for line in lines:
            # the Gaussian file is not careful to separate
            # the numbers, so we must assume that the number
            # format is fixed.
            num = re.split('([^D]+D\+..)', line)
            # cast these as floats -- must first replace
            # D with E.
            num = [float(v.replace('D', 'E')) \
                   for v in num if v]
            alpha.extend(num)
        return tuple(alpha)
    # ------------- end helper functions ------------- #

    # open the file, if a string
    if isinstance(filename, str):
        ifs = open(filename, 'r')
    else:
        ifs = filename
    # extract the polarizability
    start = r'^\s*Polarizability='
    end   = r'.*'
    rre = RegexRangeExtractor(start, end,
                              include_start=True,
                              include_stop=True)
    lines = rre(ifs)[0]
    # close file
    if ifs is not filename:
        ifs.close()
    # convert the polarizability
    alpha = parse_polarizability(lines)
    return alpha
