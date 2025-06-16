Installation guide
==================

This sections guides you through compiling and installing all the necessary code for
using the coupled model. We assume here that the modules used in your CALMIP session are
the one loaded in the following:

.. code:: bash

   module load intel/18.2
   module load intelmpi/18.2
   module load hdf5/1.10.2-intelmpi
   module load netcdf/4.6.1-intelmpi
   module load pnetcdf/1.9.0-intelmpi


If this is not the case, you will need to adapt the various paths to ``include`` and
``lib`` directories employed throughout the installation process.

**OASIS3-MCT is not an executable but a Fortran library.** It will be used by RegCM and
SYMPHONIE for their own installation. Therefore, this is the first code to install.
Afterward, RegCM and SYMPHONIE can be installed independently in any order.

.. toctree::
   :maxdepth: 1

   oasis
   regcm
   symphonie