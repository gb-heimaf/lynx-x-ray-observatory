.. _cmd-instrument:

Command Line Scripts for the Instrument Simulator
=================================================

These command-line scripts allow one to run and modify the instrument simulator.
For details on what's going on under the hood, see :ref:`instrument`.

``instrument_simulator``
------------------------

The ``instrument_simulator`` script takes a SIMPUT catalog and generates a 
simulated observation in a standard event file format which can then be 
processed by standard tools such as CIAO, HEATOOLS, XSPEC, etc. 

.. code-block:: text

    usage: instrument_simulator [-h] [--overwrite] [--dither_shape DITHER_SHAPE]
                                [--dither_size DITHER_SIZE]
                                [--roll_angle ROLL_ANGLE]
                                [--bkgnd_file BKGND_FILE] [--subpixel_res]
                                [--random_seed RANDOM_SEED]
                                [--ptsrc_bkgnd | --no_ptsrc_bkgnd]
                                [--instr_bkgnd | --no_instr_bkgnd]
                                [--foreground | --no_foreground]
                                simput_file out_file exp_time instrument
                                sky_center
    
    Run the instrument simulator and produce a simulated event file.
    
    positional arguments:
      simput_file           The SIMPUT file to be used as input, or "None" if you
                            only want to simulate backgrounds.
      out_file              The name of the event file to be written.
      exp_time              The exposure time to use, in seconds.
      instrument            The name of the instrument to use, or alternatively
                            the name of a JSON file which contains an instrument
                            specification.
      sky_center            The center RA, Dec coordinates of the observation, in
                            degrees, comma-separated
    
    optional arguments:
      -h, --help            show this help message and exit
      --overwrite           Overwrite an existing file with the same name.
      --dither_shape DITHER_SHAPE
                            The shape of the dither pattern: square, circle, or
                            None. Default: square
      --dither_size DITHER_SIZE
                            The size of the dither pattern in arcseconds. For a
                            circle, thesize is the radius; for a square, the size
                            is the width. Default: 16.0
      --roll_angle ROLL_ANGLE
                            The roll angle in degrees. Default: 0.0
      --bkgnd_file BKGND_FILE
                            Use background stored in a file instead of generating
                            one.
      --subpixel_res        Don't uniformly distribute event positions within
                            pixels.
      --random_seed RANDOM_SEED
                            A constant integer random seed to produce a consistent
                            set of random numbers.
      --ptsrc_bkgnd         Turn the point-source background on.
      --no_ptsrc_bkgnd      Turn the point-source background off.
      --instr_bkgnd         Turn the instrumental background on.
      --no_instr_bkgnd      Turn the instrumental background off.
      --foreground          Turn the galactic foreground on.
      --no_foreground       Turn the galactic foreground off.

Examples
++++++++

Changing Instrument Specification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example uses the pre-built HDXI instrument specification, assuming a 50 ks observation
with the pointing (RA, Dec) = (30, 45) degrees.

.. code-block:: bash

    [~]$ instrument_simulator sloshing_simput.fits evt.fits 50.0,ks hdxi 30.,45. --overwrite

The same, but use the HDXI specification with mirror diameter of :math:`d` = 3 m and focal length of
:math:`f` = 20 m:

.. code-block:: bash

    [~]$ instrument_simulator sloshing_simput.fits evt.fits 50.0,ks hdxi_3x20 30.,45. --overwrite

See :ref:`instrument-arg` for details on the options for the ``instrument`` argument.

This example uses a JSON file created by the user, which contains a custom instrument specification. See
:ref:`instrument-registry` for details on how to do this.

.. code-block:: bash

    [~]$ instrument_simulator sloshing_simput.fits evt.fits 50.0,ks my_inst.json 30.,45. --overwrite

The following details how to change the other options, for more info see :ref:`other-mods`.

Changing Roll Angle and Dither
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Change the roll angle to 45 degrees:

.. code-block:: bash

    [~]$ instrument_simulator sloshing_simput.fits evt.fits 50.0,ks hdxi 30.,45. --roll_angle=45.0 --overwrite

Change the dither shape to a circle and make the dither radius 32 arcsec:

.. code-block:: bash

    [~]$ instrument_simulator sloshing_simput.fits evt.fits 50.0,ks hdxi 30.,45. --dither_shape=circle --dither_size=32.0 --overwrite

Turn dithering off entirely:

.. code-block:: bash

    [~]$ instrument_simulator sloshing_simput.fits evt.fits 50.0,ks hdxi 30.,45. --dither_shape=None --overwrite

Customizing Backgrounds
~~~~~~~~~~~~~~~~~~~~~~~

Turn off the instrumental background:

.. code-block:: bash

    [~]$ instrument_simulator sloshing_simput.fits evt.fits 50.0,ks hdxi 30.,45. --no_instr_bkgnd --overwrite

Turn off the Galactic foreground:

.. code-block:: bash

    [~]$ instrument_simulator sloshing_simput.fits evt.fits 50.0,ks hdxi 30.,45. --no_foreground --overwrite

Turn off the point-source background:

.. code-block:: bash

    [~]$ instrument_simulator sloshing_simput.fits evt.fits 50.0,ks hdxi 30.,45. --no_ptsrc_bkgnd --overwrite

Any combination of these may be used to turn multiple components off or all 
of them. 

To use a background stored in an event file:

.. code-block:: bash

    [~]$ instrument_simulator sloshing_simput.fits evt.fits 50.0,ks hdxi 30.,45. --bkgnd_file="bkg_evt.fits" --overwrite

.. note::

    If you use a background stored in an event file, the background will be 
    entirely determined from the contents of this file and any of the above
    background flags will be ignored.

``simulate_spectrum``
---------------------

Generate a PI or PHA spectrum from a spectrum in an ASCII table (such as 
one made by one of the commands detailed in :ref:`cmd-spectra`) by convolving
it with responses. To be used if one wants to create a spectrum without 
worrying about spatial response. Similar to XSPEC's "fakeit". 

.. code-block:: bash

    usage: simulate_spectrum [-h] [--overwrite] [--random_seed RANDOM_SEED]
                             spec_file instrument exp_time out_file
    
    Run the instrument simulator and produce a simulated event file.
    
    positional arguments:
      spec_file             The file containing the spectrum to be used.
      instrument            The name of the instrument to use, or alternatively
                            the name of a JSON file which contains an instrument
                            specification.
      exp_time              The exposure time to use, in seconds.
      out_file              The file to write the convolved spectrum to.
    
    optional arguments:
      -h, --help            show this help message and exit
      --overwrite           Overwrite an existing file with the same name.
      --random_seed RANDOM_SEED
                            A constant integer random seed to produce a consistent
                            set of random numbers.

Examples
++++++++

.. code-block:: bash

    [~]$ simulate_spectrum power_law_spec.dat mucal 300.0,ks plaw_spec.pha

``make_exposure_map``
---------------------

This script takes an event file made by SOXS and makes a SOXS exposure map for it. 

.. code-block:: text

    usage: make_exposure_map [-h] [--energy ENERGY] [--weightsfile WEIGHTSFILE]
                             [--asol_file ASOL_FILE] [--overwrite]
                             [--nhistx NHISTX] [--nhisty NHISTY]
                             [--normalize | --no_normalize]
                             event_file expmap_file
    
    Make a SOXS exposure map from an event file.
    
    positional arguments:
      event_file            The event file to use to make the exposure map.
      expmap_file           The file to write the exposure map to.
    
    optional arguments:
      -h, --help            show this help message and exit
      --energy ENERGY       The reference energy to use when making the exposure
                            map. This parameter will be ignored if a 'weightsfile'
                            is set.
      --weightsfile WEIGHTSFILE
                            A file containing two columns: energy and spectral
                            weights, to create an exposure map weighted over an
                            energy band.
      --asol_file ASOL_FILE
                            If set, write the aspect solution to this file.
      --overwrite           Overwrite an existing file with the same name.
      --nhistx NHISTX       The number of bins in the aspect histogram in the DETX
                            direction. Default: 16
      --nhisty NHISTY       The number of bins in the aspect histogram in the DETY
                            direction. Default: 16
      --normalize           Normalize the exposure map by the exposure time. This
                            is the default.
      --no_normalize        Don't normalize the exposure map by the exposure time.

Examples
++++++++

Make an exposure map from an event file at a single energy of 3.0 keV.

.. code-block:: bash

    [~]$ make_exposure_map evt.fits expmap.fits --energy=3.0 --overwrite

Also write an aspect solution file.

.. code-block:: bash

    [~]$ make_exposure_map evt.fits expmap.fits --energy=3.0 --asol_file=asol.fits --overwrite

Make an exposure map, using an ASCII text file with two columns, energy and flux, 
to weight the exposure. 

.. code-block:: bash

    [~]$ make_exposure_map evt.fits expmap.fits --weightsfile=spec.dat --overwrite

Make an exposure map and change the binning of the aspect histogram. 

.. code-block:: bash

    [~]$ make_exposure_map evt.fits expmap.fits --energy=3.0 --overwrite --nhistx=32 --nhisty=32

Make an exposure map, but don't normalize by the exposure time. 

.. code-block:: bash

    [~]$ make_exposure_map evt.fits expmap.fits --energy=3.0 --overwrite --no_normalize

