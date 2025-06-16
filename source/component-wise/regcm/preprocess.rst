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

   ./bin/terrainPNETCDF_CLM45 namelist.f


This should create three files relating to time-independent domain-related data:

.. code:: console

   $ ls -1rt input  # TODO


Then, run the ``sst`` program:

.. code:: bash

   ./bin/sstPNETCDF_CLM45 namelist.f


This should generate a single new file containing initial and boundary conditions of sea
surface temperature throughout the simulation period:

.. code:: console

   $ ls -1rt input  # TODO


Next, run the ``mksurfdata`` program:

.. code:: bash

   ./bin/mksurfdataPNETCDF_CLM45 namelist.f


This program preprocesses every data needed by the Community Land Model version 4.5
(CLM4.5) implemented as a submodule of RegCM5.


Finally, run the ``icbc`` program:

.. code:: bash

   ./bin/icbcPNETCDF_CLM45 namelist.f


You should now see a new Initial Condition and Boundary Condition (ICBC) file,
containing all ICBC data interpolated on the simulation's period and domain.

.. code:: console

   $ ls -1rt input  # TODO


Once these preprocessing programs have ran, RegCM's main run will rely on their only
results stored in the ``input`` directory, already taylored to the period and domain
indicated in ``namelist.f``, rather than interpolating heavier files online during the
simulation.
