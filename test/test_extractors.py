from __future__ import print_function
import sys
sys.path.append('..')
from parse.core.extractors import RegexRangeExtractor
from parse.gaussian.log import get_distance_matrix
import numpy as np
import re

# To test, simply run
# [...]$ nosetests (optionally with -v)
# and a report a summary of the results

class TestClass: # keep this the same
	def setUp(self):
		# construct objects and perform any necessary setup
		pass

	def test_RegexRangeExtractorDefault(self):
		# run test one
		rre = RegexRangeExtractor(r'^\s*Distance', r'^\s*[a-zA-Z]')
		with open('data/quinoxaline_cyano_cyano_hydro_hydro.log') as ifs:
			matches = rre(ifs)
		assert len(matches) == 24
		print("\n<RegexRangeExtractor>")
		print(matches[0])
		print("</RegexRangeExtractor>")

	def test_RegexRangeExtractor(self):
		rre = RegexRangeExtractor(r'^\s*Distance', r'^\s*[a-zA-Z]',
								  include_start=False,
								  include_stop=True)
		with open('data/quinoxaline_cyano_cyano_hydro_hydro.log') as ifs:
			matches = rre(ifs)
		assert len(matches) == 24
		for match in matches:
			line = match.strip().split('\n')
			assert not re.match(rre.start, line[0])
			assert re.match(rre.stop, line[-1])
		print("\n<RegexRangeExtractor>")
		print(matches[0])
		print("</RegexRangeExtractor>")

	def tearDown(self):
		# clean up
		pass
