from soxs.spatial import PointSourceModel, BetaModel
from soxs.spectra import ApecGenerator
import os
import shutil
import tempfile
import astropy.io.fits as pyfits
from soxs.tests.utils import bin_profile
from soxs.simput import write_photon_list
from soxs.instrument import instrument_simulator
from numpy.random import RandomState

kT = 6.0
Z = 0.3
redshift = 0.03
norm = 1.0e-3
nH = 0.04
exp_time = 5.0e4
area = 30000.0

prng = RandomState(25)

agen = ApecGenerator(0.05, 12.0, 10000, broadening=True)
spec = agen.get_spectrum(kT, Z, redshift, norm)
spec.apply_foreground_absorption(nH)

def test_point_source():
    tmpdir = tempfile.mkdtemp()
    curdir = os.getcwd()
    os.chdir(tmpdir)

    e = spec.generate_energies(exp_time, area, prng=prng)

    pt_src = PointSourceModel(30.0, 45.0, e.size)

    write_photon_list("pt_src", "pt_src", e.flux, pt_src.ra, pt_src.dec,
                      e, clobber=True)

    instrument_simulator("pt_src_simput.fits", "pt_src_evt.fits", exp_time,
                         "hdxi", [30.0, 45.0], astro_bkgnd=False,
                         instr_bkgnd=False, prng=prng)

    f = pyfits.open("pt_src_evt.fits")
    x = f["EVENTS"].data["X"]
    y = f["EVENTS"].data["Y"]
    f.close()

    os.chdir(curdir)
    shutil.rmtree(tmpdir)

def test_beta_model():
    tmpdir = tempfile.mkdtemp()
    curdir = os.getcwd()
    os.chdir(tmpdir)

    e = spec.generate_energies(exp_time, area, prng=prng)

    beta_src = BetaModel(30.0, 45.0, 20.0, 2./3., e.size, prng=prng)

    write_photon_list("beta", "beta", e.flux, beta_src.ra, beta_src.dec,
                      e, clobber=True)

    instrument_simulator("beta_simput.fits", "beta_evt.fits", exp_time,
                         "hdxi", [30.0, 45.0], astro_bkgnd=False,
                         instr_bkgnd=False, prng=prng)

    f = pyfits.open("beta_evt.fits")
    x = f["EVENTS"].data["X"]
    y = f["EVENTS"].data["Y"]
    x0 = f["EVENTS"].header["TCRPX2"]
    y0 = f["EVENTS"].header["TCRPX3"]
    f.close()

    S, rbin = bin_profile(x, y, x0, y0, 0.0, 200.0, 200)

    os.chdir(curdir)
    shutil.rmtree(tmpdir)

if __name__ == "__main__":
    test_beta_model()