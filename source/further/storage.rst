Storage management
==================

**THIS PAGE IS A DRAFT: DO NOT FOLLOW**

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

As for RegCM, we will now **store the simulation's
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


   mkdir ~/oasis_namcouples
   cp $RUN/namcouple ~/oasis_namcouples/namcouple-training_cpl_init
   ln -sf ~/oasis_namcouples/namcouple-training_cpl_init oasis/namcouple-init
