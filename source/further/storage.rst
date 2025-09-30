Storage management
==================

Generalities
------------

On most supercomputers, users have access to several types of storage, whose capacity
and backup features make them adapted to different types of usage. Two typical storage
types (at least) generally exist: the so-called "home" and "work" directory:

+----------------+-------------------------+---------------------------------+
| Directory      | Home                    | Work                            |
+================+=========================+=================================+
| Path on HILO   | ``/home/$USER``         | ``/work/$USER``                 |
+----------------+-------------------------+---------------------------------+
| Path on CALMIP | ``/users/$GROUP/$USER`` | ``/tmpdir/$USER``               |
+----------------+-------------------------+---------------------------------+
| Backup         | Frequent                | None, may even have restictions |
+----------------+-------------------------+---------------------------------+
| Capacity       | A few GB per users      | Many TB (shared)                |
+----------------+-------------------------+---------------------------------+
| Typical usage  | Scripts, softwares,     | Simulation outputs,             |
|                | models, configurations, | observation data,               |
|                | environments, ...       | tests, ...                      |
+----------------+-------------------------+---------------------------------+


Characterizing our coupled run's items
--------------------------------------

With this in mind, let us span through our coupled run files and folders and sort them
into "home-type" (lightweight and critical, i.e., requiring backup) or "work-type" items
(heavyweight or not critical).

Below is a reminder of a coupled run folder structure. Qualify each item by yourself,
then open the dropdown menu for a proposition of solution.

.. code::

   coupled_run
   ├── job.sh
   ├── namcouple
   ├── oasis
   ├── regcm
   │   ├── bin
   │   ├── input
   │   ├── namelist.f
   │   └── output
   └── symphonie
       ├── bin
       ├── description_domaine.next
       ├── description_trous.txt
       ├── GRAPHICS
       ├── grid.nc
       ├── NOTEBOOKS
       ├── notebook_list.f
       ├── OFFLINE
       ├── restart_input
       ├── restart_outbis
       ├── restart_output
       ├── TIDES
       └── tmp


.. dropdown:: Solution

   We starred below the items we consider as "home-type". Others are considered as
   "work-type":

   .. code::

      coupled_run
      ├── job.sh
      ├── namcouple*
      ├── oasis
      ├── regcm
      │   ├── bin*
      │   ├── input
      │   ├── namelist.f*
      │   └── output
      └── symphonie
         ├── bin*
         ├── description_domaine.next
         ├── description_trous.txt
         ├── GRAPHICS
         ├── grid.nc
         ├── NOTEBOOKS*
         ├── notebook_list.f
         ├── OFFLINE
         ├── restart_input
         ├── restart_outbis
         ├── restart_output
         ├── TIDES
         └── tmp


   We like to think about it like: **Which items are crucial to reproduce the run?**
   To this, we answer: the models (``bin`` directories) and the run's configuration
   files with ``namcouple``, RegCM's ``namelist.f`` and SYMPHONIE's ``NOTEBOOKS``
   folder. Everything else can be recoded easily or recomputed.
   
   .. note::
      
      It's acceptable to also consider ``job.sh`` and ``symphonie/notebook_list.f``
      as crucial, but with experience, you will see that they can be easily retrieved
      or recoded from scratch.


In practice
-----------

In practice, symbolic links are employed to work with items from both home and work
storage in the same directory, while keeping the same run structure.

.. admonition:: Symbolic link basics

   A symbolic link is like a shortcut in Windows or a Finder alias on macOS. It just
   points to another file or folder, it's not a copy. If the original changes,
   the link shows the changes too. If the original is deleted, the link breaks
   (becomes useless).

   For example, to make a link named ``my_link.sh`` to the ``~/.bashrc`` file that we
   all have, we run the following command:

   .. code:: bash

      ln -sf ~/.bashrc my_link.sh

   with ``-s`` meaning "symbolic", and ``-f`` meaning "force", i.e., overwriting 
   potentially existing links with the same name.

   Note that you may also link directories.


Back to the ``$RUN`` playground folder, let us first notice that the ``bin`` directories
are already links to the training's executables. For instance, on CALMIP:

.. code:: console

   $ cd $RUN
   $ ls -l regcm/bin
   lrwxrwxrwx. 1 desmet p20055 44 Sep 17 11:01 regcm/bin -> /tmpdir/desmet/training_ROS/models/RegCM/bin


For your future experiments when you will be using your own executables, the
recommendation is to **install the models in your home directory**. You will then work
from a run directory located in a work-type storage, and access the model executables
using links to the your home storage: to RegCM's ``bin`` and/or SYMPHONIE's ``RDIR``.
For example, while building a SYMPHONIE-only run folder, and with your SYMPHONIE
installation located at ``~/SYMPHONIE``, you would implement a link command of this
type:

.. code:: bash

   ln -sf ~/SYMPHONIE/RDIR bin


Now, let us address the configuration files. The goal here is to keep the
keys needed to reproduce the run. In the long term, you should maintain a
**history of your runs safely stored in your home directory**. It is not
strictly necessary to create links in your run directory in order to edit
the files safely (i.e., with regular backups) during testing, debugging,
and configuring your simulation. Instead, you may simply work in the work
storage until your simulation is successful, and then copy the definitive
namelists to your home storage for archiving. The important point is to
ensure they are in your home at the end.

As an example, let us relocate the configuration files of ``$RUN``. The
lines below create dedicated folders in your home directory for storing
the configuration files, rename them with a date to make them unique, and
link them back to the run folder under their original names.


.. code:: bash

   cd $RUN
   mkdir -p ~/{namcouples,namelists,notebooks}
   cd oasis
   for file in namcouple*; do
       home_file=namcouple-251128${file#namcouple}
       mv $file ~/namcouples/$home_file
       ln -sf ~/namcouples/$home_file $file
   done
   cd ../regcm
   for file in namelist*.f; do
       home_file=namelist-251128${file#namelist}
       mv $file ~/namelists/$home_file
       ln -sf ~/namelists/$home_file $file
   done
   cd ../symphonie
   for dir in NOTEBOOKS*; do
       home_dir=NOTEBOOKS-251128${dir#NOTEBOOKS}
       mv $dir ~/notebooks/$home_dir
       ln -sf ~/notebooks/$home_dir $dir
   done
   cp -p notebook_list.f ~/notebooks/


Now it is up to you to **organise your workflow and apply what we have
covered on this page the way you like**. We suggest creating scripts to make all of this
systematic, so you never risk losing important files while keeping your
simulation experience comfortable.
