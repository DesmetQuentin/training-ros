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
   ``job-production.sh`` , i.e. with the 2018-07-10 date, by modifying the date on this
   line:

   .. code:: bash

      cp -p oasis/restart_20180710/*.nc .

   
   In terms of simulation duration, this production run will last one week just as the
   spinup simulation, i.e. ending 2018-07-17: we do not need to adapt OASIS ``$RUNTIME``.

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
         the files of interest were writen out at the end of the spinup run in one of the
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


.. dropdown:: 2. Re-employing interpolation files

   To re-employ the interpolation files produced by ``SCRIPR`` during the spinup run,
   let us first make sure to **retrieve** ``rmp*.nc`` **files before running**, adding
   this lines to ``job-production.sh``:

   .. code:: bash

      cp -p oasis/rmp*.nc .

   
   Then, we need to **use the** ``MAPPING`` **transformation** in place of ``SCRIPR``,
   pointing to the appropriate files (there is one for each grid dipole and direction).
   You should end up with the following ``namcouple`` file::

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


   Once this is set up, **save the** ``namcouple`` **file** with:

   .. code:: bash

      cp namcouple oasis/namcouple-production


For the rest, the setup should be the same as for the spinup simulation, so,
after making sure to delete the content of SYMPHONIE's ``tmp`` folder, you may **submit
the job** and wait for its completion.

To end the simulation flow properly, let us simply **save the last restart files**:

.. code:: bash

   mkdir oasis/restart_20180717
   mv restart*.nc oasis/restart_20180717/
