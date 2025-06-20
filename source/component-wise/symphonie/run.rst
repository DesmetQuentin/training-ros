Running and outputs
===================

After :doc:`initialization <initialize>`, we need to set and reset parameters of our
notebooks and batch script to prepare our uncoupled simulation.

First, change/check the values of the following **notebook parameters**:

.. list-table::
   :header-rows: 1

   * - File
     - Variable and value
     - Comment
   * - ``notebook_time.f``
     - ``run_option = 0``
     - Disables the initialization mode
   * - ``notebook_grid.f``
     - ``kmax = 30``
     - Back to a reasonable number of vertical layers
   * - ``notebook_vertcoord.f``
     - ``flag_merged_levels = 1``
     - Revert
   * - ``notebook_grid.f``
     - ``nbdom_imax = 6`` and ``nbdom_jmax = 10``
     - Keep the initial grid dimensions
   * - ``notebook_grid.f``
     - ``mpi_map_file_name = 'description_domaine.next'`` and ``mpi_hole_plugging = 'description_trous.txt'``
     - Files generated by the :doc:`initialization <initialize>`
   

Then, **edit the** ``job.sh`` **batch script**:

* Set the ``--job-name`` batch parameter to ``'symphonie'``.
* Set ``NPROC`` to 36, as indicated in the header of ``description_domaine.next``.
* Accordingly, set the ``--nodes`` batch parameter back to 1.
* Check that ``DIR`` is the current run directory.
* Check that ``EXE`` is ``./bin/ORIGIN/symphonie.exe``.
   

.. dropdown:: ``job.sh``

   .. code:: bash

      #!/bin/bash

      #SBATCH --job-name=symphonie
      #SBATCH --nodes=1
      #SBATCH --ntasks-per-node=36
      #SBATCH --ntasks-per-core=1
      #SBATCH --time=1:00:00
      #SBATCH --output=slurm_%x-id_%j.out
      #SBATCH --error=slurm_%x-id_%j.err

      DIR=/tmpdir/desmet/TRAINING_CPL/symphonie # <-- make sure to modify here!
      EXE=./bin/ORIGIN/symphonie.exe # from DIR
      NPROC=36
      INPUT=notebook_list.f

      module purge
      source /tmpdir/desmet/2025-05-21-WORKSHOP/config.sh

      export OMPI_FC=ifort
      export OMPI_CC=icc
      export OMP_CXX=icpc
      ulimit -s unlimited

      cd $DIR

      rm fort*
      rm core

      module list 2>./run_modules

      mpiexec.hydra -np $NPROC $EXE $INPUT


Next, **empty the** ``tmp`` **folder**:

.. code:: bash

   rm tmp/*


.. important::

   SYMPHONIE will **fail immediately if** ``tmp`` **is not empty.**

   You might want to add a ``rm tmp/*`` line to your batch script.
   However this is not advised because the ``tmp`` directory contains a number of files
   which might be important for you in some situations in the future, in which case
   you should always be fully aware when deleting the content of ``tmp``.
   It is thus preferred to type ``rm tmp/*`` manually before every rerun of your
   SYMPHONIE simulations.


Finally, **submit** the job with ``sbatch``, **check** on it with ``squeue``, and the
run should complete successfully after some time, with the following tail to its slurm
output:

.. code:: console

   $ tail slurm_symphonie*.out
    ____  __ __  ____        ___   __  _ 
   |    \|  |  ||    \      /   \ |  |/ ]
   |  D  )  |  ||  _  |    |     ||  | / 
   |    /|  |  ||  |  |    |  O  ||    \ 
   |    \|  :  ||  |  |    |     ||     |
   |  .  \     ||  |  |    |     ||  .  |
   |__|\_|\__,_||__|__|     \___/ |__|\_|


   Open /users/p20055/desmet/SYMPHONIE/SOURCES/model_name to see what's new in this version of the model


The ``GRAPHICS`` and ``OFFLINE`` folders should now also contain several files, each
containing one timestep, with the fields requested in the ``notebook_graph`` and
``notebook_offline.f``, respectively. Feel free to explore their content using
``ncview`` and/or ``ncdump -h``.

.. note::

   Notice that **none of the files in** ``GRAPHICS`` **and** ``OFFLINE`` **contains grid
   information**. Indeed, those are saved in a separate file: ``tmp/grid.nc``. However,
   if you open it with a visual tool like ``ncview``, you will notice that grid
   information is only available for the meshes of the MPI grid that contain ocean
   cells, while other meshes only display ``NaN``. This can be problematic for
   conducting preprocessing with other tools like Python for instance. This is why
   we saved the ``grid.nc`` file produced during :doc:`initialization <initialize>`.
   Yet, since initialization was done with one only vertical level, the resulting
   ``grid.nc`` is not relevant for the vertical axis. In this respect, keep in mind the
   following:
   
   * Initialization's ``grid.nc`` contains **unmasked 2D coordinates**.
   * Production run's ``grid.nc`` contains the **full vertical axis** but masked data in the horizontal.