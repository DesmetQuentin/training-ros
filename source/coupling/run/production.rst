Production
==========

As a final stage of the training, let us execute a production run, restarting from
the spinup simulation we have just conducted.

First, **copy the namelist, notebook and job files**, using the ``cpl_production``
suffix:

.. code:: bash

   cd $RUN
   cp regcm/namelist-cpl_spinup.f regcm/namelist-cpl_production.f
   cp -r symphonie/NOTEBOOKS-cpl_spinup symphonie/NOTEBOOKS-cpl_production
   cp job-spinup.sh job-production.sh


And continue **renaming** key parameters to point to the newly copied files:

* Set the job file's ``--job-name`` to ``production``.
* Rename the input of RegCM in the job file to ``regcm/namelist-cpl_production.f``.
* Change the ``notebook_list.f``'s ``directory`` to ``symphonie/NOTEBOOKS-cpl_production``.


Then, let us configure our production simulation by following the dropdown sections
below.

.. dropdown:: 1. Simulation period and restart procedure

   For the OASIS part of the setup, let us **copy the correct restart files** in
   ``job-production.sh`` , i.e., with the 2018-07-10 date, by modifying the date on this
   line:

   .. code:: bash

      cp -p oasis/restart_20180710/*.nc .


   In terms of simulation duration, this production run will last one week just as the
   spinup simulation, i.e., ending 2018-07-17: we do not need to adapt OASIS's
   ``$RUNTIME``.

   Next, the **restart procedure** differs between RegCM and SYMPHONIE:

   .. tab-set::

      .. tab-item:: RegCM

         Set ``ifrest`` to ``.true.`` and adapt ``mdate1`` and ``mdate2`` to match
         the new start and end dates for the current simulation:

         .. code:: fortran

            !
            ! Model start/restart control
            !
            &restartparam
             ifrest  = .true.,     ! If a restart
             mdate0  = 2018070300, ! Global start (is globidate1)
             mdate1  = 2018071000, ! Start date of this run
             mdate2  = 2018071700, ! End date for this run
            /


      .. tab-item:: SYMPHONIE

         In ``notebook_time.f``, change ``initial`` to 1 and change the end date to
         match the end of the run, but keep the same start as for the overall project:

         .. code:: fortran

            ! Enter the time for the start and the end of the simulation:
            datesim(1:6,1)= 2018 , 07 , 03 , 00  , 00  , 00  ! Start time (yyyy mm dd hh mm ss)
            datesim(1:6,2)= 2018 , 07 , 17 , 00  , 00  , 00  ! End   time (yyyy mm dd hh mm ss)


         SYMPHONIE will know where the previous run stopped thanks to the files of the
         ``symphonie/restart_input`` folder. For now however, this folder is empty, and
         the files of interest were written out at the end of the spinup run in one of the
         ``symphonie/restart_out*`` folders. To know which one contains the last data,
         open the last slurm output (something like ``slurm_spinup*.out``) and look
         around the end for a line of this type:

         .. code::

            ecriture de ./symphonie/restart_outbis/chanel9_0


         with either ``restart_output`` or ``restart_outbis`` indicated (here
         ``restart_outbis``).


         Move the content of the right folder into ``symphonie/restart_input``, e.g.:

         .. code:: bash

            mv symphonie/restart_outbis/* symphonie/restart_input/


         .. tip::

            You may want to save this ``restart_input`` folder in case you want to rerun
            this simulation later:

            .. code:: bash

               cd $RUN/symphonie
               tar -czvf restart_input_20180710.tar.gz restart_input


   Now all modules, OASIS, RegCM and SYMPHONIE are set up to restart from the spinup
   simulation ending 2018-07-10.


.. dropdown:: 2. Re-enabling outputs

   This is the time to output all the data you need!

   .. tab-set::

      .. tab-item:: RegCM

         Open ``namelist-cpl_production.f`` and go to the ``outparam`` namelist.
         Do not (never) disable ``SAV`` outputs; they are still required for restarting.
         Decrease the output period for ``SRF`` to 3 hours. Then, enable ``ATM`` and
         ``RAD``.

         .. code:: fortran

            prestr  =     '',   ! string to prepend to output file names
            ifcordex = .false., ! Restrict to possible CORDEX variables
            outnwf  =     0.,   ! Day interval to open new files (0 = monthly)
            ifsave  = .true.,   ! Create SAV files for restart
            savfrq  =     0.,   ! Frequency in days to create them (0 = monthly)
            ifatm   = .true.,   ! Output ATM ?
            atmfrq  =     6.,   ! Frequency in hours to write to ATM
            ifrad   = .true.,   ! Output RAD ?
            radfrq  =     6.,   ! Frequency in hours to write to RAD
            ifsrf   = .true.,   ! Output SRF ?
            srffrq  =     3.,   ! Frequency in hours to write to SRF
            ifsts   = .false.,  ! Output STS (frequence is daily) ?
            ifshf   = .false.,  ! Output SHF (frequence is hourly) ?
            ifsub   = .false.,  ! Output SUB ?
            subfrq  =     6.,   ! Frequency in hours to write to SUB
            iflak   = .false.,  ! Output LAK ?
            lakfrq  =     6.,   ! Frequency in hours to write to LAK
            ifchem  = .false.,  ! Output CHE ?
            ifopt   = .false.,  ! Output OPT ?
            chemfrq =     6.,   ! Frequency in hours to write to CHE


      .. tab-item:: SYMPHONIE's ``GRAPHICS``

         In ``NOTEBOOKS-cpl_production``'s ``notebook_graph``, start by resetting
         the output frequency to hourly, i.e., 0.041666666 days. Then, enable (set
         switches to 1) about 5 variables you'd like to produce: this is up to you!


      .. tab-item:: SYMPHONIE's ``OFFLINE``

         At the end of the ``notebook_offline.f`` file in ``NOTEBOOKS-cpl_production``,
         let us add a new line indicating a smaller periodicity, e.g., 3 hours, until
         after the end of the simulation:

         .. code::

            Note: 1- no outputs if periodicity <=0
                  2- When the lastest date is passed, we continue with the latest periodicity
            DO NOT MODIFY THE NEXT LINE AS IT IS THE SIGNAL EXPECTED BY S TO START THE TIME LIST!!!!
            Periodicity (hours) ! until yyyy / mm / dd / hh / mm / ss ! Don't touch this line
            24.                         2018   07   10   00   00   00
            3.                          2018   07   17   00   00   00


         .. note::

            You could have written all lines from the spinup run, planning ahead which
            periodicity will apply for which period.


.. dropdown:: 3. Re-employing interpolation files

   To re-employ the interpolation files produced by ``SCRIPR`` during the spinup run,
   let us first make sure to **retrieve** ``rmp*.nc`` **files before running**, adding
   this line to ``job-production.sh``:

   .. code:: bash

      cp -p oasis/rmp*.nc .


   Then, we need to **use the** ``MAPPING`` **transformation** in place of ``SCRIPR``,
   pointing to the appropriate files (there is one for each grid dipole and direction).
   You should end up with the following ``namcouple`` file:

   .. code::

      # This is a typical input file for OASIS3-MCT.
      # Keywords used in previous versions of OASIS3
      # but now obsolete are marked "Not used"
      # Don't hesitate to ask precisions or make suggestions (oasishelp@cerfacs.fr).
      #
      # Any line beginning with # is ignored. Blank lines are not allowed.
      #
      ################### -= FIRST SECTION =- ###################################
      $NNOREST
      # T (true) or F (false): make the restart file facultative, i.e. if absent
      # fields are initialized with zero values
      #
        F
      #--------------------------------------------------------------------------
      $NFIELDS
      # >= total number of field entries
      #
        5
      #--------------------------------------------------------------------------
      $RUNTIME
      # The total simulated time for this run in seconds
      #
        604800
      #--------------------------------------------------------------------------
      $NLOGPRT
      # Amount of information written to OASIS3-MCT log files (see User Guide)
      #
        0  0  0
      ################### -= SECOND SECTION =- ##################################
      $STRINGS
      # The above variables are the general parameters for the experiment.
      # Everything below has to do with the fields being exchanged.
      #
        RCM_TAUX:RCM_TAUY:RCM_NDSW SYM_TAUX:SYM_TAUY:SYM_SSRF 1 3600 2 restart_tau-sw.nc EXPORTED
        58 58 300 300 rcim symt LAG=+180
        R  0  R  0
        LOCTRANS MAPPING
        AVERAGE
        rmp_rcim_to_symt_BILINEAR.nc src opt
      #
        RCM_PREC SYM_PREC 1 3600 3 restart_PREC.nc EXPORTED
        58 58 300 300 rcim symt LAG=+180
        R  0  R  0
        LOCTRANS BLASOLD MAPPING
        AVERAGE
        0.001 0
        rmp_rcim_to_symt_BILINEAR.nc src opt
      #
        RCM_ULHF:RCM_USHF:RCM_NULW SYM_SLHF:SYM_SSHF:SYM_SNSF 1 3600 3 restart_lat-sens-lw.nc EXPORTED
        58 58 300 300 rcim symt LAG=+180
        R  0  R  0
        LOCTRANS BLASOLD MAPPING
        AVERAGE
        -1 0
        rmp_rcim_to_symt_BILINEAR.nc src opt
      #
        RCM_SLP SYM_SLP 1 3600 2 restart_SLP.nc EXPORTED
        60 60 300 300 rcem symt LAG=+180
        R  0  R  0
        LOCTRANS MAPPING
        AVERAGE
        rmp_rcem_to_symt_BILINEAR.nc src opt
      #
        SYM_SST RCM_SST 1 3600 2 restart_SST.nc EXPORTED
        300 300 58 58 symt rcim LAG=+180
        R  0  R  0
        LOCTRANS MAPPING
        AVERAGE
        rmp_symt_to_rcim_BILINEAR.nc src opt
      ###########################################################################


Once everythin is is set up, **save the** ``namcouple`` **file** with:

.. code:: bash

   cp namcouple oasis/namcouple-production


Your job file should now look like the following:

.. dropdown:: ``job-production.sh``

   .. tab-set::

      .. tab-item:: CALMIP

         .. code:: bash

            #!/bin/bash

            #SBATCH --job-name=production
            #SBATCH --nodes=2
            #SBATCH --ntasks-per-node=36
            #SBATCH --ntasks-per-core=1
            #SBATCH --time=20:00
            #SBATCH --output=slurm_%x-id_%j.out
            #SBATCH --error=slurm_%x-id_%j.err

            EXE1=regcm/bin/regcmMPICLM45_OASIS
            NPROC1=36
            INPUT1=regcm/namelist-cpl_production.f
            #
            EXE2=symphonie/bin/OASIS/symphonie.exe
            NPROC2=36
            INPUT2=symphonie/notebook_list.f

            ulimit -s unlimited

            module purge
            module load intel/18.2
            module load intelmpi/18.2
            module load hdf5/1.10.2-intelmpi
            module load netcdf/4.7.4-intelmpi
            module load pnetcdf/1.9.0-intelmpi
            module list 2>./run_modules

            cp -p oasis/{areas,grids,masks}.nc .
            cp -p oasis/restart_20180710/*.nc .
            cp -p oasis/rmp*.nc .

            echo -e "Launching...\n"

            mpiexec.hydra -np $NPROC1 $EXE1 $INPUT1 : -np $NPROC2 $EXE2 $INPUT2


      .. tab-item:: HILO

         .. code:: bash

            #!/bin/bash

            #SBATCH --job-name=production
            #SBATCH --partition=scalable
            #SBATCH --nodes=2
            #SBATCH --ntasks-per-node=40
            #SBATCH --ntasks-per-core=1
            #SBATCH --time=20:00
            #SBATCH --output=slurm_%x-id_%j.out
            #SBATCH --error=slurm_%x-id_%j.err

            EXE1=regcm/bin/regcmMPICLM45_OASIS
            NPROC1=40
            INPUT1=regcm/namelist-cpl_production.f
            #
            EXE2=symphonie/bin/OASIS/symphonie.exe
            NPROC2=40
            INPUT2=symphonie/notebook_list.f

            ulimit -s unlimited

            module purge
            module load intel/2019.u5
            module load hdf5/1.8.15p1_intel_64
            module load mvapich2/2.3.6_intel
            module load netcdf/4.6.1_intel_64
            module load PnetCDF/1.9.0_intel_64
            module list 2>./run_modules

            cp -p oasis/{areas,grids,masks}.nc .
            cp -p oasis/restart_20180710/*.nc .
            cp -p oasis/rmp*.nc .

            echo -e "Launching...\n"

            mpiexec.hydra -np $NPROC1 $EXE1 $INPUT1 : -np $NPROC2 $EXE2 $INPUT2


For the rest, the setup should be the same as for the spinup simulation, so,
after making sure to delete the content of SYMPHONIE's ``tmp`` folder, you may **submit
the job** and wait for its completion.

To end the simulation flow properly, let us simply **save the last restart files**:

.. code:: bash

   mkdir oasis/restart_20180717
   mv restart*.nc oasis/restart_20180717/
