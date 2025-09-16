Run folder structure
====================

In your ``$RUN`` directory, **create a subdirectory for RegCM** using a script
from the training materials:

.. code:: bash

   bash $TRAINING/scripts/make_run-regcm.sh regcm


There should now be a new ``$RUN/regcm`` directory, with the following structure:

.. code:: console

   regcm/
   ├── bin -> $TRAINING/models/RegCM/bin
   ├── input
   ├── job.sh
   ├── namelist.f
   └── output

   3 directories, 2 files


* The ``bin`` folder is a link toward RegCM's executable directory.
* ``input`` and ``output`` are folders to contain our simulation's input and output, respectively.
* ``namelist.f`` is the input file containing all the parameters of the simulation.
* ``job.sh`` is a batch script for running the main executable on the computing nodes.
