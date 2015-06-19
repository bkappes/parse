from ...core.extractors import RegexExtractor

def get_SMD_CDS_energy(filename, aslist=True):
    """
    Extracts the SMD-CDS (non-electrostatic) energy from the
    Gaussian log file.

    Returns
    -------
    SMD-CDS non-electrostatic energy (list of floats, kcal/mol).
    See `aslist` option.
    """
    # --------------- helper functions --------------- #
    def parse_SMD_CDS_energy(line):
        """
        Converts the text string containing the SMD-CDS energy
        Expected format:
            'SMD-CDS (non-electrostatic) energy   (kcal/mol) =     %f'
        """
        words = line.strip().split()
        return float(words[-1])
    # ------------- end helper functions ------------- #
    # open the file, if a string
    if isinstance(filename, str):
        ifs = open(filename, 'r')
    else:
        ifs = filename
    # extract the polarizability
    regex = r'^\s*SMD-CDS \(non-electrostatic\) energy'
    rre = RegexExtractor(regex)
    lines = rre(ifs)
    # close file
    if ifs is not filename:
        ifs.close()
    # get the number of atoms
    energy = [parse_SMD_CDS_energy(l) for l in lines]
    if (not aslist) and (len(energy) == 1):
        energy = energy[0]
    return energy
