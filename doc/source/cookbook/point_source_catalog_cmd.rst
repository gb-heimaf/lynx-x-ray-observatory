.. _point-source-catalog-cmd:

Point Source Catalog (Command-Line Version)
===========================================

This script shows how to make a tailor-made distribution of photons from a
distribution of point sources and simulate an observation of them. 

.. code-block:: bash

    #!/bin/sh
    
    # Use this script to create a distribution of photons from point sources 
    # and simulate an observation.

    # First, make the photons from the point sources into a SIMPUT catalog,
    # saving the point source properties to an ASCII table file and choosing 
    # "24" as a random seed to insure we get the same point sources every time.
    # If you wish, the table file can be used to generate the same sources later
    # using the "--input_sources" parameter.
    make_point_sources my_cat ptsrc 300000.0 20. 22.,-27.0 --random_seed=24 --output_sources=point_source_table.dat
 
    # Take the SIMPUT catalog and make an event file. Since we already made a
    # distribution of point sources, turn the point-source background off. 
    instrument_simulator my_cat_simput.fits ptsrc_cat_evt.fits 300000.0 hdxi 22.,-27.0 --overwrite --no_ptsrc_bkgnd

Download this script here: `point_source_catalog.sh <../point_source_catalog.sh>`_

The point sources look like this in ds9:

.. image:: ../images/point_source_catalog.png
   :width: 800px