Training: install, setup & run the RegCM-OASIS-SYMPHONIE air-sea coupled model on CALMIP
========================================================================================

This home page presents a self-contained training that covers installing, setting up and
running the RegCM-OASIS-SYMPHONIE air-sea coupled model on the supercomputer named
CALMIP. Please start by reading through this page, which precises the training's scope,
requirements, materials and outline. The left-hand side panel provides a search bar,
and indicates your location on this website at any time in the training. Code blocks
include a copy button in the top-right corner for easy reuse. We hope you find this
training clear and helpful, and that it provides the answers you're looking for.


Scope
-----

The training on this website does not focus on each component of the coupled system
we are setting up, but rather on a way to make them work together. Moreover, the
proposed flow is, precisely, a proposition, meaning that there surely are other methods
to couple the components. This way, we will only spend a minimal time on how RegCM and
SYMPHONIE work on their own, and, in particular, omit a lot of the things that make them
complex and versatile tools, focusing instead on their interaction. To go further,
please find hereafter links towards the existing documentations for each tool.

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
* and an account on the CALMIP supercomputer, implying a username and project.


Moreover, it should be supervised by a so-called training master who prepared:

* model executable (installation is not the primary focus of this training and is only detailed in the last section of this document for completeness);
* data and regional configuration files necessary to run the simulations (this is out of this training's scope);
* and a ``training_ros`` folder containing the materials explained below.


Materials and setup
-------------------

1. ``training_ros`` is a folder containing all the resources you will need for the training. Locate it.
2. Configure your environment for the training using the ``config.sh`` script:

.. code:: bash

   source /path/to/training_ros/config.sh


3. Create and record a run directory for conducting the training's tasks:

.. code:: bash

   export RUN=/tmpdir/$USER/training_playground
   mkdir $RUN


Make sure both variables ``$TRAINING`` and ``$RUN`` exist and are correct.
Then, we can proceed further.


Outline
-------

The training is decomposed in **two major parts**:

#. :doc:`Component-wise frameworks <component-wise/index>`
#. :doc:`Coupling both components <coupling/index>`


In addition (mostly if time allows it), you can follow the following sections to
**extend your understanding** of the framework, **from installation to implementing
advanced setups**:

* :doc:`Installation guide <installation/index>`
* :doc:`To go further <further/index>`


.. toctree::
   :maxdepth: 1
   :caption: Training contents
   :hidden:

   Home <self>
   component-wise/index
   coupling/index
   installation/index
   further/index

