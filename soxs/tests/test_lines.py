import tempfile
import shutil
import os
from soxs.events import write_spectrum
from soxs.instrument import instrument_simulator, \
    simulate_spectrum
from soxs.spatial import PointSourceModel
from soxs.simput import SimputCatalog
from soxs.spectra import Spectrum
from soxs.tests.utils import spectrum_answer_testing, \
    file_answer_testing
from numpy.random import RandomState

prng = RandomState(69)


def test_emission_line(answer_store):
    tmpdir = tempfile.mkdtemp()
    curdir = os.getcwd()
    os.chdir(tmpdir)

    const_flux = 1.0e-4
    line_pos = 5.0
    line_width = 0.02
    line_amp = 1.0e-5

    exp_time = (100.0, "ks")
    area = 30000.0
    inst_name = "mucal"

    spec = Spectrum.from_constant(const_flux, 1.0, 10.0, 20000)
    spec.add_emission_line(line_pos, line_width, line_amp)

    spectrum_answer_testing(spec, "emission_line_test.h5", answer_store)

    pt_src_pos = PointSourceModel(30.0, 45.0)
    sim_cat = SimputCatalog.from_models("emission_line", "emission_line", spec, 
                                        pt_src_pos, exp_time, area, prng=prng)
    sim_cat.write_catalog(overwrite=True)

    instrument_simulator("emission_line_simput.fits", "emission_line_evt.fits",
                         exp_time, inst_name, [30.0, 45.0], instr_bkgnd=False,
                         ptsrc_bkgnd=False, foreground=False, prng=prng)

    file_answer_testing("EVENTS", "emission_line_evt.fits", answer_store)

    write_spectrum("emission_line_evt.fits", "emission_line_evt.pha",
                   overwrite=True)

    file_answer_testing("EVENTS", "emission_line_evt.fits", answer_store)
    file_answer_testing("SPECTRUM", "emission_line_evt.pha", answer_store)

    os.chdir(curdir)
    shutil.rmtree(tmpdir)


def test_absorption_line(answer_store):
    tmpdir = tempfile.mkdtemp()
    curdir = os.getcwd()
    os.chdir(tmpdir)

    const_flux = 1.0e-3
    line_pos = 1.0
    line_width = 0.02
    line_amp = 1.0e-5

    exp_time = (100.0, "ks")
    inst_name = "lynx_gratings"

    spec = Spectrum.from_constant(const_flux, 0.1, 3.0, 100000)
    spec.add_absorption_line(line_pos, line_width, line_amp)

    spectrum_answer_testing(spec, "absorption_line_test.h5", answer_store)

    simulate_spectrum(spec, inst_name, exp_time, "absorption_line_evt.pha",
                      overwrite=True)

    file_answer_testing("SPECTRUM", "absorption_line_evt.pha", answer_store)

    os.chdir(curdir)
    shutil.rmtree(tmpdir)


if __name__ == "__main__":
    import sys
    answer_store = bool(sys.argv[1])
    test_emission_line(answer_store)
    test_absorption_line(answer_store)