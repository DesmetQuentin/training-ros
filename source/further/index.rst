Last words / To go further
==========================

These are the last words of this training. **Congratulations!**

Note that we kept all namelist configurations, appending a different suffix for each
simulation, allowing you to come back to parts of the training you'd like to explore
more. Also, it is now convenient to compare configurations of those many runs, using
the ``diff`` program, for instance with:

.. code:: console

   $ diff $RUN/symphonie/NOTEBOOKS-cpl_init $RUN/symphonie/NOTEBOOKS-cpl_spinup
   diff symphonie/NOTEBOOKS-cpl_init/notebook_airseaflux_s26.f symphonie/NOTEBOOKS-cpl_spinup/notebook_airseaflux_s26.f
   7c7
   < flag_meteodata='ecmwf'           ! Meteorological model key (ecmwf glorys
   ---
   > flag_meteodata='oasisflux'       ! Meteorological model key (ecmwf glorys
   diff symphonie/NOTEBOOKS-cpl_init/notebook_graph symphonie/NOTEBOOKS-cpl_spinup/notebook_graph
   15c15
   < 1  Sea surface height (SSH)                           6
   ---
   > 0  Sea surface height (SSH)                           6
   diff symphonie/NOTEBOOKS-cpl_init/notebook_oasis_generic.f symphonie/NOTEBOOKS-cpl_spinup/notebook_oasis_generic.f
   9c9
   <  l_write_grids = .true.     ! for writing grids.nc, areas.nc, masks.nc (by OASIS)
   ---
   >  l_write_grids = .false.    ! for writing grids.nc, areas.nc, masks.nc (by OASIS)
   39,41c39,41
   <  l_cpl_im_slp  = .false.    ! SYM_SLP  | symt
   <  l_cpl_im_taux = .false.    ! SYM_TAUX | symt
   <  l_cpl_im_tauy = .false.    ! SYM_TAUY | symt
   ---
   >  l_cpl_im_slp  = .true.     ! SYM_SLP  | symt
   >  l_cpl_im_taux = .true.     ! SYM_TAUX | symt
   >  l_cpl_im_tauy = .true.     ! SYM_TAUY | symt
   43c43
   <  l_cpl_im_prec = .false.    ! SYM_PREC | symt
   ---
   >  l_cpl_im_prec = .true.     ! SYM_PREC | symt
   45,47c45,47
   <  l_cpl_im_slhf = .false.    ! SYM_SLHF | symt
   <  l_cpl_im_sshf = .false.    ! SYM_SSHF | symt
   <  l_cpl_im_snsf = .false.    ! SYM_SNSF | symt
   ---
   >  l_cpl_im_slhf = .true.     ! SYM_SLHF | symt
   >  l_cpl_im_sshf = .true.     ! SYM_SSHF | symt
   >  l_cpl_im_snsf = .true.     ! SYM_SNSF | symt
   49c49
   <  l_cpl_im_ssrf = .false.    ! SYM_SSRF | symt
   ---
   >  l_cpl_im_ssrf = .true.     ! SYM_SSRF | symt
   diff symphonie/NOTEBOOKS-cpl_init/notebook_offline.f symphonie/NOTEBOOKS-cpl_spinup/notebook_offline.f
   52c52
   < 24.                          2019   12   25   00   00   00
   ---
   > 24.                         2018   07   10   00   00   00
   diff symphonie/NOTEBOOKS-cpl_init/notebook_time.f symphonie/NOTEBOOKS-cpl_spinup/notebook_time.f
   5,6c5,6
   < datesim(1:6,1)= 2018 , 07 , 02 , 00  , 00  , 00  ! Start time (yyyy mm dd hh mm ss)
   < datesim(1:6,2)= 2018 , 07 , 03 , 00  , 00  , 00  ! End   time (yyyy mm dd hh mm ss)
   ---
   > datesim(1:6,1)= 2018 , 07 , 03 , 00  , 00  , 00  ! Start time (yyyy mm dd hh mm ss)
   > datesim(1:6,2)= 2018 , 07 , 10 , 00  , 00  , 00  ! End   time (yyyy mm dd hh mm ss)


.. tip::

   Colouring is more helpful when the diff is output in a file, with, e.g.:

   .. code:: bash

      diff file1.f file2.f > file1-file2.diff


Now, if you wish to **go further**, please feel free to follow the sections below on
your own; they do not have a specific order.

.. toctree::
   :maxdepth: 1

   storage
   load-balance
   algorithm
