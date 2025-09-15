Spinup
======

With our initialization files ready, let us prepare and run a spinup simulation.

.. note::
   
   In a realistic setup, the duration of a spinup run depends on each model and is often
   dimensioned by the time required by the ocean to stabilize its domain-integrated
   turbulent kinetic energy. It should be about within the 6 months to 1 year interval.


First, **copy the namelist, notebook and job files**, using the ``cpl_spinup`` suffix:

.. code:: bash

   cd $RUN
   cp regcm/namelist-cpl_init.f regcm/namelist-cpl_spinup.f
   cp -r symphonie/NOTEBOOKS-cpl_init symphonie/NOTEBOOKS-cpl_spinup
   mv job.sh job-init.sh
   cp job-init.sh job-spinup.sh


And continue **renaming** key parameters to point to the newly copied files:

* Set the job file's ``--job-name`` to ``spinup``.
* Rename the input of RegCM in the job file to ``regcm/namelist-cpl_spinup.f``.
* For SYMPHONIE however, let us keep ``notebook_list.f`` in ``job-spinup.sh``, but instead change the ``notebook_list.f``'s ``directory`` to ``symphonie/NOTEBOOKS-cpl_spinup``.


Then, let us configure our spinup simulation by following the dropdown sections below.

.. dropdown:: 1. Simulation period and restart files

   Plans are to make the simulation run from 2018-07-03 to 2018-07-17, i.e., two
   weeks, with one week for spinup and one week for production. The **spinup run is thus
   from 2018-07-03 to 2018-07-10**, but RegCM's global dates must cover the whole period,
   like we did for the :doc:`uncoupled setup <../../component-wise/regcm/preprocess>`.

   Change RegCM's ``gdate*`` to:

   .. code:: fortran

      gdate1 = 2018070300,        ! Start date for ICBC data generation
      gdate2 = 2018071700,        ! End data for ICBC data generation

   
   and the ``restartparam`` namelist as follows:

   .. code:: fortran

      !
      ! Model start/restart control
      !
      &restartparam
       ifrest  = .false.,    ! If a restart
       mdate0  = 2018070300, ! Global start (is globidate1)
       mdate1  = 2018070300, ! Start date of this run
       mdate2  = 2018071000, ! End date for this run
      /

   
   Also adapt SYMPHONIE's ``datesim`` in ``notebook_time.f``, and OASIS' ``$RUNTIME`` in
   ``namcouple`` (with one week in seconds, i.e., 604800).

   Lastly, make sure the right restart files are accounted for by adding these lines to
   ``job-cpl_spinup.sh``, just before launching:

   .. code:: bash

      cp -p oasis/restart_20180703/*.nc .


   Of course, this goes with a ``namcouple`` ``$NNOREST`` section set to ``F`` (false).


.. dropdown:: 2. Securing grid files

   OASIS grid files has already been written by the
   :doc:`initialization run <initialize>`, thus we can **reuse them** instead of
   overwriting them with each simulation.

   Disable the ``l_write_grids`` logicals for RegCM and SYMPHONIE, then add the
   following lines to the job file, besides those about restart files:

   .. code:: bash

      cp -p oasis/{areas,grids,masks}.nc .

   
.. dropdown:: 3. Configuring air-sea flux coupling for the models

   In comparison with the :doc:`initialization <initialize>` when only exporting fields
   were enabled, we now **enable exporting and importing fields**.

   In addition, we need to tell SYMPHONIE that it will retrieve its sea-surface fluxes
   from OASIS, instead of using external data. This is done by modifying
   ``flag_meteodata`` in ``notebook_airseaflux_s26.f``:

   .. code:: fortran

      flag_meteodata='oasisflux'       ! Meteorological model key (ecmwf glorys
                                       !                          [oasisflux oasisbulk])


.. dropdown:: 4. Configuring the ``namcouple`` in ``EXPORTED`` mode

   After linking every enabled coupling field between RegCM and SYMPHONIE, taking care
   of grid dimensions, signs, units and interpolations, the ``namcouple`` for this
   spinup run should be this:

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
      LOCTRANS SCRIPR
      AVERAGE
      BILINEAR LR SCALAR LATLON 1
      #
      RCM_PREC SYM_PREC 1 3600 3 restart_PREC.nc EXPORTED
      58 58 300 300 rcim symt LAG=+180
      R  0  R  0
      LOCTRANS BLASOLD SCRIPR
      AVERAGE
      0.001 0
      BILINEAR LR SCALAR LATLON 1
      #
      RCM_ULHF:RCM_USHF:RCM_NULW SYM_SLHF:SYM_SSHF:SYM_SNSF 1 3600 3 restart_lat-sens-lw.nc EXPORTED
      58 58 300 300 rcim symt LAG=+180
      R  0  R  0
      LOCTRANS BLASOLD SCRIPR
      AVERAGE
      -1 0
      BILINEAR LR SCALAR LATLON 1
      #
      RCM_SLP SYM_SLP 1 3600 2 restart_SLP.nc EXPOUT
      60 60 300 300 rcem symt LAG=+180
      R  0  R  0
      LOCTRANS SCRIPR
      AVERAGE
      BILINEAR LR SCALAR LATLON 1
      #
      SYM_SST RCM_SST 1 3600 2 restart_SST.nc EXPORTED
      300 300 58 58 symt rcim LAG=+180
      R  0  R  0
      LOCTRANS SCRIPR
      AVERAGE
      BILINEAR LR SCALAR LATLON 1
      ###########################################################################


   Once this is set up, **save it** with:

   .. code:: bash

      cp namcouple oasis/namcouple-spinup


Before submitting the job, ``job-spinup.sh`` should now look like this:

.. dropdown:: ``job-spinup.sh``

   .. code:: bash

      #!/bin/bash

      #SBATCH --job-name=spinup
      #SBATCH --nodes=2
      #SBATCH --ntasks-per-node=36
      #SBATCH --ntasks-per-core=1
      #SBATCH --time=20:00
      #SBATCH --output=slurm_%x-id_%j.out
      #SBATCH --error=slurm_%x-id_%j.err

      EXE1=regcm/bin/regcmMPICLM45_OASIS
      NPROC1=36
      INPUT1=regcm/namelist-cpl_spinup.f
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
      cp -p oasis/restart_20180703/*.nc .

      echo -e "Launching...\n"

      mpiexec.hydra -np $NPROC1 $EXE1 $INPUT1 : -np $NPROC2 $EXE2 $INPUT2


Make sure to delete SYMPHONIE's ``tmp`` folder, then **submit the job** and wait for
its completion.

Once completed, you should notice the files generated by the ``SCRIPR`` interpolation
library:

.. code:: console

   $ ls -1 rmp*.nc
   rmp_rcem_to_symt_BILINEAR.nc
   rmp_rcim_to_symt_BILINEAR.nc
   rmp_symt_to_rcim_BILINEAR.nc


**Save those files**, as well as the restart files written at the end of the simulation:

.. code:: bash

   mv rmp*.nc oasis/
   mkdir oasis/restart_20180710
   mv restart*.nc oasis/restart_20180710/


You ``oasis`` folder should now look like this:

.. code:: console

   $ ls -1 oasis
   areas.nc
   grids.nc
   masks.nc
   namcouple-cpl_init
   namcouple-cpl_spinup
   restart_20180703
   restart_20180710
   rmp_rcem_to_symt_BILINEAR.nc
   rmp_rcim_to_symt_BILINEAR.nc
   rmp_symt_to_rcim_BILINEAR.nc
