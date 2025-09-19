Preprocessing and inputs
========================

Let us make a step closer toward our uncoupled simulation of RegCM: we are now going
to run all necessary preprocessing programs, namely, ``terrain``, ``sst``,
``mksurfdata`` and ``icbc``. Simply follow the commands below.

Change directory:

.. code:: bash

   cd $RUN/regcm


Run the ``terrain`` program:

.. code:: bash

   ./bin/terrainCLM45 namelist.f


This should create three files relating to time-independent domain-related data:

.. code:: console

   $ ls -1rt input
   QUYNHON_TEXTURE
   QUYNHON_LANDUSE
   QUYNHON_DOMAIN000.nc


Then, run the ``sst`` program:

.. code:: bash

   ./bin/sstCLM45 namelist.f


This should generate a single new file containing initial and boundary conditions of sea
surface temperature throughout the simulation period:

.. code:: console

   $ ls -1rt input
   QUYNHON_TEXTURE
   QUYNHON_LANDUSE
   QUYNHON_DOMAIN000.nc
   QUYNHON_SST.nc


Next, run the ``mksurfdata`` program:

.. code:: bash

   ./bin/mksurfdataCLM45 namelist.f


This program preprocesses every data needed by the Community Land Model version 4.5
(CLM4.5) implemented as a submodule of RegCM5.


Finally, run the ``icbc`` program:

.. code:: bash

   ./bin/icbcCLM45 namelist.f


You should now see a new Initial Condition and Boundary Condition (ICBC) file,
containing all ICBC data interpolated on the simulation's period and domain.

.. code:: console

   $ ls -1rt input
   QUYNHON_TEXTURE
   QUYNHON_LANDUSE
   QUYNHON_DOMAIN000.nc
   QUYNHON_SST.nc
   QUYNHON_CLM45_surface.nc
   QUYNHON_ICBC.2018070300.nc


Once these preprocessing programs have run, RegCM's main simulation will rely on their
only results stored in the ``input`` directory, already taylored to the period and
domain indicated in ``namelist.f``, rather than interpolating heavier files online
during the simulation.

.. note::

   Preprocessing programs behave exactly the same, whether compilation was conducted
   with OASIS enabled or not (i.e., whether the programs have the ``OASIS`` suffix or
   not).
