Component-wise frameworks
=========================

Running the coupled model basically consists of running both components at the same
time in their OASIS-enabled version, making it essential to understand first how they
work independently. Therefore, as a first step in this training, we will get to
**understand each component's distinct framework**, ultimately **running uncoupled
simulations** and getting through their specific **outputs**.

Whether to start by RegCM or SYMPHONIE does not matter here, although you'll get a more
progressive difficulty by starting with RegCM, whose execution is more straightforward.

.. toctree::
   :maxdepth: 1
   :hidden:

   regcm/index
   symphonie/index


.. grid:: 2
   :gutter: 5

   .. grid-item-card:: RegCM framework
      :link: regcm/index
      :link-type: doc
      :text-align: center

      Run directory structure, namelists, preprocessing, running...


   .. grid-item-card:: SYMPHONIE framework
      :link: symphonie/index
      :link-type: doc
      :text-align: center

      Run directory structure, notebooks, initialization, running...
