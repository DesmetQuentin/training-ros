Run folder structure
====================

In your ``$RUN`` directory, **create a subdirectory for RegCM** using a script
from the training materials:

.. code:: bash

   bash $TRAINING/scripts/make_run-regcm.sh regcm


There should now be a new ``$RUN/regcm`` directory, with the following structure:

.. code:: console

   regcm/
   ├── bin -> /tmpdir/desmet/training_ROS/models/RegCM/bin
   ├── input
   ├── job.sh
   ├── namelist.f
   └── output

   3 directories, 2 files


* The ``bin`` folder is a link towards RegCM's executable directory.
* ``input`` and ``output`` are folders to contain our simulation's input and output, respectively.
* ``namelist.f`` is the input file containing all the parameters of the simulation.
* ``job.sh`` is a batch script for running the main executable on CALMIP's computing nodes.


The ``tmpdir`` storage of CALMIP will never have backup saving. For this reason, it is
recommended to store important and lightweight files in one's ``$HOME`` directory, so as
to protect it from potential crashes of CALMIP's ``tmpdir`` (you may have noticed that
RegCM's executable ``bin`` directory is located at a path starting by ``/users``, i.e., 
in someone's home directory). In the RegCM framework, while the run directory we have
just created will certainly become heavy once a simulation is run, the input namelist
contains all the parameters required to reproduce our simulation later: this is a
typical example of *important* and *lightweight* file you'd like to store in your
``$HOME``. Let us thus be consistent and **store** ``namelist.f`` **in our home
directory.**

Start by creating a dedicated folder in your home:

.. code:: bash

   mkdir ~/regcm_namelists


Choose a unique identifier for you simulation -- on this page, we'll opt for
``training_uncoupled`` -- and move your namelist in the new folder with its new name:

.. code:: bash

   mv $RUN/regcm/namelist.f ~/regcm_namelists/namelist-training_uncoupled.f


Finally, make a symbolic link back to your run directory, such that the workflow
remains as convenient as it was:

.. code:: bash

   ln -sf ~/regcm_namelists/namelist-training_uncoupled.f $RUN/regcm/namelist.f
