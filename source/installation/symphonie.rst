Install SYMPHONIE
=================

Let us get to the right directory:

.. code:: bash

   cd $SYMPHONIE


Here, we drag our attention on three folders, each relating to the installation of a
specific configuration in some way:


.. list-table::
   :header-rows: 1

   * - Folder
     - Meaning
     - Function
   * - ``CDIR_*``
     - Compiled Directory
     - Contain all compilation results
   * - ``RDIR``
     - Run Directory
     - Contain the executable
   * - ``UDIR``
     - User Directory
     - Contain configuration-specific source code and Makefiles


.. note::

   The suffix put after ``CDIR_`` refers to the employed compiler. In our case, we will
   be using ``ifort``, hence focusing on ``CDIR_IFORT``.


When designing a configuration, each of these three folders will have one subdirectory
named after it. We're now going to create our own. Let us start by installing an
OASIS-disabled version of SYMPHONIE: we call it ``ORIGIN``. The first step is to
**create the configuration subdirectories**:

.. code:: bash

   mkdir -p {CDIR_IFORT,RDIR,UDIR}/ORIGIN


Then, everything happens **in the user directory**:

.. code:: bash

   cd UDIR/ORIGIN


From here, we need to **create two Makefiles**: ``makefile`` which contains all the
compilation instructions to the ``make`` program, and ``makefile.inc`` which stores all
the dependencies of your configuration. You can find many examples of these files in
``$SYMPHONIE/configbox``. For this training on CALMIP and using ``intel18``, use the
two following:

.. dropdown:: ``makefile``

   .. code:: make

      TODO


.. dropdown:: ``makefile.inc``

   .. code:: make

      TODO


.. tip::

   Beside ``makefile`` and ``makefile.inc``, you can also add some source code in the
   user directory. Concretely, ``make`` will see a list of file names in your
   ``makefile``, then will look after them in your configuration's user directory first,
   before searching in ``$SYMPHONIE/SOURCES``. Therefore, source files with the same
   name as in ``$SYMPHONIE/SOURCES`` but placed in your configuration's user directory
   will be those actually considered for the compilation, allowing you to bring up some
   modifications to the code without permanently affecting the original source files
   (another configuration could still be compiled using the original source, or
   different user modifications). To implement this workflow safely, make sure first to
   copy the file of interest from the sources (from your user directory):

   .. code:: bash

      cp -p $SYMPHONIE/SOURCES/<some-file>.F90 .


   Then only may you modify it.


The ``make`` command then **proceeds to both compilation and installation**
(potentially taking several minutes):

.. code:: bash

   make


Compilation results are stored in ``$SYMPHONIE/CDIR_IFORT/ORIGIN``, and the executable
goes to ``$SYMPHONIE/RDIR/ORIGIN``:

.. code:: console

   $ ls $SYMPHONIE/RDIR/ORIGIN
   symphonie.exe


.. admonition:: Cleaning command

   To restart compilation/installation from scratch (e.g., because you have changed
   the compilation keys in your configuration's ``makefile``), run the command below
   before running make again:

   .. code:: bash

      make clean


Let us now follow the same steps, but **designing an OASIS-enabled configuration**.
Let us simply call it ``OASIS``:

.. code:: bash

   cd $SYMPHONIE
   mkdir -p {CDIR_IFORT,RDIR,UDIR}/OASIS
   cd UDIR/OASIS


Then, **copy the** ``makefile`` from the ``ORIGIN`` configuration:

.. code:: bash

   cp ../ORIGIN/makefile .


Open it, and **edit the** ``KEY1`` variable to enable OASIS-related compilation keys:

.. code:: make

   KEY1 = -Dstokes -Dkey_oasis_generic


Then, **create a** ``makefile.inc`` **including the OASIS library**:

.. dropdown:: OASIS-enabled ``makefile.inc``

   .. code:: make

      TODO


You can now **use** ``make`` in the same way as before, and check that this creates the
``symphonie.exe`` executable in ``$SYMPHONIE/RDIR/OASIS``.
