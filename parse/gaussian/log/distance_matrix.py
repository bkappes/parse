from ...core.extractors import RegexRangeExtractor
import numpy as np

def get_distance_matrix(filename, aslist=True):
    """
    Extracts the distance matrix/matrices from a Gaussian log file.

    Parameters
    ----------
    :filename, {str|file-like}: filename/filestream from which to
            extract the distance matrix/matrices.

    Keywords
    --------
    :aslist, bool: If True, a list of matrices is returned, even if
            only one is found. If False and if only one matrix is
            found, then the matrix is returned as an np.array object.
            If more than one matrix is found, this keyword has no
            affect. (Default: True)

    Returns
    -------
    tuple, (N x N distance matrix OR list of matrices, N element symbols).
    See `aslist` keyword.
    """
    # ---------- helper functions ----------- #
    def parse_matrix(matrix):
        """
        Converts a split lower-triangular matrix, as found in
        Gaussian 09 output, into a fully dense np.ndarray.

        Returns
        -------
        distance matrix as np.ndarray
        """
        def not_header(field):
            # At a minimum, data rows have fields
            #   (element index) (symbol) (distance_ii)
            if len(field) < 3:
                return False
            # (symbol) is a character/string
            try:
                _ = int(field[1])
            except ValueError:
                return True
            else:
                return False
        distances = []
        for line in matrix.strip().split('\n'):
            words = line.split()
            # get index information from row/column labels
            if not_header(words):
                # row index: 1 indexed --> 0 indexed
                row = int(words[0])-1
                # distances
                dist = map(float, words[2:])
            else:
                # col index: 1 indexed --> 0 indexed
                col = [int(w)-1 for w in words]
                continue
            # read values into lower triangular matrix
            if len(distances) <= row:
                distances.append(dist)
            else:
                distances[row].extend(dist)
        # populate matrix upper triangle
        N = len(distances)
        for i in xrange(N):
            m = len(distances[i])
            distances[i].extend((N-m)*[0.0])
        distances = np.array(distances)
        distances = distances + distances.transpose()
        return distances
    # --------- end helper functions --------- #

    # open the file, if a string
    if isinstance(filename, str):
        ifs = open(filename, 'r')
    else:
        ifs = filename
    # extract distance matrices
    start = r'^\s*Distance'
    stop = r'^\s*[a-zA-Z]'
    rre = RegexRangeExtractor(start, stop,
                              include_start=False,
                              include_stop=False)
    blocks = rre(ifs)
    # close file
    if ifs is not filename:
        ifs.close()
    # convert the matrices
    distances = [parse_matrix(b) for b in blocks]
    # return as list or single ndarray?
    if (not aslist) and (len(distances) == 1):
        distances = distances[0]
    return distances
