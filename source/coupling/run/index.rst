Execution
=========

Now that we understand well how to configure all the namelists to exchange coupling
fields through OASIS, we can actually run coupled simulations.
The flow proposed in this section is not necessarily the flow you should always use
when runing the coupled system, yet the narrative allows covering some essential
technical points to give you all foundational skills to use the models.

Like for :doc:`uncoupled setup <../../component-wise/index>`, we will first explain
the run folder structure of a coupled setup. Then, we will conduct several coupled runs:
initialization will allow us to produce restart files, and the main run will be
divided into a spinup and a production run, enabling to demonstrate how to restart the
whole system from a previous simulation.

.. toctree::
   :maxdepth: 1

   structure
   initialize
   spinup
   production