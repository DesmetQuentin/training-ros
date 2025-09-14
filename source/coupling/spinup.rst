Running a spinup
================

* copy namelists ``cpl_spinup``
* copy job and edit job ``spinup``
   * name is ``spinup``
   * cp grid files and restart
   * namelists and notebook_list

.. dropdown:: job.sh

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


* time
   * all dates as before for regcm
   * 3rd to 10th for symphonie
   * 7 days in namcouple
* namelists
   * enable import
   * disable grid writing
   * airseaflux for symphonie
* namcouple
   EXPORTED
   FAlse

.. dropdown:: namcouple

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


* copy namcouple in oasis
* delete symphonie/tmp
* run
* save rmp*.nc files
* save restart* files in restart_20180710
