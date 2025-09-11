Components' OASIS-related namelists
===================================

Those namelists are ``oasisparam`` with RegCM and the ``notebook_oasis_generic.f`` file
with SYMPHONIE. You can find examples for each component below:

.. tab-set::

   .. tab-item:: RegCM

      .. code:: fortran

         TODO ! Yolo


   .. tab-item:: SYMPHONIE

      .. code:: fortran

         TODO ! Yolo

      
They are structured in a very similar way because coded by the same person:

* ``write_restart_option`` enables writing out the fields at specific timesteps (note that a restart file will be written anyways at the end of the simulation).
* ``l_write_grids`` enables grid writing during initialization. ``grids.nc``, ``areas.nc`` and ``masks.nc`` are necessary files for the simulation, and must contain information about the grids of all involved components. They can be reused from a previous simulation where the same components were coupled, hence setting this logical to ``.false.``. On the contrary, if the components or their grid change, or if this is the first coupled simulation, then the files must be generated, implying ``l_write_grids`` to be set to ``.true.``.

.. note::

   For the case of SYMPHONIE, where a production run likely does not have resources
   allocated over land-only areas of the domain, a complete unholed ``grid.nc`` must be
   provided with ``default_grid_file_name`` for ``l_write_grids = .true.`` to work.


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
      Arakawa-B grid framework, whether you use MOLOCH or not), in their "internal" and
      "external" variations, respectively. ``rcem`` has the size ``jx - 1`` x
      ``iy - 1``, and ``rcim`` excludes the borders, hence having the size ``jx - 3`` x
      ``iy - 3`` (``dimparam``).

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
      the (``iglb``, ``jglb``) dimensions (``notebook_grid.f``).


Last but not least, OASIS-related parts of the code must be enabled in both components.
RegCM has the ``ioasiscpl`` in ``physicsparam``. SYMPHONIE employs a logical directly
within the ``notebook_oasis_generic.f`` file: ``ioasis_generic``.