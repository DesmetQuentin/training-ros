Initialization
==============

Although SYMPHONIE does not provide any preprocessing program, the
``symphonie.exe`` program **can be ran only for its initialization part**, i.e.,
stopping right before entering the main model loop. This allows users to check whether
the notebook configuration is well interpreted by the model, but also to trigger some
checks, debugging outputs or preliminary analyses without committing to book computing
nodes for the long run.

In particular, on this page, we are going to run an initialization to determine the
CPU allocation of our configuration. Indeed, as an ocean model, **SYMPHONIE does not
need to book computing resources for land-only areas of the domain**. This way, instead
of simply dividing the domain into a grid then assigning each CPU with one mesh in this
grid, we want, in addition, to filter out the land-only meshes, ultimately resulting in
a reduced need of computing resources. In this context, let us set up an initialization
run to compute which parts of the grid are land-only and can thus be ignored.

First, after changing directory to ``$RUN/symphonie``, change/check the values of the
following **notebook parameters**:

.. list-table::
   :header-rows: 1

   * - File
     - Variable and value
     - Comment
   * - ``notebook_time.f``
     - ``run_option = -1``
     - Enables the initialization mode.
   * - ``notebook_grid.f``
     - ``nbdom_imax = 7`` and ``nbdom_jmax = 6`` on CALMIP/``nbdom_imax = 8`` and ``nbdom_jmax = 6`` on HILO
     - The initial grid dimensions.
   * - ``notebook_grid.f``
     - ``mpi_map_file_name = 'default'`` and ``mpi_hole_plugging = 'none'``
     - These variables should point to the files that contain information on which part of the grid decomposition are land-only. Setting them to their defaults triggers their computation.


And make sure that you are pointing to the right ``NOTEBOOKS`` folder by **editing**
``notebook_list.f``.

.. tab-set::

   .. tab-item:: HILO

      Then, **edit the** ``job.sh`` **batch script**:

      * Set ``--job-name`` to ``init``.
      * Set ``NPROC`` and ``--ntasks`` to 48: this corresponds to the size of the grid as indicated in ``notebook_grid.f``.
      * Set ``EXE`` to ``bin/ORIGIN/symphonie.exe``.


      .. dropdown:: ``job.sh``

         .. code:: bash

            #!/bin/bash

            #SBATCH --job-name=init
            #SBATCH --ntasks=48
            #SBATCH --cpus-per-task=1
            #SBATCH --time=20:00
            #SBATCH --output=slurm_%x-id_%j.out
            #SBATCH --error=slurm_%x-id_%j.err

            EXE=bin/ORIGIN/symphonie.exe
            NPROC=48
            INPUT=notebook_list.f

            ulimit -s unlimited

            module purge
            module load slurm/21.08.5
            module load intel/2019.u5
            module load hdf5/1.8.15p1_intel_64
            module load mvapich2/2.3.6_intel
            module load netcdf/4.6.1_intel_64
            module load PnetCDF/1.9.0_intel_64
            module list 2>./run_modules

            echo -e "Launching...\n"

            mpiexec.hydra -np $NPROC $EXE $INPUT


   .. tab-item:: CALMIP

      Then, **edit the** ``job.sh`` **batch script**:

      * Set ``--job-name`` to ``init``.
      * Set ``NPROC`` to 42: this corresponds to the size of the grid as indicated in ``notebook_grid.f``.
      * Set the ``--nodes`` batch parameter to 2, so it can contains all needed CPUs.
      * Set ``EXE`` to ``bin/ORIGIN/symphonie.exe``.


      .. dropdown:: ``job.sh``

         .. code:: bash

            #!/bin/bash

            #SBATCH --job-name=init
            #SBATCH --nodes=2
            #SBATCH --ntasks-per-node=36
            #SBATCH --ntasks-per-core=1
            #SBATCH --time=15:00
            #SBATCH --output=slurm_%x-id_%j.out
            #SBATCH --error=slurm_%x-id_%j.err

            EXE=bin/ORIGIN/symphonie.exe
            NPROC=42
            INPUT=notebook_list.f

            ulimit -s unlimited

            module purge
            module load intel/18.2
            module load intelmpi/18.2
            module load hdf5/1.10.2-intelmpi
            module load netcdf/4.7.4-intelmpi
            module load pnetcdf/1.9.0-intelmpi
            module list 2>./run_modules

            echo -e "Launching...\n"

            mpiexec.hydra -np $NPROC $EXE $INPUT


Next, **submit the job** as follows
(and use ``squeue -u $USER`` to check on its status):

.. code:: bash

   sbatch job.sh


If the **initialization completes successfully**, tailing its output should print
something like this:

.. code:: console

   $ tail -n1 slurm_init*out
    RUN stopped after initial state as requested in notebooktime


And for what interests us, two ``description_*`` files should now exist in the run
directory:

.. code:: console

   $ ls -1 .
   authors_of_the_simulation
   bin
   currently_loaded_modulefiles
   description_domaine.next
   description_trous.txt
   GRAPHICS
   job.sh
   notebook_list.f
   NOTEBOOKS
   OFFLINE
   output_file_extension
   restart_input
   restart_outbis
   restart_output
   run_modules
   slurm_init-id_1746588.err
   slurm_init-id_1746588.out
   TIDES
   title_for_netcdf_files
   tmp


They are the two files we intended to generate. **Head** ``description_domaine.next``:

.. tab-set::

   .. tab-item:: HILO

      .. code:: console

         $ head -n3 description_domaine.next
              8     6    40           ! Number of sub-domains in each direction & nbdom
                  300         300  ! iglb jglb
         ------------------------


   .. tab-item:: CALMIP

      .. code:: console

         $ head -n3 description_domaine.next
              7     6    36           ! Number of sub-domains in each direction & nbdom
                  300         300  ! iglb jglb
         ------------------------


Three numbers are displayed on the first line: the two first are the initial grid
dimensions, and the last is the number of meshes in this grid which contain ocean cells.
This indicates us the **number of CPUs to use for our future runs**. Lucky us! This
is exactly the amount of CPUs in one node!

We are now ready to run SYMPHONIE in normal mode. Before that, however, quickly
**move the grid file somewhere safe**, i.e., out of the ``tmp`` directory (we will come
back to it very soon):

.. code:: bash

   mv tmp/grid.nc .


.. tip::

   If you're using a configuration in a long-term project and that you'll get to conduct
   several runs with the same domain and CPU allocation, you may want to store the
   ``description_*`` and ``grid.nc`` files in dedicated folders, **preventing you from
   rerunning initialization** each time.
