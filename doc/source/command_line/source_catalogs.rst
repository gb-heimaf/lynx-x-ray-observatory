.. _cmd-source-catalogs:

Command Line Scripts for Source Catalogs
========================================

This section documents command-line scripts for generating a SIMPUT catalog
of photons from a halo catalog drawn from a cosmological simulation. 

For more information about how the source catalog generation is implemented
in SOXS, see :ref:`source-catalogs`. 

``make_cosmological_sources``
-----------------------------

.. code-block:: text

    usage: make_cosmological_sources [-h] [--cat_center CAT_CENTER] [--nh NH]
                                     [--area AREA] [--append] [--overwrite]
                                     [--output_sources OUTPUT_SOURCES]
                                     [--random_seed RANDOM_SEED]
                                     simput_prefix phlist_prefix exp_time fov
                                     sky_center
    
    Create a SIMPUT photon list of a cosmological background.
    
    positional arguments:
      simput_prefix         The prefix of the SIMPUT file to be used as the root
                            of the catalog. If it does not exist, it will be
                            created.
      phlist_prefix         The prefix of the photon list file to be written.
      exp_time              The exposure time to use, in seconds.
      fov                   The field of view on a side in arcminutes.
      sky_center            The center RA, Dec coordinates of the observation, in
                            degrees, comma-separated
    
    optional arguments:
      -h, --help            show this help message and exit
      --cat_center CAT_CENTER
                            The center of the field in the coordinates of the halo
                            catalog, which range from -5.0 to 5.0 degrees in both
                            directions. If not set, a center will be randomly
                            chosen.
      --nh NH               The hydrogen column in units of 10**22 atoms/cm**2.
                            Default: 0.05
      --area AREA           The collecting area to use, in cm^2. Default: 30000.0
      --append              If set, append a new source an existing SIMPUT
                            catalog.
      --overwrite           Overwrite an existing file with the same name.
      --output_sources OUTPUT_SOURCES
                            Output the source properties to the specified file.
      --random_seed RANDOM_SEED
                            A constant integer random seed to produce a consistent
                            set of random numbers.

Examples
++++++++

Generate photons from halos with a field of view of 10.0 arcminutes, to a new SIMPUT
catalog, with an exposure time of 100 ks. Let a random location in the halo catalog
be chosen:

.. code-block:: bash

    [~]$ make_cosmological_sources halos halos 100000.0 10.0 22.0,-12.0 --overwrite

The same as before, but choose a particular location in the halo catalog:

.. code-block:: bash

    [~]$ make_cosmological_sources halos halos 100000.0 10.0 22.0,-12.0 --cat_center=-0.1,2.0 --overwrite

Append the halo photons to an existing SIMPUT catalog, "my_cat":

.. code-block:: bash

    [~]$ make_cosmological_sources my_cat halos 100000.0 10.0 22.0,-12.0 --append

Change the Galactic hydrogen column to :math:`2 \times 10^{20}~cm^{-2}`:

.. code-block:: bash

    [~]$ make_cosmological_sources halos halos 100000.0 10.0 22.0,-12.0 --nh=0.02 --overwrite

Write the source properties to an ASCII text file:

.. code-block:: bash

    [~]$ make_cosmological_sources halos halos 100000.0 10.0 22.0,-12.0 --output_sources=my_halos.txt --overwrite

``make_point_sources``
----------------------

.. code-block:: text

    usage: make_point_sources [-h] [--nh NH] [--area AREA] [--append]
                              [--overwrite] [--random_seed RANDOM_SEED]
                              [--output_sources OUTPUT_SOURCES]
                              simput_prefix phlist_prefix exp_time fov
                              sky_center
    
    Create a SIMPUT photon list of a point-source background.
    
    positional arguments:
      simput_prefix         The prefix of the SIMPUT file to be used as the root
                            of the catalog. If it does not exist, it will be
                            created.
      phlist_prefix         The prefix of the photon list file to be written.
      exp_time              The exposure time to use, in seconds.
      fov                   The field of view on a side in arcminutes.
      sky_center            The center RA, Dec coordinates of the observation, in
                            degrees, comma-separated.
    
    optional arguments:
      -h, --help            show this help message and exit
      --nh NH               The galactic hydrogen column in units of 10**22
                            atoms/cm**2. Default: 0.05
      --area AREA           The collecting area to use, in cm^2. Default: 30000.0
      --append              If set, append a new source an existing SIMPUT
                            catalog.
      --overwrite           Overwrite an existing file with the same name.
      --output_sources OUTPUT_SOURCES
                            Output the source properties to the specified file.
      --random_seed RANDOM_SEED
                            A constant integer random seed to produce a consistent
                            set of random numbers.

Examples
++++++++

Generate photons from point sources with a field of view of 5.0 arcminutes, to a new SIMPUT
catalog, with an exposure time of 75 ks:

.. code-block:: bash

    [~]$ make_point_sources pt_src pt_src 10.0 75000.0 90.0,5.0 --overwrite

Append the point source photons to an existing SIMPUT catalog, "my_cat":

.. code-block:: bash

    [~]$ make_point_sources my_cat pt_src 10.0 75000.0 90.0,5.0 --append

Change the Galactic hydrogen column to :math:`3.5 \times 10^{20}~cm^{-2}`:

.. code-block:: bash

    [~]$ make_point_sources pt_src pt_src 10.0 75000.0 90.0,5.0 --nh=0.035 --overwrite

Write the source properties to an ASCII text file:

.. code-block:: bash

    [~]$ make_point_sources pt_src pt_src 10.0 75000.0 90.0,5.0 --output_sources=my_ptsrc.txt --overwrite
