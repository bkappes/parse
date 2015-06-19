from ...core.extractors import RegexRangeExtractor
import numpy as np
import re

def get_spectroscopic_data(filename):
    """
    Extract the spectroscopic data.

    Returns
    -------
    {
        'frequencies' : harmonic frequencies (cm**-1),
        'red. masses' : reduced masses (amu),
        'Frc' : force constants (mDyne/Ang),
        'IR' : IR intensity (KM/mol)
    }
    """
    # --------------- helper functions --------------- #
    def parse_data(block):
        """
        Parse the line(s) to get the data.
        """
        rval = {
            'Frequencies' : [],
            'Red. Masses' : [],
            'Frc consts' : [],
            'IR Inten' : []
        }
        for line in block.splitlines():
            if re.match(r'^\s*Frequencies', line):
                key = 'Frequencies'
            elif re.match(r'^\s*Red\. masses', line):
                key = 'Red. Masses'
            elif re.match(r'^\s*Frc consts', line):
                key = 'Frc consts'
            elif re.match(r'^\s*IR Inten', line):
                key = 'IR Inten'
            else:
                key = None
            if key:
                label, values = line.split('--')
                values = [float(x) for x in values.strip().split()]
                rval[key].extend(values)
        return rval
    # ------------- end helper functions ------------- #
    # open the file, if a string
    if isinstance(filename, str):
        ifs = open(filename, 'r')
    else:
        ifs = filename
    # extract the relevent lines
    start = r'^\s*Frequencies'
    stop  = r'^\s*IR Inten'
    rre = RegexRangeExtractor(start, stop,
                              include_start=True,
                              include_stop=True)
    blocks = rre(ifs)
    # close file
    if ifs is not filename:
        ifs.close()
    # parse data
    #+ single value/file, but split across multiple blocks
    rval = None
    for block in blocks:
        subset = parse_data(block)
        if not rval:
            rval = subset
        else:
            for k in rval:
                rval[k].extend(subset[k])
    # transform these into values into ndarrays
    for k in rval:
        rval[k] = np.array(rval[k])
    return rval
