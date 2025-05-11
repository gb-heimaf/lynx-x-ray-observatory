.. _change-dither:

Change the Dither Pattern
=========================

This script shows how to create a point source in a SIMPUT catalog and then 
simulate it with three different types of dither patterns. 

.. code-block:: bash

    #!/bin/bash
    
    # We will use this script to illustrate how to change the dithering options. 
    
    # First, make an absorbed power-law spectrum, which will be for a point source.
    make_powerlaw_spectrum 1.1 0.05 1.0e-4 powerlaw_spec.dat --absorb --nh 0.04 --overwrite
    
    # Take this spectrum and make a SIMPUT catalog with a point source photon list
    make_point_source my_cat point_source 30.0 45.0 powerlaw_spec.dat 100000.0 --overwrite
    
    # Next, we make three event files, using a different dither for each
    
    # Normal HDXI with the default 16.0 arcsec square dither
    instrument_simulator my_cat_simput.fits evt_square.fits 50000.0 hdxi 30.0,45.0 --overwrite
    
    # HDXI with a 16.0 arcsec radius circle dither
    instrument_simulator my_cat_simput.fits evt_circle.fits 50000.0 hdxi 30.0,45.0 --dither_shape=circle --dither_size=16.0 --overwrite
    
    # HDXI with no dither
    instrument_simulator my_cat_simput.fits evt_none.fits 50000.0 hdxi 30.0,45.0 --dither_shape=None --overwrite

Download this script here: `change_dither.sh <../change_dither.sh>`_

If we look at the CHIPX/Y coordinates of each event file together, we see the difference in the
dither pattern:

.. image:: ../images/change_dither.png
   :width: 800px