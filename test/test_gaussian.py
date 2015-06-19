from __future__ import print_function
import sys
sys.path.append('..')
from StringIO import StringIO
import numpy as np
# log
from parse.gaussian import get_apt_charges
from parse.gaussian import get_atom_count
from parse.gaussian import get_atom_positions
from parse.gaussian import get_cavity_surface_area
from parse.gaussian import get_cavity_volume
from parse.gaussian import get_dipole
from parse.gaussian import get_dipole_moment
from parse.gaussian import get_distance_matrix
from parse.gaussian import get_electron_count
from parse.gaussian import get_electronic_spatial_extent
from parse.gaussian import get_entropy
from parse.gaussian import get_heat_capacity
from parse.gaussian import get_HOMO
from parse.gaussian import get_internal_energy
from parse.gaussian import get_isotropic_polarizability
from parse.gaussian import get_LUMO
from parse.gaussian import get_molecular_mass
from parse.gaussian import get_mulliken_charges
from parse.gaussian import get_pcm_nonelectrostatic_energy
from parse.gaussian import get_polarizability
from parse.gaussian import get_rotational_constants
from parse.gaussian import get_scf_energy
from parse.gaussian import get_SMD_CDS_energy
from parse.gaussian import get_spectroscopic_data
from parse.gaussian import get_ZPE

# parse the thermodynamic table
def parse_thermo(filename):
    table = np.loadtxt(filename, dtype=str)
    keys = ('Total',
            'Electronic',
            'Translational',
            'Rotational',
            'Vibrational')
    thermo = { 'E'  : dict(zip(keys, [float(v) for v in table[2:, 1]])),
               'CV' : dict(zip(keys, [float(v) for v in table[2:, 2]])),
               'S'  : dict(zip(keys, [float(v) for v in table[2:, 3]])) }
    return thermo

# To test, simply run
# [...]$ nosetests (optionally with -v)
# and a report a summary of the results

class TestClass: # keep this the same
    sfs = None

    def setUp(self):
        if not TestClass.sfs:
            # to avoid reading the file many times, create
            # a StringIO object to hold the file
            filename = 'data/quinoxaline_cyano_cyano_hydro_hydro_solv+0.log'
            with open(filename, 'r') as ifs:
                s = ifs.read()
            TestClass.sfs = StringIO(s)
        else:
            TestClass.sfs.seek(0)

    def test_get_apt_charges(self):
        print('Testing APT charges')
        values = get_apt_charges(TestClass.sfs)
        indices, symbols, charges = np.loadtxt('data/apt-charges.txt',
                                               dtype=str,
                                               unpack=True)
        indices = indices.astype(int)
        charges = charges.astype(float)
        assert(np.all(values[0] == indices))
        assert(np.all(values[1] == symbols))
        assert(np.allclose(values[2], charges))

    def test_get_apt_charges_with_hydrogen_summed_into_heavy_atoms(self):
        values = get_apt_charges(TestClass.sfs, hydrogen_summed_into_heavy_atoms=True)
        indices, symbols, charges = np.loadtxt('data/apt-charges-w-hydrogen.txt',
                                               dtype=str,
                                               unpack=True)
        indices = indices.astype(int)
        charges = charges.astype(float)
        assert(np.all(values[0] == indices))
        assert(np.all(values[1] == symbols))
        assert(np.allclose(values[2], charges))

    def test_get_atom_count(self):
        values = get_atom_count(TestClass.sfs)
        try:
            assert(values == 28)
        except:
            print(sys.stderr, "{} != {}".format(values, 28))

    def test_get_atom_positions(self):
        values = get_atom_positions(TestClass.sfs)
        indices, anum, zero, x, y, z = np.loadtxt('data/atom_coordinates.txt',
                                                  dtype=str,
                                                  unpack=True)
        indices = indices.astype(int)
        anum = anum.astype(int)
        zero = zero.astype(int)
        x = x.astype(float)
        y = y.astype(float)
        z = z.astype(float)
        m = np.transpose([x, y, z])
        assert(np.allclose(values[0], m))

    def test_get_cavity_surface_area(self):
        values = get_cavity_surface_area(TestClass.sfs)
        area = np.loadtxt('data/cavity-surface-area.txt')
        assert(np.allclose(values, area))

    def test_get_cavity_volume(self):
        values = get_cavity_volume(TestClass.sfs)
        volume = np.loadtxt('data/cavity-volume.txt')
        assert(np.allclose(values, volume))

    def test_get_dipole(self):
        values = get_dipole(TestClass.sfs)
        dipole = np.loadtxt('data/dipole.txt')
        assert(np.allclose(values, dipole))

    def test_get_dipole_moment(self):
        values = get_dipole_moment(TestClass.sfs)
        moment = np.loadtxt('data/dipole-moment.txt')
        assert(np.allclose(values, moment))

    def test_get_distance_matrix(self):
        values = get_distance_matrix(TestClass.sfs)
        matrix = np.loadtxt('data/distance-matrix.txt')
        try:
            assert(np.allclose(values[0], matrix))
        except:
            print(values[0][:5, :5], matrix[:5, :5])
            raise

    def test_get_electron_count(self):
        values = get_electron_count(TestClass.sfs)
        assert(values == 112)

    def test_get_electronic_spatial_extent(self):
        values = get_electronic_spatial_extent(TestClass.sfs)
        ese = np.loadtxt('data/electronic-spatial-extent.txt')
        assert(np.allclose(values, ese))

    def test_get_entropy(self):
        values = get_entropy(TestClass.sfs)
        thermo = parse_thermo('data/thermodynamics.txt')
        vkeys = values.keys()
        tkeys = thermo['S'].keys()
        try:
            assert(all([v in tkeys for v in vkeys]))
        except:
            print("values: {}".format(vkeys))
            print("thermo: {}".format(tkeys))
            raise
        try:
            assert(np.allclose(thermo['S'].values(), values.values()))
        except:
            print("A/B = {}/{}".format(thermo['S'], values))
            raise

    def test_get_heat_capacity(self):
        values = get_heat_capacity(TestClass.sfs)
        thermo = parse_thermo('data/thermodynamics.txt')
        vkeys = values.keys()
        tkeys = thermo['CV'].keys()
        assert(all([v in tkeys for v in vkeys]))
        try:
            assert(np.allclose(thermo['CV'].values(), values.values()))
        except:
            print("A/B = {}/{}".format(thermo['CV'], values))
            raise

    def test_get_HOMO(self):
        values = get_HOMO(TestClass.sfs)
        homo = np.loadtxt('data/homo.txt')
        assert(np.allclose(values, homo))

    def test_get_internal_energy(self):
        values = get_internal_energy(TestClass.sfs)
        thermo = parse_thermo('data/thermodynamics.txt')
        vkeys = values.keys()
        tkeys = thermo['E'].keys()
        assert(all([v in tkeys for v in vkeys]))
        assert(np.allclose(thermo['E'].values(), values.values()))

    def test_get_isotropic_polarizability(self):
        values = get_isotropic_polarizability(TestClass.sfs)
        assert(np.allclose(values, 266.10))

    def test_get_LUMO(self):
        values = get_LUMO(TestClass.sfs)
        lumo = np.loadtxt('data/lumo.txt')
        assert(np.allclose(values, lumo))

    def test_get_molecular_mass(self):
        values = get_molecular_mass(TestClass.sfs)
        assert(np.allclose(values, 212.10620))

    def test_get_mulliken_charges(self):
        values = get_mulliken_charges(TestClass.sfs)
        values = values[0]
        indices, symbols, charges = np.loadtxt('data/mulliken-charges.txt',
                                               dtype=str,
                                               unpack=True)
        indices = indices.astype(int)
        charges = charges.astype(float)
        assert(np.all(values[0] == indices))
        assert(np.all(values[1] == symbols))
        assert(np.allclose(values[2], charges))

    def test_get_mulliken_charges_with_hydrogen_summed_into_heavy_atoms(self):
        values = get_mulliken_charges(TestClass.sfs,
                                      hydrogen_summed_into_heavy_atoms=True)
        values = values[0]
        indices, symbols, charges = np.loadtxt('data/mulliken-charges-w-hydrogen.txt',
                                               dtype=str,
                                               unpack=True)
        indices = indices.astype(int)
        charges = charges.astype(float)
        assert(np.all(values[0] == indices))
        assert(np.all(values[1] == symbols))
        assert(np.allclose(values[2], charges))

    def test_get_pcm_nonelectrostatic_energy(self):
        values = get_pcm_nonelectrostatic_energy(TestClass.sfs)
        pcm = np.loadtxt('data/pcm-nonelectrostatic-energy.txt')
        assert(np.allclose(values, pcm))

    def test_get_polarizability(self):
        values = get_polarizability(TestClass.sfs)
        alpha = np.loadtxt('data/polarizability.txt')
        assert(np.allclose(values, alpha))

    def test_get_rotational_constants(self):
        values = get_rotational_constants(TestClass.sfs)
        rotate = np.loadtxt('data/rotational-constants.txt')
        assert(np.allclose(values, rotate))

    def test_get_scf_energy(self):
        values = get_scf_energy(TestClass.sfs)
        scf = np.loadtxt('data/scf-energy.txt')
        assert(np.allclose(values, scf))

    def test_get_SMD_CDS_energy(self):
        values = get_SMD_CDS_energy(TestClass.sfs)
        smd = np.loadtxt('data/smd-cds-energy.txt')
        assert(np.allclose(values, smd))

    def test_get_spectroscopic_data(self):
        values = get_spectroscopic_data(TestClass.sfs)
        freq = np.loadtxt('data/frequencies.txt')
        mred = np.loadtxt('data/red-masses.txt')
        Frc  = np.loadtxt('data/Frc-consts.txt')
        IR   = np.loadtxt('data/IR-inten.txt')
        try:
            assert(np.allclose(values['Frequencies'], freq))
            assert(np.allclose(values['Red. Masses'], mred))
            assert(np.allclose(values['Frc consts'], Frc))
            assert(np.allclose(values['IR Inten'], IR))
        except:
            print("Frequences: {}/{}".format(values['Frequencies'],
                                             freq))
            print("Red. Masses: {}/{}".format(values['Red. Masses'],
                                             mred))
            print("Frc consts: {}/{}".format(values['Frc consts'],
                                             Frc))
            print("IR Inten: {}/{}".format(values['IR Inten'],
                                             IR))
            raise

    def test_get_ZPE(self):
        values = get_ZPE(TestClass.sfs)
        assert(np.allclose(values, 587487.4))

    def tearDown(self):
        pass
#class TestClass: # keep this the same
