Namelist essentials
===================

Let us open ``namelist.f`` and span through its most important sections for the present
training. Note that an actual Fortran namelist is a container formatted as follows for
a namelist named ``name`` (``namelist.f`` contains several actual *namelists*):

.. code:: fortran

   &name
     var = "value"  ! some variable here
                    ! and more...
   /


You can go through ``namelist.f`` in autonomy. It is fairly well commented. In addition,
however, the table below drags our attention on specific parts of the file.

.. list-table::
   :header-rows: 1

   * - Namelist/variable(s)
     - Information
   * - ``inpter`` and ``inpglob``
     - Directory to the raw data for the terrain and initial and boundary conditions
   * - ``dirter`` and ``dirglob``
     - Should point to the ``input`` directory: where to write preprocessed input data
   * - ``dirout``
     - Should point to the ``output`` directory: path for the simulation outputs
   * - ``gdata1``, ``gdate2`` and ``&restartparam``
     - Define the simulation period
   * - ``&timeparam``
     - Define the temporal discretization (in our case, ``dt`` equals 180 sec)
   * - ``&outparam``
     - Define what variables to output and at which frequency
   * - ``&physicsparam``
     - Scheme selection and switches, including for OASIS with the ``ioasiscpl`` switch (this should remain 0 for now)
   * - ``&oasisparam``
     - Parameters to finely set up field exchanges through OASIS.
