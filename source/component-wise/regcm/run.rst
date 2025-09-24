Running and outputs
===================

Let us now **edit the** ``job.sh`` **batch script**. In the header, lines starting by
``#SBATCH`` contain the workload keywords to book computing nodes. The file
then consists of ``bash`` language commands to prepare and launch RegCM, once on the
computing nodes' session.

For this uncoupled run of RegCM, we especially care about the following parameters:

* The ``--nodes`` batch parameter set to 1;
* ``--ntasks-per-node`` and ``NPROC`` must be identical and adapted to the supercomputer architecture (36 on CALMIP; 40 on HILO);
* The ``EXE`` variable set to ``bin/regcmMPICLM45``.


.. dropdown:: ``job.sh``

   .. tab-set::

      .. tab-item:: CALMIP

         .. code:: bash

            #!/bin/bash

            #SBATCH --job-name=regcm
            #SBATCH --nodes=1
            #SBATCH --ntasks-per-node=36
            #SBATCH --ntasks-per-core=1
            #SBATCH --time=10:00
            #SBATCH --output=slurm_%x-id_%j.out
            #SBATCH --error=slurm_%x-id_%j.err

            EXE=bin/regcmMPICLM45
            NPROC=36
            INPUT=namelist.f

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


      .. tab-item:: HILO

         .. code:: bash

            #!/bin/bash

            #SBATCH --job-name=regcm
            #SBATCH --ntasks=40
            #SBATCH --cpus-per-task=1
            #SBATCH --time=10:00
            #SBATCH --output=slurm_%x-id_%j.out
            #SBATCH --error=slurm_%x-id_%j.err

            EXE=bin/regcmMPICLM45
            NPROC=40
            INPUT=namelist.f

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


After ``job.sh`` is set up, we can **submit** it as follows:

.. code:: bash

   sbatch job.sh


The following command can then be used to to **check on your job's status**:

.. code:: bash

   squeue -u $USER


If the **job completes successfully**, tailing its output should print something like
this:

.. code:: console

   $ tail slurm*.out
                     solar TSI irradiance    =    1361.3264 W/m^2
   ATM variables written at  2018-07-10 00:00:00 UTC
   SRF variables written at  2018-07-10 00:00:00 UTC
   SAV variables written at  2018-07-10 00:00:00 UTC
   Final time  2018-07-10 00:00:00 UTC reached.
   Elapsed seconds of run for this final timeslice :    178.6434
   : this run stops at  : 2025-09-13 16:03:18+0200
   : Run has been completed using           36  processors.
   : Total elapsed seconds of run :    178.644547998718
   RegCM V5 simulation successfully reached end


And the ``output`` directory should now contain several new files, i.e., the **outputs
of the simulation**:

.. code:: console

   $ ls -1 output
   QUYNHON.2018070300.txt
   QUYNHON_ATM.2018070300.nc
   QUYNHON.clm.regcm.r.2018071000.nc
   QUYNHON.clm.regcm.rh0.2018071000.nc
   QUYNHON_SAV.2018071000.nc
   QUYNHON_SRF.2018070300.nc


Below is a brief description of what they contain:

.. list-table::
   :header-rows: 1

   * - Output key
     - Description
   * - ``ATM``
     - 3D thermodynamics
   * - ``SRF``
     - 2D surface fields (including precipitation)
   * - ``SAV`` and ``clm``
     - Data necessary for restarting


You may explore them using ``ncview`` and/or ``ncdump -h``.
In any case, we are done with the uncoupled framework of RegCM and you can proceed to
the next part.
