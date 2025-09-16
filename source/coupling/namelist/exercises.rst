Hands-on exercises
==================

We have gone through the three namelist frameworks of the system relating to configuring
field exchange through OASIS. Let us now practice setting up specific field exchanges
consistently between OASIS and the two components.

Create a new directory for this page:

.. code:: console

   $ bash $TRAINING/scripts/make_practice_directory.sh $PRACTICE
   $ cd $PRACTICE
   $ ls -1
   namcouple
   namelist.f
   notebook_oasis_generic.f


For each practice, propose a solution for RegCM's ``oasisparam``, SYMPHONIE's
``notebook_oasis_generic.f`` and (a) field entry(ies) for OASIS's ``namcouple``.
Then, open the dropdown section to see the solution.


Exercise 1
----------

**Task:** Exchange instantaneous sea level pressure and sea surface temperature between
the two models, with a coupling period of 30 minutes.

**Model key features:**

+-----------------+--------------+-------------------+
|                 | RegCM        | SYMPHONIE         |
+=================+==============+===================+
| Grid dimensions | ``jx = 100`` | ``iglb = 200``    |
|                 | ``iy = 150`` | ``jglb = 300``    |
+-----------------+--------------+-------------------+
| Timestep        | ``dt = 60.`` | ``dti_fw = 180.`` |
+-----------------+--------------+-------------------+


.. dropdown:: Solution

   .. tab-set::

      .. tab-item:: ``namcouple`` entries

         .. code::

              RCM_SLP SYM_SLP 1 1800 1 restart_SLP.nc EXPORTED
              99 149 200 300 rcem symt LAG=+60
              R  0  R  0
              SCRIPR
              BILINEAR LR SCALAR LATLON 1
            #
              SYM_SST RCM_SST 1 1800 1 restart_SST.nc EXPORTED
              200 300 97 147 symt rcim LAG=+180
              R  0  R  0
              SCRIPR
              BILINEAR LR SCALAR LATLON 1

      
         **Key points:**

         * The 30 minute coupling period is in seconds.
         * Grid dimensions for ``rcim`` (used for sea surface temperature) are reduced by two when compared to ``rcem`` (used for sea level pressure).
         * The ``LAG`` takes the same value as the sender's timestep.
         * Only one transformation is required: for interpolation (``MAPPING`` instead of ``SCRIPR`` is accepted as well).


      .. tab-item:: RegCM's ``oasisparam``

         .. code:: fortran
            
            !
            ! OASIS parameters
            !
            &oasisparam
             write_restart_option = 2, ! 0 => no restart file writing
                                       ! 1 => write restart files at the first time
                                       ! 2 => write restart files at the last time
                                       ! 3 => both 1 & 2
             l_write_grids = .true.,   ! For writing grids.nc, areas.nc, masks.nc.
             oasis_sync_lag = 0,       ! Synchronisation lag with other components (sec)
                                       ! > 0 => Regcm starts late
                                       ! < 0 => Regcm starts in advance
                                       ! Should be a multipe of the coupling period
                                       !   in the namcouple.
                                       ! In the namcouple, RUNTIME must have
                                       !   the run duration + oasis_sync_lag.
                                       !------ NAMCOUPLE FIELD ENTRIES ------
                                       ! field    | grid
                                       !-------------------------------------
             l_cpl_im_sst  = .true.,   ! RCM_SST  | rcim     
             l_cpl_im_wz0  = .false.,  ! RCM_WZ0  | rcim     
             l_cpl_im_wust = .false.,  ! RCM_WUST | rcim     
             l_cpl_ex_u10m = .false.,  ! RCM_U10M | rcin/rcim
             l_cpl_ex_v10m = .false.,  ! RCM_V10M | rcin/rcim
             l_cpl_ex_wspd = .false.,  ! RCM_WSPD | rcin/rcim
             l_cpl_ex_wdir = .false.,  ! RCM_WDIR | rcin/rcim
             l_cpl_ex_t2m  = .false.,  ! RCM_T2M  | rcin/rcim
             l_cpl_ex_q2m  = .false.,  ! RCM_Q2M  | rcin/rcim
             l_cpl_ex_slp  = .true.,   ! RCM_SLP  | rcen/rcem
             l_cpl_ex_taux = .false.,  ! RCM_TAUX | rcin/rcim
             l_cpl_ex_tauy = .false.,  ! RCM_TAUY | rcin/rcim
             l_cpl_ex_z0   = .false.,  ! RCM_Z0   | rcin/rcim
             l_cpl_ex_ustr = .false.,  ! RCM_USTR | rcin/rcim
             l_cpl_ex_evap = .false.,  ! RCM_EVAP | rcin/rcim
             l_cpl_ex_prec = .false.,  ! RCM_PREC | rcin/rcim
             l_cpl_ex_nuwa = .false.,  ! RCM_NUWA | rcin/rcim
             l_cpl_ex_ulhf = .false.,  ! RCM_ULHF | rcin/rcim
             l_cpl_ex_ushf = .false.,  ! RCM_USHF | rcin/rcim
             l_cpl_ex_uwlw = .false.,  ! RCM_UWLW | rcin/rcim
             l_cpl_ex_dwlw = .false.,  ! RCM_DWLW | rcin/rcim
             l_cpl_ex_nulw = .false.,  ! RCM_NULW | rcin/rcim
             l_cpl_ex_uwsw = .false.,  ! RCM_UWSW | rcin/rcim
             l_cpl_ex_dwsw = .false.,  ! RCM_DWSW | rcin/rcim
             l_cpl_ex_ndsw = .false.,  ! RCM_NDSW | rcin/rcim
             l_cpl_ex_rhoa = .false.,  ! RCM_RHOA | rcin/rcim
                                      !------ NAMCOUPLE FIELD ENTRIES ------
            /

      
      .. tab-item:: SYMPHONIE's ``notebook_oasis_generic.f``

         .. code:: fortran
            
            &notebook_oasis_generic
            ! https://docs.google.com/document/d/1stIu_SuZY7l729gXjDB-LS37fAPGyDexNmeieQ07-eA/edit#

             ioasis_generic = 1         ! enables OASIS coupling
             write_restart_option = 2   ! 0 => not writing any restart files
                                        ! 1 => writing restart files at the first oasis_put processes
                                        ! 2 => writing restart files at the last oasis_put processes
                                        ! 3 => both 1 & 2
             l_write_grids = .true.     ! for writing grids.nc, areas.nc, masks.nc (by OASIS)
                                        ! --> put .false. if these already exist.
                                        ! --> if .true., then indicate the SYMPHONIE grid below.

            ! The grid.nc describing the global grid when no land proc has been removed.
             default_grid_file_name = 'grid.nc'
            !default_grid_file_name = 'default' ! indicates the grid.nc that will be produced
                                                ! in the tmp directory.

             oasis_sync_lag = 0         ! synchronisation lag with other components (sec)
                                        ! > 0 => SYMPHONIE starts late
                                        ! < 0 => SYMPHONIE starts in advance
                                        ! should be equal to the coupling period in the
                                        !   namcouple
                                        ! in the namcouple, RUNTIME must have the run
                                        !   duration + |oasis_sync_lag|
             oasis_dummy_dt = 180       ! model time step to use during the dummy loops
                                        !   for filling the lag
                                        ! should be equal to the LAG parameter in the
                                        !   namcouple
 
                                        !------ NAMCOUPLE FIELD ENTRIES ------
                                        ! field    | grid
                                        !-------------------------------------
             l_cpl_im_wndu = .false.    ! SYM_WNDU | symt
             l_cpl_im_wndv = .false.    ! SYM_WNDV | symt
             l_cpl_im_t2m  = .false.    ! SYM_T2M  | symt
             l_cpl_im_t10m = .false.    ! SYM_T10M | symt
             l_cpl_im_q2m  = .false.    ! SYM_Q2M  | symt
             l_cpl_im_q10m = .false.    ! SYM_Q10M | symt
             l_cpl_im_slp  = .true.     ! SYM_SLP  | symt
             l_cpl_im_taux = .false.    ! SYM_TAUX | symt
             l_cpl_im_tauy = .false.    ! SYM_TAUY | symt
             l_cpl_im_evap = .false.    ! SYM_EVAP | symt
             l_cpl_im_prec = .false.    ! SYM_PREC | symt
             l_cpl_im_watf = .false.    ! SYM_WATF | symt
             l_cpl_im_slhf = .false.    ! SYM_SLHF | symt
             l_cpl_im_sshf = .false.    ! SYM_SSHF | symt
             l_cpl_im_snsf = .false.    ! SYM_SNSF | symt
             l_cpl_im_dnsf = .false.    ! SYM_DNSF | symt
             l_cpl_im_ssrf = .false.    ! SYM_SSRF | symt
             l_cpl_im_dsrf = .false.    ! SYM_DSRF | symt
             l_cpl_ex_sst  = .true.     ! SYM_SST  | symt
             l_cpl_ex_ssh  = .false.    ! SYM_SSH  | symt
             l_cpl_ex_ocnu = .false.    ! SYM_OCNU | symt
             l_cpl_ex_ocnv = .false.    ! SYM_OCNV | symt
                                        !------ NAMCOUPLE FIELD ENTRIES ------
            /


Exercise 2
----------

**Task:** Send averaged surface fluxes of latent and sensible heat from RegCM to
SYMPHONIE, with a coupling period of 1 hour.

**Model key features:**

+-----------------+--------------+-------------------+
|                 | RegCM        | SYMPHONIE         |
+=================+==============+===================+
| Grid dimensions | ``jx = 112`` | ``iglb = 243``    |
|                 | ``iy = 156`` | ``jglb = 338``    |
+-----------------+--------------+-------------------+
| Timestep        | ``dt = 90.`` | ``dti_fw = 120.`` |
+-----------------+--------------+-------------------+


.. dropdown:: Solution

   .. tab-set::

      .. tab-item:: ``namcouple`` entries

         .. code::

            RCM_ULHF:RCM_USHF SYM_SLHF:SYM_SSHF 1 3600 3 restart_TURB.nc EXPORTED
            109 153 243 338 rcim symt LAG=+90
            R  0  R  0
            LOCTRANS BLASOLD MAPPING
            AVERAGE
            -1 0
            rmp_rcim_to_symt_BILINEAR.nc src opt

      
         **Key points:**

         * Only one entry is needed, using the colon separator for field names.
         * ``LOCTRANS`` is employed to average the fields over the coupling period.
         * Those fluxes have a different sign convention in the two models: it is positive upward in RegCM, and positive downward in SYMPHONIE. As a result, the sign must be changed using a ``BLASOLD`` transformation.
         * Interpolation employs a ``MAPPING`` here, but using ``SCRIPR`` instead is accespted.
         * The number of transformation is now 3.


      .. tab-item:: RegCM's ``oasisparam``

         .. code:: fortran
            
            !
            ! OASIS parameters
            !
            &oasisparam
             write_restart_option = 2, ! 0 => no restart file writing TODO
                                       ! 1 => write restart files at the first time
                                       ! 2 => write restart files at the last time
                                       ! 3 => both 1 & 2
             l_write_grids = .true.,   ! For writing grids.nc, areas.nc, masks.nc.
             oasis_sync_lag = 0,       ! Synchronisation lag with other components (sec)
                                       ! > 0 => Regcm starts late
                                       ! < 0 => Regcm starts in advance
                                       ! Should be a multipe of the coupling period
                                       !   in the namcouple.
                                       ! In the namcouple, RUNTIME must have
                                       !   the run duration + oasis_sync_lag.
                                       !------ NAMCOUPLE FIELD ENTRIES ------
                                       ! field    | grid
                                       !-------------------------------------
             l_cpl_im_sst  = .false.,  ! RCM_SST  | rcim     
             l_cpl_im_wz0  = .false.,  ! RCM_WZ0  | rcim     
             l_cpl_im_wust = .false.,  ! RCM_WUST | rcim     
             l_cpl_ex_u10m = .false.,  ! RCM_U10M | rcin/rcim
             l_cpl_ex_v10m = .false.,  ! RCM_V10M | rcin/rcim
             l_cpl_ex_wspd = .false.,  ! RCM_WSPD | rcin/rcim
             l_cpl_ex_wdir = .false.,  ! RCM_WDIR | rcin/rcim
             l_cpl_ex_t2m  = .false.,  ! RCM_T2M  | rcin/rcim
             l_cpl_ex_q2m  = .false.,  ! RCM_Q2M  | rcin/rcim
             l_cpl_ex_slp  = .false.,  ! RCM_SLP  | rcen/rcem
             l_cpl_ex_taux = .false.,  ! RCM_TAUX | rcin/rcim
             l_cpl_ex_tauy = .false.,  ! RCM_TAUY | rcin/rcim
             l_cpl_ex_z0   = .false.,  ! RCM_Z0   | rcin/rcim
             l_cpl_ex_ustr = .false.,  ! RCM_USTR | rcin/rcim
             l_cpl_ex_evap = .false.,  ! RCM_EVAP | rcin/rcim
             l_cpl_ex_prec = .false.,  ! RCM_PREC | rcin/rcim
             l_cpl_ex_nuwa = .false.,  ! RCM_NUWA | rcin/rcim
             l_cpl_ex_ulhf = .true.,   ! RCM_ULHF | rcin/rcim
             l_cpl_ex_ushf = .true.,   ! RCM_USHF | rcin/rcim
             l_cpl_ex_uwlw = .false.,  ! RCM_UWLW | rcin/rcim
             l_cpl_ex_dwlw = .false.,  ! RCM_DWLW | rcin/rcim
             l_cpl_ex_nulw = .false.,  ! RCM_NULW | rcin/rcim
             l_cpl_ex_uwsw = .false.,  ! RCM_UWSW | rcin/rcim
             l_cpl_ex_dwsw = .false.,  ! RCM_DWSW | rcin/rcim
             l_cpl_ex_ndsw = .false.,  ! RCM_NDSW | rcin/rcim
             l_cpl_ex_rhoa = .false.,  ! RCM_RHOA | rcin/rcim
                                      !------ NAMCOUPLE FIELD ENTRIES ------
            /

      
      .. tab-item:: SYMPHONIE's ``notebook_oasis_generic.f``

         .. code:: fortran
            
            &notebook_oasis_generic
            ! https://docs.google.com/document/d/1stIu_SuZY7l729gXjDB-LS37fAPGyDexNmeieQ07-eA/edit#

             ioasis_generic = 1         ! enables OASIS coupling
             write_restart_option = 2   ! 0 => not writing any restart files
                                        ! 1 => writing restart files at the first oasis_put processes
                                        ! 2 => writing restart files at the last oasis_put processes
                                        ! 3 => both 1 & 2
             l_write_grids = .true.     ! for writing grids.nc, areas.nc, masks.nc (by OASIS)
                                        ! --> put .false. if these already exist.
                                        ! --> if .true., then indicate the SYMPHONIE grid below.

            ! The grid.nc describing the global grid when no land proc has been removed.
             default_grid_file_name = 'grid.nc' TODO
            !default_grid_file_name = 'default' ! indicates the grid.nc that will be produced
                                                ! in the tmp directory.

             oasis_sync_lag = 0         ! synchronisation lag with other components (sec)
                                        ! > 0 => SYMPHONIE starts late
                                        ! < 0 => SYMPHONIE starts in advance
                                        ! should be equal to the coupling period in the
                                        !   namcouple
                                        ! in the namcouple, RUNTIME must have the run
                                        !   duration + |oasis_sync_lag|
             oasis_dummy_dt = 120       ! model time step to use during the dummy loops
                                        !   for filling the lag
                                        ! should be equal to the LAG parameter in the
                                        !   namcouple
 
                                        !------ NAMCOUPLE FIELD ENTRIES ------
                                        ! field    | grid
                                        !-------------------------------------
             l_cpl_im_wndu = .false.    ! SYM_WNDU | symt
             l_cpl_im_wndv = .false.    ! SYM_WNDV | symt
             l_cpl_im_t2m  = .false.    ! SYM_T2M  | symt
             l_cpl_im_t10m = .false.    ! SYM_T10M | symt
             l_cpl_im_q2m  = .false.    ! SYM_Q2M  | symt
             l_cpl_im_q10m = .false.    ! SYM_Q10M | symt
             l_cpl_im_slp  = .false.    ! SYM_SLP  | symt
             l_cpl_im_taux = .false.    ! SYM_TAUX | symt
             l_cpl_im_tauy = .false.    ! SYM_TAUY | symt
             l_cpl_im_evap = .false.    ! SYM_EVAP | symt
             l_cpl_im_prec = .false.    ! SYM_PREC | symt
             l_cpl_im_watf = .false.    ! SYM_WATF | symt
             l_cpl_im_slhf = .true.     ! SYM_SLHF | symt
             l_cpl_im_sshf = .true.     ! SYM_SSHF | symt
             l_cpl_im_snsf = .false.    ! SYM_SNSF | symt
             l_cpl_im_dnsf = .false.    ! SYM_DNSF | symt
             l_cpl_im_ssrf = .false.    ! SYM_SSRF | symt
             l_cpl_im_dsrf = .false.    ! SYM_DSRF | symt
             l_cpl_ex_sst  = .false.    ! SYM_SST  | symt
             l_cpl_ex_ssh  = .false.    ! SYM_SSH  | symt
             l_cpl_ex_ocnu = .false.    ! SYM_OCNU | symt
             l_cpl_ex_ocnv = .false.    ! SYM_OCNV | symt
                                        !------ NAMCOUPLE FIELD ENTRIES ------
            /


Exercise 3
----------

**Task:** Send averaged wind stress (x- and y- components) and precipitation from RegCM to
SYMPHONIE, with coupling occurring every 8 timesteps in the atmosphere.

**Model key features:**

+-----------------+--------------+-------------------+
|                 | RegCM        | SYMPHONIE         |
+=================+==============+===================+
| Grid dimensions | ``jx = 99``  | ``iglb = 150``    |
|                 | ``iy = 99``  | ``jglb = 150``    |
+-----------------+--------------+-------------------+
| Timestep        | ``dt = 90.`` | ``dti_fw = 180.`` |
+-----------------+--------------+-------------------+


.. dropdown:: Solution

   .. tab-set::

      .. tab-item:: ``namcouple`` entries

         .. code::

              RCM_TAUX:RCM_TAUY SYM_TAUX:SYM_TAUY 1 720 2 restart_TAU.nc EXPORTED
              96 96 150 150 rcim symt LAG=+90
              R  0  R  0
              LOCTRANS MAPPING
              AVERAGE
              rmp_rcim_to_symt_BILINEAR.nc src opt
            #
              RCM_PREC SYM_PREC 1 720 3 restart_PR.nc EXPORTED
              96 96 150 150 rcim symt LAG=+90
              R  0  R  0
              LOCTRANS BLASOLD MAPPING
              AVERAGE
              0.001 0
              rmp_rcim_to_symt_BILINEAR.nc src opt


      
         **Key points:**

         * 8 times 90 seconds is 12 minutes, i.e., 720 seconds for the coupling period.
         * Wind stress components can be grouped into one single entry, but not with precipitation, which requires scaling.
         * Did you notice in the previous page the difference of unit for precipitation, between SYMPHONIE and RegCM?


      .. tab-item:: RegCM's ``oasisparam``

         .. code:: fortran
            
            !
            ! OASIS parameters
            !
            &oasisparam
             write_restart_option = 2, ! 0 => no restart file writing TODO
                                       ! 1 => write restart files at the first time
                                       ! 2 => write restart files at the last time
                                       ! 3 => both 1 & 2
             l_write_grids = .true.,   ! For writing grids.nc, areas.nc, masks.nc.
             oasis_sync_lag = 0,       ! Synchronisation lag with other components (sec)
                                       ! > 0 => Regcm starts late
                                       ! < 0 => Regcm starts in advance
                                       ! Should be a multipe of the coupling period
                                       !   in the namcouple.
                                       ! In the namcouple, RUNTIME must have
                                       !   the run duration + oasis_sync_lag.
                                       !------ NAMCOUPLE FIELD ENTRIES ------
                                       ! field    | grid
                                       !-------------------------------------
             l_cpl_im_sst  = .false.,  ! RCM_SST  | rcim     
             l_cpl_im_wz0  = .false.,  ! RCM_WZ0  | rcim     
             l_cpl_im_wust = .false.,  ! RCM_WUST | rcim     
             l_cpl_ex_u10m = .false.,  ! RCM_U10M | rcin/rcim
             l_cpl_ex_v10m = .false.,  ! RCM_V10M | rcin/rcim
             l_cpl_ex_wspd = .false.,  ! RCM_WSPD | rcin/rcim
             l_cpl_ex_wdir = .false.,  ! RCM_WDIR | rcin/rcim
             l_cpl_ex_t2m  = .false.,  ! RCM_T2M  | rcin/rcim
             l_cpl_ex_q2m  = .false.,  ! RCM_Q2M  | rcin/rcim
             l_cpl_ex_slp  = .false.,  ! RCM_SLP  | rcen/rcem
             l_cpl_ex_taux = .true.,   ! RCM_TAUX | rcin/rcim
             l_cpl_ex_tauy = .true.,   ! RCM_TAUY | rcin/rcim
             l_cpl_ex_z0   = .false.,  ! RCM_Z0   | rcin/rcim
             l_cpl_ex_ustr = .false.,  ! RCM_USTR | rcin/rcim
             l_cpl_ex_evap = .false.,  ! RCM_EVAP | rcin/rcim
             l_cpl_ex_prec = .true.,   ! RCM_PREC | rcin/rcim
             l_cpl_ex_nuwa = .false.,  ! RCM_NUWA | rcin/rcim
             l_cpl_ex_ulhf = .false.,  ! RCM_ULHF | rcin/rcim
             l_cpl_ex_ushf = .false.,  ! RCM_USHF | rcin/rcim
             l_cpl_ex_uwlw = .false.,  ! RCM_UWLW | rcin/rcim
             l_cpl_ex_dwlw = .false.,  ! RCM_DWLW | rcin/rcim
             l_cpl_ex_nulw = .false.,  ! RCM_NULW | rcin/rcim
             l_cpl_ex_uwsw = .false.,  ! RCM_UWSW | rcin/rcim
             l_cpl_ex_dwsw = .false.,  ! RCM_DWSW | rcin/rcim
             l_cpl_ex_ndsw = .false.,  ! RCM_NDSW | rcin/rcim
             l_cpl_ex_rhoa = .false.,  ! RCM_RHOA | rcin/rcim
                                      !------ NAMCOUPLE FIELD ENTRIES ------
            /

      
      .. tab-item:: SYMPHONIE's ``notebook_oasis_generic.f``

         .. code:: fortran
            
            &notebook_oasis_generic
            ! https://docs.google.com/document/d/1stIu_SuZY7l729gXjDB-LS37fAPGyDexNmeieQ07-eA/edit#

             ioasis_generic = 1         ! enables OASIS coupling
             write_restart_option = 2   ! 0 => not writing any restart files
                                        ! 1 => writing restart files at the first oasis_put processes
                                        ! 2 => writing restart files at the last oasis_put processes
                                        ! 3 => both 1 & 2
             l_write_grids = .true.     ! for writing grids.nc, areas.nc, masks.nc (by OASIS)
                                        ! --> put .false. if these already exist.
                                        ! --> if .true., then indicate the SYMPHONIE grid below.

            ! The grid.nc describing the global grid when no land proc has been removed.
             default_grid_file_name = 'grid.nc' TODO
            !default_grid_file_name = 'default' ! indicates the grid.nc that will be produced
                                                ! in the tmp directory.

             oasis_sync_lag = 0         ! synchronisation lag with other components (sec)
                                        ! > 0 => SYMPHONIE starts late
                                        ! < 0 => SYMPHONIE starts in advance
                                        ! should be equal to the coupling period in the
                                        !   namcouple
                                        ! in the namcouple, RUNTIME must have the run
                                        !   duration + |oasis_sync_lag|
             oasis_dummy_dt = 180       ! model time step to use during the dummy loops
                                        !   for filling the lag
                                        ! should be equal to the LAG parameter in the
                                        !   namcouple
 
                                        !------ NAMCOUPLE FIELD ENTRIES ------
                                        ! field    | grid
                                        !-------------------------------------
             l_cpl_im_wndu = .false.    ! SYM_WNDU | symt
             l_cpl_im_wndv = .false.    ! SYM_WNDV | symt
             l_cpl_im_t2m  = .false.    ! SYM_T2M  | symt
             l_cpl_im_t10m = .false.    ! SYM_T10M | symt
             l_cpl_im_q2m  = .false.    ! SYM_Q2M  | symt
             l_cpl_im_q10m = .false.    ! SYM_Q10M | symt
             l_cpl_im_slp  = .false.    ! SYM_SLP  | symt
             l_cpl_im_taux = .true.     ! SYM_TAUX | symt
             l_cpl_im_tauy = .true.     ! SYM_TAUY | symt
             l_cpl_im_evap = .false.    ! SYM_EVAP | symt
             l_cpl_im_prec = .true.     ! SYM_PREC | symt
             l_cpl_im_watf = .false.    ! SYM_WATF | symt
             l_cpl_im_slhf = .false.    ! SYM_SLHF | symt
             l_cpl_im_sshf = .false.    ! SYM_SSHF | symt
             l_cpl_im_snsf = .false.    ! SYM_SNSF | symt
             l_cpl_im_dnsf = .false.    ! SYM_DNSF | symt
             l_cpl_im_ssrf = .false.    ! SYM_SSRF | symt
             l_cpl_im_dsrf = .false.    ! SYM_DSRF | symt
             l_cpl_ex_sst  = .false.    ! SYM_SST  | symt
             l_cpl_ex_ssh  = .false.    ! SYM_SSH  | symt
             l_cpl_ex_ocnu = .false.    ! SYM_OCNU | symt
             l_cpl_ex_ocnv = .false.    ! SYM_OCNV | symt
                                        !------ NAMCOUPLE FIELD ENTRIES ------
            /
