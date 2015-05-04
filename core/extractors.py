from __future__ import print_function
import re
import sys

class Extractor(object):
    def __init__(self, *args, **kwds):
        """Base class for all extractors. Defines the extractor API."""
        pass

    def __call__(self, *args, **kwds):
        """
        Executes the extractor on an object.
        """
        raise NotImplementedError("The call function must be overloaded by " \
                                  "any classes that derive from Extractor.")

class RegexRangeExtractor(Extractor):
    def __init__(self, start, stop, *args, **kwds):
        """
        For each line in a file, reads starting where `re.match(start, line)`
        is true, then reads up to, but excluding where `re.match(stop, line)`
        is true (or the EOF is reached).

        Parameters
        ----------
        :start, {str|regex}: regular expression where to start reading
        :stop, {str|regex}: regular expression where to stop reading
        """
        super(RegexRangeExtractor, self).__init__(*args, **kwds)
        self.start = re.compile(start)
        self.stop = re.compile(stop)

    def __call__(self, ifs,
                 debug=False,
                 error=True,
                 include_start=True,
                 include_stop=False):
        """
        Finds those blocks bounded by the start/stop regex expressions
        that define this extractor.

        Parameters
        ----------
        :ifs, file-like object: stream from which matching blocks are to be
                extracted.

        Keywords
        --------
        :debug, bool: shall the start/stop matching lines be printed to the
                stderr? (Default: False)
        :error, bool: raise an IOError if the end-of-file is reached in the
                middle of a matching block, i.e. after start, but before stop.
                (Default: True)
        :include_start, bool: shall the line matching start be included?
                (Default: True)
        :include_stop, bool: shall the line matching stop be included?
                (Default: False)
        """
        inblock = False
        matches = []
        for line in ifs:
            # if not currently reading the block...
            if not inblock:
                # ... is this the start of the block?
                if re.search(self.start, line):
                    if debug:
                        print("start:", line, file=sys.stderr)
                    # include the first (start) line?
                    s = line if include_start else ''
                    inblock = True
            else:
                # check if we've reached the end
                if re.search(self.stop, line):
                    if debug:
                        print("stop:", line, file=sys.stderr)
                    # include the last (stop) line?
                    if include_stop:
                        s += line
                    matches.append(s)
                    inblock = False
                else:
                    s += line
        # was the EOF reached in the middle of a block?
        if inblock:
            matches.append(s)

        try:
            if inblock and error:
                raise IOError("The input ended in the middle of a data block.")
        finally:
            return matches
