|algo| algorithm
================

This section describes an evolutionary algorithm for oblique full DT induction using supervised learning - |algo|. As we have seen in the introduction (:num:`Section #sec-dt-induction`), an algorithm that would take advantage of the full DT induction, but limit its resource consumption to make it attractive for the world of embedded systems is lacking in the open literature. The main motivation for creating |algo|, was thus to develop an algorithm that:

- is suitable for the implementation on embedded systems, i.e. has low hardware resource requirements,
- is easy parallelizable and accelerated in hardware, and
- uses nonincremental DT induction to induce smaller DTs than the existing solutions, without the loss in DT accuracy.

Since inferring an optimal DT in terms of both size and accuracy is an NP-hard problem, the |algo| algorithm needed to be based on some kind of heuristic. In order to minimize the hardware resource consumption of the algorithm implementation, it was chosen to be operated only on a single candidate solution, effectively excluding all the algorithms that operate on populations, such as particle swarm optimization, memetic algorithms, genetic algorithms, and some types of evolutionary algorithms. For all these reasons, it was chosen to base the |algo| algorithm on the (1+1) Evolutionary Strategy, since on one hand it operates on a single individual, while on the other it was supposed to be capable of managing the highly complex problem of searching for the small, yet accurate enough DTs, by using the nature inspired evolutionary process. The following topics will be covered in this section:

- :num:`Section #sec-algorithm-overview` - Overview of the algorithm
- :num:`Section #sec-algo-detailed-description` - Detailed description of the algorithm
- :num:`Section #sec-algo-improvements` - The improvements to the basic algorithm version
- :num:`Section #sec-complexity` - Analysis of the algorithm's computational complexity
- :num:`Section #sec-efti-experiments` - Experimental section that shows the performance of the |algo| algorithm in comparison to the performances of the existing DT induction algorithms

.. _sec-algorithm-overview:

The algorithm overview
----------------------

The :num:`Algorithm #fig-algorithm-pca` shows the algorithmic framework for the |algo| algorithm, which is similar for all evolutionary algorithms and comprises mutation, fitness evaluation and selection tasks, but lacks the crossover step, since the algorithm does not employ a population of individuals. The DT is induced from the training set - the argument ``train_set`` received by the ``efti()`` function as shown in pseudo-code. Since the |algo| algorithm performs supervised learning, the training set should consist of the problem instances, together with their known class memberships. The |algo| algorithm maintains a single candidate solution, stored in the variable ``dt`` in the pseudo-code. The evolution is started from a randomly generated (by the ``initialize()`` function) one-node DT, consisting only of the root node, and the effort is iteratively made to improve on it. In each iteration, the DT is slightly changed by the ``mutate()`` function, to obtain the mutated individual which is then stored in the ``dt_mut`` variable. Two types of mutations are employed on the DT individual:

- Every iteration, a node test coefficient in a certain number of randomly selected nodes is changed, and
- Every few iterations, a node is either added or removed from the DT

.. _fig-algorithm-pca:

.. literalinclude:: code/algorithm.py
    :caption: Overview of the |algo| algorithm

The fitness of the mutated individual, calculated by the ``fitness_eval()`` function (:num:`Algorithm #fig-fitness-eval-pca`), is then compared with the fitness of the candidate solution within the ``select()`` function (:num:`Algorithm #fig-selection-vanilla-pca), which decides whether the mutated individual will be taken as the new candidate solution, i.e. will it become the base for the mutation in the iterations to follow. During ``max_iter`` iterations, the |algo| algorithm tries to improve upon the DT candidate solution, after which the algorithm exits and the fittest DT individual found during this process is returned. Once the DT is formed in this way, it can be used to classify problem instances outside of the training set.

In the :num:`Figures #fig-efti-overview00` through :num:`#fig-efti-overview07`, one example evolutionary process performed by the |algo| algorithm on the ``vene`` dataset is shown. The ``vene`` dataset contains instances of three different classes: :math:`C_1`, marked by the red stars, :math:`C_2`, marked by the green squares, and :math:`C_3`, marked by the blue triangles. Eight specific moments in the DT evolution where significant breakthroughs in the fitness of the DT were made, are presented in these figures by both plotting the tree structure and displaying the partition of the attribute space that the DT individuals at these moments induced. The nodes are drawn in the figures using circles and the leaves using squares, and each node and each leaf is assigned a unique ID. Each leaf node and its corresponding attribute space region are labeled in the format *i-Cj*, where *i* equals the ID of the leaf, and *j* equals the class number assigned to that leaf, hence also to the region. For each of these figures, the following information is given:

- Iteration - the iteration number in which the DT individual was evolved
- Fitness - the fitness of the DT individual
- Size - the size of the DT individual: calculated as the number of leaves in the DT
- Accuracy - the accuracy of the DT individual on the training set: calculated as the percentage of the instances from the training set that the DT individual classifies correctly

.. subfigstart::

.. _fig-efti-overview-dot00:

.. figure:: images/efti_overview_dts/dot00.png
    :width: 100%
    :align: center

    Initial one-node DT generated by the ``initialize()`` function

.. _fig-efti-overview-attr00:

.. figure:: images/efti_overview_dts/dt00.pdf
    :width: 93%
    :align: center

    Initial attribute space partition

.. subfigend::
    :width: 0.48
    :label: fig-efti-overview00
    :after: \quad

    An example evolutionary process by the |algo| algorithm. Iteration: 000000, Fitness: 0.6024, Size: 2, Accuracy: 0.6005

.. subfigstart::

.. _fig-efti-overview-dot01:

.. figure:: images/efti_overview_dts/dot01.png
    :width: 100%
    :align: center

    No added nodes that were tried managed to increase fitness

.. _fig-efti-overview-attr01:

.. figure:: images/efti_overview_dts/dt01.pdf
    :width: 93%
    :align: center

    Position of the split shifted to increase the accuracy

.. subfigend::
    :width: 0.48
    :label: fig-efti-overview01
    :after: \quad

    An example evolutionary process by the |algo| algorithm. Iteration: 000013, Fitness: 0.6287, Size: 2, Accuracy: 0.6274

.. subfigstart::

.. _fig-efti-overview-dot02:

.. figure:: images/efti_overview_dts/dot02.png
    :width: 100%
    :align: center

    Three new nodes added to increase the accuracy

.. _fig-efti-overview-attr02:

.. figure:: images/efti_overview_dts/dt02.pdf
    :width: 93%
    :align: center

    Three new splits added for finer attribute space partition

.. subfigend::
    :width: 0.48
    :label: fig-efti-overview02
    :after: \quad

    An example evolutionary process by the |algo| algorithm. Iteration: 003599, Fitness: 0.9138, Size: 5, Accuracy: 0.9202

.. subfigstart::

.. _fig-efti-overview-dot03:
.. figure:: images/efti_overview_dts/dot03.png
    :width: 100%
    :align: center

    Since the region of leaf #6 contained almost no individuals in the :num:`Figure #fig-efti-overview-attr02`, it was removed and the node #7 was basically moved up to replace node #3 (:num:`Figure #fig-efti-overview-dot02`), and thus removing the said empty region.

.. _fig-efti-overview-attr03:
.. figure:: images/efti_overview_dts/dt03.pdf
    :width: 93%
    :align: center

    The region of the leaf #6 (:num:`Figure #fig-efti-overview-attr02`) was removed, since it was almost empty and contributed little to accuracy. The resulting DT is smaller, even with a slight increase in accuracy (since the split induced by node 1 has also shifted slightly to a better position).

.. subfigend::
    :width: 0.48
    :label: fig-efti-overview03
    :after: \quad

    An example evolutionary process by the |algo| algorithm. Iteration: 007859, Fitness: 0.9265 Size: 4, Accuracy: 0.9297

.. subfigstart::

.. _fig-efti-overview-dot04:
.. figure:: images/efti_overview_dts/dot04.png
    :width: 100%
    :align: center

    The leaf #5 was made into a node

.. _fig-efti-overview-attr04:
.. figure:: images/efti_overview_dts/dt04.pdf
    :width: 93%
    :align: center

    Small increase in accuracy was obtained by further dividing the central region of the attribute space, where the individuals of all three classes overlap

.. subfigend::
    :width: 0.48
    :label: fig-efti-overview04
    :after: \quad

    An example evolutionary process by the |algo| algorithm. Iteration: 030268, Fitness: 0.9272, Size: 5, Accuracy: 0.9331

.. subfigstart::

.. _fig-efti-overview-dot05:
.. figure:: images/efti_overview_dts/dot05.png
    :width: 100%
    :align: center

    The leaf #4 was now made into a node

.. _fig-efti-overview-attr05:
.. figure:: images/efti_overview_dts/dt05.pdf
    :width: 93%
    :align: center

    Again, further division of central attribute space region produced a small increase in accuracy. Fitness has progressed even less, since the addition of a new node diminished the advantage of a small accuracy increase.

.. subfigend::
    :width: 0.48
    :label: fig-efti-overview05
    :after: \quad

    An example evolutionary process by the |algo| algorithm. Iteration: 177050, Fitness: 0.9273, Size: 6, Accuracy: 0.9374

.. subfigstart::

.. _fig-efti-overview-dot06:
.. figure:: images/efti_overview_dts/dot06.png
    :width: 100%
    :align: center

    The leaf #8 was split into two

.. _fig-efti-overview-attr06:
.. figure:: images/efti_overview_dts/dt06.pdf
    :width: 93%
    :align: center

    The region of leaf #8 was split, bringing no improvement to the class separation, but with some other shifts in the split positions, some small accuracy gain was achieved

.. subfigend::
    :width: 0.48
    :label: fig-efti-overview06
    :after: \quad

    An example evolutionary process by the |algo| algorithm. Iteration: 279512, Fitness: 0.9274, Size: 7, Accuracy: 0.9395

.. subfigstart::

.. _fig-efti-overview-dot07:
.. figure:: images/efti_overview_dts/dot07.png
    :width: 100%
    :align: center

    Leaf #9 was removed together with the node #4, which brought the node #8 up in the place of the node #4. Leaves #10 and #11 were removed, and the node #5 was reverted to leaf again.

.. _fig-efti-overview-attr07:
.. figure:: images/efti_overview_dts/dt07.pdf
    :width: 93%
    :align: center

    |algo| gave up on finely partitioning the central attribute space region, since very little gain in accuracy could not justify the increase in the DT size, and it managed to produce the smaller DT without sacrificing the accuracy. The split by the node #8 between the regions #12 and #13 in the :num:`Figure #fig-efti-overview06`, became the split between the regions #8 and #9 after the node #8 moved up to replace the node #4. This, once useless split, has now shifted to turn out very useful in separating instances of the classes :math:`C_1` and :math:`C_3` and hence contributing to the accuracy.

.. subfigend::
    :width: 0.48
    :label: fig-efti-overview07
    :after: \quad

    An example evolutionary process by the |algo| algorithm. Iteration: 415517, Fitness: 0.9342, Size: 5, Accuracy: 0.9396

At the beginning of the |algo| algorithm, the initial individual is generated (:num:`Figure #fig-efti-overview00`) to contain only one node, since |algo| has a goal of creating DTs as small as possible. By the iteration #13 (:num:`Figure #fig-efti-overview01`), no new nodes were added, but the root node test was modified to produce the increase in the DT accuracy from 0.6005 to 0.6274. During the further evolution, some nodes were added which raised the accuracy of the DT. Notice how fitness started to deviate from the accuracy when the DT grew bigger. This is because the fitness also depends on the size of the DT to which it applies, in that it is more significantly penalized, the more leaves the DT has. In this example, the biggest drop in the fitness caused by the DT size is in the iteration #279512 of the DT evolution (:num:`Figure #fig-efti-overview06`), where the DT individual comprised 7 leaves and even though the accuracy climbed to 0.9395 (classification success rate of 94%), the fitness remained at 0.9274. In this way, the evolutionary process was forced to search for the smaller DT solutions, in which it eventually succeeded by the iteration #415517 (:num:`Figure #fig-efti-overview07`), where the DT size dropped to only 5 leaves with no loss in accuracy.

.. _sec-algo-detailed-description:

Detailed description
--------------------

In this section, the detailed descriptions of the individual |algo| sub-tasks are given. Although |algo| is based on the (1+1)-ES, it comprises many additional features which are specific to the DT induction, that need to be discussed here, like tree structure mutation procedure, fitness calculation specifics, etc.

.. _sec-mutation:

Mutation
........

For the sake of describing an oblique DT, two different sets of information need to be provided: the coefficient numerical data that describe the oblique tests in the nodes, and the topological data that describes the connections between the nodes. Accordingly, inducing an oblique DT implies inducing the node test coefficients as well as the topological structure. Hence, as it was already discussed in the algorithm overview, the |algo| algorithm needs to perform two types of mutations on the DT individual:

- The node test coefficients mutation
- The DT topology mutation

During each iteration of the |algo| algorithm, a small number (|alpha|) of DT nodes' test coefficients is selected at random and then mutated by adding (or subtracting) to it a small random number. Every change in the node test influences the classification, as the instances take different paths through the DT and get classified in a different way. Finding the optimal oblique split is in itself an NP hard problem (as already discussed in the :num:`Section #sec-general-dt-induction`), hence deciding which coefficients should be mutated in order to enhance the DT accuracy is also a hard algorithmic problem. For this reason, the coefficients to be mutated are selected randomly according to the uniform distribution from the set of all coefficients from all DT nodes. Usually, only one to several coefficients (dictated by the parameter |alpha|) are mutated in each iteration in order for the classification result to change in small steps. The larger the number of coefficients mutated in each iteration, the more the algorithm starts behaving as a random search.

Once the decision is made which coefficients are to be mutated, the amount by which to change each of the coefficients needs to be specified. Since the algorithm cannot know in advance the optimal order of magnitude of a coefficient value, which would in turn allow it to adjust the size of the coefficient mutation step, the only reference it can take the advantage of is the coefficient's current value. Furthermore, as it will be discussed in the :num:`Section #sec-node-insertion`, the node test coefficients are not initialized completely at random, but are calculated according to an algorithm to provide an improvement to the overall accuracy of the DT, hence their initial values provide a useful starting reference point in searching for their optimal values. Due to all this, the |algo| algorithm selects the mutation step for the coefficients according to the normal distribution centered at zero, with the standard deviation proportional to the value of the coefficient to be mutated. However, for the coefficients with small values, the deviation would be likewise low, and it would be hard to escape this situation via process of mutation. Similarly, for the coefficients with large values, the deviation would be likewise high, and these coefficients would be changed in too large increments. Hence, the |algo| algorithm saturates the deviation for both small and large coefficient values at :math:`\sigma_{min}` and :math:`\sigma_{max}` respectively. The saturation points :math:`\sigma_{min}` and :math:`\sigma_{max}` are fixed throughout the algorithm operation and selected by the user. The random variable representing the mutation step for the coefficient :math:`w_i`, named :math:`X_{mwi}` is finally given by the equation:

.. math::
    :label: eq-coeff-mutation-distrib

    X_{mwi}\ \sim\ \mathcal{N}(0,\sigma^2)|\sigma=\left\{\begin{alignedat}{2}
        & \sigma_{min}, & & w_i \leq \sigma_{min} \\
        & w_i,          \qquad & \sigma_{min} < & w_i < \sigma_{max} \\
        & \sigma_{max}, \qquad & \sigma_{max} \leq & w_i
    \end{alignedat}\right.

This means that the mutated value :math:`w^m_i` for the selected coefficient :math:`w_i` is obtained as :math:`w^m_i = w_i + X_{mwi}`.

.. subfigstart::

.. _fig-node-addition-before:

.. bdp:: images/node_addition_before.py
    :width: 80%
    :align: center

    DT before the addition of the node in place of the leaf #2

.. _fig-node-addition-after:

.. bdp:: images/node_addition_after.py
    :width: 80%
    :align: center

    DT after a node has been added in place of the leaf #2

.. subfigend::
    :width: 0.35
    :label: fig-node-addition
    :after: \qquad\qquad

    Example showing how a DT is mutated by adding a node to it

.. subfigstart::

.. _fig-node-removal-before:

.. bdp:: images/node_removal_before.py
    :width: 90%
    :align: center

    DT before the removal of the leaf #4, together with its parent node #2

.. _fig-node-removal-after:

.. bdp:: images/node_removal_after.py
    :width: 90%
    :align: center

    DT after the leaf #4 and its parent node #2 were removed, and the sub-tree induced by former node #5 moved to the position of node #2

.. subfigend::
    :width: 0.40
    :label: fig-node-removal
    :after: \qquad

    Example showing how a DT is mutated by removing a node from it

On the other hand, the topology mutations represent very large moves in the search space, so they are performed even less often. In every iteration, there is a chance (|beta|) that a single node will either be added to the DT or removed from it. This change either adds an additional test to the classification process, or removes one from it. The node is always added in place of an existing leaf, i.e. never in place of an internal non-leaf node, as shown in the example in the :num:`Figure #fig-node-addition`. The leaf which is to be turned into a node is selected at random uniformly from all the leaves in the DT. The test coefficients of the newly added non-leaf node are calculated using the same initialization procedure as for the root test coefficients, which is explained in the :num:`Section #sec-node-insertion`. On the other hand, if a node is to be removed, first a leaf is selected at random uniformly from all the leaves in the DT. Then both the leaf and its parent are removed from the DT, while the leaf's sibling moves up to replace its former parent, as shown in the example in the :num:`Figure #fig-node-removal`. By adding a test, a new point is created where during the classification, instances from different classes might separate and take different paths through the DT and eventually be classified as different, which can in turn increase the accuracy of the DT. On the other hand, by removing unnecessary tests the DT is made smaller, and the size of the DT is also an important factor in the fitness calculation in the |algo| algorithm as discussed in the :num:`Section #sec-oversize`.

There is a known result regarding (1+1)-ES algorithms called 1/5 success rule :cite:`auger2009benchmarking`, stating that the mutation step size should be adapted dynamically in order to keep the mutation success rate close to one-fifth, meaning that approximately every fifth mutation should lead to an individual with higher fitness. To accomplish this, the mutation step is dynamically adapted try to control the success rate. There are at least two problems with adopting the 1/5 strategy here: first there are two different types of mutations (coefficient and topological) with each one having its own mutation rate, and second the success rates were measured to be closer to around 1% when the |algo| algorithm was run on practical datasets. Although the effort was made in an attempt to devise a dynamic adaptation strategy akin to the 1/5 success rule that would provide statistically significant benefits to the |algo| algorithm, it was futile.

.. _sec-node-insertion:

The DT node insertion algorithm
...............................

Each time a node is to be added to the DT, whether it is the root node for the DT initialization or any other node in the mutation procedure, the node's test needs to be initialized. Initializing the test coefficients with random numbers proved to be an impediment to the evolutionary process, since there is a rather small probability for a node test generated in this way to provide a useful split in the attribute space, i.e. a split that divides instances of different classes. With this, completely random, procedure, the hyperplane usually lands completely outside the attribute space region where the instances are located, where the :num:`Figure #fig-split-init-miss1` shows one such hyperplane as an example. Even if the hyperplane intersects the area of the attribute space where the instances reside, the split can still be ineffective in the way that it does not help distinguish between instances of different classes, i.e. it does not contribute to the DT accuracy, where the :num:`Figure #fig-split-init-miss2` shows one such hyperplane as an example. This influences the algorithm convergence negatively, in that it takes too many generations to relocate the ill-positioned hyperplane to the location where it starts contributing to the accuracy of the DT individual.

.. subfigstart::

.. _fig-split-init-miss1:

.. plot:: images/split_init_miss1.py
    :width: 100%
    :align: center

    Hyperplane initialized to the position outside the region where the instances reside

.. _fig-split-init-miss2:

.. plot:: images/split_init_miss2.py
    :width: 100%
    :align: center

    Hyperplane initialized to the position where it does not contribute to the DT accuracy

.. subfigend::
    :width: 0.48
    :label: fig-split-init-miss
    :after: \quad

    Hyperplanes cannot be initialized completely at random, since there is a high chance of them being ineffective

However, in order to allow for wider search space exploration, the node tests need to be generated at random, but this process needs to be guided by the structure of the training set, to speed up the convergence of the evolutionary algorithm towards the optimal solution. One of the approaches for the random initialization basically ensures that two randomly selected training set instances (called a mixed dipole) take different paths during classification at the node being initialized, and is suggested in :cite:`krketowski2005global`. The mixed dipole comprises two instances from the training set that belong to different classes. As shown in the :num:`Figure #fig-dipole-hyperplane`, the procedure consists of placing the hyperplane :math:`H_{ij}(\mathbf{w},\theta)` in the attribute space, perpendicular to the line connecting the mixed dipole :math:`(\mathbf{x}^i, \mathbf{x}^j)`. The hyperplane corresponds to the node test given by the equation :eq:`oblique-test`, where |w| is the test coefficient vector and |th| is the test threshold. The attribute space of the ``vene`` dataset, used in this example has two dimensions, one for each of the attributes :math:`x_1` and :math:`x_2`. The hyperplane's exact position is finally fixed by randomly generated parameter :math:`\delta \in (0,1)`, which determines whether the hyperplane is placed closer to :math:`\mathbf{x}^i` (for :math:`\delta < 0.5`), or closer to :math:`\mathbf{x}^j` (for :math:`\delta > 0.5`). Mathematically, the equation for the hyperplane generated by the method of the mixed dipole described in this paragraph is obtained in the following way:

.. math::
    :label: eq-rnd-dipole-hyperplane

    H_{ij}(\mathbf{w},\theta) &= \mathbf{w}\begin{pmatrix}x_1\\x_2\end{pmatrix} - \theta,\\
    \mathbf{w} &= (\mathbf{x}^i - \mathbf{x}^j),\\
    \theta &= \delta\mathbf{w}\cdot\mathbf{x}^i + (1-\delta)\mathbf{w}\cdot\mathbf{x}^j

.. _fig-dipole-hyperplane:
.. plot:: images/dipole_hyperplane_plot.py
    :width: 55%
    :bbox: tight

    Initialization of the node test based on the randomly chosen dipole. :math:`H_{ij}(\mathbf{w},\theta)` is a hyperplane corresponding to the node test, |w| is coefficient vector, and |th| is the threshold.

This procedure aims to introduce a useful test into the DT, based on the assumption that the instances of the same class are somehow grouped in the attribute space, and that the test produced in this way will help separate the instances belonging to the classes of the dipole instances.

Fitness evaluation
..................

The DT can be optimized with respect to various parameters, where the DT accuracy and its size are usually the most important. Hence, in order to solve this multi-objective optimizational problem with the evolutionary approach, a fitness function needs to be defined to effectively collapse it to a single objective optimizational problem. This can be done in various ways, and here one procedure, employed by the |algo| algorithm is given.

.. _fig-fitness-eval-pca:

.. literalinclude:: code/fitness_eval.py
    :caption: The pseudo-code of the fitness evaluation task, given by :samp:`fitness_eval()` function.

Accuracy calculation
;;;;;;;;;;;;;;;;;;;;

The main task of the optimization process performed by |algo| is to maximize the accuracy of the DT individual on the training set. The accuracy is calculated by letting the DT individual classify all problem instances from the training set and then by comparing the classification results to the desired classifications, specified in the training set. The pseudo-code for this task is given in the :num:`Algorithm #fig-accuracy-calc-pca` by the function ``accuracy_calc()``, where the input parameter ``dt`` receives the DT individual whose accuracy is to be calculated, and ``train_set`` expects the training set.

.. _fig-accuracy-calc-pca:

.. literalinclude:: code/accuracy_calc.py
    :language: python3
    :caption: The pseudo-code of the accuracy calculation task, given by :literal:`accuracy_calc()` function.

First, the class distribution is determined by letting all instances from the training set traverse the DT, within the ``find_dt_leaf_for_inst()`` function whose pseudo-code is given in the :num:`Algorithm #fig-find-dt-leaf-for-inst-pca`. This function determines the instance traversal path, and returns the leaf node in which the instance finished the traversal. The traversal starts at the root node (accessed via ``dt.root``), and is performed in the manner depicted in the :numref:`fig-dt-traversal`, where one possible path is given by the red curvy line. Until a leaf is reached, the node tests are evaluated and the decisions to which child to proceed, are made based on the test outcomes. The function ``dot_product()``, calculates the scalar product of the node test coefficient vector |w| (stored in ``cur_node.w`` attribute), and the attribute vector of the instance |x| (stored in ``instance.x`` variable). The value returned, is compared with the node test threshold |th| (stored in ``cur_node.thr`` attribute).

.. _fig-find-dt-leaf-for-inst-pca:

.. literalinclude:: code/find_dt_leaf_for_inst.py
    :caption: The pseudo-code of the procedure for determining the end-leaf for an instance, implemented by :literal:`find_dt_leaf_for_inst()` function.

Next step in the accuracy calculation process (the first for loop in the :num:`Algorithm #fig-accuracy-calc-pca`) is to calculate the class distribution matrix. The distribution matrix, shown in the :num:`Figure #fig-distribution-matrix`, has one row for each of the leaves in the DT, i.e. for each attribute space partition induced by the DT. Each row in turn contains one element for each of the classes in the training set. Hence, a row of the distribution matrix contains the statistics on how many instances of each of the training set classes finished the traversal in the leaf corresponding to the row.

.. _fig-distribution-matrix:

.. bdp:: images/distribution_matrix.py
    :width: 80%

    The structure of the distribution matrix. From each matrix row *i*, the dominant class :math:`k_i` and the number of instances of the dominant class :math:`d_{(i,k_i)}` that finished the traversal in the leaf with ID *i* are obtained.

The classes of all the instances from the training set are known and accessed via the instance attribute ``instance.cls`` (within the ``accuracy_calc()`` function). For each instance in the training set, based on its class and the ID of the leaf in which it finished the traversal, the distribution matrix is updated. This leaf is obtained via the ``find_dt_leaf_for_inst()`` function and stored into the ``leaf`` variable, and its ID is accessed via the attribute ``leaf.id``. The :math:`d_{i,j}` element of the distribution matrix contains the number of instances of the class *j* (:math:`C_j`) that finished in the leaf node with the ID *i* after the DT traversal. After all the instances from the training set traverse the DT, this matrix contains the distribution of classes among the leaf nodes.

The second ``for`` loop of the ``accuracy_calc()`` function finds the dominant class for each leaf node. The dominant class for a leaf node is the class having the largest percentage of instances, among the ones that finished the traversal in that leaf node. Formally, the dominant class :math:`k_i` of the leaf node with the ID *i* is:

.. math:: k_i | (d_{(i,k_i)} = \max_{j}(d_{i,j}))
    :label: dominant_class

The structure of the distribution matrix is displayed in the :num:`Figure #fig-distribution-matrix`. Rows correspond to the leaves of the DT, and the columns correspond to the classes of the training set. From each row (*i*) of the distribution matrix, we obtain the dominant class :math:`k_i` and the number of instances of the dominant class :math:`d_{(i,k_i)}` that finished the traversal in the leaf with ID *i*.

If we were to do a classification run with the current DT individual of the training set, the maximum accuracy would be attained if all leaf nodes were assigned their corresponding dominant classes. Thus, each instance which finishes in a certain leaf node, that belongs to that node's dominant class, is added to the number of classification hits (the ``hits`` variable of the :num:`Algorithm #fig-accuracy-calc-pca`), otherwise it is qualified as a missclassification. Hence,

.. math:: \texttt{hits}=\sum_{i=1}^{N_l}{d_{(i,k_i)}}.
    :label: hits_sum

The accuracy of the DT is, hence, equal to the percentage of the instances whose classifications were declared as hits, as given in the pseudo-code: ``accuracy = hits/len(train_set)``.

.. _sec-oversize:

Oversize
;;;;;;;;

The DT oversize is calculated as the relative difference between the number of leaves in the DT and the total number of classes (|NC|) in the training set (obtained via the ``train_set.cls_cnt()`` function). In order to be able to classify correctly all training set instances, the DT needs to have at least one leaf for each class occurring in the training set. Therefore, without knowing anything else about the dataset, our best guess is that the minimal DT that could be consistent with the dataset has one leaf for each of the dataset classes. For that reason, the oversize measure given by the equation :eq:`eq-oversize`, was defined in such a way to have the DT start suffering penalties to the fitness when the number of its leaves exceeds the total number of classes in the training set, i.e. the oversize measure is zero when :math:`\Nl=\NC`:

.. math::
    :label: eq-oversize

    \begin{aligned}
    \texttt{oversize} &= \frac{\Nl - \NC}{\NC}, \\
    \texttt{fit} &= \texttt{accuracy}\cdot(1-K_o\cdot\texttt{oversize}^2)
    \end{aligned}

The DT oversize negatively influences the fitness, as it can be seen from the equation :eq:`eq-oversize`. The parameter |Ko| is used to control how much influence the DT oversize will have on the overall fitness. In other words, it determines the shape of the collection of Pareto frontiers for the DT individual. Each DT individual can be represented as a point in a 2-D space induced by the DT oversize and accuracy measures. In a Pareto set all elements have the same fitness value, even though they have different accuracy and oversize measures.

.. _fig-fit-overSize:
.. plot:: images/pareto.py
    :width: 70%

    The layout of Pareto frontiers for the accuracy value of 0.8, when |NC| equals 5, for |Ko| parameter values of: 0, 0.02 and 0.1.

The :num:`Figure #fig-fit-oversize` shows the layout of the Pareto frontier for an example of fitness value of 0.8 and few different values of the parameter |Ko|, with the value of 5 selected for the parameter |NC|. It can be seen that if |Ko| is chosen to be 0, the oversize does not influence the fitness, which is in turn always equal to the value of the accuracy. When :math:`K_o > 0`, the |algo| algorithm will be willing to trade accuracy for the DT size. As it can be seen from the figure, when the parameter |Ko| has a large value, for an example 0.1, the big DTs are highly discouraged in that an individual of size 5 with the accuracy of 0.8 is equally fit in the eyes of the algorithm as the larger one with more than 10% higher accuracy, but of size 10.

As shown in the :num:`Algorithm #fig-fitness-eval-pca`, the dependence of the fitness on the oversize measure is quadratic. This serves two purposes:

#. Since oversize turns negative when the DT size falls below |NC|, such undersized DTs would be getting a boost in fitness if it were not for the squaring. If all classes are to be represented in the DT, the number of leaves should at least match the number of classes, so that it would be at least possible, for each class to have a leaf. By squaring the oversize, the undersized DTs are discouraged in the same way the oversized are.

#. By using the quadratic dependence, the rate at which fitness decreases with the DT size is lower when the size is closer to the |NC|, and gets progressively higher as the size increases. This way, the DTs whose size is close to |NC| are penalized less then they would be if the dependence of the fitness on oversize were linear.

In order to measure the influence of the oversize on the induced DTs, an experiment has been conducted on all datasets from the :numref:`tbl-uci`. The DTs were induced for a number of values for the parameter |Ko|, namely :math:`K_o \in \{0, 0.001, 0.01, 0.02, 0.06, 0.1, 0.2\}`. The results are presented in the :num:`Table #tbl-oversize-size-comp`, :num:`Table #tbl-oversize-acc-comp`, :num:`Figure #fig-oversize-comp1` and :num:`Figure #fig-oversize-comp2`. The :num:`Table #tbl-oversize-size-comp` and the :num:`Table #tbl-oversize-acc-comp` list the induced DT sizes and accuracies respectively, for all datasets and all values of the oversized weight parameter |Ko| used in the experiment. In the figures, the plots are organized in pairs, where each pair consists of the accuracy and size plots for the same five algorithms displayed in juxtaposition. Please notice that the x-axis, corresponding to the value of the parameter |Ko|, is given in logarithmic scale, as well as the y-axis of the DT size plots. Please also notice that the ranges for the y-axis, be it for the accuracy or the size plots, vary from plot to plot and depend on the datasets used for the induction.

The values in the :num:`Table #tbl-oversize-size-comp` clearly indicate that the largest DTs are induced when the DT oversize is ignored during the induction, :math:`K_o=0`. From there, the induced DT sizes drop quickly when the value of |Ko| is increased, only to start saturating after certain |Ko| value, which is different for each dataset. This is usually the place where the |algo| algorithm needs to start inflicting serious damage to the DT accuracies, only to compress the DTs furher in size by small factors. This trend can be also observed with accuracies in the :num:`Table #tbl-oversize-acc-comp`. The accuracies are, naturaly, largest when there is no size limit imposed, i.e. :math:`K_o=0`. Then, as the value of |Ko| increases, the induced DTs of some of the datasets experience a significant drop in the accuracy, where this drop is of course traded-off against a significant drop in their sizes. These datasets, like ``bch``, ``cmc``, ``krkopt``, ``letter``, ``ttt``, ``wfr``, ``wine``, etc., are the ones whose internal complexity really demands for bigger DTs in order to describe them more precisely. On the other hand, the induced DTs of some of the datasets, experience little or no change in the accuracy when the |Ko| value increases up to a certain point. For these datasets, like ``ausc``, ``bank``, ``bcw``, ``irs``, ``psd``, ``shuttle``, ``sick``, ``zoo``, etc., initial large DTs are indeed excessive in size and the more succinct DT representation was successfully found by the |algo| aglorithm. When the |algo| algorithm is used in practice, it is a design choice whether the most accurate DTs are needed no matter their size, or we are interested in the smallest DTs at the cost of their accuracy, or we are willing to accept certain trade-off between the DT size and its accuracy. It is obvious from these results that there is a different behavior of the inferred DTs from different datasets, in terms of DT accuracies and sizes, when the oversize fitness weight |Ko| is varied. Hence, the actual value of the |Ko| parameter will depend on the domain of the problem being solved.

.. raw:: latex

   \begingroup
   \small
   \renewcommand{\arraystretch}{0.8}

.. tabularcolumns:: L{0.15\linewidth} | R{0.08\linewidth} R{0.08\linewidth} R{0.08\linewidth} R{0.08\linewidth} R{0.08\linewidth} R{0.08\linewidth} R{0.08\linewidth}

.. _tbl-oversize-size-comp:
.. csv-table:: The average sizes of the DTs induced for various values of the parameter |Ko|
    :header-rows: 1
    :file: scripts/oversize-comp-size.csv

.. tabularcolumns:: L{0.15\linewidth} | R{0.08\linewidth} R{0.08\linewidth} R{0.08\linewidth} R{0.08\linewidth} R{0.08\linewidth} R{0.08\linewidth} R{0.08\linewidth}

.. _tbl-oversize-acc-comp:
.. csv-table:: The average accuracies of the DTs induced for various values of the parameter |Ko|
    :header-rows: 1
    :file: scripts/oversize-comp-acc.csv

.. raw:: latex

    \endgroup

.. subfigstart::

.. _fig-oversize-comp-size0:

.. figure:: images/oversize-comp/size0.pdf
    :align: center

    DT size: ger, sick, ca, vote, wilt

.. _fig-oversize-comp-acc0:

.. figure:: images/oversize-comp/acc0.pdf
    :align: center

    DT accuracy: ger, sick, ca, vote, wilt

.. _fig-oversize-comp-size1:

.. figure:: images/oversize-comp/size1.pdf
    :align: center

    DT size: bcw, irs, msh, psd, thy

.. _fig-oversize-comp-acc1:

.. figure:: images/oversize-comp/acc1.pdf
    :align: center

    DT accuracy: bcw, irs, msh, psd, thy

.. _fig-oversize-comp-size2:

.. figure:: images/oversize-comp/size2.pdf
    :align: center

    DT size: ausc, bank, ca, hep, hrts

.. _fig-oversize-comp-acc2:

.. figure:: images/oversize-comp/acc2.pdf
    :align: center

    DT accuracy: ausc, bank, ca, hep, hrts

.. _fig-oversize-comp-size3:

.. figure:: images/oversize-comp/size3.pdf
    :align: center

    DT size: ion, sb, spect, thy, bc

.. _fig-oversize-comp-acc3:

.. figure:: images/oversize-comp/acc3.pdf
    :align: center

    DT accuracy: ion, sb, spect, thy, bc

.. _fig-oversize-comp-size4:

.. figure:: images/oversize-comp/size4.pdf
    :align: center

    DT size: son, w21, adult, car, magic

.. _fig-oversize-comp-acc4:

.. figure:: images/oversize-comp/acc4.pdf
    :align: center

    DT accuracy: son, w21, adult, car, magic

.. subfigend::
    :width: 0.49
    :label: fig-oversize-comp1

    Dependencies of the induced DT sizes and accuracies on the oversize weight (|Ko|) parameter values. Datasets 1-25.

.. subfigstart::

.. _fig-oversize-comp-size5:

.. figure:: images/oversize-comp/size5.pdf
    :align: center

    DT size: zoo, shuttle, seg, page, gls

.. _fig-oversize-comp-acc5:

.. figure:: images/oversize-comp/acc5.pdf
    :align: center

    DT accuracy: zoo, shuttle, seg, page, gls

.. _fig-oversize-comp-size6:

.. figure:: images/oversize-comp/size6.pdf
    :align: center

    DT size: nurse, pen, pid, w40, ctg

.. _fig-oversize-comp-acc6:

.. figure:: images/oversize-comp/acc6.pdf
    :align: center

    DT accuracy: nurse, pen, pid, w40, ctg

.. _fig-oversize-comp-size7:

.. figure:: images/oversize-comp/size7.pdf
    :align: center

    DT size: cvf, hrtc, jvow, liv, ttt

.. _fig-oversize-comp-acc7:

.. figure:: images/oversize-comp/acc7.pdf
    :align: center

    DT accuracy: cvf, hrtc, jvow, liv, ttt

.. _fig-oversize-comp-size8:

.. figure:: images/oversize-comp/size8.pdf
    :align: center

    DT size: spf, veh, vow, cmc, wine

.. _fig-oversize-comp-acc8:

.. figure:: images/oversize-comp/acc8.pdf
    :align: center

    DT accuracy: spf, veh, vow, cmc, wine

.. _fig-oversize-comp-size9:

.. figure:: images/oversize-comp/size9.pdf
    :align: center

    DT size: eb, eye, krkopt, letter, bch

.. _fig-oversize-comp-acc9:

.. figure:: images/oversize-comp/acc9.pdf
    :align: center

    DT accuracy: eb, eye, krkopt, letter, bch

.. subfigend::
    :width: 0.49
    :label: fig-oversize-comp2

    Dependencies of the induced DT sizes and accuracies on the oversize weight (|Ko|) parameter values. Datasets 25-50.

Selection
.........

The selection task is responsible for deciding, in each iteration, which DT will be taken for the candidate solution for the next iteration: either the current candidate solution, i.e. the parent (in the evolutionary sense), or the mutated individual. The selection procedure implemented by the :num:`Algorithm #fig-selection-vanilla-pca` is the most basic one, where whenever the mutated individual outperforms its parent in fitness, it is always taken as the new candidate solution, and is discarded otherwise. Hence, it can be called greedy. An improvement to this basic version of the selection procedure will be discussed in the :num:`Section #sec-search-probability`, in which a less fit individual is sometimes given a chance to be selected.

.. _fig-selection-vanilla-pca:
.. literalinclude:: code/selection-vanilla.py
    :caption: The pseudo-code of the :literal:`select()` function of the |algo| algorithm, that implements the basic individual selection procedure

.. _sec-algo-improvements:

Improvements to the basic |algo| algorithm
------------------------------------------

In this section several additional features that can improve either the execution time or the quality of solutions produced by the |algo| algorithm are discussed:

- :num:`Section #sec-perc-missing-classes` - Make fitness dependent on the number of training set classes that are not represented in the DT individual, i.e not assigned to any leaf.
- :num:`Section #sec-search-probability` - Introduce the search probability, i.e. the probability with which a less fit individual can be selected for the candidate solution.
- :num:`Section #sec-partial-reclass` - Improve the induction times by keeping track of the classification traversal paths, and trying to reuse them between iterations.

.. _sec-perc-missing-classes:

Unrepresented classes
.....................

When working with highly imbalanced datasets, the induced DT can happen to contain no leaves to which an under-represented class has been assigned. In these cases it might be useful to encourage the |algo| algorithm to represent all classes from the dataset within the DT. Here, an extension to the fitness formula is given that aims at discouraging the DTs in which some classes are not represented. The percentage of missing classes is calculated as the percentage of the classes for which the DT does not have a leaf, to the total number of classes in the training set (|NC|):

.. math:: missing = \frac{\NC - N_{DTc}}{\NC}
    :label: eq-missing

where |NDTc| is the number of classes represented in the DT leaves. The fitness calculation is then updated so that the penalties are taken for the missing classes in the DT individual: ``dt.fit = accuracy*(1 - Ko*oversize*oversize)*(1 - Km*missing)``, where the parameter |Km| is used to control how much influence the number of missing classes will have on overall fitness.

.. _sec-search-probability:

Search probability
..................

Evolution is inherently an unpredictable process. It is akin to searching for the highest peak in the mountain range but only being able to see one's immediate vicinity, i.e. not being able to peek at distant mountain tops that could guide one's exploration (see :num:`Figure #fig-escape-local-optimum`). Simplest strategy for conquering the peak closest to one's current location is to always choose the path that leads upwards. This strategy is thus called the greedy hill-climbing strategy. However, there is no guarantee that the closest peak is in the same time the highest in the mountain range and it often is not. One example of such a peak is the peak marked by the letter A in the :num:`Figure #fig-escape-local-optimum`, which is called the local maximum. It is a maximum, since all points in its neighborhood have lower elevation, but it is only local since there is a higher peak in this search space, namely B from the :num:`Figure #fig-escape-local-optimum`. The greedy approach described above fails in finding a path from point A to point B, since there exist no monotonically uphill path connecting A to B. In order to get to point B the exploration has to first traverse through the regions with lower elevation, shown by an arrow in the :num:`Figure #fig-escape-local-optimum`, in order to get to the base of the hill with the summit at the point B, from which it can start moving up again. However, it is not clear in which direction from the point A the movement should proceed. Nothing is gained if the movement continues towards the point C, since the predominant uphill movement will eventually bring the exploration back to the point A, only wasting the computational time. Even worse, if the exploration step size is large, the position might be moved to the point D, from where it could wander off in the opposite direction from the global maximum B.

.. _fig-escape-local-optimum:
.. plot:: images/escape_local.py
    :bbox: tight
    :pad: -1.0
    :width: 80%

    An example of the hill climbing problem and the issue of escaping the local optimum A by a greedy strategy in order to reach point B.

In terms of the evolutional DT induction, instead of striving for higher elevation, the algorithm is striving for a DT individual with higher fitness, and instead of walking in the mountains, the DT individual is being mutated to move around in the search space. For practical problems, the search spaces for the DT individuals have much higher dimensionality and are thus much more complicated than the hill-climbing problem described above. However, the main idea is the same, in order to visit and discover as many fitness peaks as possible (in order to find the highest one), the algorithm sometimes needs to pursue a less fit individual. Since it is impossible to tell which poorer performing solution will eventually lead to an improved one, the decision of going after a poorer solution is made at random with some probability. Here, this probability will be called the search probability, since it allows for the evolutionary process to search the wider neighborhood of the current solution. Without this search, the systems tend to get stuck at local maximas.

Several approaches to providing the values for the search probability that were tried with the |algo| algorithm in an effort to increase its performance, will now be discussed. The results of the experiments used to infer which of the approaches offers statistically significant improvement to the quality of solutions induced by |algo|, are discussed in the :num:`Section #sec-searchprob-exp`.

HereBoy
;;;;;;;

One approach for selecting the search probability is implemented by the HereBoy algorithm :cite:`levi2000hereboy`, and is based on the concept used in the Simulated Annealing. The probability is given high value in the beginning and is reduced over time, which is referred as the cooling schedule in the Simulated Annealing literature. The idea behind the cooling schedule is to allow the system a lot of freedom to explore the search space at the beginning when the system is in a high state of disorder, i.e. when only poor solutions are available. Then, slowly, as the desired structures emerge, i.e. better solutions are being found, the freedom to search is restricted so that these structures are not destroyed. The following equation shows how HereBoy calculates the search probability, but in terms of the DT fitness as used by the |algo| algorithm, where the constant 1 in the equation corresponds to the maximal possible fitness:

.. math:: \rho = \rho_0(1 - \texttt{fit})
    :label: eq-hereboy-searchprob

There are several potential issues with using the HereBoy approach to search probability. The :num:`Figure #fig-searchprob-fitpath-hereboy` shows two examples of how the fitness changes during the DT induction when the HereBoy approach is used and when no search probability is used. Several potential issues are pointed out on the plots, by marking the relevant moments in the DT induction when the effects of these issues make an influence on the evolution of the DT fitness.

.. subfigstart::

.. _fig-veh-searchprob-fitpath-hereboy:
.. plot:: images/veh_searchprob_fitpath_hereboy.py
    :bbox: tight
    :width: 100%

    Induction from ``veh`` dataset.

.. _fig-ion-searchprob-fitpath-hereboy:
.. plot:: images/ion_searchprob_fitpath_hereboy.py
    :bbox: tight
    :width: 100%

    Induction from ``ion`` dataset.

.. subfigend::
    :width: 0.49
    :label: fig-searchprob-fitpath-hereboy

    Plots of the fitness evolutions during first 15k iterations of the DT induction from ``veh`` and ``ion`` datasets when the HereBoy search probability strategy is used (green) and when no search probability is used (blue). Several potential issues with the HereBoy search probability approach are pointed out: 1 - Poorer solution accepted and interrupted a series of fitness advancements, 2 - No new solutions accepted for a long time, wasting execution time, 3 - Solution with significantly less fitness accepted.

First, the maximum possible fitness that the DT can attain, which influences the search probability via equation :eq:`eq-hereboy-searchprob`, is different for different datasets, and is not known in advance. Second, sometimes during the DT evolution, there are intervals when better solutions are found often, which is akin to standing at the slope of a hill in the hill climbing problem (for an example at the point C in the :num:`Figure #fig-escape-local-optimum`). It might be worthwhile to let evolution reach a plateau before trying to search the less fit neighborhood. With the HereBoy approach there is no such mechanism, and it is possible to interrupt the hill climbing any time, which manifests itself in the drops in fitness in the middle of rapid climbing, marked with #1 in the :num:`Figure #fig-searchprob-fitpath-hereboy`. On the other hand, by not changing the candidate solution for a large number of iterations, the execution time is wasted by not exploring as large portion of the search space as it was possible. With the HereBoy approach, the search probability remains fixed when there is no change in fitness, making possible for a large iteration intervals when no solutions are accepted, especially if the search probability is low (for an example the current fitness is close to the maximum value of 1). These intervals are marked with #2 in the :num:`Figure #fig-searchprob-fitpath-hereboy`. Finally, the search probability is equal for all mutated individuals, no matter their fitness. Sometimes, even small changes to the node test coefficients can produce significant shifts in the way the DT classifies the training set, especially if the DT is large and the mutated node is near the root. Hence, there is a substantial chance of accepting a significantly less fit individual with this approach, which is akin to jumping to the point D in the search space, as shown in the :num:`Figure #fig-escape-local-optimum`. These large jumps can be seen in the :num:`Figure #fig-searchprob-fitpath-hereboy` marked with #3.

Metropolis
;;;;;;;;;;

The Metropolis approach to the search probability calculation was devised for the |algo| algorithm based on the idea of the similar method used in the Simulated Annealing called the Metropolis criterion (or Metropolis-Hastings criterion) :cite:`metropolis1953equation`. The adoption of Metropolis criterion is an attempt to remedy the issue where all less fit mutated individuals have the same probability of being accepted, no matter their fitness. Hence in the Metropolis approach, the fitness of the mutated individual (``dt_mut.fit``), more precisely the relative difference between the candidate solution fitness (``dt.fit``) and the mutated individual fitness, will have its influence through the following factor:

.. math::
   :label: eq-metropolis-criterion

   \begin{aligned}
      \rho &\sim e^{-\frac{\Delta_F}{S_T}}, \\
      \Delta &= \frac{\texttt{dt.fit} - \texttt{dt\_mut.fit}}{\texttt{dt.fit}},
    \end{aligned}

where :math:`S_T` is the search temperature, which dictates how much less fit an individual can be, and still have a chance to be accepted. This is user supplied parameter, and it is kept constant throughout the induction. Furthermore, for at the same time to allow the algorithm to climb the current hill uninterrupted, and to discourage long iteration intervals where no solution is selected, a concept of stagnation duration :math:`D_{s}` is introduced, which is defined as the number of iterations where no improvement to fitness has been made. The search probability is then made proportional to the :math:`D_{s}` to finally obtain its final form within the Metropolis approach:

.. math:: \rho(D_s, \Delta_F) = \rho_0 D_s e^{-\frac{\Delta_F}{S_T}}
    :label: eq-metropolis-searchprob

Basically, the search probability restarts to 0 after each advancement in the fitness happens, and increases linearly with each iteration in which no such advancement is made. Since the main idea is not to select a less fit individual either too early or too late after the advancement in the fitness, we are basically interested in determining how high is the probability :math:`p_s`, of accepting an individual of certain fitness in an iteration interval after the advancement in fitness, as a function of :math:`D_s`:

.. math::
    :label: eq-cumul-searchprob

    \begin{aligned}
    p_s(D_s) &= \sum_{i=1}^{D_s} \rho_i \prod_{j=1}^{i-1}(1 - \rho_j) \\
             &= \sum_{i=1}^{D_s} \rho_0 i e^{-\frac{\Delta_{Fi}}{S_T}}\prod_{j=1}^{i-1}(1 - \rho_0 j e^{-\frac{\Delta_{Fj}}{S_T}})
    \end{aligned}

It is obvious from the equation :eq:`eq-cumul-searchprob`, that :math:`p_s` depends on the fitnesses of all proposed mutated individuals in previous :math:`D_s` iterations, which are in turn some random variables. Hence to avoid elaborate mathematical procedure of obtaining the distribution for the :math:`p_s` in general case, a simplified case is considered. The plots in the :num:`Figure #fig-searchprob-func` represent :math:`p_s(D_s)` functions for various values of :math:`\Delta_F`, :math:`\rho_0` and :math:`S_T`, with the simplification that all :math:`\Delta_Fi` values from the :eq:`eq-cumul-searchprob`, are equal to :math:`\Delta_F`. In other words, a case is considered where in all past :math:`D_s` iterations, all proposed mutated individuals had an equal fitness. This simplified version of :math:`p_s(D_s)` is called :math:`p'_s(D_s)`.

.. subfigstart::

.. _fig-searchprob-func1:
.. plot:: images/searchprob_plot_1.py
    :bbox: tight
    :width: 100%

    :math:`S_T=0.05`, :math:`\rho_0=\num{5e-5}`

.. _fig-searchprob-func2:
.. plot:: images/searchprob_plot_2.py
    :bbox: tight
    :width: 100%

    :math:`S_T=0.05`, :math:`\rho_0=\num{5e-4}`

.. _fig-searchprob-func3:
.. plot:: images/searchprob_plot_3.py
    :bbox: tight
    :width: 100%

    :math:`S_T=0.2`, :math:`\rho_0=\num{5e-5}`

.. _fig-searchprob-func4:
.. plot:: images/searchprob_plot_4.py
    :bbox: tight
    :width: 100%

    :math:`S_T=0.2`, :math:`\rho_0=\num{5e-4}`

.. subfigend::
    :width: 0.49
    :label: fig-searchprob-func

    The simplified version of the probability of accepting a less fit individual of certain fitness in :math:`D_s` iterations after the advancement in fitness. In each plot, for different values of :math:`S_T` and :math:`\rho_0`, the :math:`p'_s(D_s)` function is plotted for an individuals whose fitness is smaller than that of the current candidate solution by: 1%, 5%, 10%, 20% and 40%.

It can be seen from the plots in the :num:`Figure #fig-searchprob-func`, that all the functions have a sigmoid shape, which is in fact what was intended. The probability of accepting the less fit solution is low in the interval where the stagnation duration is small, then increases at certain pace (depending on the parameters selected) as the iterations pass, until it approaches a 100% chance of being selected. The plots show that the parameter :math:`S_T` influences how differently will the individuals with different fitnesses be treated. When :math:`S_T=0.05` (:num:`Figure #fig-searchprob-func1` and :num:`Figure #fig-searchprob-func2`), the curves are far apart, hence it will be much harder for the individuals with lower fitnesses to get selected, and the algorithm will only explore individuals with fitnesses closer to the fitness of the candidate solution. On the other hand, for higher values of the parameter :math:`S_T` (:num:`Figure #fig-searchprob-func3` and :num:`Figure #fig-searchprob-func4`), the :math:`p_s` curves are tighter together and the differences between individuals of different fitnesses are blurred. In this case, the algorithm will explore individuals from wide fitness range. As for the parameter :math:`\rho_0`, the higher its value is, the sooner another less fit individual will get selected.

.. subfigstart::

.. _fig-veh-searchprob-fitpath-metropolis:
.. plot:: images/veh_searchprob_fitpath_metropolis.py
    :bbox: tight
    :width: 100%

    Induction from ``veh`` dataset.

.. _fig-ion-searchprob-fitpath-metropolis:
.. plot:: images/ion_searchprob_fitpath_metropolis.py
    :bbox: tight
    :width: 100%

    Induction from ``ion`` dataset.

.. subfigend::
    :width: 0.49
    :label: fig-searchprob-fitpath-metropolis

    Plots of the fitness evolutions during first 15k iterations of the DT induction from ``veh`` and ``ion`` datasets, when the Metropolis search probability strategy is used (green) and when no search probability is used (blue).

The :num:`Figure #fig-searchprob-fitpath-metropolis` shows the way the fitness of the induced DT individual evolved when Metropolis approach was used. It can be seen that there are significantly less big fitness drops and that the plateaus are shorter. And indeed, this approach succeeded in helping find better solutions in the first 15k iterations than the HereBoy approach did (:num:`Figure #fig-veh-searchprob-fitpath-hereboy` and :num:`Figure #fig-ion-searchprob-fitpath-hereboy`).

Multiple restarts
;;;;;;;;;;;;;;;;;

It was observed that sometimes, for some datasets, after the poorer solution has been selected, the evolutionary process never succeeds in bringing the fitness back to the levels where it was before. Hence an addition to the search method has been proposed that would prevent the evolutionary process to explore for too long with individuals with the fitness less then the current known best fit individual. A parameter called return probability :math:`p_R` was introduced that determines the probability the evolutionary process has each iteration of returning to the best known candidate solution.

.. _sec-searchprob-exp:

Experiments
;;;;;;;;;;;

The experimental procedure explained in the :num:`Section #sec-exp-struct` was used to discover whether any of the proposed approaches statistically influences the induced DTs' fitnesses for the better. The values of the parameters relevant to the search probability that were used in the experiments are given in the :num:`Table #tbl-searchprob-exp-params` for all tested approaches.

.. tabularcolumns:: L{0.47\linewidth} R{0.15\linewidth} R{0.15\linewidth} R{0.15\linewidth}

.. _tbl-searchprob-exp-params:

.. list-table:: The values of the parameters relevant to the search probability set to the |algo| algorithm while running the experiments for comparing different search probability approaches
    :header-rows: 1

    * - Approach
      - :math:`\rho_0`
      - :math:`S_T`
      - :math:`p_R`
    * - Greedy
      - 0
      - --
      - --
    * - HereBoy
      - :math:`\num{1e-3}`
      - --
      - 0
    * - Metropolis
      - :math:`\num{5e-5}`
      - 0.05
      - 0
    * - Metropolis with restarts
      - :math:`\num{5e-5}`
      - 0.05
      - :math:`\num{1e-4}`

The results are given in the :num:`Table #tbl-searchprob-comp`, where for each of the discussed approaches, the mean value of the induced DTs fitness is given together with the 95% confidence intervals, and its ranking based on the Tukey HSD. The fitness values shown in the results table are not the ones used during the induction, but are calculated based on the accuracy of the induced DT on the test set. The results in the first table column, titled Greedy, were obtained without using any search strategy, i.e. by only ever accepting the solution with higher fitness.

.. raw:: latex

   \begingroup
   \small
   \renewcommand{\arraystretch}{1}

.. tabularcolumns:: L{0.085\linewidth} | R{0.135\linewidth} R{0.04\linewidth} | R{0.135\linewidth} R{0.04\linewidth} | R{0.135\linewidth} R{0.04\linewidth} | R{0.135\linewidth} R{0.04\linewidth}

.. _tbl-searchprob-comp:
.. csv-table:: Average fitness values of the induced DTs using four selection strategies, together with their 95% confidence intervals and Tukey HSD based rankings
    :header-rows: 2
    :file: scripts/searchprob-comp-fit.csv

.. raw:: latex

    \endgroup

The results shown in the :num:`Table #tbl-searchprob-comp` clearly indicate that any approach that allows for exploring the search space via less fit individuals, i.e. any approach that uses some kind of search probability is superior than the greedy hill-climbing, which was ranked lowest with average ranking of 2.33. As for the Hereboy and Metropolis approaches, for some datasets one generated better results and for the others the other one did. However, for vast majority of the datasets used, the best results were obtained by using the Metropolis with multiple restarts that yielded average ranking of 1.08, hence this technique was finally implemented into the |algo| algorithm.

Search probability implementation in |algo|
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

Metropolis with multiple restarts approach was implemented for the selection procedure, since it was shown in :num:`Section #sec-searchprob-exp` to yield the best results among proposed solutions. A new variable ``dt_best`` needed to be included into the ``efti()`` function to store the best solution found so far, because when selecting less fit individuals is allowed, the current solution candidate ``dt`` might not be in the same time the best solution overall. The new pseudo-code for the ``efti()`` function is given in the :num:`Algorithm #fig-efti-metropolis-rp-pca`.

.. _fig-efti-metropolis-rp-pca:
.. literalinclude:: code/algorithm-metropolis-rp.py
    :caption: The pseudo-code of the :literal:`efti()` function of the |algo| algorithm when using Metropolis with multiple restarts

Within the ``select()`` function, the logic for selecting the less fit individual and returning to the best solution need to be implemented, as shown in the :num:`Figure #fig-selection-metropolis-rp-pca`. When the evolution finds a solution better then the current candidate, the selection procedure will also check if it is the overall best, and if so, store it inside ``dt_best`` variable. On the other hand, if mutation did not advance the fitness, the stagnation duration will be increased and the search probability will be calculated based on it using the Metropolis criterion. A chance will be than given to the selection procedure to terminate the search and return to the best solution overall. Otherwise, the less fit ``dt_mut`` individual might get selected at random with the current value of search probability.

.. _fig-selection-metropolis-rp-pca:
.. literalinclude:: code/selection-metropolis-rp.py
    :caption: The pseudo-code of the :literal:`select()` function of the |algo| algorithm  when using Metropolis with multiple restarts

.. _sec-partial-reclass:

Partial reclassification
........................

As it was already discussed in the :num:`Section #sec-mutation`, the DT mutations alter only a small portion of the DT individual in each iteration, hence only the classification of the instances on whose traversal paths the mutated nodes happen to reside, will be affected by the mutation. Therefore the majority of instances will travel along identical paths from iteration to iteration, meaning that all related computations will remain the same. Recomputation is thus only necessary for the instances whose paths contain a mutated node. Please also notice that even when the mutated node test coefficients change, only the elements of the vector scalar product sum (given in the equation :eq:`oblique-test`) that correspond to the mutated coefficients must be recomputed, while the computation of all other elements can be skipped.

Therefore, the traversal paths could be memorized for the candidate DT individual in order to avoid unnecessary recalculations of the node tests during the classification of the mutated DT individual, for the instances whose paths do not cross the mutated nodes. Each instance could start the DT traversal by following its memorized path from the candidate DT individual classification, and checking whether it will encounter any of the mutated nodes while traversing the DT. While no mutated nodes are encountered, no test recalculations need to be executed and the instance moves through the DT as dictated by the path stored in the memory. When the instance encounters a mutated node, its path in the mutated DT might diverge from its memorized path. If the topological mutation produced the changes in the encountered node, where either a new node was added in the place of a leaf (see :num:`Figure #fig-node-addition` for an example) or the node was removed and a different one took its place (see :num:`Figure #fig-node-removal` for an example), the sub-tree which the instance has reached has changed, and the rest of the traversal path needs to recomputed. If the instance encounters a node with only some of its coefficients |w| mutated, the dot product of the mutated node test (:math:`\mathbf{w^{mut}}\cdot \mathbf{x}`), can be calculated based on the dot product of the original node test (:math:`\mathbf{w}\cdot \mathbf{x}`) in the following way:

.. math:: \mathbf{w^{mut}}\cdot \mathbf{x} = \mathbf{w}\cdot \mathbf{x} + \sum_{i \in M}(w^{mut}_{i} - w_{i}) x_{i},
    :label: dot-product-recalc

where *M* is the set of indices of all the mutated coefficients in that node. Furthermore, the mutation on the encountered node may not be strong enough to deflect the instance from its previous path. Hence, the outcome of the mutated node test is monitored whether it will align with the stored path, in which case the instance has not diverged and the instance can continue following the memorized path. Otherwise, the instance entered a new DT sub-tree and all subsequent node tests need to be recalculated.

In the case the mutated individual is selected for the new candidate solution, the paths which have diverged in the classification run need to be updated to the memory. One possible way to implement this is to keep track of each deviation from the memorized paths during the classification run for the mutated DT individual, and apply all these changes to the stored traversal paths if the individual is selected for the new candidate solution. However, a different method that takes advantage of the fact that usually less than 1% of the mutated individuals get selected, proved to be more efficient with respect to both execution time and the memory resource consumption. In this approach, the |algo| algorithm does not keep track of the deviations from the memorized paths in each classification run of a mutated DT, which in turn saves on memory access time and on the memory space for tracking the changes. Only once a mutated DT has been selected for the new candidate solution, is the classification rerun with the instructions to change the stored traversal paths in the memory where needed.

The proposed partial reclassification algorithm has an additional performance issue with the small DT individuals. If the DT individual is only one or two levels deep, there is very large probability that many of the instance paths will be affected by the mutation, and the time consumption overhead of the partial reclassification exceeds its benefits. The |algo| algorithm implements a strategy to turn the partial reclassification off when it operates with small individuals.

.. _fig-partial-find-dt-leaf-for-inst:

.. literalinclude:: code/find_dt_leaf_for_inst_delta.py
    :caption: The modified :samp:`find_dt_leaf_for_inst()` function that implements the partial reclassification method

The pseudo-code in the :num:`Algorithm #fig-partial-find-dt-leaf-for-inst` describes the implementation of the partial reclassification method within ``find_dt_leaf_for_inst()`` function (the original implementation is given by the :num:`Algorithm #fig-find-dt-leaf-for-inst-pca`). If the partial reclassification is turned off by |algo| algorithm (by passing the value ``True`` for the argument ``recalc_all``), the paths of all the training set instances will be immediately considered to have diverged from the stored paths, and the partial classification algorithm will not be used, making the classification procedure effectively same as the original one. Otherwise, the classification for an instance (variable ``instance``) starts by following the stored path (``path_diverged = recalc_all = False``) from the root node (``cur_node = dt.root``). The path is followed one node at a time (``cur_node = get_stored_next_node(instance, cur_node)``), in order to look out for mutated nodes along its length, by using the functions ``dt.is_topo_mutated(cur_node)`` and ``dt.is_coeff_mutated(cur_node)``, which signal, respectively, if the current node was mutated via topological mutation or only its test coefficients were mutated. If it was changed by a topological mutation, the instance is facing completely different node, hence the dot product is calculated a new. On the other hand if the current node's test coefficients were mutated, the dot product is reconstructed from the stored value (retrieved via ``get_stored_psum(instance, cur_node)``), using the equation :eq:`dot-product-recalc`. In both cases, it is considered that the instance has diverged from the memorized path: ``path_diverged = True``. The rest of the node test is carried out by comparing the dot product with the threshold to obtain the next node in the path, and if that node corresponds to the next node in the stored path, instance can safely go back to following it (once again ``path_diverged = False``). Finally, in order not to update the memorized paths in each classification run, the argument ``store_paths`` is used to signal to ``find_dt_leaf_for_inst()`` function whether the mutated DT individual has become the new candidate solution and the updates to the memory should take place.

In the :num:`Table #tbl-delta-time-comp` the results of an experiment are shown that tests the performance benefits of utilizing the partial reclassification procedure, obtained by the cross-validation procedure explained in the :num:`Section #sec-exp-struct` and the set of parameters listed in the :num:`Table #tbl-partial-comp-exp-params`. The results show that the partial reclassification really shortens the execution time, but that the induction speedups differ between the datasets, and depend on the size of the induced DTs, as was expected and already discussed in this section.

.. tabularcolumns:: R{0.2\linewidth} R{0.1\linewidth} R{0.08\linewidth} R{0.1\linewidth} R{0.14\linewidth} R{0.1\linewidth} R{0.14\linewidth}

.. _tbl-partial-comp-exp-params:

.. list-table:: The parameter set used for the |algo| algorithm in the partial reclassification comparison experiments
    :header-rows: 1

    * - ``max_iter``
      - :math:`K_o`
      - :math:`\alpha`
      - :math:`\beta`
      - :math:`\rho_0`
      - :math:`S_T`
      - :math:`p_R`
    * - 500k
      - 0.01
      - 1
      - 0.6
      - :math:`\num{5e-5}`
      - 0.05
      - :math:`\num{1e-4}`

.. raw:: latex

   \begingroup
   \small
   \renewcommand{\arraystretch}{1}

.. tabularcolumns:: L{0.09\linewidth} | R{0.18\linewidth} R{0.175\linewidth} | L{0.09\linewidth} | R{0.18\linewidth} R{0.175\linewidth}

.. _tbl-delta-time-comp:
.. csv-table:: The results of the experiments testing the benefits on the |algo| algorithm induction times of using the partial reclassification procedure
    :header-rows: 1
    :file: scripts/delta-comp-time.csv

.. raw:: latex

    \endgroup

.. _sec-complexity:

Complexity of the |algo| algorithm
----------------------------------

The computational complexity of the |algo| algorithm can be calculated by following its pseudo-code. The computational complexity is given here in the big O notation, i.e. the worst-case complexity will be calculated. Since the individual selection is performed in constant time it can be omitted, and the total complexity can be computed as:

.. math:: T(EFTI) = \texttt{max\_iter}\cdot(O(\texttt{mutate}) + O(\texttt{fitness\_eval}))
    :label: cplx_algo_tot_components

The number of leaves, |Nl|, in binary DT is always by 1 larger then the number of non-leaf nodes. If *n* represents the number of non-leaf nodes in the DT, then:

.. math:: N_l = n + 1
    :label: leaves_cnt

In the worst case, the depth of the DT equals the number of non-leaf nodes, hence:

.. math:: D = N_l - 1
	:label: depth

Each iteration |alpha| coefficients are mutated, so the complexity of mutating coefficients is constant:

.. math:: T(\texttt{coefficient\ mutation}) = O(1)
  :label: cplx_mut_coef

The topology can be mutated by either adding or removing the node from the DT. When the node is removed, only a pointer to the removed child is altered so the complexity is:

.. math:: T(\texttt{node\ removal}) = O(1)
	:label: cplx_rem_node

When the node is added, the new set of node test coefficients needs to be calculated. hence the complexity is:

.. math:: T(\texttt{node\ addition}) = O(\NA)
	:label: cplx_add_node

Hence, the complexity of the whole DT Mutation task sums to:

.. math:: T(\texttt{mutation}) = O(\NA)
    :label: cplx_mutation

Once the number of hits is determined, the fitness can be calculated in constant time :math:`O(1)`, hence the complexity of the whole ``fitness_eval()`` function is:

.. math:: T(\texttt{fitness\_eval}) = N_I\cdot O(\texttt{find\_dt\_leaf\_for\_inst}) + O(N_l\cdot \NC) + O(1)
    :label: fitness_eval

where |NI| is the number of instances in the training set and |NC| is the total number of classes in the classification problem, and :math:`O(N_l\cdot \NC)` is for the dominant class calculation for each leaf. As for the ``find_dt_leaf_for_inst()`` function, the complexity can be calculated as:

.. math:: T(\texttt{find\_dt\_leaf\_for\_inst}) = D\cdot O(\texttt{dot\_product}),
    :label: find_dt_leaf

and the complexity of the node test evaluation is:

.. math:: T(\texttt{dot\_product}) = O(\NA)
    :label: node_test_eval

By inserting the equation :eq:`node_test_eval` into the equation :eq:`find_dt_leaf`, and then both of them into the equation :eq:`fitness_eval`, we obtain the complexity for the ``fitness_eval()`` function:

.. math:: T(\texttt{fitness\_eval}) = O(N_{I}\cdot D\cdot\NA + \Nl\cdot \NC)
    :label: fitness_eval_tot

By inserting the equations :eq:`fitness_eval_tot`, :eq:`cplx_mutation`, :eq:`leaves_cnt` and :eq:`depth` into the equation :eq:`cplx_algo_tot_components`, we obtain the total complexity of the |algo| algorithm:

.. math:: T(EFTI) = \texttt{max\_iter}\cdot(N_I\cdot N_l \cdot\NA + N_l\cdot \NC + \NA)
    :label: cplx_all_together

Since :math:`N_A \ll N_I\cdot N_l\cdot N_A` the mutation insignificantly influences the complexity and can be disregarded. We finally obtain that the complexity of the |algo| algorithm is dominated by the fitness evaluation task complexity, and sums up to:

.. math:: T(EFTI) = O(\texttt{max\_iter}\cdot(N_I\cdot N_l\cdot\NA + N_l\cdot \NC))
    :label: cplx_final

.. _sec-efti-experiments:

Experiments
-----------

In this section, the results of the experiments are presented, that were conducted in order to compare the |algo| algorithm to the existing solutions. The algorithms listed in the :num:`Table #tbl-existing-algo`, available in open literature, were used for the comparison. The experimental procedure explained in the :num:`Section #sec-exp-struct` was used to compare the quality of the induced DTs, in terms of their sizes and accuracies. For the incremental DT inference algorithms, a pruning set was created and the induced DTs were pruned after the induction. For the algorithms: CART-LC, OC1, OC1-AP, OC1-ES and OC1-SA, the default value of 10% randomly selected training set  instances were used to form a pruning set, and the Error-Complexity pruning algorithm was used. For the NODT algorithm, the pruning was performed in the manner described in the original publication :cite:`struharik2014inducing`, where a specific pruning algorithm is described and pruning set is created by taking 30% of the training set instances selected at random.

.. raw:: latex

   \begingroup
   \setlength{\tabcolsep}{.6em}

.. tabularcolumns:: p{0.1\linewidth} L{0.3\linewidth} p{0.5\linewidth}
.. _tbl-existing-algo:
.. list-table:: The list of the existing algorithms used for the comparison with the proposed |algo| algorithm
    :header-rows: 1

    * - Short Name
      - Name
      - Description
    * - CART-LC
      - The Classification and Regression Tree with Linear Combinations
      - an incremental deterministic algorithm for oblique DT induction. For its implementation, the description provided in :cite:`murthy1994system` was used as a reference.
    * - OC1
      - Oblique Classifier
      - an incremental randomized algorithm for oblique DT induction,
    * - OC1-AP
      - Oblique Classifier - Axis-Parallel
      - the OC1 algorithm limited to inducing only axis-parallel tests,
    * - OC1-ES
      - Oblique Classifier - Evolutionary Strategy
      - an extension to OC1 that uses ES to optimize the oblique hyperplanes,
    * - OC1-SA
      - Oblique Classifier - Simulated Annealing
      - an extension to OC1 that uses simulated annealing to optimize the oblique hyperplanes,
    * - NODT
      - HereBoy Decision Tree induction
      - an incremental randomized algorithm for oblique DT induction, that uses HereBoy :cite:`levi2000hereboy` for the hyperplane optimization process.
    * - GaTree
      - Genetic Algorithm decision Tree induction
      - a nonincremental (full tree) DT induction algorithm based on genetic algorithms.
    * - GALE
      - Genetic and Artificial Life Environment
      - a nonincremental (full tree) DT induction algorithm based on the cellular automata and the Pittsburgh approach :cite:`smith1983flexible`.

.. raw:: latex

   \endgroup

The software implementation of the |algo| algorithm was developed in C, using many optimization techniques in order to maximize its performance regarding the induction speed:

- The node test coefficients are represented in fixed point and all dot product arithmetic operations are performed on 64-bit operands only (optimized for the 64-bit CPU).
- The dot product calculation loop is unfolded for all supported |NA| values.
- To save on copying the DT individuals, the current candidate solution (``dt``) and the mutated individual (``dt_mut``) are represented by a single DT in memory. Hence, the mutations are applied directly to the candidate solution. If the mutated solution gets rejected by the ``select()`` function, the mutations are undone, which since they are sparse is more efficient than copying the whole DT to create a mutated individual. On the other hand if the mutated solution is selected, no actions are needed since the mutated solution is at the same time the candidate solution.
- Special case was introduced for traversing the DT which contains only the root node. The ``find_dt_leaf_for_inst()`` function contains a lot of programming structures for iterating through the DT and also for deciding whether memorized traversal paths can be reused or not, which is all superfluous for a simple case of one node DT.
- The maximum compiler optimization settings for speed were used.

The software implementation of the |algo| algorithm was compiled using the GCC 5.4.1 compiler, and all the experiments were executed on a PC with 64-bit, 4-core, Intel i5-2500K CPU operating at approximately 3.5GHz, with 8GB or RAM, running Ubuntu 16.04 operating system. GALE software, written in java, was run on OpenJDK 1.8, and GaTree, written for Windows OS, was run using Wine 1.6.2 .

Dependence on the number of iterations
......................................

First, the results are presented for the set of the experiments that test the dependency of the inferred DT quality to the number of iterations the |algo| algorithm was run. The induced DT accuracies and sizes are shown in the :num:`Table #tbl-max-iter-comp-acc` and :num:`Table #tbl-max-iter-comp-size` respectively, for different number of iterations. The same results are also presented in series of plots in the :num:`Figure #fig-max-iter-comp1` and :num:`Figure #fig-max-iter-comp2`. In these figures, the plots are organized in pairs, where each pair consists of the accuracy and size plots for the same five algorithms displayed in juxtaposition. Please notice that the x-axis, corresponding to the number of iterations, is given in logarithmic scale. Please also notice that the ranges for the y-axis, be it for the accuracy or the size plots, vary from plot to plot and depend on which datasets were used for the induction.

.. raw:: latex

   \begingroup
   \small
   \renewcommand{\arraystretch}{0.8}
   \setlength{\tabcolsep}{.2em}

.. tabularcolumns:: L{0.09\linewidth} | *{10}{R{0.075\linewidth}}

.. _tbl-max-iter-comp-acc:
.. csv-table:: The average fitness values for the DTs induced using different number of iterations
    :header-rows: 1
    :file: scripts/max-iter-comp-acc.csv

.. tabularcolumns:: L{0.09\linewidth} | *{10}{R{0.075\linewidth}}

.. _tbl-max-iter-comp-size:
.. csv-table:: The average sizes of the DTs induced using different number of iterations
    :header-rows: 1
    :file: scripts/max-iter-comp-size.csv

.. raw:: latex

    \endgroup

.. subfigstart::

.. _fig-max-iter-comp-size0:

.. figure:: images/max-iter-comp/size0.pdf
    :align: center

    DT size: ger, sick, ca, vote, wilt

.. _fig-max-iter-comp-acc0:

.. figure:: images/max-iter-comp/acc0.pdf
    :align: center

    DT acc: ger, sick, ca, vote, wilt

.. _fig-max-iter-comp-size1:

.. figure:: images/max-iter-comp/size1.pdf
    :align: center

    DT size: bcw, irs, msh, psd, thy

.. _fig-max-iter-comp-acc1:

.. figure:: images/max-iter-comp/acc1.pdf
    :align: center

    DT acc: bcw, irs, msh, psd, thy

.. _fig-max-iter-comp-size2:

.. figure:: images/max-iter-comp/size2.pdf
    :align: center

    DT size: ausc, bank, ca, hep, hrts

.. _fig-max-iter-comp-acc2:

.. figure:: images/max-iter-comp/acc2.pdf
    :align: center

    DT acc: ausc, bank, ca, hep, hrts

.. _fig-max-iter-comp-size3:

.. figure:: images/max-iter-comp/size3.pdf
    :align: center

    DT size: ion, sb, spect, thy, bc

.. _fig-max-iter-comp-acc3:

.. figure:: images/max-iter-comp/acc3.pdf
    :align: center

    DT acc: ion, sb, spect, thy, bc

.. _fig-max-iter-comp-size4:

.. figure:: images/max-iter-comp/size4.pdf
    :align: center

    DT size: son, w21, adult, car, magic

.. _fig-max-iter-comp-acc4:

.. figure:: images/max-iter-comp/acc4.pdf
    :align: center

    DT acc: son, w21, adult, car, magic

.. subfigend::
    :width: 0.49
    :label: fig-max-iter-comp1

    Dependency of the induced DT sizes and accuracies on the number of iterations the |algo| algorithm was run. Datasets 1-25.

.. subfigstart::

.. _fig-max-iter-comp-size5:

.. figure:: images/max-iter-comp/size5.pdf
    :align: center

    DT size: zoo, shuttle, seg, page, gls

.. _fig-max-iter-comp-acc5:

.. figure:: images/max-iter-comp/acc5.pdf
    :align: center

    DT acc: zoo, shuttle, seg, page, gls

.. _fig-max-iter-comp-size6:

.. figure:: images/max-iter-comp/size6.pdf
    :align: center

    DT size: nurse, pen, pid, w40, ctg

.. _fig-max-iter-comp-acc6:

.. figure:: images/max-iter-comp/acc6.pdf
    :align: center

    DT acc: nurse, pen, pid, w40, ctg

.. _fig-max-iter-comp-size7:

.. figure:: images/max-iter-comp/size7.pdf
    :align: center

    DT size: cvf, hrtc, jvow, liv, ttt

.. _fig-max-iter-comp-acc7:

.. figure:: images/max-iter-comp/acc7.pdf
    :align: center

    DT acc: cvf, hrtc, jvow, liv, ttt

.. _fig-max-iter-comp-size8:

.. figure:: images/max-iter-comp/size8.pdf
    :align: center

    DT size: spf, veh, vow, cmc, wine

.. _fig-max-iter-comp-acc8:

.. figure:: images/max-iter-comp/acc8.pdf
    :align: center

    DT acc: spf, veh, vow, cmc, wine

.. _fig-max-iter-comp-size9:

.. figure:: images/max-iter-comp/size9.pdf
    :align: center

    DT size: eb, eye, krkopt, letter, bch

.. _fig-max-iter-comp-acc9:

.. figure:: images/max-iter-comp/acc9.pdf
    :align: center

    DT acc: eb, eye, krkopt, letter, bch

.. subfigend::
    :width: 0.49
    :label: fig-max-iter-comp2

    Dependency of the induced DTs on the number of iterations the |algo| algorithm was run. Datasets 25-50.

It can be seen from the results that indeed the more iterations are at disposal, the more accurate the DT solutions become. However, after a certain point, which is different for different datasets, the |algo| algorithm is unable to improve on the solution significantly when more iterations are given for the induction. Usually, at around 500k iterations, all advancements in the quality of induced DT individuals have stopped for the vast majority of the datasets. Furthermore, for some datasets like ``bank``, ``bcw``, ``ca``, ``irs`` and ``wilt``, even a 1000 iterations were enough to find a decent solution.

Equitemporal comparison with the existing solutions
...................................................

This section presents the results of comparison of the quality between DTs induced by the existing algorithms from the :num:`Table #tbl-existing-algo`, and DTs induced by the |algo| algorithm in the same amount of time. Each subsection is devoted to comparison of the |algo| algorithm to one of the existing solutions, which was performed by first letting the other algorithm induce the DTs in a five 5-fold cross-validations on all datasets from the :num:`Table #tbl-uci`, while measuring the induction times. The average induction times were then calculated for each of the dataset, and |algo| was then let to perform same five 5-fold cross-validations but constrained per dataset to running only the amount of time that the other algorithm needed on average for the same dataset. For each comparison, two tables were generated: one showing the average induction times per dataset for the algorithm |algo| is being compared to, and the other showing the comparison per dataset between the average induced DT accuracies, sizes and fitnesses. The DT fitness used for this comparison is not the same fitness used during the induction by the |algo| algorithm, but is recalculated after the induction from the induced DTs' size and the accuracy attained on the test set using the equation :eq:`eq-oversize`. The backgrounds of cells in the comparison table are colored in shades of red and blue. The better the performance regarding certain feature (either accuracy, size or fitness), of |algo| in comparison to the other algorithm on certain dataset, the darker shade of blue is used. On the other hand if the |algo| algorithm performed worse, the worse its performance the darker the shade of red is used as the cell background. The average data in both tables are supplied with their 95% confidence intervals.

The :num:`Table #tbl-existing-comp-exp-params` shows two sets of the |algo| algorithm parameters that were used in the experiments. The "High accuracy" set was used for the comparison with incremental algorithms, since they tend to create larger, but more accurate DTs, and the "High compression" set was used for the comparison with full DT induction algorithms (namely GaTree and GALE), since they tend to create smaller, but less accurate DTs.

.. tabularcolumns:: L{0.3\linewidth} | R{0.08\linewidth} R{0.06\linewidth} R{0.1\linewidth} R{0.12\linewidth} R{0.08\linewidth} R{0.12\linewidth}

.. _tbl-existing-comp-exp-params:

.. list-table:: Two sets of the parameters set to the |algo| algorithm for the comparison experiments
    :header-rows: 1

    * - Approach
      - :math:`K_o`
      - :math:`\alpha`
      - :math:`\beta`
      - :math:`\rho_0`
      - :math:`S_T`
      - :math:`p_R`
    * - High accuracy
      - **0.01**
      - 1
      - 0.6
      - :math:`\num{5e-5}`
      - 0.05
      - :math:`\num{1e-4}`
    * - High compression
      - **0.2**
      - 1
      - 0.6
      - :math:`\num{5e-5}`
      - 0.05
      - :math:`\num{1e-4}`

.. _sec-cart-comp:

CART-LC
;;;;;;;

The following section presents the results of the comparison between the CART-LC algorithm and the |algo| algorithm with the "High accuracy" parameter set. CART-LC is the quickest oblique induction algorithm of the ones used in the experiments, and its induction times are shown in the :num:`Table #tbl-cart-time`.

.. raw:: latex

   \begingroup
   \small

.. tabularcolumns:: L{0.09\linewidth} | R{0.18\linewidth} | L{0.09\linewidth} | R{0.18\linewidth} | L{0.09\linewidth} | R{0.18\linewidth}
.. _tbl-cart-time:
.. csv-table:: The average induction times of the CART-LC algorithm per dataset
    :header-rows: 1
    :file: scripts/cart-time.csv

.. raw:: latex

   \endgroup

The results of the comparison experiments are displayed side by side in the :num:`Table #tbl-cart-acc`. The results show that, although the |algo| algorithm was not built for time efficiency as its primary objective, it can still readily compete with a fast algorithm such as CART-LC. There are some datasets, such as ``car``, ``ctg``, ``eb``, ``eye``, ``jvow``, ``krkopt``, ``letter``, ``nurse``, ``psd``, ``seg``, ``vow`` and ``wfr``, where |algo| significantly underachieved with respect to the DT accuracy. Generally these are the cases which require big DTs, for which the |algo| algorithm did not have time in this scenario, or was too constrained by the oversize weight parameter |Ko|. For all other datasets, the |algo| algorithm managed to either produce smaller DTs, or the DTs with increased accuracy by paying a small price in the DT size. For the datasets like: ``adult``, ``bank``, ``cmc``, ``magic``, ``page``, ``shuttle``, ``sick``, ``spf``, ``ttt``, ``wilt``, and ``wine``. |algo| managed to compress the DTs up to 20 times (40 in the case of ``wine`` dataset), compared to the CART-LC, with the loss in accuracy of only few percent. For the others like ``ausc``, ``bc``, ``bch``, ``bcw``, ``ca``, ``hrts``, ``liv``, ``pid``, ``w21`` and ``w40``, |algo| even succeeded in producing more accurate DTs, with their sizes being up to 3 times smaller than the DTs induced by the CART-LC. Finally, for some datasets like: ``gls``, ``hep``, ``hrtc``, ``irs``, ``lym``, ``son``, ``spect`` and ``zoo``, |algo| created DTs that are 10-20% more accurate, by paying small price in their size, compared to the CART-LC. There are only four datasets, for which the |algo| algorithm fitness measure shows poorer combined performance on both fields of accuracy and size: ``ger``, ``psd``, ``seg`` and ``thy``.

.. raw:: latex

   \begingroup
   \small

.. tabularcolumns:: L{0.09\linewidth} | R{0.12\linewidth} R{0.08\linewidth} | R{0.15\linewidth} R{0.12\linewidth} | R{0.2\linewidth} R{0.12\linewidth}
.. _tbl-cart-acc:
.. csv-table:: The results of the comparison experiments between the CART-LC algorithm and the |algo| algorithm, displayed side by side for different induced DTs' characteristics:  accuracy, size and fitness
    :header-rows: 2
    :file: scripts/cart-comp.csv

.. raw:: latex

    \endgroup

.. _sec-oc1-es-comp:

OC1-ES
;;;;;;

The following section presents the results of the comparison between the OC1-ES algorithm and the |algo| algorithm with the "High accuracy" parameter set. The OC1-ES is the second fastest algorithm among the ones used in the experiments, and needs on average (it varies with the dataset) twice as much time for the induction as CART-LC, and its induction times are shown in the :num:`Table #tbl-oc1-es-time`. However, for some of the more complex datasets, the average induction times were similar to the CART-LC's (``jvow``, ``pen``, ``w40``), and some were even shorter (``bch``, ``letter``). OC1-ES was run with the default setting of 1000 iterations per node. Several experiments were made to test whether higher iteration counts (2000, 5000, 10000 and 50000) would increase the quality of the solutions, but no benefits were observed over the defaults.

.. raw:: latex

   \begingroup
   \small

.. tabularcolumns:: L{0.09\linewidth} | R{0.18\linewidth} | L{0.09\linewidth} | R{0.18\linewidth} | L{0.09\linewidth} | R{0.18\linewidth}
.. _tbl-oc1-es-time:
.. csv-table:: The average induction times of the OC1-ES algorithm per dataset
    :header-rows: 1
    :file: scripts/oc1_es-time.csv

.. raw:: latex

    \endgroup

The results of the comparison experiments are displayed side by side in the :num:`Table #tbl-oc1-es-acc`. The results show, that OC1-ES has very similar performance with respect to the DT accuracy to the CART-LC for most of the datasets, with a tendency to induce larger DTs. On the other hand, the |algo| algorithm managed only slightly to improve on DT accuracy, where it was given more time. Hence, the discussion about the results from the :num:`Section #sec-cart-comp`, can be applied almost verbatim to the results from the :num:`Table #tbl-oc1-es-acc`. The only differences stem from the fact that OC1-ES produces even larger DTs, hence the compresion ratios of the |algo| algorithm are even higher. This resulted in |algo| now producing smaller DTs for the datasets: ``ger``, ``hep``, ``son`` and ``spect`` as opposed to the comparison results with CART-LC, while still retaining an advantage in the accuracy, and even increasing it.

.. raw:: latex

   \begingroup
   \small

.. tabularcolumns:: L{0.09\linewidth} | R{0.11\linewidth} R{0.08\linewidth} | R{0.16\linewidth} R{0.12\linewidth} | R{0.2\linewidth} R{0.12\linewidth}
.. _tbl-oc1-es-acc:
.. csv-table:: The results of the comparison experiments between the OC1-ES algorihtm and the |algo| algorithm, displayed side by side for different induced DTs' characteristics: accuracy, size and fitness
    :header-rows: 2
    :file: scripts/oc1_es-comp.csv

.. raw:: latex

    \endgroup

OC1-SA
;;;;;;

The following section presents the results of the comparison between the OC1-SA algorithm and the |algo| algorithm with the "High accuracy" parameter set. OC1-SA takes even more time than OC1-ES to run, and is 10 to 20 times slower than CART-LC. Its induction times are shown in the :num:`Table #tbl-oc1-sa-time`. OC1-SA was run with the default setting of 20 temperature values with 50 iterations for each of them per node. Several experiments were made to test whether different number of temperature values (10, 20, 40 and 80) and iteration counts (25, 50 and 100) would increase the quality of the solutions, but no benefits were observed over the defaults.

.. raw:: latex

   \begingroup
   \small

.. tabularcolumns:: L{0.09\linewidth} | R{0.18\linewidth} | L{0.09\linewidth} | R{0.18\linewidth} | L{0.09\linewidth} | R{0.18\linewidth}
.. _tbl-oc1-sa-time:
.. csv-table:: The average induction times of the OC1-SA algorithm per dataset
    :header-rows: 1
    :file: scripts/oc1_sa-time.csv

.. raw:: latex

    \endgroup

The results of the comparison experiments are displayed side by side in the :num:`Table #tbl-oc1-es-acc`. The results show, that OC1-SA produced very similar results in terms of accuracy to OC1-ES, and tended to produce somewhat smaller DTs. Nevertheless, the conclusions for the comparison results are almost identical to the ones discussed for OC1-ES in the :num:`Section #sec-oc1-es-comp`

.. raw:: latex

   \begingroup
   \small

.. tabularcolumns:: L{0.09\linewidth} | R{0.11\linewidth} R{0.08\linewidth} | R{0.16\linewidth} R{0.12\linewidth} | R{0.2\linewidth} R{0.12\linewidth}
.. _tbl-oc1-sa-acc:
.. csv-table:: The results of the comparison experiments between the OC1-SA algorihtm and the |algo| algorithm, displayed side by side for different induced DTs' characteristics: accuracy, size and fitness
    :header-rows: 2
    :file: scripts/oc1_sa-comp.csv

.. raw:: latex

    \endgroup

.. _sec-oc1-comp:

OC1
;;;

The following section presents the results of the comparison between the OC1 algorithm and the |algo| algorithm with the "High accuracy" parameter set. OC1 takes similar time to run as OC1-SA does, which is 10 to 20 times slower than CART-LC. Its induction times are shown in the :num:`Table #tbl-oc1-time`.

.. raw:: latex

   \begingroup
   \small

.. tabularcolumns:: L{0.09\linewidth} | R{0.18\linewidth} | L{0.09\linewidth} | R{0.18\linewidth} | L{0.09\linewidth} | R{0.18\linewidth}
.. _tbl-oc1-time:
.. csv-table:: The average induction times of the OC1 algorithm per dataset
    :header-rows: 1
    :file: scripts/oc1-time.csv

.. raw:: latex

    \endgroup

The results of the comparison experiments are displayed side by side in the :num:`Table #tbl-oc1-es-acc`. The results show, that OC1 has very similar performance with respect to the DT accuracy to the CART-LC, but has a tendency to induce smaller DTs. However, the |algo| algorithm had a significant advantage over CART-LC when it comes to the induced DT size, and this remains true when compared to OC1 as well. This means that the discussion about the results from the :num:`Section #sec-cart-comp`, remains valid for the results from the :num:`Table #tbl-oc1-acc` too. The differences between results of comparisons with CART-LC and OC1 arise mainly because in case of comparison with OC1, |algo| had 10 to 20 times more time for the evolution, hence average accuracies have significantly improved for some of the datasets like: ``bch``, ``car``, ``cmc``, ``ctg``, ``eb``, ``jvow``, ``nurse``,  ``veh``, ``vow`` and ``wfr``, while OC1 brought no significant improvement to the accuracies over CART-LC.

.. raw:: latex

   \begingroup
   \small

.. tabularcolumns:: L{0.09\linewidth} | R{0.11\linewidth} R{0.08\linewidth} | R{0.16\linewidth} R{0.12\linewidth} | R{0.2\linewidth} R{0.12\linewidth}
.. _tbl-oc1-acc:
.. csv-table:: The results of the comparison experiments between the OC1 algorihtm and the |algo| algorithm, displayed side by side for different induced DTs' characteristics: accuracy, size and fitness
    :header-rows: 2
    :file: scripts/oc1-comp.csv

.. raw:: latex

    \endgroup

.. _sec-nodt-comp:

NODT
;;;;

The following section presents the results of the comparison between the NODT algorithm and the |algo| algorithm with the "High accuracy" parameter set. NODT was run with the default settings:

   - Number of iterations: 100000
   - Search probability: 0
   - Percentage of available data used as validation set: 30%,
   - Percentage of mutated bits: 10%

.. raw:: latex

   \begingroup
   \small

.. tabularcolumns:: L{0.09\linewidth} | R{0.18\linewidth} | L{0.09\linewidth} | R{0.18\linewidth} | L{0.09\linewidth} | R{0.18\linewidth}
.. _tbl-nodt-time:
.. csv-table:: The average induction times of the NODT algorithm per dataset
    :header-rows: 1
    :file: scripts/nodt-time.csv

.. raw:: latex

    \endgroup

The results of the comparison experiments are displayed side by side in the :num:`Table #tbl-oc1-es-acc`. It can be seen from the results, that only in few cases has the NODT induced significantly advantageous DTs in terms of accuracy, like from datasets: ``eye``, ``jvow``, ``krkopt``, and ``letter``, but usually the |algo| algorithm had better results both in terms of the accuracy and size. For other datasets, when NODT produced slightly more accurate DTs then |algo|, it was compensated by their size being significantly larger in comparison to the DTs induced by |algo|. And vice versa, when NODT produced smaller DTs, their accuracy was usually worse than that of DTs induced by |algo|. This can also be seen in the fitness column, where |algo| always had advantage over NODT.

.. raw:: latex

   \begingroup
   \small

.. tabularcolumns:: L{0.09\linewidth} | R{0.12\linewidth} R{0.08\linewidth} | R{0.15\linewidth} R{0.12\linewidth} | R{0.2\linewidth} R{0.12\linewidth}
.. _tbl-nodt-acc:
.. csv-table:: The results of the comparison experiments between the NODT algorithm and the |algo| algorithm, displayed side by side for different induced DTs' characteristics: accuracy, size and fitness
    :header-rows: 2
    :file: scripts/nodt-comp.csv

.. raw:: latex

    \endgroup

.. _sec-gale-comp:

GALE
;;;;

The following section presents the results of the comparison between the GALE algorithm and the |algo| algorithm with the "High compression" parameter set, since GALE operates on full DTs in its induction procedure and thus tends to create smaller DTs. The induction times of the GALE algorithm are shown in the :num:`Table #tbl-gale-time`, and are even higher than OC1, since GALE operates on the population of the full DTs, which requires more computational time.

.. raw:: latex

   \begingroup
   \small

.. tabularcolumns:: L{0.09\linewidth} | R{0.18\linewidth} | L{0.09\linewidth} | R{0.18\linewidth} | L{0.09\linewidth} | R{0.18\linewidth}
.. _tbl-gale-time:
.. csv-table:: The average induction times of the GALE algorithm per dataset
    :header-rows: 1
    :file: scripts/gale-time.csv

.. raw:: latex

    \endgroup

The results of the comparison experiments are displayed side by side in the :num:`Table #tbl-gale-acc`. The results show that the |algo| algorithm produces more accurate DTs with all datasets used in experiments (except for the ``ttt`` dataset, where it produced on average 15 times smaller DTs, with 4% loss in accuracy). In addition, for most of the datasets, it was able to produce smaller DTs as well. In case of the datasets where DTs produced by GALE were smaller, like: ``bch``, ``cvf``, ``eb``, ``gls``, ``krkopt``, ``letter``, ``seg`` and ``shuttle``, they were also much less accurate then the ones induced by |algo|.

.. raw:: latex

   \begingroup
   \small

.. tabularcolumns:: L{0.09\linewidth} | R{0.12\linewidth} R{0.08\linewidth} | R{0.15\linewidth} R{0.12\linewidth} | R{0.2\linewidth} R{0.12\linewidth}
.. _tbl-gale-acc:
.. csv-table:: The results of the comparison experiments between the GALE algorithm and the |algo| algorithm, displayed side by side for different induced DTs' characteristics: accuracy, size and fitness
    :header-rows: 2
    :file: scripts/gale-comp.csv

.. raw:: latex

    \endgroup

GaTree
;;;;;;

The following section presents the results of the comparison between the GaTree algorithm and the |algo| algorithm with the "High compression" parameter set, since GaTree operates on full DTs in its induction procedure and thus tends to create smaller DTs. The induction times of the GaTree algorithm are shown in the :num:`Table #tbl-gatree-time`.

.. raw:: latex

   \begingroup
   \small

.. tabularcolumns:: L{0.09\linewidth} | R{0.18\linewidth} | L{0.09\linewidth} | R{0.18\linewidth} | L{0.09\linewidth} | R{0.18\linewidth}
.. _tbl-gatree-time:
.. csv-table:: The average induction times of the GaTree algorithm per dataset
    :header-rows: 1
    :file: scripts/gatree-time.csv

.. raw:: latex

    \endgroup

The results of the comparison experiments are displayed side by side in the :num:`Table #tbl-gatree-acc`. The results show that the |algo| algorithm produces more accurate DTs with all datasets used in experiments, with almost all of them being smaller in size as well. In case of the datasets where DTs produced by GaTree were smaller, like: ``bch``, ``eb``, ``letter``, ``page``, and ``thy``, they were also much less accurate then the ones induced by |algo|.

.. raw:: latex

   \begingroup
   \small

.. tabularcolumns:: L{0.09\linewidth} | R{0.12\linewidth} R{0.08\linewidth} | R{0.15\linewidth} R{0.12\linewidth} | R{0.2\linewidth} R{0.12\linewidth}
.. _tbl-gatree-acc:
.. csv-table:: The results of the comparison experiments between the GaTree algorithm and the |algo| algorithm, displayed side by side for different induced DTs' characteristics: accuracy, size and fitness
    :header-rows: 2
    :file: scripts/gatree-comp.csv

.. raw:: latex

    \endgroup

Group comparison of all algorithms
..................................

In this section, the results of the experiments are displayed and discussed, that compare all the algorithms from the :num:`Table #tbl-existing-algo` together with the proposed |algo| algorithm in terms of induced DT accuracies and sizes. In these experiments, the |algo| algorithm was setup using the "High accuracy" configuration for the :num:`Table #tbl-existing-comp-exp-params` and given 1000k iterations for the induction. The cross-validation employed and the rankings devised in the manner described in the :num:`Section #sec-exp-struct`. The results are listed in the following tables:

   - :num:`Table #tbl-comp-mean-acc-01` shows the average accuracies of the induced DTs,
   - :num:`Table #tbl-comp-conf-acc-01` shows the 95% confidence intervals for the accuracies of the induced DTs
   - :num:`Table #tbl-comp-mean-relative-acc-01` shows the relative differences in accuracies of the DTs induced by the existing algorithms compared to the DTs induced by the |algo| algorithm on the same dataset. Values are given in percents, where the positive numbers show the amount by which an existing algorithm produces more accurate DTs, relative to those induced by |algo|, and negative numbers show the opposite.
   - :num:`Table #tbl-comp-mean-size-01` shows the average sizes of the induced DTs,
   - :num:`Table #tbl-comp-conf-size-01` shows the 95% confidence intervals for the sizes of the induced DTs
   - :num:`Table #tbl-comp-mean-relative-size-01` shows the relative differences in sizes of the DTs induced by the existing algorithms compared to the DTs induced by the |algo| algorithm on the same dataset. Values are given in percents, where the positive numbers show the amount by which an existing algorithm produces larger DTs, relative to those induced by |algo|, and negative numbers show the opposite.
   - :num:`Table #tbl-comp-rank-acc-01` shows the ranking of the algorithms based on the accuracies of the induced DTs
   - :num:`Table #tbl-comp-rank-size-01` shows the ranking of the algorithms based on the sizes of the induced DTs

.. raw:: latex

   \begingroup
   \setlength{\tabcolsep}{.2em}
   \renewcommand{\arraystretch}{0.9}
   \normalsize

.. tabularcolumns:: p{0.05\linewidth} *{9}{R{0.09\linewidth}}

.. _tbl-comp-mean-acc-01:
.. csv-table:: The average accuracies of the induced DTs by all algorithms from the :num:`Table #tbl-existing-algo` and |algo|, on all datasets from the :num:`Table #tbl-uci` from five 5-fold cross-validation test.
    :header-rows: 1
    :file: scripts/comp-mean-acc-0.01.csv

.. tabularcolumns:: p{0.05\linewidth} *{9}{R{0.09\linewidth}}

.. _tbl-comp-conf-acc-01:
.. csv-table:: The 95% confidence intervals for the accuracies of the induced DTs by all algorithms from the :num:`Table #tbl-existing-algo`, on all datasets from the :num:`Table #tbl-uci` from five 5-fold cross-validation test.
    :header-rows: 1
    :file: scripts/comp-conf-acc-0.01.csv

.. tabularcolumns:: p{0.05\linewidth} *{8}{R{0.1\linewidth}}

.. _tbl-comp-mean-relative-acc-01:
.. csv-table:: The relative differences in accuracies of the DTs induced by the algorithms from the :num:`Table #tbl-existing-algo`, compared to the DTs induced by the |algo| algorithm on the same dataset.
    :header-rows: 1
    :file: scripts/comp-mean-relative-acc-0.01.csv

.. tabularcolumns:: p{0.05\linewidth} *{9}{R{0.09\linewidth}}

.. _tbl-comp-mean-size-01:
.. csv-table:: The average sizes of the induced DTs by all algorithms from the :num:`Table #tbl-existing-algo` and |algo|, on all datasets from the :num:`Table #tbl-uci` from five 5-fold cross-validation test.
    :header-rows: 1
    :file: scripts/comp-mean-size-0.01.csv

.. raw:: latex

   \begingroup
   \setlength{\tabcolsep}{.15em}

.. tabularcolumns:: p{0.05\linewidth} *{9}{R{0.095\linewidth}}

.. _tbl-comp-conf-size-01:
.. csv-table:: The 95% confidence intervals for the sizes of the induced DTs by all algorithms from the :num:`Table #tbl-existing-algo`, on all datasets from the :num:`Table #tbl-uci` from five 5-fold cross-validation test.
    :header-rows: 1
    :file: scripts/comp-conf-size-0.01.csv

.. raw:: latex

   \endgroup

.. tabularcolumns:: p{0.05\linewidth} *{8}{R{0.1\linewidth}}

.. _tbl-comp-mean-relative-size-01:
.. csv-table:: The relative differences in sizes of the DTs induced by the algorithms from the :num:`Table #tbl-existing-algo`, compared to the DTs induced by the |algo| algorithm on the same dataset.
    :header-rows: 1
    :file: scripts/comp-mean-relative-size-0.01.csv

.. tabularcolumns:: p{0.05\linewidth} *{9}{C{0.09\linewidth}}

.. _tbl-comp-rank-acc-01:
.. csv-table:: The ranking of the algorithms from the :num:`Table #tbl-existing-algo` and |algo| based on the induced DT accuracies, calculated using the procedure explained in the :num:`Section #sec-exp-struct`.
    :header-rows: 1
    :file: scripts/comp-rank-acc-0.01.csv

.. tabularcolumns:: p{0.05\linewidth} *{9}{C{0.09\linewidth}}

.. _tbl-comp-rank-size-01:
.. csv-table:: The ranking of the algorithms from the :num:`Table #tbl-existing-algo` and |algo| based on the induced DT sizes, calculated using the procedure explained in the :num:`Section #sec-exp-struct`.
    :header-rows: 1
    :file: scripts/comp-rank-size-0.01.csv

.. raw:: latex

    \endgroup

The results of the experiments in this section show that the proposed |algo| algorithm is capable of inducing the DTs of the accuracies comparable to other well known incremental algorithms like CART-LC and OC1, but with the significant reduction in their sizes. This can be seen in the average rankings of the algorithms based on their accuracies and sizes. In terms of accuracy, the |algo| scored an average of 1.804, compared to 1.686 of CART-LC and 1.961 of OC1. On the other hand, when it comes to size, |algo| had a significantly higher average rank of 1.118, compared to 1.843 of CART-LC and 1.627 of OC1. When compared to full DT induction algorithms GALE and GaTree, |algo| was better in terms of induced DT size and significantly better when it came to DT accuracies.
