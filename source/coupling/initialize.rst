Initialization
==============

OASIS-exchanged data should be initialized properly, otherwise, they will be assigned
with a uniform zero field which can be problematic. In other words, the ``$NNOREST``
section of the ``namcouple`` should never be set to true (``T``) during simulation when
coupling is enabled. In this context, this page focuses on generating OASIS
initialization files (or "restart files" in OASIS documentation).

The strategy we employ consists of **running a single-day simulation** of both
components (one exact day before the intended coupled simulation period),
**using OASIS to output the interface fields into NetCDF files** rather than to exchange
data between the models. End-of-the-day output files will represent the air-sea
interface for the variables of interest in each model. They will serve as restart files
for our subsequent coupled simulation.

Such a strategy translates into the following **three configuration key points**, each
detailed in a dedicated drop-down section. Apply these directions to the namelists
you have prepared with the ``cpl_init`` suffix, as well as to ``$RUN/namcouple``.

.. dropdown:: 1. Simulation period

   The simulation period must be set from one day before the intended coupled
   simulation, and for a duration of one day. Let us say that the intended coupled
   simulation will run for the same period as the uncoupled runs we conducted in the
   :doc:`first part of this training <../component-wise/index>`
   (i.e., from 2023-01-10 to 2023-01-12).
   Then **relevant start and end dates are 2023-01-09 and 2023-01-10**, respectively.
   
   Let us apply this to the different compartments:

   * **RegCM:** Adapt ``gdata1``, ``gdate2`` and ``&restartparam``.
   * **SYMPHONIE:** Adapt ``datesim`` in ``notebook_time.f``.
   * **OASIS:** Set the ``namcouple`` ``$RUNTIME`` to 86400 (i.e., the number of seconds in one day).


.. dropdown:: 2. Enabling only exporting fields

   Let us now modify the field-enabling logicals of the OASIS-related namelist of
   each component: namely ``&oasisparam`` for RegCM and ``notebook_oasis_generic.f`` for
   SYMPHONIE. We enable (set to ``.true.``) the exporting fields we plan to use for
   coupling, and disable (set to ``.false.``) all others.
   Below are fields to enable:

   * **RegCM:**
      * ``l_cpl_ex_slp``
      * ``l_cpl_ex_taux``
      * ``l_cpl_ex_tauy``
      * ``l_cpl_ex_prec``
      * ``l_cpl_ex_ulhf``
      * ``l_cpl_ex_ushf``
      * ``l_cpl_ex_uwlw``
      * ``l_cpl_ex_dwsw``
   * **SYMPHONIE** (in ``notebook_oasis_generic.f``):
      * ``l_cpl_ex_sst``


   .. important::

      Don't forget to enable OASIS in general:

      * ``ioasiscpl = 1`` for RegCM,
      * ``ioasis_generic = 1`` in ``notebook_oasis_generic.f`` for SYMPHONIE,


      as well as grid writing with the ``l_write_grids`` logical, indicating the full
      grid for SYMPHONIE with ``default_grid_file_name = "./symphonie/grid.nc"``.


.. dropdown:: 3. Configuring the ``namcouple`` in ``OUTPUT`` mode

   This initialization run will not exchange data between the components, but instead
   use the OASIS interface as an output stream. The entry mode for this case
   is ``OUTPUT``. Following the directions of a previous :doc:`page <namelist/namcouple>`
   of this training, the ``$STRINGS`` section of the ``namcouple`` file should look like
   this: 

   .. code:: console

      $STRINGS
      # The above variables are the general parameters for the experiment.
      # Everything below has to do with the fields being exchanged.
      #
      RCM_TAUX:RCM_TAUY:RCM_NDSW RCM_TAUX:RCM_TAUY:RCM_NDSW 1 3600 1 restart_tau-sw.nc OUTPUT
      rcim rcim LAG=+180
      LOCTRANS
      AVERAGE
      #
      RCM_PREC RCM_PREC 1 3600 1 restart_RCM_PREC.nc OUTPUT
      rcim rcim LAG=+180
      LOCTRANS
      AVERAGE
      #
      RCM_ULHF:RCM_USHF:RCM_NULW RCM_ULHF:RCM_USHF:RCM_NULW 1 3600 1 restart_lat-sens-lw.nc OUTPUT
      rcim rcim LAG=+180
      LOCTRANS
      AVERAGE
      #
      RCM_SLP RCM_SLP 1 3600 1 restart_RCM_SLP.nc OUTPUT
      rcem rcem LAG=+180
      LOCTRANS
      AVERAGE
      #
      SYM_SST SYM_SST 1 3600 1 restart_SYM_SST.nc OUTPUT
      symt symt LAG=+180
      LOCTRANS
      AVERAGE


   Accordingly, make sure the ``$NFIELDS`` section indicates 5 entries.

   .. dropdown:: Why don't we group all ``rcim`` fields into one single entry?

      Because when setting up the coupled run, they will need distinct scaling
      (to convert precipitation, and revert the sign of most heat fluxes). We thus
      want to generate distinct restart files: fields are grouped from now on,
      based on the transformations they will need later.

   
When you have configured everything as guided above, **save the** ``namcouple`` **file**
in your home directory:

.. code:: shell

   mkdir ~/oasis_namcouples
   cp $RUN/namcouple ~/oasis_namcouples/namcouple-training_cpl_init
   ln -sf ~/oasis_namcouples/namcouple-training_cpl_init oasis/namcouple-cpl_init


Then, **edit** ``job.sh`` and modify/check the following points:

* Set ``--job-name`` to ``'init'``.
* Set ``NPROC1`` and ``NPROC2`` to 36, refering to the allocation for RegCM and SYMPHONIE, respectively.
* Set the ``--nodes`` batch parameter to 2.
* Set ``DIR`` to the current run directory.
* Set ``EXE1`` and ``EXE2`` to ``./regcm/bin/regcmMPICLM45_OASIS`` and ``./symphonie/bin/OASIS/symphonie.exe``.

.. dropdown:: ``job.sh``

   .. code:: bash

      TODO


Delete the content of the ``tmp`` folder of SYMPHONIE:

.. code:: bash

   rm symphonie/tmp/*


And proceed: **submit the job** and follow is progress:

.. code:: bash

   sbatch job.sh
   squeue -u $USER -i 5


If the **run completes successfully**, you should find the ending message of both models
around the end of the slurm output, in an order that depends on the models' relative
computing speed. RegCM should print the following:

.. code::

   TODO


and SYMPHONIE:

.. code::

   TODO


Moreover, there should now **exist grid files and the restart files** we aim to produce:

.. code:: console

   $ ls -1 *.nc
   TODO


**Save the grid files** in the ``oasis`` directory:

.. code:: bash

   mv areas.nc grids.nc masks.nc oasis/


Now however, if you **check the restart files' content**, for example using ``ncdump -h``:

.. code:: console

   $ ncdump -h restart_SST.nc
   TODO


you should notice that **the fields only have one dimension**.
In other words, they are *flattened*:
this is one flaw of the ``OUTPUT`` mode in OASIS...
No worries, though, simple Python can make it up!
Simply ``source`` the following script of the ``$TRAINING`` directory.

.. code:: bash

   cd $RUN
   source $TRAINING/postprocess_restart_files.sh


You may check their content; things should be right now.
**Save the restart files** in a dedicated folder:

.. code:: bash

   mkdir oasis/restart_20230201
   mv restart_*.nc oasis/restart_20230201


We now have our grids, ``namcouple`` and restart files in ``oasis``:

.. code:: console

   $ ls -1 oasis
   TODO


We are ready to run our first coupled simulation!