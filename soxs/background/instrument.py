import os
from soxs.utils import soxs_files_path, mylog
from soxs.background.spectra import BackgroundSpectrum
import numpy as np

# ACIS-I particle background
acisi_bkgnd_file = os.path.join(soxs_files_path, "acisi_particle_bkgnd.dat")
acisi_particle_bkgnd = BackgroundSpectrum(acisi_bkgnd_file, "instrumental")

# Athena-like microcalorimeter background (http://adsabs.harvard.edu/abs/2014A%26A...569A..54L)
mucal_bkgnd_file = os.path.join(soxs_files_path, "mucal_particle_bkgnd.dat")
mucal_particle_bkgnd = BackgroundSpectrum(mucal_bkgnd_file, "instrumental")

# Athena microcalorimeter background (http://adsabs.harvard.edu/abs/2014A%26A...569A..54L)
xifu_bkgnd_file = os.path.join(soxs_files_path, "xifu_bkgnd.dat")
athena_xifu_bkgnd = BackgroundSpectrum(xifu_bkgnd_file, "instrumental")

# Athena imager background 
wfi_bkgnd_file = os.path.join(soxs_files_path, "wfi_bkgnd.dat")
athena_wfi_bkgnd = BackgroundSpectrum(wfi_bkgnd_file, "instrumental")

instrument_backgrounds = {"acisi": acisi_particle_bkgnd,
                          "mucal": mucal_particle_bkgnd,
                          "athena_xifu": athena_xifu_bkgnd,
                          "athena_wfi": athena_wfi_bkgnd}

def add_instrument_background(name, filename):
    """
    Add a particle/instrument background to the list of known
    backgrounds.

    Parameters
    ----------
    name : string
        The short name of the background, which will be the key in the 
        registry.
    filename : string
        The file containing the background. It must have two columns: 
        energy in keV, and background intensity in units of
        photons/s/cm**2/arcmin**2/keV.
    bkgnd_type : string
        The type of background, either "instrumental" or "astrophysical".
    """
    instrument_backgrounds[name] = BackgroundSpectrum(filename, "instrumental")

default_f = {"acisi": 10.0,
             "mucal": 10.0,
             "athena_wfi": 12.0,
             "athena_xifu": 12.0}

def make_instrument_background(bkgnd_name, event_params, focal_length, rmf, 
                               prng=np.random):

    fov = event_params["fov"]

    bkgnd_spec = instrument_backgrounds[bkgnd_name]

    # Generate background events

    bkg_events = {}

    area = (focal_length/default_f[bkgnd_name])**2
    bkg_events["energy"] = bkgnd_spec.generate_energies(event_params["exposure_time"],
                                                        area, fov, prng=prng).value

    n_events = bkg_events["energy"].size

    bkg_events['chipx'] = np.round(prng.uniform(low=1.0, high=event_params['num_pixels'],
                                                size=n_events))
    bkg_events['chipy'] = np.round(prng.uniform(low=1.0, high=event_params['num_pixels'],
                                                size=n_events))
    bkg_events["detx"] = np.round(bkg_events["chipx"] - event_params['pix_center'][0] +
                                  prng.uniform(low=-0.5, high=0.5, size=n_events))
    bkg_events["dety"] = np.round(bkg_events["chipy"] - event_params['pix_center'][1] +
                                  prng.uniform(low=-0.5, high=0.5, size=n_events))
    bkg_events["xpix"] = bkg_events["detx"] + event_params['pix_center'][0]
    bkg_events["ypix"] = bkg_events["dety"] + event_params['pix_center'][1]

    if bkg_events["energy"].size == 0:
        raise RuntimeError("No instrumental background events were detected!!!")

    mylog.info("Scattering energies with RMF %s." % os.path.split(rmf.filename)[-1])
    bkg_events = rmf.scatter_energies(bkg_events, prng=prng)

    bkg_events['time'] = np.random.uniform(size=bkg_events["energy"].size, low=0.0,
                                           high=event_params["exposure_time"])

    return bkg_events