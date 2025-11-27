Install, setup & run the RegCM-OASIS-SYMPHONIE air-sea coupled model
====================================================================

This home page presents a training that covers installing, setting up and
running the RegCM-OASIS-SYMPHONIE air-sea coupled model on a supercomputer
(either CALMIP or HILO). Please start by reading through this page, which precises the
training's scope, requirements, materials and outline.

The left-hand side panel indicates your location on this website at any time in the
training.
Code blocks include a copy button in the top-right corner for easy reuse
(although it's not always relevant to copy the whole block).

We hope you
find this training clear and helpful, and that it provides the answers you're looking
for.


Scope
-----

The training on this website does not focus on each component of the coupled system
we are setting up, but rather on a way to make them work together. Moreover, the
proposed flow is, precisely, a proposition, meaning that there surely are other methods
to couple those two models. This way, we will only spend a minimal time on how RegCM and
SYMPHONIE work on their own, and, in particular, omit a lot of the things that make them
complex and versatile tools, focusing instead on OASIS and their interaction through it.
To go further, please find hereafter links toward the existing documentations for each
tool.

.. seealso::

   * `RegCM documentation <https://github.com/ICTP/RegCM/tree/master/Doc/UserGuide>`_
   * `SYMPHONIE general references and documentation <https://sirocco.obs-mip.fr/ocean-models/s-model/documentation/>`_
   * `SYMPHONIE-OASIS documentation <https://docs.google.com/document/d/1IsX4KteY13ByUUhumB1FmdGSYLAPn6180NDo6U_MEBw/edit?tab=t.0#heading=h.1y75zn6tkh5o>`_
   * `OASIS documentation <https://cerfacs.fr/oa4web/oasis3-mct_5.0/oasis3mct_UserGuide/index.html>`_


Requirements
------------

The training relies on the following requirements:

* basic Unix system understanding;
* familiarity with command-line text editors such as ``nano``, ``vim``, or ``emacs``, including basic operations like editing, saving, and performing search-and-replace;
* and an account on the CALMIP/HILO supercomputer.


Moreover, it should be supervised by a so-called training master, who prepared:

* model executable (installation is covered at last to prioritize configuring and running the system);
* data and regional configuration files necessary to run the simulations (this is out of this training's scope, and is already described in the models' own documentation);
* and a ``training_ROS`` folder containing the materials explained below.


Where to get the sources
------------------------

**You don't need to get the sources yourself for this training!**
Nonetheless, below is presented how to get the original source for each component.

RegCM is public with an MIT licence, available on `GitHub <https://github.com/ICTP/RegCM>`_.

SYMPHONIE can be shared freely (you can retrieve the source from the training materials),
but you first need to contact the `SIROCCO <https://sirocco.obs-mip.fr/register-for-download-access/>`_
group.

As for OASIS, you must first **inform the OASIS team** about your use of their coupling
tool, by filling their form at the following `link <https://oasis.cerfacs.fr/en/download-oasis3-mct-sources/>`_
(one registration per laboratory is enough). Once you've filled the form, you'll be
given access to the most updated source code (which merges several licences). However,
this training does not rely on your own codes, so you can download the coupler for
yourself only later.


Materials and setup
-------------------

1. Log in to your cluster session (replace ``$USER`` by your username):

.. tab-set::

   .. tab-item:: HILO

      .. code:: bash

         scp -XY $USER@hilo.usth.edu.vn

   
   .. tab-item:: CALMIP

      .. code:: bash

         scp -XY $USER@olympe.calmip.univ-toulouse.fr


2. Then, ``training_ROS`` is a folder containing all the resources you will need for the training. Let us start by using its ``config.sh`` script to configure our environment:

.. tab-set::

   .. tab-item:: HILO

      .. code:: bash

         source /work/users/desmetq/training_ROS/config.sh


   .. tab-item:: CALMIP

      .. code:: bash

         source /tmpdir/desmet/training_ROS/config.sh


Make sure both variables ``$TRAINING`` and ``$RUN`` exist and are correct.
They are the directories we will be using throughout the training.
``$TRAINING`` contains the training materials; ``$RUN`` is your playground directory
for running the models.

.. code:: bash

   echo $TRAINING
   echo $RUN


3. Create your run directory for conducting the training tasks:

.. code:: bash

   mkdir $RUN


.. important::

   You will need to ``source`` the ``config.sh`` file **each time you reconnect**.


Outline
-------

After installation, the training is decomposed in **two major parts**. Those parts
do not rely on your own model executables, such that the installation guide can be
addressed independently.

0. :doc:`Installation guide (optional) <installation/index>`
1. :doc:`Component-wise frameworks <component-wise/index>`
2. :doc:`Coupling both components <coupling/index>`


.. toctree::
   :maxdepth: 1
   :caption: Training contents
   :hidden:

   Home <self>
   installation/index
   component-wise/index
   coupling/index
   further/index
