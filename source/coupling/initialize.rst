Initialization
==============

OASIS-exchanged data should be initialized properly, otherwise, they will be assigned
with a uniform zero field which can be problematic. In other words, the first section
of the ``namcouple`` should never be set to true (``T``) during simulation when coupling
is enabled. In this context, this page focuses on generating OASIS initialization files
(or "restart files" in OASIS documentation).

The strategy we employ consists of **running a single-day simulation** of both
components (one exact day before the intended coupled simulation period),
**using OASIS to output the interface fields into NetCDF files** rather than to exchange
data between the models. End-of-the-day output files will represent the air-sea
interface for the variables of interest in each model. They will serve as restart files
for our subsequent coupled simulation.

Such a strategy translates into the following **three configuration key points**, each
detailed in a dedicated drop-down section:

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

   Let us now modify the field-enabling logicals of the OASIS-related namelist from
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


   And don't forget to enable OASIS in general:

   * ``ioasiscpl = 1`` for RegCM
   * ``ioasis_generic = 1`` in ``notebook_oasis_generic.f`` for SYMPHONIE


.. dropdown:: 3. Configuring the ``namcouple`` in ``OUTPUT`` mode

   This initialization run will not exchange data between the components, but instead
   use the OASIS interface as an output stream. The ``namcouple`` keyword for this case
   is ``OUTPUT``. They are other formatting rules that go with this mode, and in the
   end, the ``$STRINGS`` section of the ``namcouple`` file should look like this: 

   .. code:: console

      $STRINGS
      # The above variables are the general parameters for the experiment.
      # Everything below has to do with the fields being exchanged.
      #
      RCM_TAUX:RCM_TAUY:RCM_NDSW RCM_TAUX:RCM_TAUY:RCM_NDSW 1 3600 1 restart_tau-sw.nc OUTPUT
      rcin rcin LAG=+180
      LOCTRANS
      AVERAGE
      #
      RCM_PREC RCM_PREC 1 3600 1 restart_RCM_PREC.nc OUTPUT
      rcin rcin LAG=+180
      LOCTRANS
      AVERAGE
      #
      RCM_ULHF:RCM_USHF:RCM_NULW RCM_ULHF:RCM_USHF:RCM_NULW 1 3600 1 restart_lat-sens-lw.nc OUTPUT
      rcin rcin LAG=+180
      LOCTRANS
      AVERAGE
      #
      RCM_SLP RCM_SLP 1 3600 1 restart_RCM_SLP.nc OUTPUT
      rcen rcen LAG=+180
      LOCTRANS
      AVERAGE
      #
      SYM_SST SYM_SST 1 3600 1 restart_SYM_SST.nc OUTPUT
      symt symt LAG=+180
      LOCTRANS
      AVERAGE
      #
