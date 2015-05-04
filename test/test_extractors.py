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
		rre = RegexRangeExtractor(r'^\s*Distance', r'^\s*[a-zA-Z]')
		with open('data/quinoxaline_cyano_cyano_hydro_hydro.log') as ifs:
			matches = rre(ifs, include_start=False, include_stop=True)
		assert len(matches) == 24
		for match in matches:
			line = match.strip().split('\n')
			assert not re.match(rre.start, line[0])
			assert re.match(rre.stop, line[-1])
		print("\n<RegexRangeExtractor>")
		print(matches[0])
		print("</RegexRangeExtractor>")

	def test_get_distance_matrix(self):
		distances, symbols = get_distance_matrix('data/quinoxaline_cyano_cyano_hydro_hydro.log')
		d00 = np.array([0.000000,
						1.430800,
						2.474993,
						2.827191,
						2.447828,
						1.422639,
						2.482018,
						3.714268,
						4.293332,
						3.782227,
						3.122386,
						4.977313,
						2.531515,
						3.594529,
						3.905870,
						3.430690,
						3.894210,
						4.553332,
						5.268593,
						4.665590,
						2.931260,
						3.454438,
						4.126936,
						5.098814,
						5.857746,
						5.274378,
						1.466500,
						2.626400])
		assert len(distances) == 24
		assert len(symbols) == 28
		assert np.allclose(distances[0][:,0], d00)
		assert all([np.allclose(d, d.transpose()) for d in distances])

	def tearDown(self):
		# clean up
		pass
