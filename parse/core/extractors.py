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

        Keywords
        --------
        :include_start, bool: shall the line matching start be included?
                (Default: True)
        :include_stop, bool: shall the line matching stop be included?
                (Default: False)
        :reverse_start, bool: reverses the truth match of the start.
        :reverse_stop, bool: reverses the truth match of the stop.
        :skip, int: Include *after* lines after matching start without
                attempting to match stop. This allows matching to a
                characteristic pattern that precedes the desired information.
                (Default: 0)
        """
        super(RegexRangeExtractor, self).__init__(*args, **kwds)
        self.start = re.compile(start)
        self.stop = re.compile(stop)
        # include the start and end points?
        if 'include_start' in kwds:
            self.include_start = bool(kwds['include_start'])
        else:
            self.include_start = False
        if 'include_stop' in kwds:
            self.include_stop = bool(kwds['include_stop'])
        else:
            self.include_stop = False
        # reverse the match of the start/stop expression
        if 'reverse_start' in kwds:
            self.reverse_start = bool(kwds['reverse_start'])
        else:
            self.reverse_start = False
        if 'reverse_stop' in kwds:
            self.reverse_stop = bool(kwds['reverse_stop'])
        else:
            self.reverse_stop = False
        # should lines after the matching start be skipped, i.e.
        # untreated?
        if 'skip' in kwds:
            self.skip = int(kwds['skip'])
        else:
            self.skip = 0

    def __call__(self, ifs,
                 debug=False,
                 error=True,
                 **kwds):
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
        """
        skip = self.skip
        include_start = self.include_start
        include_stop = self.include_stop
        inblock = False
        matches = []
        for line in ifs:
            # if not currently reading the block...
            if not inblock:
                # ... is this the start of the block?
                is_start = bool(re.search(self.start, line))
                is_start = (not is_start) if self.reverse_start else is_start
                if is_start:
                    if debug:
                        print("start:", line, file=sys.stderr)
                    # include the first (start) line?
                    s = line if include_start else ''
                    inblock = True
            else:
                # include skipped lines after initial match
                if skip > 0:
                    s += line
                    skip -= 1
                    continue
                # check if we've reached the end
                is_stop = bool(re.search(self.stop, line))
                is_stop = (not is_stop) if self.reverse_stop else is_stop
                if is_stop:
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


class RegexExtractor(RegexRangeExtractor):
    def __init__(self, regex, *args, **kwds):
        """
        For each line in a file, reads every line where `re.match(start, line)`
        is true.

        Parameters
        ----------
        :regex, {str|regex}: regular expression describing lines that match.
        """
        super(RegexExtractor, self).__init__(start=regex,
                                             stop=r'.*',
                                             include_start=True,
                                             include_stop=False)

    def __call__(self, ifs, **kwds):
        """
        Finds those lines that match the regex expression that define this
        extractor.

        Parameters
        ----------
        :ifs, file-like object: stream from which matching blocks are to be
                extracted.

        Keywords
        --------
        :debug, bool: shall the matching lines be printed to the
                stderr? (Default: False)
        :error, bool: raise an IOError if the end-of-file is reached in the
                middle of a matching block, i.e. after start, but before stop.
                (Default: True)
        """
        kwds['error'] = False
        return super(RegexExtractor, self).__call__(ifs, **kwds)
