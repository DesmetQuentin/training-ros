Initialization
==============

Although SYMPHONIE does not provide any preprocessing program, the
``symphonie.exe`` program **can be ran only for its initialization part**, i.e.,
stopping right before entering the main model loop. This allows users to check whether
the notebook configuration is well interpreted by the model, but also to trigger some,
checks, debugging outputs or preliminary analyses without committing to book computing
nodes for the long run.

In particular, on this page, we are going to run an initialization to determine the
CPU allocation of our configuration. Indeed, as an ocean model, **SYMPHONIE does not
need to book computing resources for land-only areas of the domain**. This way, instead
of simply dividing the domain into a grid then assigning each CPU with one mesh in this
grid, we want, in addition, to filter out the land-only meshes, ultimately resulting in
a reduced need of computing resources. In this context, let us set up an initialization
run to compute which parts of the grid are land-only and can thus be ignored. The
results will be in the form of two files, the one informing of the land-only meshes to
be ignored, and the other for the rest of the grid.

First, change/check the values of the following **notebook parameters**:

.. list-table::
   :header-rows: 1

   * - File
     - Variable and value
     - Comment
   * - ``notebook_time.f``
     - ``run_option = -1``
     - Enables the initialization mode.
   * - ``notebook_grid.f``
     - ``kmax = 1``
     - One only vertical layer makes it quicker.
   * - ``notebook_vertcoord.f``
     - ``flag_merged_levels = 0``
     - Goes with ``kmax = 1``.
   * - ``notebook_grid.f``
     - ``nbdom_imax = 6`` and ``nbdom_jmax = 10``
     - The initial grid dimensions.
   * - ``notebook_grid.f``
     - ``mpi_map_file_name = 'default'`` and ``mpi_hole_plugging = 'none'``
     - These variables should point to the very two files we want to generate with the initialization run. Setting them to their defaults triggers their computation.


And make sure that you are pointing to the right ``NOTEBOOKS`` folder by **editing**
``notebook_list.f``. 
   
Then, **edit the** ``job.sh`` **batch script**:

* Set ``--job-name`` to ``'init'``.
* Set ``NPROC`` to 60: this corresponds to the size of the grid as indicated in ``notebook_grid.f``.
* Set the ``--nodes`` batch parameter to 2, so it can contains the 60 needed CPUs.
* Set ``DIR`` to the current run directory.
* Set ``EXE`` to ``./bin/ORIGIN/symphonie.exe``.


.. dropdown:: ``job.sh``

   .. code:: bash

      #!/bin/bash

      #SBATCH --job-name=init
      #SBATCH --nodes=2
      #SBATCH --ntasks-per-node=36
      #SBATCH --ntasks-per-core=1
      #SBATCH --time=1:00:00
      #SBATCH --output=slurm_%x-id_%j.out
      #SBATCH --error=slurm_%x-id_%j.err

      DIR=/tmpdir/desmet/TRAINING_CPL/symphonie # <-- make sure to modify here!
      EXE=./bin/ORIGIN/symphonie.exe # from DIR
      NPROC=60
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

   $ ls -1rt .
   TIDES
   restart_output
   restart_outbis
   restart_input
   bin
   notebook_list.f
   title_for_netcdf_files
   job.sh
   NOTEBOOKS
   run_modules
   slurm_init-id_1693377.err
   description_trous.txt
   description_domaine.next
   OFFLINE
   currently_loaded_modulefiles
   authors_of_the_simulation
   tmp
   slurm_init-id_1693377.out
   output_file_extension
   GRAPHICS


They are the two files we intended to generate. **Head** ``description_domaine.next``:

.. code:: console

   $ head -n3 description_domaine.txt
        6    10    36           ! Number of sub-domains in each direction & nbdom
            245         420  ! iglb jglb
   ------------------------


Three numbers are displayed on the first line: the two first are the initial grid
dimensions, and the last is the number of meshes in this grid which contain ocean cells.
This indicates us the **number of CPUs to use for our future runs: 36**. Lucky us! This
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
