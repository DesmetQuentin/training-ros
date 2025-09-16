Run folder structure
====================

If you followed well the "Run folder structure" sections of the training's first part
for :doc:`RegCM <../component-wise/regcm/index>` and
:doc:`SYMPHONIE <../component-wise/symphonie/index>`, then your ``$RUN`` directory
should look like this:

.. code:: console

   $ ls -1 $RUN
   regcm
   symphonie


This is the starting point of our coupled model run folder. Let us **complete this
structure** with the following lines:

.. code:: bash

   cd $RUN
   mkdir oasis
   cp $TRAINING/namcouples/namcouple .
   cp $TRAINING/jobs/job-coupled_model.sh job.sh


.. note::

   If you did not exactly follow the first part of this training, you may rebuild
   everything from scratch using:

   .. code:: bash

      bash $TRAINING/make_run-coupled_model.sh $RUN


Now, the same ``$RUN`` directory should look like:

.. code:: console

   $ ls -1 $RUN
   job.sh
   namcouple
   oasis
   regcm
   symphonie


* The ``oasis``, ``regcm`` and ``symphonie`` are independent folders relating to each specific component.
* ``namcouple`` is the namelist read by OASIS at run time (this is actually formatted in ASCII, not Fortran).
* ``job.sh`` is a batch script for running the executables on the computing nodes.

.. attention::

   You cannot rename ``namcouple``! OASIS will specifically search for that file in the
   directory where the models are executed from.


We then need to **prepare the namelists of our coupled system.** Let us simply copy
those from our uncoupled runs for each component, using the ``cpl_init`` suffix:

.. code:: bash

   cp regcm/namelist.f regcm/namelist-cpl_init.f
   cp -r symphonie/NOTEBOOKS symphonie/NOTEBOOKS-cpl_init


As a last step, let us **adapt those dedicated namelists to the coupled run folder
structure**. Indeed, while we ran RegCM and SYMPHONIE from their own folder, we now aim
to run the coupled model one folder ahead, and this must be translated into the
namelists.

To be more specific, what the coupled system sees is now:

.. code:: console

   $ tree -d 2 $RUN
   $RUN
   ├── oasis
   ├── regcm
   │   ├── bin -> $TRAINING/models/RegCM/bin
   │   ├── input
   │   └── output
   └── symphonie
       ├── bin -> $TRAINING/models/SYMPHONIE/RDIR
       ├── GRAPHICS
       ├── NOTEBOOKS
       ├── NOTEBOOKS-cpl_init
       ├── OFFLINE
       ├── restart_input
       ├── restart_outbis
       ├── restart_output
       ├── TIDES
       └── tmp

   16 directories


The several directories used by our components are thus slightly different: RegCM's
``output`` is now ``regcm/output``, SYMPHONIE's ``OFFLINE`` is now
``symphonie/OFFLINE``, etc. Accordingly, let us adapt all mentions of relative paths in
the namelists, adding the right prefix, i.e., ``regcm/`` and ``symphonie/`` for RegCM
and SYMPHONIE, respectively.

In the newly copied namelists, modify the following variables:

.. tab-set::

   .. tab-item:: RegCM

      * ``dirter``
      * ``dirglob``
      * ``dirout``


   .. tab-item:: SYMPHONIE

      * ``restartdir_*`` in ``notebook_time.f``
      * ``tmpdirname``, ``mpi_map_file_name`` and ``mpi_hole_plugging`` in ``notebook_grid.f``
      * The directory for ``GRAPHICS`` in ``notebook_graph``
      * ``directory_offline`` and ``offlinefile`` in ``notebook_offline.f``
      * (If tides are enabled: the directory for ``TIDES`` in ``notebook_tide``)
      * ``default_grid_file_name`` in ``notebook_oasis_generic.f``
      * ``directory`` in ``notebook_list.f``


And that's it! We can proceed the next part.
