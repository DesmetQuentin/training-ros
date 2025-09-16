With RegCM and SYMPHONIE
========================

Apart from ``namcouple`` for OASIS, each component has specific namelists to control
its own interaction with the coupler. These namelists are ``oasisparam`` with RegCM and
the ``notebook_oasis_generic.f`` file with SYMPHONIE. You can find examples for each
component below:

.. tab-set::

   .. tab-item:: RegCM

      .. code:: fortran

         !
         ! OASIS parameters
         !
         &oasisparam
          write_restart_option = 0, ! 0 => no restart file writing
                                    ! 1 => write restart files at the first time
          l_write_grids = .false.,  ! For writing grids.nc, areas.nc, masks.nc.
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
          l_cpl_ex_taux = .true.,   ! RCM_TAUX | rcin/rcim
          l_cpl_ex_tauy = .true.,   ! RCM_TAUY | rcin/rcim
          l_cpl_ex_z0   = .false.,  ! RCM_Z0   | rcin/rcim
          l_cpl_ex_ustr = .false.,  ! RCM_USTR | rcin/rcim
          l_cpl_ex_evap = .false.,  ! RCM_EVAP | rcin/rcim
          l_cpl_ex_prec = .true.,   ! RCM_PREC | rcin/rcim
          l_cpl_ex_nuwa = .false.,  ! RCM_NUWA | rcin/rcim
          l_cpl_ex_ulhf = .true.,   ! RCM_ULHF | rcin/rcim
          l_cpl_ex_ushf = .true.,   ! RCM_USHF | rcin/rcim
          l_cpl_ex_uwlw = .false.,  ! RCM_UWLW | rcin/rcim
          l_cpl_ex_dwlw = .false.,  ! RCM_DWLW | rcin/rcim
          l_cpl_ex_nulw = .true.,   ! RCM_NULW | rcin/rcim
          l_cpl_ex_uwsw = .false.,  ! RCM_UWSW | rcin/rcim
          l_cpl_ex_dwsw = .false.,  ! RCM_DWSW | rcin/rcim
          l_cpl_ex_ndsw = .true.,   ! RCM_NDSW | rcin/rcim
          l_cpl_ex_rhoa = .false.,  ! RCM_RHOA | rcin/rcim
                                    !------ NAMCOUPLE FIELD ENTRIES ------
         /


   .. tab-item:: SYMPHONIE

      .. code:: fortran

         &notebook_oasis_generic
         ! https://docs.google.com/document/d/1stIu_SuZY7l729gXjDB-LS37fAPGyDexNmeieQ07-eA/edit#

          ioasis_generic = 1         ! enables OASIS coupling
          write_restart_option = 2   ! 0 => not writing any restart files
                                     ! 1 => writing restart files at the first oasis_put processes
                                     ! 2 => writing restart files at the last oasis_put processes
                                     ! 3 => both 1 & 2
          l_write_grids = .false.    ! for writing grids.nc, areas.nc, masks.nc (by OASIS)
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
          l_cpl_im_taux = .true.     ! SYM_TAUX | symt
          l_cpl_im_tauy = .true.     ! SYM_TAUY | symt
          l_cpl_im_evap = .false.    ! SYM_EVAP | symt
          l_cpl_im_prec = .true.     ! SYM_PREC | symt
          l_cpl_im_watf = .false.    ! SYM_WATF | symt
          l_cpl_im_slhf = .true.     ! SYM_SLHF | symt
          l_cpl_im_sshf = .true.     ! SYM_SSHF | symt
          l_cpl_im_snsf = .true.     ! SYM_SNSF | symt
          l_cpl_im_dnsf = .false.    ! SYM_DNSF | symt
          l_cpl_im_ssrf = .true.     ! SYM_SSRF | symt
          l_cpl_im_dsrf = .false.    ! SYM_DSRF | symt
          l_cpl_ex_sst  = .true.     ! SYM_SST  | symt
          l_cpl_ex_ssh  = .false.    ! SYM_SSH  | symt
          l_cpl_ex_ocnu = .false.    ! SYM_OCNU | symt
          l_cpl_ex_ocnv = .false.    ! SYM_OCNV | symt
                                     !------ NAMCOUPLE FIELD ENTRIES ------
         /


They are structured in a very similar way (because coded by the same person):

* ``write_restart_option`` enables writing out the fields at specific timesteps (note that a restart file will be written anyways at the end of the simulation).
* ``l_write_grids`` enables grid writing during initialization. ``grids.nc``, ``areas.nc`` and ``masks.nc`` are necessary files for the simulation, and must contain information about the grids of all involved components. They can be reused from a previous simulation where the same components were coupled, hence setting this logical to ``.false.``. On the contrary, if the components or their grid change, or if this is the first coupled simulation, then the files must be generated, implying ``l_write_grids`` set to ``.true.``.

.. important::

   For the case of SYMPHONIE, where a production run likely does not have resources
   allocated over land-only areas of the domain, a complete *unholed* ``grid.nc`` must
   be provided with ``default_grid_file_name`` for ``l_write_grids = .true.`` to work.


* ``oasis_sync_lag`` serves to configure advanced coupling algorithms where some components are not synced with the main OASIS timeline. Such coupling configurations are not covered in this training (SYMPHONIE's ``oasis_dummy_dt`` also refers to this framework).
* ``l_cpl_*`` logicals are switches to enable/disable each specific field input/output stream through OASIS.


Below is listed a selection of possible streams, together with their names and the
grids they are defined on (those you need to use in the ``namcouple`` file). Note that
field and grid names are already indicated in the namelists' comments.

.. tab-set::

   .. tab-item:: RegCM

      +-------------------+-----------+--------------+-----------+-----------------------------------------------------------+------------------------------+
      | Logical           | Grid name | Field name   | Direction | Description                                               | Unit                         |
      +===================+===========+==============+===========+===========================================================+==============================+
      | ``l_cpl_im_sst``  | ``rcim``  | ``RCM_SST``  | in        | Sea Surface Temperature                                   | K                            |
      +-------------------+-----------+--------------+-----------+-----------------------------------------------------------+------------------------------+
      | ``l_cpl_ex_slp``  | ``rcem``  | ``RCM_SLP``  | out       | Sea Level Pressure                                        | Pa                           |
      +-------------------+-----------+--------------+-----------+-----------------------------------------------------------+------------------------------+
      | ``l_cpl_ex_taux`` | ``rcim``  | ``RCM_TAUX`` | out       | Surface Eastward Wind Stress                              | Pa                           |
      +-------------------+-----------+--------------+-----------+-----------------------------------------------------------+------------------------------+
      | ``l_cpl_ex_tauy`` | ``rcim``  | ``RCM_TAUY`` | out       | Surface Northward Wind Stress                             | Pa                           |
      +-------------------+-----------+--------------+-----------+-----------------------------------------------------------+------------------------------+
      | ``l_cpl_ex_prec`` | ``rcim``  | ``RCM_PREC`` | out       | Precipitation Flux                                        | kg.m\ :sup:`-2`.s\ :sup:`-1` |
      +-------------------+-----------+--------------+-----------+-----------------------------------------------------------+------------------------------+
      | ``l_cpl_ex_ulhf`` | ``rcim``  | ``RCM_ULHF`` | out       | Surface Upward Latent Heat Flux                           | W.m\ :sup:`-2`               |
      +-------------------+-----------+--------------+-----------+-----------------------------------------------------------+------------------------------+
      | ``l_cpl_ex_ushf`` | ``rcim``  | ``RCM_USHF`` | out       | Surface Upward Sensible Heat Flux                         | W.m\ :sup:`-2`               |
      +-------------------+-----------+--------------+-----------+-----------------------------------------------------------+------------------------------+
      | ``l_cpl_ex_ndlw`` | ``rcim``  | ``RCM_NDLW`` | out       | Surface Net Upward Long-Wave Radiation Flux               | W.m\ :sup:`-2`               |
      +-------------------+-----------+--------------+-----------+-----------------------------------------------------------+------------------------------+
      | ``l_cpl_ex_ndsw`` | ``rcim``  | ``RCM_NDSW`` | out       | Surface Net Downward Short-Wave Radiation Flux            | W.m\ :sup:`-2`               |
      +-------------------+-----------+--------------+-----------+-----------------------------------------------------------+------------------------------+


      where ``rcim`` and ``rcem`` correspond to the "cross" grid of RegCM (using an
      Arakawa-B grid framework, whether you use MOLOCH or not), in their "internal"
      (i.e. excluding the borders) and "external" variations, respectively. With ``jx``
      and ``iy`` the dimensions of the grid as configured in ``dimparam``:

      +-----------+-------------------------+
      | Grid name | Grid dimensions         |
      +===========+=========================+
      | ``rcem``  | ``jx - 1`` x ``iy - 1`` |
      +-----------+-------------------------+
      | ``rcim``  | ``jx - 3`` x ``iy - 3`` |
      +-----------+-------------------------+


      .. note::

         Grids exist in a variation using an ``n`` for the last character instead of an
         ``m``. The ``m`` versions we employ mask land areas, thereby preventing land
         data to weight in the interpolation.


   .. tab-item:: SYMPHONIE

      +-------------------+-----------+--------------+-----------+-----------------------------------------------------------+----------------+
      | Logical           | Grid name | Field name   | Direction | Description                                               | Unit           |
      +===================+===========+==============+===========+===========================================================+================+
      | ``l_cpl_ex_sst``  | ``symt``  | ``SYM_SST``  | out       | Sea Surface Temperature                                   | K              |
      +-------------------+-----------+--------------+-----------+-----------------------------------------------------------+----------------+
      | ``l_cpl_im_slp``  | ``symt``  | ``SYM_SLP``  | in        | Sea Level Pressure                                        | Pa             |
      +-------------------+-----------+--------------+-----------+-----------------------------------------------------------+----------------+
      | ``l_cpl_im_taux`` | ``symt``  | ``SYM_TAUX`` | in        | Surface Eastward Wind Stress                              | Pa             |
      +-------------------+-----------+--------------+-----------+-----------------------------------------------------------+----------------+
      | ``l_cpl_im_tauy`` | ``symt``  | ``SYM_TAUY`` | in        | Surface Northward Wind Stress                             | Pa             |
      +-------------------+-----------+--------------+-----------+-----------------------------------------------------------+----------------+
      | ``l_cpl_im_prec`` | ``symt``  | ``SYM_PREC`` | in        | Precipitation Flux                                        | m.s\ :sup:`-1` |
      +-------------------+-----------+--------------+-----------+-----------------------------------------------------------+----------------+
      | ``l_cpl_im_slhf`` | ``symt``  | ``SYM_SLHF`` | in        | Surface Downward Latent Heat Flux                         | W.m\ :sup:`-2` |
      +-------------------+-----------+--------------+-----------+-----------------------------------------------------------+----------------+
      | ``l_cpl_im_sshf`` | ``symt``  | ``SYM_SSHF`` | in        | Surface Downward Sensible Heat Flux                       | W.m\ :sup:`-2` |
      +-------------------+-----------+--------------+-----------+-----------------------------------------------------------+----------------+
      | ``l_cpl_im_snsf`` | ``symt``  | ``SYM_SNSF`` | in        | Surface Net Downward Long-Wave Radiation Flux (non-solar) | W.m\ :sup:`-2` |
      +-------------------+-----------+--------------+-----------+-----------------------------------------------------------+----------------+
      | ``l_cpl_im_ssrf`` | ``symt``  | ``SYM_SSRF`` | in        | Surface Net Downward Short-Wave Radiation Flux (solar)    | W.m\ :sup:`-2` |
      +-------------------+-----------+--------------+-----------+-----------------------------------------------------------+----------------+


      where ``symt`` refers to the "tracer" grid in an Arakawa-C setup, with exactly
      the (``iglb``, ``jglb``) dimensions indicated in ``notebook_grid.f``.


Last but not least, OASIS-related parts of the code must be enabled in both components.
RegCM has the ``ioasiscpl`` in ``physicsparam``. SYMPHONIE employs a logical directly
within the ``notebook_oasis_generic.f`` file: ``ioasis_generic``.
