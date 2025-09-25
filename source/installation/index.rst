Installation guide
==================

This sections guides you through compiling and installing all the necessary code for
using the coupled model. The guide proposes compilers and libraries that fit either HILO
or CALMIP. If you want to install the model on another machine, we may be able to
provide some assistance but make sure to contact the machine administrator to know
what are the recommanded tools and versions on your machine. Beside compilers and
library versions, those pages on installation will give you the procedure to follow,
whether you work on HILO/CALMIP or not, so you should find value here anyways.
Good luck, now!

First, below are the modules we will use throughout these pages. They should already
be loaded after you have ``source`` d the ``config.sh`` script:

.. tab-set::

   .. tab-item:: HILO

      .. code:: console

         $ module list
         Currently Loaded Modulefiles:
           1) intel/2019.u5            3) mvapich2/2.3.6_intel     5) PnetCDF/1.9.0_intel_64
           2) hdf5/1.8.15p1_intel_64   4) netcdf/4.6.1_intel_64


   .. tab-item:: CALMIP

      .. code:: console

         $ module list
         Currently Loaded Modulefiles:
           1) intel/18.2               3) hdf5/1.10.2-intelmpi     5) pnetcdf/1.9.0-intelmpi
           2) intelmpi/18.2            4) netcdf/4.7.4-intelmpi


If they are not loaded yet, you may load each of them manually using
``module load <module name>``, e.g., ``module load intel/18.2``.

If you wish to proceed to the installation with a different set of modules and/or on
another machine, you will need to adapt the various paths to ``include`` and ``lib``
directories employed throughout the installation process.

**OASIS3-MCT is not an executable but a Fortran library.** It will be used by RegCM and
SYMPHONIE for their own installation. Therefore, this is the first code to install.
Afterward, RegCM and SYMPHONIE can be installed independently in any order.

.. toctree::
   :maxdepth: 1

   oasis
   regcm
   symphonie
