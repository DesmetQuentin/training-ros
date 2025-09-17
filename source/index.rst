Install, setup & run the RegCM-OASIS-SYMPHONIE air-sea coupled model
====================================================================

This home page presents a training that covers installing, setting up and
running the RegCM-OASIS-SYMPHONIE air-sea coupled model on a supercomputer
(either CALMIP or HILO). Please start by reading through this page, which precises the
training's scope, requirements, materials and outline. The left-hand side panel provides
a search bar, and indicates your location on this website at any time in the training.
Code blocks include a copy button in the top-right corner for easy reuse. We hope you
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


Materials and setup
-------------------

1. ``training_ROS`` is a folder containing all the resources you will need for the training. You can locate it with the help of your training master.
2. Configure your environment for the training using the ``config.sh`` script:

.. tab-set::

   .. tab-item:: CALMIP

      .. code:: bash

         source /tmpdir/desmet/training_ROS/config.sh
   

   .. tab-item:: HILO

      .. code:: bash

         TODO


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


Outline
-------

After installation, the training is decomposed in **two major parts**:

0. :doc:`Installation guide <installation/index>`
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
