Running and outputs
===================

Let us now **edit the** ``job.sh`` **batch script**. In the header, lines starting by
``#BATCH`` contain the workload keywords to book computing nodes on CALMIP. The file
then consists of ``bash`` language commands to prepare and launch RegCM, once on the
computing nodes' session.

For this uncoupled run of regcm, we care about the following parameters:

* The ``--nodes`` batch parameter set to 1;
* The ``NPROC`` variable set to 36 (there are 36 cores per node);
* The ``DIR`` variable set to the current run directory;
* The ``EXE`` variable set to ``./bin/regcmMPICLM45``.


.. dropdown:: ``job.sh``

   .. code:: bash

      TODO


After ``job.sh`` is set up, we can **submit** it as follows:

.. code:: bash

   sbatch job.sh


The following command can then be used to to **check on your job's status**:

.. code:: bash

   squeue -u $USER


If the **job completes successfully**, tailing its output should print something like
this:

.. code:: console

   $ tail slurm*.out
   TODO


And the ``output`` directory should now contain several new files, i.e., the **outputs
of the simulation**:

.. code:: console

   $ ls -1rt output  # TODO remove unnecessary outputs


Below is a brief description of what they contain:

.. list-table::
   :header-rows: 1

   * - Output key
     - Description
   * - ``ATM``
     - 3D thermodynamics
   * - ``RAD``
     - 3D radiative transfer
   * - ``SRF``
     - 2D surface fields (including precipitation)
   * - ``SAV`` and ``clm``
     - Data necessary for restarting


You may explore them using ``ncview`` and/or ``ncdump -h``.
In any case, we are done with the uncoupled framework of RegCM and you can proceed to
the next part.
