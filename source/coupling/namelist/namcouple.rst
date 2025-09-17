For OASIS: ``namcouple``
========================

``namcouple`` is a text file separated in sections, each with a specific format.
Any line beginning with ``#`` is ignored and blank lines are not allowed.


Head settings
-------------

The first section is ``$NNOREST``:

.. code:: console

   $NNOREST
   # T (true) or F (false): make the restart file facultative, i.e. if absent
   # fields are initialized with zero values
   #
     F


This means that when set to true, restart files are optional, thereby allowing
initializing fields with zeros if they are missing. When set to false, a missing
restart file will make OASIS fail.

Then, there is ``$NFIELDS``:

.. code:: console

   $NFIELDS
   # = total number of field entries
   #
     7


which refers to the entries of the last section we will detail below.


Now, ``$RUNTIME``:

.. code:: console

   $RUNTIME
   # The total simulated time for this run in seconds
   #
     39571200


which must match the duration of the simulation for each component.

.. attention::

   A **mismatch** between ``namcouple``'s run time and the models' start and end dates
   **will not be detected** during the initialization, and will simply raise an error
   when one of the components increments its time further whereas others terminate.
   Thus, be extra careful in planning dates and run time.


And for debugging:

.. code:: console

   $NLOGPRT
   # Amount of information written to OASIS3-MCT log files (see User Guide)
   #
     0  0  0


the maximum debugging mode being set with the first index at 30.


Basic field entries
-------------------

The coupling fields are defined in a last section starting with ``$STRINGS``.
Each entry is formatted on several lines. Entries then follow each other, and their
amount must match the number defined in ``$NFIELDS``.


First line
~~~~~~~~~~

The first line of each entry looks like this:

.. code:: console

   SRC_NAME DST_NAME 1 3600 0 restart.nc EXPORTED


* ``SRC_NAME`` and ``DST_NAME`` are the names of the coupling field as defined in its source and destination components, respectively.
* ``1`` is always ``1``.
* ``3600`` represents the coupling period, here one hour (in the same unit as the run time, i.e., in seconds).
* ``0`` indicates the number of transformations to apply to the fields, which we will detail further below.
* ``restart.nc`` is the name of the NetCDF file used for initialization. It will be overwritten by the last fields' value at the end of the run (thus serving as a restart file for the following simulation).
* ``EXPORTED`` is the mode of the entry, determining how coupling fields will be treated as well as the format of the following lines.

.. tip::

   If several fields aim to be treated identically during the simulation (same mode,
   same grids, etc.), they may be included in one single entry, hence counting as one
   for the ``$NFIELDS`` section. This can be done using the colon separator for the
   fields' source and destination names. Here is an example of two fields for one entry:

   .. code:: console

      SRC_NAME1:SRC_NAME2 DST_NAME1:DST_NAME2 1 3600 0 restart.nc EXPORTED


In this training, we focus on two modes: ``EXPORTED`` (or ``EXPOUT``) and ``OUTPUT``.
``EXPORTED`` enables an actual transfer of data between the source and destination
components. ``OUTPUT`` simply writes the source data in a NetCDF file.

.. note::

   With identical formatting as ``EXPORTED``, ``EXPOUT`` enables data transfer, while
   also writing out this same data in a NetCDF file. This must be enabled
   mindfully because involving a **huge and increasing memory usage** as the simulation
   progresses (which impacts the computing time as well).


``EXPORTED`` mode
~~~~~~~~~~~~~~~~~

Here is an example of ``EXPORTED`` entry:

.. code:: console

   SRC_NAME DST_NAME 1 3600 0 restart.nc EXPORTED
   253 205 1197 972 rcim symt LAG=+180
   R  0  R  0


After the first line we've already covered, the second line contains:

* the source grid's *x* and *y* dimensions;
* the destination grid's *x* and *y* dimensions;
* the source grid's name;
* the destination grid's name;
* and optional keyword arguments, here ``LAG`` with the ``+180`` value.


.. admonition:: The ``LAG`` concept

   A positive lag indicates that the source data will be sent ahead of the coupling time
   by the provided value (still in the same unit as the coupling period, i.e., in
   seconds). If *T* is a coupling time (i.e., a multiplier of the coupling period), and
   *t* is the time of a given model loop, then the lagged field is sent by the source at
   *t = T - LAG* and received at the destination at *t = T*. The general rule is to
   **set the lag equal to the sending model's timestep**: the field will be sent by the
   source model at the end of the last model loop before a coupling time, such that it
   can be received at the beginning of the receiving model's loop corresponding to a
   coupling time.


The third line, ``R 0 R 0``, refers to grid periodicity and overlapping. We won't
change this line during this training, i.e., choosing no periodicity nor overlapping.

.. note::

   Field and grid names are not defined in the ``namcouple`` but within each component.
   ``namcouple`` field entries simply use those names to indicate which are the sources
   and the destinations.



``OUTPUT`` mode
~~~~~~~~~~~~~~~

Here is an example of ``OUTPUT`` entry:

.. code:: console

   SRC_NAME SRC_NAME 1 3600 0 restart.nc OUTPUT
   rcim rcim LAG=+180


Notice the repetition of the source field and grid names, underlying that there is no
transfer to a destination component in this mode.
Compared to ``EXPORTED`` entries, ``OUTPUT`` entries do not contain grid dimensions, but
employ optional keywords all the same.


Field transformations
---------------------

As mentioned earlier, you can configure field transformations for each entry.
In the following example, two transformations are set up, namely ``LOCTRANS`` and
``SCRIPR``:

.. code::

   SRC_NAME DST_NAME 1 3600 2 restart.nc EXPORTED
   253 205 1197 972 rcim symt LAG=+180
   R  0  R  0
   LOCTRANS SCRIPR
   AVERAGE
   BILINEAR LR SCALAR LATLON 1


* ``2`` (the number of transformations) is indicated right after the coupling period in the first line.
* Lines 2 and 3 relate to the ``EXPORTED`` mode and are thus identical, with or without transformation.
* Line 4 presents the keyword of each transformation, here ``LOCTRANS`` and ``SCRIPR``.
* Following lines contain parameters for each transformation, in order: line 5 for the first one (``LOCTRANS``), line 6 for the second, line 7 for the third if existing, so on, so forth.


``LOCTRANS`` is about **time transformations**. At a coupling time, the data sent is
by default the instantaneous field of the timestep it is sent from. ``LOCTRANS`` can change
this into sending instead a field averaged over the past coupling period, using the
``AVERAGE`` keyword as in the example. Other options include accumulation, minimum and
maximum (we won't cover those during the training).

``SCRIPR`` refers to an **interpolation** library. We won't touch its parameter line
during this training, but of course, the ``BILINEAR`` keyword could be changed into other
interpolation methods such as ``BICUBIC``, ``GAUSWGT`` and so on.

.. tip::

   The ``SCRIPR`` transformation implies generating the interpolation weights at run
   time during the initialization. Depending on the grids, this can be quite a
   **resource-consuming step**. Luckily, once computed, the weights are saved in a
   NetCDF    file which can be reused for the next simulations instead of recomputed. To
   do this, once you have your interpolation weights saved in a file, change your
   interpolation transformation to ``MAPPING``, like this (simply adapt the file name):

   .. code:: console

      SRC_NAME DST_NAME 1 3600 2 restart.nc EXPORTED
      253 205 1197 972 rcim symt LAG=+180
      R  0  R  0
      LOCTRANS MAPPING
      AVERAGE
      rmp_rcim_to_symt_BILINEAR.nc src opt


Lastly, **scaling** can be performed with the ``BLASOLD`` transformation, to change
units for example. In the example below, ``BLASOLD`` is used to revert the direction of
the surface longwave heat flux, whose convention is positive upward for the sender,
but positive downward for the receiver:

.. code:: console

   RCM_NULW SYM_SNSF 1 1440 3 restart_LW.nc EXPORTED
   253 205 1197 972 rcin symt LAG=+180
   R  0  R  0
   LOCTRANS BLASOLD MAPPING
   AVERAGE
   -1 0
   rmp_rcin_to_symt_BILINEAR.nc src opt


.. tip::

   ``BLASOLD`` can also serve to **add a constant** to the field. In this case, the second
   index must be set to 1, and a new line must define the added constant (and this must be
   a real).
   In the following example,
   sea surface temperature is converted from degree Celsius for the sender, to Kelvin
   for the receiver:

   .. code:: console

      SYM_SST RCM_SST 1 1440 2 restart_SST.nc EXPORTED
      1197 972 253 205 symt rcim LAG=+180
      R  0  R  0
      BLASOLD MAPPING
      1 1
      CONSTANT 273.15
      rmp_symt_to_rcim_BILINEAR.nc src opt


Full file example
-----------------

Below is an example ``namcouple`` file, implementing nearly everything we will see on
this page. This is only a **minimal working example**. This is not exactly the file we
will use for the coupled model.

.. dropdown:: ``namcouple``

   .. code::

      # This is a typical input file for OASIS3-MCT.
      # Keywords used in previous versions of OASIS3
      # but now obsolete are marked "Not used"
      # Don't hesitate to ask precisions or make suggestions (oasishelp@cerfacs.fr).
      #
      # Any line beginning with # is ignored. Blank lines are not allowed.
      #
      #--------------------------------------------------------------------------
      $NNOREST
      # T (true) or F (false): make the restart file facultative, i.e. if absent
      # fields are initialized with zero values
      #
        F
      #--------------------------------------------------------------------------
      $NFIELDS
      # = total number of field entries
      #
        2
      #--------------------------------------------------------------------------
      $RUNTIME
      # The total simulated time for this run in seconds
      #
        63072000
      #--------------------------------------------------------------------------
      $NLOGPRT
      # Amount of information written to OASIS3-MCT log files (see User Guide)
      #
        0  0  0
      #--------------------------------------------------------------------------
      $STRINGS
      # The above variables are the general parameters for the experiment.
      # Everything below has to do with the fields being exchanged.
      #
        RCM_TAUX:RCM_TAUY SYM_TAUX:SYM_TAUY 1 720 2 restart_TAU.nc EXPORTED
        253 205 1197 972 rcin symt LAG=+180
        R  0  R  0
        LOCTRANS MAPPING
        AVERAGE
        rmp_rcin_to_symt_BILINEAR.nc src opt
      #
        RCM_NULW SYM_SNSF 1 1440 3 restart_LW.nc EXPORTED
        253 205 1197 972 rcin symt LAG=+180
        R  0  R  0
        LOCTRANS BLASOLD MAPPING
        AVERAGE
        -1 0
        rmp_rcin_to_symt_BILINEAR.nc src opt
