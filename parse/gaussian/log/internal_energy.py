from ...core.extractors import RegexRangeExtractor
import re

def get_internal_energy(filename):
    """
    Extracts the internal energy, in kcal/mol.

    Returns
    -------
    {
        'Total' : float,
        'Electronic' : float,
        'Translational' : float,
        'Rotational' : float,
        'Vibrational' : float
    }
    """
    # --------------- helper functions --------------- #
    def parse_data(block):
        """
        Parse the line(s) to get the data.
        """
        rval = {
            'Total' : None,
            'Electronic' : None,
            'Translational' : None,
            'Rotational' : None,
            'Vibrational' : None
        }
        for line in block.splitlines():
            if re.match(r'^\s*Total', line):
                key = 'Total'
            elif re.match(r'^\s*Electronic', line):
                key = 'Electronic'
            elif re.match(r'^\s*Translational', line):
                key = 'Translational'
            elif re.match(r'^\s*Rotational', line):
                key = 'Rotational'
            elif re.match(r'^\s*Vibrational', line):
                key = 'Vibrational'
            else:
                key = None
            if key:
                words = line.strip().split()
                try:
                    rval[key] = float(words[1])
                except ValueError:
                    raise ValueError('Invalid thermodynamic format.')
        return rval
    # ------------- end helper functions ------------- #
    # open the file, if a string
    if isinstance(filename, str):
        ifs = open(filename, 'r')
    else:
        ifs = filename
    # extract the relevent lines
    start = r'^\s*E\s+\(Thermal\)'
    stop  = r'^\s*Vibrational'
    rre = RegexRangeExtractor(start, stop,
                              include_start=True,
                              include_stop=True)
    block = rre(ifs)[0]
    # close file
    if ifs is not filename:
        ifs.close()
    # parse data
    #+ single value/file
    rval = parse_data(block)
    return rval
