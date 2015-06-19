from __future__ import print_function
from ...core.extractors import RegexExtractor
import numpy as np

def get_data(filename):
#def get_data(filename, aslist=True):
    """
    Description
    """
    # --------------- helper functions --------------- #
    def parse_data(line):
        """
        Parse the line(s) to get the data.
        """
        line = line.replace('=', ' ')
        words = line.strip().split()
        return int(words[1])
    # ------------- end helper functions ------------- #
    # open the file, if a string
    if isinstance(filename, str):
        ifs = open(filename, 'r')
    else:
        ifs = filename
    # extract the relevent lines
    regex = raise NotImplementedError()
    rre = RegexExtractor(regex)
    lines = rre(ifs)
    # close file
    if ifs is not filename():
        ifs.close()
    # parse data
    #+ single value/file
    #rval = parse_data(line)
    #+ multiple values/file
    #rval = [parse_data(l) for l in lines]
    #if (not aslist) and (len(rval) == 1):
    #   rval = rval[0]
    return rval
