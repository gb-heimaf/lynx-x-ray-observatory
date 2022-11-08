.. _spatial:

Spatial Models in SOXS
======================

The ``SpatialModel`` class can be used to create RA and Dec positions of photons, which can be combined with
the energies from a ``Spectrum`` object to create a source that can be written to a SIMPUT photon list. Several
``SpatialModel`` derivatives are available, which are documented below.

In general, each ``SpatialModel`` takes the following information:

1. A central RA and Dec for the source
2. Some prescription for how the photons should be distributed on the sky
3. The number of photons to generate positions for

The latter is given as as integer since it is expected that the number of photons you need will be determined
by some other criterion (e.g., from the corresponding ``Spectrum``) and can be supplied here.

Each ``SpatialModel`` has only two attributes, ``ra`` and ``dec``, which are unitful NumPy arrays giving the
positions of the photons on the sky in degrees.

Point Sources
-------------

The :class:`~soxs.spatial.PointSourceModel` generates photon positions for a point source.

.. code-block:: python

    from soxs import PointSourceModel
    ra0 = 30.0 # source RA in degrees
    dec0 = 45.0 # source Dec in degrees
    num_events = 100000 # The number of events
    pt_src = PointSourceModel(ra0, dec0, num_events)

Though this model is trivial, it is constructed in the same way as the other models below for consistency.

Beta Model
----------

The :class:`~soxs.spatial.BetaModel` generates photon positions for a :math:`\beta`-model profile,
often used to model galaxy clusters. The functional form of the :math:`\beta`-model for a surface
brightness profile is:

.. math::

    S(r) = S_0\left[1+\left(\frac{r}{r_c}\right)^2\right]^{(-3\beta+1/2)}

where :math:`S_0` is the central surface brightness, :math:`\beta` is the slope parameter, and :math:`r_c`
is the core radius. To construct one:

.. code-block:: python

    from soxs import BetaModel
    ra0 = 30.0 # center RA in degrees
    dec0 = 45.0 # center Dec in degrees
    r_c = 20.0 # the core radius in arc seconds
    beta = 2./3. # the beta slope parameter
    num_events = 100000 # The number of events
    beta_src = BetaModel(ra0, dec0, r_c, beta, num_events)

Annulus
-------

The :class:`~soxs.spatial.AnnulusModel` can be used to generate photon positions for a annulus or disk
with uniform surface brightness:

.. code-block:: python

    from soxs import AnnulusModel
    ra0 = 30.0 # center RA in degrees
    dec0 = 45.0 # center Dec in degrees
    r_in = 0.0 # inner radius of shell in arcseconds
    r_out = 0.0 # outer radius of shell in arcseconds
    num_events = 100000 # The number of events
    ann_src = AnnulusModel(ra0, dec0, r_in, r_out, num_events)

Generic Radial Models
---------------------

The following classes generate azimuthally symmetric models from generic functions or lookup tables for
a surface brightness profile as a function of radius.

``RadialFunctionModel``
+++++++++++++++++++++++

:class:`~soxs.spatial.RadialFunctionModel` takes as input a central RA, Dec, and a Python function or callable
object to generate an azimuthally symmetric distribution of photon positions:

.. code-block:: python

    from soxs import RadialFunctionModel
    # A simple inverse square-law surface brightness profile.
    # There is no need to normalize it properly, since that is taken
    # care of by the number of photons. r is in arcseconds.
    def S_r(r):
        return 1.0/(r*r)
    ra0 = 100.0 # center RA in degrees
    dec0 = -30.0 # center Dec in degrees
    num_events = 100000 # The number of events
    my_src = RadialFunctionModel(ra0, dec0, S_r, num_events)

``RadialArrayModel``
++++++++++++++++++++

:class:`~soxs.spatial.RadialArrayModel` takes as input a central RA, Dec, and two NumPy arrays
of radius and surface brightness to generate an azimuthally symmetric distribution of photon positions:

.. code-block:: python

    from soxs import RadialArrayModel
    ra0 = 100.0 # center RA in degrees
    dec0 = -30.0 # center Dec in degrees
    num_events = 100000 # The number of events
    r = np.linspace(0.0, 100.0, 10000) # binned array of radii in arcseconds
    r_s = 100.0 # scale radius of arcseconds
    S_r = 1.0/((1.0+r/r_s)**2*(r/r_s)) # the surface brightness array
    my_src = RadialArrayModel(ra0, dec0, r, S_r, num_events)

``RadialFileModel``
+++++++++++++++++++

:class:`~soxs.spatial.RadialFileModel` takes as input a central RA, Dec, and an ASCII table of two columns,
radius and surface brightness, to generate an azimuthally symmetric distribution of photon positions:

.. code-block:: python

    from soxs import RadialFileModel
    ra0 = 100.0 # center RA in degrees
    dec0 = -30.0 # center Dec in degrees
    num_events = 100000 # The number of events
    my_src = RadialFileModel(ra0, dec0, "my_profile.dat", num_events)

"Field of View" Sources
-----------------------

The :class:`~soxs.spatial.FillFOVModel` generates photon positions on the sky which fill a given field of view:

.. code-block:: python

    from soxs import FillFOVModel
    ra0 = 30.0 # center RA in degrees
    dec0 = 45.0 # center Dec in degrees
    fov = 20.0 # width of the field of view in arcminutes
    num_events = 100000 # The number of events
    fov_src = FillFOVModel(ra0, dec0, fov, num_events)

This may be useful for creating background-like sources.

Combining Sources
-----------------

The spatial positions for the two sources can be combined simply via addition:

.. code-block:: python

    ann_src = AnnulusModel(ra0, dec0, r_in, r_out, num_events)
    pt_src = PointSourceModel(ra0, dec0, num_events)
    all_src = ann_src+pt_src

which concatenates the arrays of RA and Dec.