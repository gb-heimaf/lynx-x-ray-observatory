import os
from astropy import log as mylog
import numpy as np
import astropy.wcs as pywcs

mylog.setLevel('INFO')

sox_path = os.path.abspath(os.path.dirname(__file__))
sox_files_path = os.path.join(sox_path, "files")

def check_file_location(fn, subdir):
    if os.path.exists(fn):
        return os.path.abspath(fn)
    else:
        sto_fn = os.path.join(sox_path, subdir, fn)
        if os.path.exists(sto_fn):
            return sto_fn
    raise IOError("Could not find file %s!" % fn)

def iterable(obj):
    """
    Grabbed from Python Cookbook / matploblib.cbook.  Returns true/false for
    *obj* iterable.
    """
    try: len(obj)
    except: return False
    return True

def ensure_list(obj):
    """
    This function ensures that *obj* is a list.  Typically used to convert a
    string to a list, for instance ensuring the *fields* as an argument is a
    list.
    """
    if obj is None:
        return [obj]
    if not isinstance(obj, list):
        return [obj]
    return obj

def ensure_numpy_array(obj):
    """
    This function ensures that *obj* is a numpy array. Typically used to
    convert scalar, list or tuple argument passed to functions using Cython.
    """
    if isinstance(obj, np.ndarray):
        if obj.shape == ():
            return np.array([obj])
        # We cast to ndarray to catch ndarray subclasses
        return np.array(obj)
    elif isinstance(obj, (list, tuple)):
        return np.asarray(obj)
    else:
        return np.asarray([obj])

one_arcsec = 1.0/3600.0

def construct_wcs(ra0, dec0):
    w = pywcs.WCS(naxis=2)
    w.wcs.crval = [ra0, dec0]
    w.wcs.crpix = [0.0]*2
    w.wcs.cdelt = [-one_arcsec, one_arcsec]
    w.wcs.ctype = ["RA---TAN","DEC--TAN"]
    w.wcs.cunit = ["deg"]*2
    return w
