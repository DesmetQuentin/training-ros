Training: install, setup & run the RegCM-OASIS-SYMPHONIE air-sea coupled model on CALMIP
========================================================================================

This training is self-contained and follows the structure shown in the table of contents
below. You can also navigate using the right-hand panel, and return to the top of the
document by clicking on section titles. Code blocks include a copy button in the
top-right corner for easy reuse. We hope you find this training clear and helpful, and
that it provides the answers you're looking for.


Scope
-----

.. seealso::

   * `RegCM documentation <https://github.com/ICTP/RegCM/tree/master/Doc/UserGuide>`_
   * `SYMPHONIE general references and documentation <https://sirocco.obs-mip.fr/ocean-models/s-model/documentation/>`_
   * `SYMPHONIE-OASIS documentation <https://docs.google.com/document/d/1IsX4KteY13ByUUhumB1FmdGSYLAPn6180NDo6U_MEBw/edit?tab=t.0#heading=h.1y75zn6tkh5o>`_
   * `OASIS documentation <https://cerfacs.fr/oa4web/oasis3-mct_5.0/oasis3mct_UserGuide/index.html>`_


Requirements
------------

* Basic unix system understanding
* Familiarity with command-line text editors such as nano, vim, or emacs is required, including basic operations like editing, saving, and performing search-and-replace.
* username
* group name & macro
* a training master has prepared model executable (installation is not the primary focus of this training and is only detailed in the last section of this document)
* a training master has prepared data and regional configuration files necessary to run the simulations (this is out of this training's scope)
* access to the training_ros materials explained below


Materials
---------

* tree structure
* environment variable
* source config.sh
* mkdir training_playground


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

