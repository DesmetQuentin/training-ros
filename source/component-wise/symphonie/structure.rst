Run folder structure
====================

In your ``$RUN`` directory, **create a subdirectory for SYMPHONIE** using a script
from the training materials:

.. code:: bash

   cd $RUN
   bash $TRAINING/make_run-symphonie.sh symphonie


There should now be a new ``$RUN/symphonie`` directory, with the following structure:

.. code:: console

   symphonie/
   ├── bin -> $TRAINING/models/SYMPHONIE/RDIR
   ├── GRAPHICS
   ├── job.sh
   ├── notebook_list.f
   ├── NOTEBOOKS
   ├── OFFLINE
   ├── restart_input
   ├── restart_outbis
   ├── restart_output
   ├── TIDES
   └── tmp

   9 directories, 2 files


* The ``bin`` folder is a link toward SYMPHONIE's executable directory.
* ``GRAPHICS``, ``OFFLINE`` and ``TIDES`` are folders to contain our simulation outputs.
* ``tmp`` is a directory to write logging/debugging messages during the simulation.
* ``restart_*`` are only useful to the restart procedure, which we will address later in this training.
* ``NOTEBOOKS`` contains all the simulation parameters, split into various Fortran namelists and ASCII files.
* ``notebook_list.f`` is the input file for SYMPHONIE, the "master" namelist, pointing to the various files stored in ``NOTEBOOKS``.
* ``job.sh`` is a batch script for running the executable on the computing nodes.
