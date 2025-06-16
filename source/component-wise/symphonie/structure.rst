Run folder structure
====================

In your ``$RUN`` directory, **create a subdirectory for SYMPHONIE** using a script
from the training materials:

.. code:: bash

   bash $TRAINING/make_run-symphonie.sh symphonie


There should now be a new ``$RUN/symphonie`` directory, with the following structure:

.. code:: console

   symphonie/
   ├── bin -> /users/p20055/desmet/SYMPHONIE/RDIR
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


* The ``bin`` folder is a link towards SYMPHONIE's executable directory.
* ``GRAPHICS``, ``OFFLINE`` and ``TIDES`` are folders to contain our simulation outputs.
* ``tmp`` is a directory to write logging/debugging messages during the simulation.
* ``restart_*`` are only useful to the restart procedure, which we will address later in this training.
* ``NOTEBOOKS`` contains all the simulation parameters, split into various Fortran namelists and ASCII files.
* ``notebook_list.f`` is the input file for SYMPHONIE, the "master" namelist, pointing to the various files stored in ``NOTEBOOKS``.
* ``job.sh`` is a batch script for running the executable on CALMIP's computing nodes.


As for :doc:`RegCM <../regcm/structure>`, we will now **store the simulation's
notebooks in our home directory**, so as to have them backed up in case we later need to
reproduce this same simulation.

Start by creating a dedicated folder in your home:

.. code:: bash

   mkdir ~/symphonie_notebooks


Choose a unique identifier for you simulation -- on this page, we'll opt for
``training_uncoupled`` -- and move your ``NOTEBOOKS`` folder in the new folder of your
home, with its new name:

.. code:: bash

   mv $RUN/symphonie/NOTEBOOKS ~/symphonie_notebooks/NOTEBOOKS-training_uncoupled


Finally, make a symbolic link back to your run directory, such that the workflow
remains as convenient as it was:

.. code:: bash

   ln -sf ~/symphonie_notebooks/NOTEBOOKS-training_uncoupled $RUN/symphonie/NOTEBOOKS