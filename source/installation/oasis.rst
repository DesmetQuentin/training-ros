Install OASIS3-MCT
==================

Let us get to the right directory:

.. code:: bash

   cd $OASIS/util/make_dir


From here, you should see many examples of ``make.*`` files, containing compilation
dependencies adapted to various setups. Our setup is based on ``intel18`` on the CALMIP
center: let us name our own file ``make.intel18_calmip``. The file content is
expandable below.

.. dropdown:: ``make.intel18_calmip``

   .. code:: make

      #
      # Include file for OASIS3 Makefile for a Linux system using 
      # Portland Group Fortran Compiler and MPICH
      #
      ###############################################################################
      #
      # CHAN	: communication technique used in OASIS3 (MPI1/MPI2)
      CHAN    = MPI1
      #
      # Paths for libraries, object files and binaries
      #
      # COUPLE	: path for oasis3-mct main directory
      COUPLE  = $(OASIS)
      #
      # ARCHDIR : directory created when compiling
      ARCHDIR = $(COUPLE)/intel18_calmip
      #
      # MPI library (see the file /etc/modulefiles/mpi/openmpi-x86_64)
      #
      MPIDIR      = /usr/local/intel/2018.2.046/impi/2018.2.199/intel64
      MPIBIN      = $(MPIDIR)/bin
      MPI_INCLUDE = -I$(MPIDIR)/include 
      MPILIB      = -L$(MPIDIR)/lib
      #
      # NETCDF library of the system
      #
      NETCDF_INCLUDE = -I/usr/local/netcdf/4.6.1-intelmpi/include -I/usr/local/pnetcdf/1.9.0/include
      NETCDF_LIBRARY = -L/usr/local/netcdf/4.6.1-intelmpi/lib -lnetcdff -Wl,-rpath,/usr/local/intel/2018.2.046/compilers_and_libraries/linux/lib/intel64 -Wl,-rpath,/usr/local/hdf5/1.10.2/intel_mpi/lib -lnetcdf -lnetcdf /usr/local/pnetcdf/1.9.0/lib/libpnetcdf.a
      #
      # Compiling and other commands
      #
      MAKE        = gmake
      F90         = $(MPIBIN)/mpiifort $(MPI_INCLUDE)
      F           = $(F90)
      f90         = $(F90)
      f           = $(F90)
      CC          = $(MPIBIN)/mpiicc $(MPI_INCLUDE)
      LD          = $(MPIBIN)/mpiifort $(MPILIB)
      AR          = ar
      ARFLAGS     = -ruv
      #
      # CPP keys and compiler options
      #  
      CPPDEF    = -Duse_comm_$(CHAN) -D__VERBOSE -DTREAT_OVERLAY
      F90FLAGS_1  = -g -traceback -O2 -xAVX -I. -assume byterecl -mt_mpi 
      f90FLAGS_1  = $(F90FLAGS_1)
      FFLAGS_1    = $(F90FLAGS_1)
      fFLAGS_1    = $(F90FLAGS_1)
      CCFLAGS_1   = 
      LDFLAGS     = $(F90FLAGS_1)
      #
      #
      ###################
      #
      # Additional definitions that should not be changed
      #
      FLIBS		= $(NETCDF_LIBRARY)
      # BINDIR        : directory for executables
      BINDIR          = $(ARCHDIR)/bin
      # LIBBUILD      : contains a directory for each library
      LIBBUILD        = $(ARCHDIR)/build/lib
      # INCPSMILE     : includes all *o and *mod for each library
      INCPSMILE       = -I$(LIBBUILD)/psmile.$(CHAN) -I$(LIBBUILD)/scrip -I$(LIBBUILD)/mct 

      F90FLAGS  = $(F90FLAGS_1) $(CPPDEF) $(INCPSMILE) $(NETCDF_INCLUDE)
      f90FLAGS  = $(f90FLAGS_1) $(CPPDEF) $(INCPSMILE) $(NETCDF_INCLUDE)
      FFLAGS    = $(FFLAGS_1) $(CPPDEF) $(INCPSMILE) $(NETCDF_INCLUDE)
      fFLAGS    = $(fFLAGS_1) $(CPPDEF) $(INCPSMILE) $(NETCDF_INCLUDE)
      CCFLAGS   = $(CCFLAGS_1) $(CPPDEF) $(INCPSMILE) $(NETCDF_INCLUDE)
      #
      #############################################################################


Then, include the above file in the ``make.inc``.

.. dropdown:: ``make.inc``

   .. code:: make

      #
      # System dependent settings
      #
      ##### User configurable options #####
      #
      # Note: The absolute path name must be indicated.
      #
      # Note: Choose one of these includes files and modify it according to your
      #       local settings. Replace the currently active file with your own.
      #
      include $(OASIS)/util/make_dir/make.intel18_calmip
      #
      ### End User configurable options ###


Once those files are configured as indicated, compile with the following command:

.. code:: bash

   make -f TopMakefileOasis3


.. admonition:: Cleaning command

   To restart compilation from scratch, run the command below before recompiling:

   .. code:: bash

      make -f TopMakefileOasis3 realclean
