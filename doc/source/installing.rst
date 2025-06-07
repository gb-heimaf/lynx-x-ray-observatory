.. _installing:

Installation
============

SOXS and its dependencies are installed as a standard Python package, and it is 
compatible with Python 2.7, 3.5, and 3.6. You may use ``pip`` to install it (if 
you do not have pip, check that your executable is not named ``pip3``, otherwise 
visit https://pip.pypa.io/ to download it):

.. code-block:: bash

    pip install soxs

If the Python distribution is not "owned" by you on your machine you might have
to call ``sudo pip install soxs``. If you need to upgrade from a previous 
version of SOXS, issue ``[sudo] pip install -U soxs`` from the command line. 

If you use `Anaconda Python <https://www.continuum.io/anaconda-overview>`_, you
may install SOXS using ``conda``:

.. code-block:: bash

    conda install -c jzuhone soxs
  
These methods install both the Python interface and the command-line scripts. 

Of course, you can always clone the source from 
`GitHub <http://github.com/XRStools/soxs>`_ and install it manually:

.. code-block:: bash
    
    git clone http://github.com/XRStools/soxs
    cd soxs
    python setup.py install
    
or run ``python setup.py develop`` instead if you want to make changes to the 
code and see them reflected without recompiling (though if you make updates to 
the command-line scripts you will have to run ``python setup.py develop`` 
again). 

SOXS Dependencies
=================

SOXS has the following Python dependencies:

* `NumPy <http://www.numpy.org>`_
* `AstroPy (v1.3) <http://www.astropy.org>`_
* `SciPy <http://www.scipy.org>`_
* `h5py <http://www.h5py.org>`_
* `tqdm <http://github.com/noamraph/tqdm>`_

Using any installation method, these dependencies should automatically install 
(if you do not already have them) provided you are connected to the internet.