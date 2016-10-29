.. _sec-cop:

Co-processor for the DT induction - the |cop|
=============================================

Very few theorems exist about evolutionary algorithms that can be used to guarantee some of their behaviour, with probably the most famous results being the one that statesl that (1+1) ES takes :math:`O(n log(n))` iterations to find a maximum of any linear function :cite:`droste2002analysis`. Even worse, the "No Free Lunch" theorem :cite:`wolpert1996lack` implies that no optimization algorithm can have, on average, a superior performance on many different problems, which means that usually optimization algorithms need to be specifically tuned for each problem. However, in order to find the optimal parameter set for an EA, or test the efficiency of a new algorithm feature, usually an experimantal approach needs to be used for the lack of theoretical guidelines. In order for the experiment to have a level of statistical significance, usually multiple runs of cross-validation technique are used.

For tuning the parameters and testing new features for the |algo| algorithm, five 5-fold cross-validations were performed for each dataset with 500k iterations, which for the largest of them, ``shuttle`` took almost 6 hours on a desktop PC (average induction times when partial reconfiguration is used can be found in :num:`Table #tbl-delta-time-comp`). In order to find an optimal parameter set, some kind of meta-heuristic needs to be employed, where in each of its iterations such a cross-validation test would be needed to evaluate its current candidate solution. This would then amount to days or even weeks of processing time. Embedded CPUs are even less powerfull and would take even more time for these operations. Hence, the application of the DT induction using EAs in a dynamically adaptable real-time embedded machine learning system would be impractical.

In an attempt to address these issues, the |cop| co-processor (Evolutionary Full Tree Induction co-Processor) is proposed

.. _profiling-results:

Profiling results
-----------------

It is clear from the equation :eq:`cplx_final` that the ``fitness_eval()`` function is a good candidate for the hardware acceleration since it is the dominant contributor to the algorithm time complexity. To confirm the results obtained by the computational complexity analysis, the software profiling was performed on the |algo| algorithm's C implementation. The |algo| algorithm was let to induce DTs from all datasets from the :num:`Table #tbl-uci` in order to gather the profiling data. The software implementation of the |algo| algorithm was compiled using the GCC 5.4.1 compiler, run on the PC with 64-bit, 4-core, Intel i5-2500K CPU operating at approximately 3.5GHz, with 8GB or RAM, running Ubuntu 16.04 operating system and profiled using the GProf performance analysis tool for each of the datasets individually.

.. raw:: latex

   \begingroup
   \small
   \renewcommand{\arraystretch}{0.8}

.. tabularcolumns:: L{0.12\linewidth} | *{5}{R{0.12\linewidth}}

.. _tbl-profiling:
.. csv-table:: The percentage of the induction time of the |algo| algorithm on each dataset spent in the functions within the fitness evaluation task on average: FLDFI - :literal:`find_dt_leaf_for_inst()`, AC - :literal:`accuracy_calc()`, ENT - :literal:`evaluate_node_test()` and ASPC - :literal:`apply_single_path_change()`, versus the percentage of the time spent inside all other functions, given in the column titled "others".
    :header-rows: 1
    :file: scripts/profiling.csv

.. raw:: latex

    \endgroup

The results obtained by the profiling are listed in the :num:`Table #tbl-profiling` and displayed graphically in the :num:`Figure #fig-profiling-plot`. The results displayed in the table represent the percentage of the induction time of the |algo| algorith on each dataset that was spent in the functions within the fitness evaluation task on average: FLDFI - :literal:`find_dt_leaf_for_inst()`, AC - :literal:`accuracy_calc()`, ENT - :literal:`evaluate_node_test()` and ASPC - :literal:`apply_single_path_change()`, together with the percentage of the time spent inside all other functions, given in the column titled "others". The percentages given for the individual functions represent self-time, i.e. the execution time of the function without the execution times of its subfunctions. On the other hand, the :num:`Figure #fig-profiling-plot` shows, for each dataset, the percentage of the time spent in all fitness evaluation related functions combined.

.. subfigstart::

.. _fig-profiling-plot1:

.. plot:: images/profiling_plot1.py
    :align: center

    The datasets adult - hrtc

.. _fig-profiling-plot2:

.. plot:: images/profiling_plot2.py
    :align: center

    The datasets hrts - seg

.. _fig-profiling-plot3:

.. plot:: images/profiling_plot3.py
    :align: center

    The datasets shuttle - zoo

.. subfigend::
    :width: 1
    :label: fig-profiling-plot

    The percentage of the induction time, the |algo| algorithm spent in the ``fitness_eval()`` function and its subfuctions for the datasets listed in the :num:`Table #tbl-uci`.

The results presented in this subsection are consistent with the algorithm complexity analysis performed in the :num:`Section #sec-complexity`. On average, |algo| spent 99.0% of time calculating the fitness of the individual, hence the obvious computational bottleneck lays in the fitness evaluation task, which makes it an undoubtful candidate for the hardware acceleration.

Since all other tasks (mutation, selection, initialiation, etc.) take an insignificant amount of time on average to perform, it seems that there is no need to accelerate them in hardware. The |algo| algorithm can thus be implemented using HW/SW co-design architecure, where the fitness evaluation task would be implemented in hardware, while the rest of the functionality would remain in software. However, the |algo| algorithm could still benefit from moving all the remaining tasks to hardware too, since that would lower the communication overhead between the CPU and the custom hardware.

Nevertheless, for two reasons it was decided for the proposed |cop| co-processor to accelerate only the ``accuracy_calc()`` function (and all of its subfunctions) from the fitness evaluation task, with the rest of the |algo| algorithm functionality left in software. The first reason is that it would be much more difficult to change and experiment with the fitness formula and the tasks of mutation, selection, initialization, etc. if they were implemented in hardware. Second reason is that many other evolutionary algorithms for optimizing the DT structure can then be implemented in software and make use of the hardware accelerated fitness evaluation task, like: Genetic Algorithms (GA), Genetic Programming (GP), Simulated Annealing (SA), etc. This fact significantly expands the potential field of use for the proposed |cop| co-processor core.

.. _classifier-arch-overview:

Architectures for hardware implementation of the DT accuracy calculation
------------------------------------------------------------------------

The accuracy of a DT is calculated by letting the DT classify the instances of a training set. The results of the DT classification are then compared with the known classification of the training set and the accuracy is calculated as a number of the correct classifications to the total number of instances in the training set. A sequential algorithm for performing this task is employed by the |algo| algorithm and is described in the :num:`Section #accuracy-calculation`.

First attempt at developping a hardware implementation of this procedure might be to implement every DT node as a separate hardware module, and connect the modules in the form of the DT. The hardware architecture based on this idea is proposed in :cite:`lopez2006decision`, and shown in the :num:`Figure #fig-dt-class-arch-ex1`.

.. _fig-dt-class-arch-ex1:

.. bdp:: images/dt_class_arch_ex1.py
    :width: 60%

    The DT classification hardware implementation using one hardware module per DT node

The instance that is to be classified is sent to each of the hardware DT nodes, in which the node tests are evaluated. All the DT classes are made available on the inputs of the Demultiplexer (:num:`Figure #fig-dt-class-arch-ex1`). Depending on the classification result, one of the classes will be passed by the Demultiplexer to the output of the classifier. Starting from the root, the node tests' are evalulated sequentially along the classification path of the instance, and based on their results  the correct class for the output of the Demultiplexer is selected.

The hardware architecture proposed in :cite:`lopez2006decision` has two major drawbacks, one regarding the amount of hardware resources needed, and the other regarding the time needed to perform the classification. First, the architecture needs one hardware module per DT node, which in turn requires a significant amount of resources in order to be able to perform the dot product calculation of the node test (equation :eq:`oblique-test`). Second, the time needed to perform the classification is proportional to the depth of the DT and to the time needed to perform the node test calculation. In other words, this architecture does not scale well with the size of the DT.

One possible way of decreasing the classification time using this architecture is to perform all the node tests in parallel. This is akin to what has been suggested in :cite:`bermak2003compact`, where an equivalence between decision trees and threshold networks is used to devise a hardware architecture for decision tree classification, where all of the node tests are performed in parallel. Once all of the node tests have been evaluated, their results can be combined using a boolean function in order to determine in which node the instance finished the classification, and hence to which class it should be classified into. This way, the time needed to perform the classification equals the time needed to evaluate one node test, plus the time needed to evaluate the output boolean function. Still, the issue with number of node hardware modules remains.

The architecture that remedies both resource and timing problems and was adapted for the |cop| co-processor, is proposed in :cite:`struharik2009intellectual` and called *SMPL* (Single Module Per Layer). Instead of implementing each DT node in hardware separately, this architecture requires only one universal node per DT level, which is used to evaluate the test of all the nodes from that DT level. The fact that the instances traverse the DT only in one direction from top to bottom, never returning to already visited nodes, makes this solution possible.

.. _fig-smpl-dt:

.. bdp:: images/smpl_dt.py
    :width: 100%

    The idea behind *SMPL* (Single Module Per Layer) architecture. There is one universal hardware module (Universal nodes :math:`L_1 - L_3`) per DT level that implements all the DT nodes on the level.

The :num:`Figure #fig-smpl-dt` shows the structure of the *SMPL* architecture implementation for the same example of the DT used in :num:`Figure #fig-dt-class-arch-ex1`. The architecture implementation consists of three universal nodes :math:`L_1` through :math:`L_3`, one for each of the DT levels that contain nonleaf nodes. The instance starts its traversal of the DT by being input to the :math:`L_1` module, which implements the root DT node in every *SMPL* architecture implementation. The universal node :math:`L_1` evaluates the root node test and passes the instance along with the test results to the :math:`L_2` module, which is akin to the instance continuing its traversal to the level 2 of the DT. The :math:`L_2` module has the capability of calculating the node test for all the nodes on the level 2 of the DT, in this case node #2 and #3. Based on the root node test results received from :math:`L_1`, the :math:`L_2` module knows to which root child the instance has been passed, and thus the appropriate level 2 node test is evaluated, whose results, together with the instance, are in turn passed to its successor and this process is continued until one of the unicersal nodes detects that the instance has arrived to a leaf node, i.e. it has been classified. Thereafter, the information about the class is passed onwards and following universal nodes perform no test evaluations on this instance. Finally, the last module of the *SMPL* architecture outputs the class of the instance.

The *SMPL* is a pipelined architecture, hence the instances can be effectively classified in parallel on all universal nodes, with the small cost of an initial pipeline latency. The node test evaluation results calculated by an universal node, that are to be made available to the next universal node in pipeline, are stored in the register available between every two nodes (blocks named *reg* in the :num:`Figure #fig-smpl-dt`). That way, once the node test is evaluated for an instance and stored in the output register, the universal node is free to start processing the following instance from the dataset, while the next universal node in pipeline utilizes the stored results from the register.

The |cop| co-processor classification module was decided to be based on the *SMPL* architecture as it requires significantly less hardware resources for the implementation then the architectures :cite:`lopez2006decision` and :cite:`bermak2003compact`. In order to evalate oblique DT node tests, the addition, multiplication and comparison operations are needed. Hence, the *SMPL* architecture requires notably less adders, multipliers and comparators then architectures proposed in :cite:`lopez2006decision` and :cite:`bermak2003compact`. However, the memory resources requirements for storing the node test coefficients and leaf classes are identical between all three given architectures.

Overview
--------

In this section, an overview of the |cop| co-processor is given. As it was discussed in the section :num:`Section #profiling-results`, the |cop| is designed to accelerate the most time consuming task of the evolutionary DT induction algorithms, which is the task of determining the accuracy of the DT individual, which is in turn needed for the fitness evaluation of the DT (the :num:`Algorithm #fig-fitness-eval-pca`). More precisely, the |cop| co-processor calculates the number of successfull classifications, i.e. the number of classifications hits - the ``hits`` variable of the :num:`Algorithm #fig-accuracy-calc-pca`.

The |cop| co-processor is designed as an IP core and embedded to the SoC through the interconnect interface AXI4 AMBA bus. The ARM Advanced Microcontroller Bus Architecture (AMBA) is an open-standard, on-chip interconnect specification for the connection and management of functional blocks in system-on-a-chip (SoC) designs. Today, AMBA is widely used on a range of ASIC and SoC parts including applications processors used in modern portable mobile devices like smartphones. Via the AXI4 bus, the software running on the CPU can completely control the |cop| operation:

- Download of the training set
- Download of the DT description, including the structural organization and the coefficient values for all node tests present in the DT
- Start of the accuracy evaluation process
- Read-out of the classification performance results

.. _fig-system-bd:

.. bdp:: images/eftip_system_bd.py
    :width: 100%

    The |cop| co-processor structure and integration with the host CPU

The major components of the |cop| co-processor and their connections are depicted in the :num:`Figure #fig-system-bd`:

- **Classifier** - Performs the DT traversal for each training set instance, i.e. implements the ``find_dt_leaf_for_inst()`` function from the :num:`Algorithm #fig-find-dt-leaf-for-inst-pca`. The classification process is pipelined using a number of Node Test Evaluator modules (*NTEs*) corresponding to the universal nodes of the *SMPL* architecture, with each NTE performing the DT node test calculations for one DT level. The parameter |DM| is the number of pipeline stages and thus the maximum supported depth of the induced DT. For each instance in the training set, the Classifier outputs the ID assigned to the leaf in which the instance finished the traversal (please refer to the ``accuracy_calc()`` function from the :num:`Algorithm #fig-accuracy-calc-pca`).
- **Training Set Memory** - The memory for storing all training set instances that should be processed by the |cop| co-processor.
- **DT Memory Array** - The array of memories used for storing the DT description, composed of sub-modules :math:`L_{1}` through :math:`L_{D^{M}}`. Each Classifier pipeline stage requires its own memory that holds the description of all nodes at the DT level it is associated with. Each DT Memory sub-module is further divided into two parts: the CM (Coefficient Memory - memory for the node test coefficients) and the SM (Structural Memory - memory for the DT structural information).
- **Accuracy Calculator** - Based on the classification data received from the Classifier, it calculates the accuracy of the DT and keeps track of which training set classes were found as dominant for at least one DT leaf. For each instance of the training set, the Classifier supplies the ID of the leaf in which the instance finished the DT traversal. Based on this information, the Accuracy Calculator updates the distribution matrix, calculates the results, which are then forwarded to the Control Unit, ready to be read by the user.
- **Control Unit** - Acts as a bridge between the AXI4 interface and the internal protocols. It also controls the accuracy evaluation process and generates an IRQ when the calculation is done.

Hardware description
--------------------

The following section provides the detailed description of all |cop| modules:

- :num:`Section #sec-cop-classifier` - The Classifier module
- :num:`Section #sec-cop-training-set-memory` - The Training Set Memory module
- :num:`Section #sec-cop-dt-memory-array` - The DT Memory Array
- :num:`Section #sec-cop-accuracy-calc` - The Accuracy Calculator module
- :num:`Section #sec-cop-control-unit` - The Control Unit

.. _sec-cop-classifier:

Classifier
..........

The classifier module performs the classification of an arbitrary set of instances on an arbitrary binary oblique DT. As it was already discussed in the :num:`Section #classifier-arch-overview`, the Classifier module was implemented by modifying the *SMPL* architecture described in :cite:`struharik2009intellectual`. The original architecture from :cite:`struharik2009intellectual` was designed to perform the classification using already induced DTs, hence it was adapted so that it could be used with the |algo| algorithm for the DT induction as well.

.. _fig-dt-classifier-bd:

.. bdp:: images/classifier.py

    The architecture of the Classifier module consisting of the |NTE| modules connected in an array.

In order for the |cop| co-processor to calculate the accuracy of a DT on a dataset, the Classifier needs to perform the DT traversal for each instance of the dataset, i.e. it needs to implement the ``find_dt_leaf_for_inst()`` function from the :num:`Algorithm #fig-find-dt-leaf-for-inst-pca` in hardware. As it was discussed in the :num:`Section #classifier-arch-overview`, during the traversal of an instance, only one node per DT level is visited, i.e. only one node test is performed per DT level for a single instance. Hence, a single module that implements the evaluation of the oblique node test (equation :eq:`oblique-test`), could be used to incorporate the test evaluations for all nodes on one DT level. Naturally, this module would have to be programmable in that it would have to support the node test evaluation with different coefficient vectors in order to be able to evaluate tests for all nodes residing at same DT level. However, this would need to be the case even if one module was used to implement each DT node, since the |cop| co-processor is used for the DT induction so the node test coefficients are not known in advance.

The :num:`Figure #fig-dt-classifier-bd` shows the Classifier module as being composed from |NTE| modules, each of which is associated with one DT level, and implements the node test evaluation procedure for all nodes on that DT level. The |NTE| modules correspond to the universal nodes of the *SMPL* architecture. During the traversal of the DT, an instance always descends one DT level at the time, and never returns to the levels it already visited. The |NTE| modules are thus connected into a chain, where an instance is transfered from the first |NTE| to the last one in the chain, in order to calculate its DT traversal path. The number of *NTEs* the Classifier comprises - |DM|, determines the maximum depth of the DT whose accuracy can be calculated by that hardware instance of the |cop| co-processor. The |DM| value can be specified by the user during the design phase of the |cop| co-processor.

Since an instance always travels down the |NTE| chain, one |NTE| at a time, there is no reason why multiple instances could not traverse the chain simultaneously. The moment the :math:`NTE_1` evaluated the node test for the first instance of the dataset and the instance was transferred to the :math:`NTE_2`, the :math:`NTE_1` becomes free to evaluate the node test for the next instance in the dataset. In other words, the |NTE| modules can form the pipeline, with one stage per DT level, capable of accomodating |DM| instances in parallel, after the initial latency during which the pipeline is filled.

The :math:`NTE_1` always processes the root DT node. However, which nodes are processed by other stages depends on the path of the traversal for each individual instance. Hence each |NTE| module needs to have access to the descriptions of all the nodes on the DT level assosicated with it. Since each stage of the |NTE| pipeline needs to operate in parallel (in a distributed manner), the node description data needs to be distributed as well, and thus each stage has one sub-module of the DT Memory Array assigned to it that holds the descriptions of all the nodes on the DT level associated with that stage. Furthermore, each DT Memory Array sub-module is divided into two parts in order to save on some |NTE| hardware resources, namely |CM| and *SM*, because the data from these two memory parts is needed at different times in the node test evaluation, which will be discussed in more detail in the following text. Therefore, each |NTE| contains interfaces, comprising the address and data buses, for accessing the |CM| and *SM* parts of the assigned DT Memory Array sub-module: *CM addr*, *CM data*, *SM addr* and *SM data*.

When an instance is transferred from one |NTE| module to the next, the decision via which node the traversal continues (made by evaluating the node test) needs to be communicated along with it too. There are two major cases that need to be handled differently:

1. the instance continues the traversal via one of the children of the node whose test has been evaluated by the current |NTE| module. In this case, the next |NTE| in the chain is sent the ID of the child (non-leaf) node to which the instance should descend.

2. the instance has already been classified, in which case the traversal is finished. However, in order not to disturbe the filled pipeline, the instance is nevertheless transfered down the |NTE| chain. In this case, the next |NTE| in the chain is sent the ID of the leaf in which the instances finished its traversal. Based on that, the next |NTE| will recognize that no further calculations need to be performed for this instance, and that it can simply pass leaf ID onward.

The inter-NTE interface comprises the following buses:

- **Instance bus** - Passes the instance to the next |NTE|, as the instance traverses the DT.
- **Node ID bus** - Passes to the next |NTE| either the ID of a non-leaf node, through which the traversal is to be continued, or the ID of a leaf node into which the instance has already been classified in some of the previous pipeline stages. The leaf and the non-leaf IDs are distinguished by the value of the node ID's MSB. If the value of the MSB is zero, the node ID is a non-leaf ID, otherwise it is a leaf ID.

For each instance, received at the Classifier input, the first NTE block processes the dot product calculation using the attributes of the received instance |x| and the root node coefficients |w|. Based on the result, it then decides on how to proceed with the DT traversal: via the left or via the right child. The ID of the selected child node, which can either be a leaf or a non-leaf, is output via the *Node ID Output* port. If the selected child is a leaf node, the classification is done, and the next stages will perform no further calculations, but only pass forward the ID of the leaf into which the instance has been classified. On the other hand, if the selected child is a non-leaf node, the next stage will continue the traversal through the selected child by calculating the node test associated to it. The calculation of each NTE corresponds to one iteration of the ``find_dt_leaf_for_inst()`` function loop (:num:`Algorithm #fig-find-dt-leaf-for-inst-pca`), and the NTE output *Node ID* corresponds to the ``cur_node`` variable, more specifically to its attribute :literal:`id` needed for the formation of the distribution matrix in the function ``accuracy_calc()`` of the :num:`Algorithm #fig-accuracy-calc-pca` (``leaf.id``). The node ID is output synchronously with the instance via the *Instance Output* port.

All subsequent stages operate in a similar manner, except that in addition, they also receive the calculation results from their predecessor stage. Somewhere along the NTE chain, all instances will have finished into some leaf. This information is output from the Classifier module via the *Node ID Output* port of the last |NTE| in the chain to the Accuracy Calculator module (together with the corresponding instance description via the *Instance Output* port) in order to update the distribution matrix and calculate the final number of classification hits.

.. _sec-dot-product-parallelism:

The dot product parallelism
;;;;;;;;;;;;;;;;;;;;;;;;;;;

To evaluate a DT node test, each |NTE| needs to evaluate the dot product between node test coefficient vector |w| and instance attribute vector |x|, which is at the same time by far the most complex operation of the |NTE| module. By extracting the parallelism from the dot product operation, additional speedup could be gained. The :num:`Figure #fig-node-test-parallelism` shows which parts of the dot product calculation can be performed in parallel on an example where :math:`N_A=7`. If we are only allowed to perform binary addition (which is usually the case when a hardware block performs the adition), the calculation could be performed in 4 steps, with all the operations that could be executed in parallel in each step circled with dashed line. In Step 1 all the multiplications could be performed in parallel since there is no data dependency between them, while in later steps the |NA|-ary addition is broken down into the sequence of binary addition operations, where some of them could be executed in parallel in each of the remaining steps to obtain the final dot product result value.

.. _fig-node-test-parallelism:

.. bdp:: images/node_test_parallelism.py
    :width: 100%

    The figure shows which parts of the dot product calculation can be performed in parallel on an example where :math:`N_A=7`. If we are only allowed to perform binary addition (which is usually the case when a hardware block performs the addition), the calculation could be performed in 4 steps, with all the operations that could be executed in parallel in each step circled with dashed line.

To take advantage of this dot product calculation parallelism, the |NTE| module could be again pipelined internally for the maximal throughput. Each of the steps (:num:`Figure #fig-node-test-parallelism`) of the dot product calculation could be mapped into one internal pipeline stage. The number of stages needed for the dot product pipeline equals 1 for the multiplication step, plus :math:`\left \lceil ld(\NA)  \right \rceil` for |NA|-ary addition to be performed via binary addition operations. Furthermore, there is no additional overhead that could come from the need of pipeline flushing, since for this application of the DT accuracy calculation, the instances enter the pipeline in predefined order, one by one, until whole dataset is classified.

Node Test Evaluator - NTE
;;;;;;;;;;;;;;;;;;;;;;;;;

The block diagram in the :num:`Figure #fig-dt-test-eval-bd` shows the architecture of the |NTE| module. When the value received at the *Node ID Input* of an |NTE| contains a non-leaf node ID, it tells the |NTE| which node's test is to be evaluated among all the nodes at the DT level for which that that |NTE| module operates. The node test is performed on the dataset instance received at the *Instance Input* port together (at the same time) with the node ID. Each instance carries two types of information: the attribute vector |x| and the class to which it belongs. The instance and the selected node together make a pair of objects that all procedures in the |NTE| module operate on, and they will be called the current instance and the current node. Please notice that due to the pipelining, different stages of the |NTE| operate in fact on different current nodes and instances. The |NTE| expects the ID of a non-leaf node to equal its index in the list of all non-leaf nodes at the DT level for which the |NTE| operates. Hence, the non-leaf node IDs are local to, i.e. only unique within, the DT level they are at, and the node numbering restarts from 0 for each DT level. On the other hand, the leaf IDs need to be global, i.e. unique accross the whole DT, since they will be used to identify which leaf was the instance classified in.

On the other hand, when the value received at the *Node ID Input* of an |NTE| contains a leaf node ID, this signals the |NTE| that the corresponding instance has already been classified, hence the dot product calculation is not performed (more precisely, in order to simplify the design it is still performed, but the results are discarded). The received node ID value is simply output verbatim via the "Node ID Output" port along with the corresponding dataset instance.

.. _fig-dt-test-eval-bd:

.. bdp:: images/nte.py

    The NTE (Node Test Evaluator) block architecture

The Classifier hence performs the following:

1. The test coefficient vector |w| of the current node is fetched from the CM part of the DT Memory Array sub-module via the *Coefficient Memory Interface*. The current node's ID is used as index to calculate the address of the node's coefficient vector in the CM memory, which is communicated via the *CM addr* port. If the current node is a leaf, the fetch is not performed and all zeros are loaded for the vector |w|, but the results of the dot product are discarded anyway in this case.
2. The dot product between the fetced coefficient vector |w| and the attribute vector |x| of the current instance, is calculated in several steps discussed in the :num:`Section #sec-dot-product-parallelism`. First the multiplication step is performed in parallel, and then the products are summed using the adder tree.
3. The current node's test threshold (|th|) and the IDs of the current node's both children (|ChL| - the ID of the left child and |ChR| - the ID of the right child) are retrieved from the SM part of the DT Memory Array sub-module, again using the current node ID as an index to calculate the address where this information is stored in the SM memory. Again, if the current node is a leaf, the fetch is not performed and all zeros are loaded for |th|, |ChR| and |ChL|.
4. Finally, the decision on where to proceed with the DT traversal is made. If the current node is a non-leaf node, the MSB of its ID will have value 0, which will make the *MUX2* block forward the output of the *MUX1* to the *Node ID Output* port of the |NTE|. The output of the *MUX1* will in turn depend on the result of the comparison between the dot product value and the value of |th|, and either |ChL| or |ChR| will be sent to the *Node ID Output*. On the other hand, if the current node is a leaf (meaning that the current instance has already been classified), the MSB of its ID will have value 1, which will make the *MUX2* block forward the current node's ID to the *Node ID Output*. Whichever the case may be, a node ID will be output via *Node ID Output* port along with the current instance via *Instance Output* port, and they will become the current node and the current instance for the next |NTE| in the chain.

The main parameter that needs to be specified by the user during the design phase of the |cop| is the maximum supported number of attributes per instance - |NAM|, i.e. the maximum supported sizes of the vectors |w| and |x|. This parameter affects the size and latency of the |NTE| module as it will be explained in the text that follows.

The |NTE| module's main task is the dot product calculation of the vectors |w| and |x|. By using only two input multipliers and adders, this computation is parallelized and pipelined as much as possible as discussed in the :num:`Section #the-dot-product-parallelism`. The multiplications are all performed in parallel, for all |NAM| coefficient and attribute pairs. Since usually two input adders are used in hardware design, but the |NAM|-ary sum is needed, the tree of two input adders that is :math:`\left \lceil ld(\NAM)  \right \rceil` deep, is necessary to implement the summing operation. In order to acheive higher operating frequency of the implemented |cop| co-processor, the dot product calculation datapath is broken into stages, with one stage per calculation step. Each step comprises multiplication or addition operations that can be performed in parallel. Finally, the outputs of each of the adder and multiplier blocks are registered to form the pipeline.

Second important parameter besides |NAM|, that needs to be specified by the user during the design phase of the |cop| is |RA| - the number of bits used for the signed fixed point representation of the elements of the vectors |w| and |x|. Hence, the elements of |w| and |x| are considered to be in the Q0.(:math:`R_A-1`) format. For an example, if 16 bits are used for the representation of the vector elements, they are considered to be in Q0.15 format. After the multiplication stage, the products will thus be in the Q0.(:math:`2R_A-2`) signed fixed point format. The value of the sum output by each adder is larger by 1 bit than the value of its operands, hence the registers increase in size by 1 integer bit per pipeline stage. After the final addition, the sum representation will have reached the size of: :math:`2R_A-1+\NPADD` bits in the Q(|NPADD|).(:math:`2R_A-2`) format. Finally, the value of the finall sum, which is compared to the threshold |th|, is truncated to the Q(|NPADD|).(:math:`R_A-1-\NPADD`) format in order to return to the operands of |RA| bits in size. Consequently, the |NTE| expects the value of |th| to be supplied encoded in the Q(|NPADD|).(:math:`R_A-1-\NPADD`) format. The |NTE| module also supports datasets with less than |NAM| number of instance attributes, :math:`\NA < \NAM`. In this case, the surpluss coefficients :math:`w_{\NA+1}, w_{\NA+2}, ... w_{\NAM}` should be all set to zero, in order not to affect the calculation of the sum.

The necessary number of bits used to encode the non-leaf node and leaf IDs - |RN|, can be calculated based on the parameter |DM|. Since the non-leaf node IDs are unique only accross one DT level, of which the last level can have the largest number of nodes, and the |DM| parameter limits the number of levels the induced DT can have, there is a maximum of :math:`2^{D^M-1}` different non-leaf node IDs to be encoded for the selected value of the parameter |DM|. On the other hand, the leaf IDs need to be globaly unique, hence there needs to be one ID available for each leaf in the DT. The possible number of leaves is also related to the parameter |DM|, and equals :math:`2^{D^M}`. Additionaly, the MSB of the ID representation is reserved for differentiating between the leaf and non-leaf node IDs, which finally means that the total number of bits for encoding IDs should be :math:`R_N \ge D^M+1`.

The :num:`Figure #fig-dt-test-eval-bd` shows the |NTE| module partitioned in |NP| pipeline stages by the vertical dotted lines, with each part labeled by the stage ID: Stage 1, Stage 2, ... Stage |NP|. The total number of pipeline stages needed (|NP|), equals the depth of the adder tree, plus the multiplication stage and the decision stage in the end where node test results are intepreted:

.. math:: N_{P}=\NPADD + 2
	:label: np

Prior to the Stage 1 of the |NTE|, the coefficients of the vector |w| are fetched from the *CM* memory, which seems like it requires a separate pipeline stage. However, this step was merged with the Stage :math:`N_P` of the previous |NTE| to be performed together in a single clock cycle. This implementation choice saved both one clock cycle per |NTE| on the |cop| co-processor latency, and on additional registers that would be needed were the decision step of one |NTE| and the vector |w| fetch step of the next implemented in two separate pipeline stages.

The Instance Queue and the Node Queue delay lines are necessary due to the pipelining. Each |NTE| performs calculations only for a single DT level, hence once the calculations is finished the instance needs to be transferred to the next |NTE| module in the Classifier chain. This transfer needs to correlate in time with the output of the node test evaluation results via the *Node ID output* port. Hence, the Instance Queue has to have the length equal to |NP|, since it needs to delay the output of the instance to the next |NTE| module for |NP| clock cycles.

The Node Queue is necessary for preserving the current node's ID (the signal *Node ID* in the :num:`Figure #fig-dt-test-eval-bd`). If the current node is a non-leaf node, in the pipeline Stage :math:`N_P-1`, this ID will be used to calculate the address of the node's structural description in the SM part of the DT Memory Array sub-module, comprising three values: the ID of the left child - |ChL|, the ID of the right child - |ChR| and the node test threshold value - |th|. These values are needed in the last pipeline stage, where a decision on how to continue the traversal will be made. On the other hand if the current node is a leaf, its ID is be needed in the last pipeline stage since it should be output via *Node ID Output* to the next |NTE| in the chain.

The operations in each pipeline stage depend only on the output of the previous stage, i.e. there are no loops in the design. This allows for each pipeline stage to start processing the next dataset instance immediatelly after it has finished with the current intance. The indices of the instances and nodes inside the *Instance Queue* and *Node Queue* reflect this feature. While Stage :math:`N_P` processes the instance :math:`I_i` in the node :math:`N_i`, the Stage :math:`N_P-1` can process in parallel the next instance in the dataset, namely :math:`I_{i+1}` in the node :math:`N_{i+1}`. Hence, the total of :math:`N_P` instances are processed in different pipeline stages by a single |NTE| in parallel.

The Classifier operation example
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

Lets use the DT from the :num:`Figure #fig-efti-overview-dot07`, whose induction from the ``vene`` dataset by the |algo| algorithm was discussed in the :num:`Section #sec-algorithm-overview`. First, the parameters compatible with the ``vene`` dataset need to be selected for the Classifier module. The ``vene`` training set instances are described using two attributes, :math:`N_A=2`, hence the minimum value that can be chosen for |NAM| is :math:`\NAM=N_A=2`. For the sake of simplicity, in this example, |NAM| will be set to this minimum value of 2. The value of |RA| can be chosen freely based on the accuracy that needs to be acheived during the dot product calculation, and here it will be set to 16, which should provide the high enough precision to obtain the highest possible classification results. The example DT is 3 levels deep, hence the |DM| parameter needs to be set to at least that value. Even though the Classifier would provide correct results even if it contained more levels than that, for the sake of simplicity |DM| will be set 3. Also, even though it would suffice to select :math:`R_N=D^M + 1=4`, |RN| will be set to 8 to gain on the readability of the leaf IDs. Based on these selections the other parameters can be calculated: |NPADD| = 1, |NP| = 3, |w| and |x| elements format is Q0.15, and |th| format is Q1.14. The list of all relevant parameters for the Classifier module is given in the :num:`Table #tbl-classifier-operation-example-params`.

.. tabularcolumns:: C{0.09\linewidth} C{0.09\linewidth} C{0.09\linewidth} C{0.09\linewidth} C{0.14\linewidth} C{0.1\linewidth} C{0.12\linewidth} C{0.12\linewidth}

.. _tbl-classifier-operation-example-params:

.. list-table:: The parameter set for configuring the |cop| co-processor compatible with the ``vene`` dataset.
    :header-rows: 1

    * - |DM|
      - |NAM|
      - |RA|
      - :math:`R_N`
      - |NPADD|
      - :math:`N_P`
      - FP format |x|, |w|
      - FP format |th|
    * - 3
      - 2
      - 16
      - 8
      - 1
      - 3
      - Q0.15
      - Q1.14


.. _fig-nte-example-dt:

.. bdp:: images/nte_example_dt.py
    :width: 100%

    The example DT used to discuss the |NTE| operation. |th| and |w| are displayed for all nodes, first in decimal format and then in the fixed point representation immediately below.

.. _fig-nte-example-attrspace:

.. plot:: images/nte_example_attrspace_plot.py
    :width: 60%

    The ``vene`` dataset with the marked instance that will be used for the Classifier module operation demonstration. The attribute space regions are titled by the leaf IDs they are associated to.

The :num:`Figure #fig-nte-example-dt` shows the induced DT with the values of |th| and |w| displayed for all nodes, first in decimal format and then in the fixed point representation immediately below. Next, it will be shown how the Classifier module calculates the classification results of the example DT on a single instance. For this example an instance marked in the :num:`Figure #fig-nte-example-attrspace` will be classified. The instance belongs to the class :math:`C_2` and has the attribute vector :math:`\mathbf{x}=[0.5929, 0.6425]`, which encoded to Q0.15 becomes :math:`\mathbf{x}=[\mathtt{4BE4},\mathtt{523D}]`. As the :num:`Figure #fig-dt-classifier-bd` shows, the instance is first input to the :math:`\textrm{NTE}_1` module's *Instance Input* port. Please notice that the information about the class to which the instance belongs is not used by the Classifier module, and will be used only once the instance is classified and the results are transmitted to the Accuracy Calculator module. The value of the *Node ID Input* on the :math:`\textrm{NTE}_1` module is fixed to 0, i.e. the node with ID 0 is always selected since the root node is the only possible choice for the first DT level.

.. _fig-classifier-example-nte1-pre:

.. bdp:: images/classifier_example_nte1_pre.py
    :width: 100%

    The preparation for the first pipeline stage, where the loading of the coefficient vector for the selected node from the CM memory is performed. All the blocks and the signal paths active in this phase are highlighted in blue.

Before the first pipeline stage, |w| needs to be loaded from memory for the selected node. The read from the CM memory is performed asynchronously and the coefficients are lead to their corresponding registers in order to be used in the first pipeline stage that performs the multiplication operation. The vector |x| is led to the Instance Queue, and the current node ID is led to the Node Queue.  All blocks and signal paths active in this phase are highlighted in blue in the figure :num:`Figure #fig-classifier-example-nte1-pre`.

Next, in the first pipline stage the elementwise multiplication between vectors |w| and |x| is performed as shown in the :num:`Figure #fig-classifier-example-nte1-stage1` with all active parts highlighted in blue. The current instance and the current node ID are now stored in the first elements of the Instance and Node queues respectively. The vector |w| and |x| element values are shown in the figure, as well as the multiplication results which are in Q0.30 fixed point format as it was already described. Please notice, that |NTE| preforms signed additions and multiplications, hence the sign extension is needed for all operands, but this is not shown in the figures. Hence, in order to obtain the correct result for the :math:`w_2 \cdot x_2` multiplication, the coefficient :math:`w_2` which is negative first needs to be sign extended to Q0.30 format: :math:`w_2 = \mathtt{7FFF81D1}`, and then only lower 31 bits from the product are kept, while discarding the upper bits which arised from multiplying with the sign extension:

.. math::  w_2 \cdot x_2 = \mathtt{7FFF81D1} \cdot \mathtt{0000523D} = \mathtt{523CD776E0CD} \xrightarrow[]{Q0.30} \mathtt{5776E0CD}
   :label: eq-sign-ext-mul

.. _fig-classifier-example-nte1-stage1:

.. bdp:: images/classifier_example_nte1_stage1.py
    :width: 100%

    The first pipeline stage, where the elementwise multiplication between vectors |w| and |x| is performed. All the active parts are highlighted in blue in the figure.

Then in the pipeline Stage 2 (:num:`Figure #fig-classifier-example-nte1-stage2`), the addition of the elementwise products is performed. Since the Classifier module was configured to support only two instance attributes via the |NAM| attribute, the addition can be performed within single pipeline stage. If a higher value were selected for the |NAM| parameter, multiple stages would be needed in order to calculate the dot product sum. The current instance and the current node ID are now stored in the second element of the Instance and Node queues respectively. The vector elementwise products are shown in the figure, as well as the addition result, that is also the dot product result, which is in Q1.30 fixed point format. Again, the negative element :math:`w_2 \cdot x_2` needs to be sign extended to the format of the result :math:`w_2 \cdot x_2 = \mathtt{D776E0CD}` and then the addition can be performed:

.. math::  w_1 \cdot x_1 + w_2 \cdot x_2 = \mathtt{16E00768} + \mathtt{D776E0CD} = \mathtt{EE56E835} \xrightarrow[]{Q1.15} \mathtt{EE56}
   :label: eq-sign-ext-add

The dot product sum is finally converted to the format of |th|, which is Q1.15 in this example, by truncating the lower bits. Additionally, the information needed for the final decision on where the traversal will continue is fetched from the SM memory and prepared for the last pipeline stage. The fetched values for |th|, |ChL| and |ChR| for this example are shown in the figure.

.. _fig-classifier-example-nte1-stage2:

.. bdp:: images/classifier_example_nte1_stage2.py
    :width: 100%

    The second pipeline stage, where the final evaluation of the node test is performed and the decision on where the traversal will continue is made. All the blocks and the signal paths active in this stage are marked in the figure.

Finally in the pipeline Stage 3, the dot product calculation results are compared to the value of |th|, to obtain the node test result, which in this case :math:`\mathtt{EE56} \leq \mathtt{FA20}` evaluated to ``true`` (these are both negative values in Q1.14 and the comparator block performs the signed comparison). Based on the comparison result, the MUX1 block forwards the ID of the left child :math:`ChL=0` to its output, which is then passed to the port 0 of the MUX2 block. Since the current node in not a leaf (the current instance is yet to be classified), the *Node ID* MSB has a value 0, which selects the value from the MUX2 port 0 to be forwarded by the MUX2 block to its output, which is in turn lead to the *Node ID Output* port. Hence, the result of the :math:`NTE_1` operation in this example is that the :math:`ChL=0` value is output via *Node ID Output* port, and the DT traversal for this instance will continue via node with ID 0 on the second DT level, which will in turn be performed by the :math:`NTE_2` module.

.. _fig-classifier-example-nte1-stage3:

.. bdp:: images/classifier_example_nte1_stage3.py
    :width: 100%

    The third pipeline stage, where the addition of the elementwise products is performed. All the blocks and the signal paths active in this stage are highlighted in blue.

The outputs *Instance Output* = :math:`[\mathtt{4BE4},\mathtt{523D}], C=2` and *Node ID Output* = 0, as shown in the :num:`Figure #fig-classifier-example-nte1-stage3`, are then passed to the :math:`NTE_2` module where the traversal of the instance continues. The :math:`NTE_2` module performs in the exact same 3 stages as the :math:`NTE_1` module did, but on a different DT node. The :num:`Figure #fig-classifier-example-nte2` combines the results of the computations from all 3 :math:`NTE_2` stages in one image, which in fact occure in successive cycles. This time, the value passed from the previous |NTE| (the value 0 in this example), is used to select the node for the test evaluation, among the two possible nodes on the DT level 2. As it is shown in the figure, the test evaluates to ``false``, and hence the traversal is to be continued via the right child. In this case, the right child is a leaf with the ID :math:`\mathtt{80}`, and the instance's classification is thus determined.

Notice however, how similar the dot product sum :math:`\mathtt{16AA}` is to the |th| value :math:`\mathtt{14DF}`. This is due to the proximity of the instance to the hyperplane separating region :math:`\mathtt{80}` and regions :math:`\mathtt{83}` and :math:`\mathtt{84}` in the attribute space. If the instance were positioned exactly on the hyperplane, these two values would be identical. Anyway, the instance is passed to the next (and also the last) |NTE| module, which will recognize that no further computation is needed for the instance, and simply pass the results to the Classifier output. The :num:`Figure #fig-classifier-example-nte3` shows the relevant computation results from all 3 stages of :math:`NTE_3` module in one image. Basically, the results of the dot product calculations are disregarded (and omitted from the figure for this reason), and the MUX2 component of the |NTE| module recognizes that it has received a leaf ID on its *Node ID Input* port (node ID's MSB value is 1), and simply outputs the same leaf ID value for the instance to the *Node ID Output* port. Since the :math:`NTE_3` is the last |NTE| module in the Classifier chain, its *Node ID Output* port is at the same time the output of the whole Classifier module.

The Classifier thus calculated that the instance :math:`[\mathtt{4BE4},\mathtt{523D}]` finishes its traversal of the DT from the :num:`Figure #fig-nte-example-dt` in the leaf with the ID :literal:`80`. From the attribute space partition induced by the DT shown in the :num:`Figure #fig-nte-example-attrspace`, it can be seen that the classification is indeed correct.

.. _fig-classifier-example-nte2:

.. bdp:: images/classifier_example_nte2.py
    :width: 100%

    The results of the node test evaluation on the second DT level by the :math:`NTE_2` module.

.. _fig-classifier-example-nte3:

.. bdp:: images/classifier_example_nte3.py
    :width: 100%

    The results of the node test evaluation on the third DT level by the :math:`NTE_3` module.

However, the Classifier module operates on multiple instances of the dataset in parallel using the pipelining technique. The :num:`Figure #fig-pipeline-demo` shows this process by displaying only the contents of the Instance and Node queues, which is enough to represent which instance is being processed by which stage of which |NTE|. Each pipeline stage is represented by a pair of Instance and Node queue elements which are displayed directly above one another in the figure. The Instance Queue element of the pair shows the attribute vector and the class assigned to the instance it contains, while the Node Queue element shows the current ID of the node this instance is at.

At the beginning, the queues are empty and the first instance :math:`I_0` is received from the Training Set Memory as shown in the :num:`Figure #fig-pipeline-demo1`. The node test evaluation computation is carried out in the :math:`NTE_1` module stage by stage, and in three clock cycles the :math:`I_0` instance is transfered to the :math:`NTE_2` module, as shown in the :num:`Figure #fig-pipeline-demo2`. There, its traversal is continued via the node with ID 0 on the DT level 1 (:num:`Figure #fig-nte-example-dt`). By this time, three more instances have been loaded from the Training Set Memory, and are in the process of the node test evaluation in three stages of the :math:`NTE_1` module. Since they all need to start from the root node, their selected node IDs are all 0. Finally, the :num:`Figure #fig-pipeline-demo3` shows the moment in the classification where the first instance of the dataset :math:`I_0` has reached the end of the pipeline and is outputted to the Accuracy Calculator module, along with its classification into the leaf node with the ID :math:`\mathtt{83}`.

.. subfigstart::

.. _fig-pipeline-demo1:

.. bdp:: images/pipeline_demo1.py
    :width: 100%
    :align: center

    State after the 1st clock cycle

.. _fig-pipeline-demo2:

.. bdp:: images/pipeline_demo2.py
    :width: 100%
    :align: center

    State after the 4th clock cycle

.. _fig-pipeline-demo3:

.. bdp:: images/pipeline_demo3.py
    :width: 100%
    :align: center

    State after the 10th clock cycle

.. subfigend::
    :width: 0.99
    :label: fig-pipeline-demo

    The process of pipelined operation of the Classifier module with only the contents of the Instance and Node queues displayed, which in thurn represent which instance is being processed by which stage of which |NTE|.

.. _sec-cop-training-set-memory:

Training Set Memory
...................

This is the memory that holds all the training set instances that should be processed by the |cop| co-processor. It is a two-port memory with ports of different widths and is shown in the :num:`Figure #fig-inst-mem-org`. It is comprised of the 32-bit wide stripes, in order to be accessed by the host CPU via the 32-bit AXI interface. Each instance description, spanning multiple stripes, comprises the following fields:

- Array of instance attribute values: :math:`x_{i,1}` to :math:`x_{i,\NAM}`, each :math:`R_A` bits wide (parameter specified by the user at design time),
- Instance class: :math:`C_{i}`, which is :math:`R_C` bits wide (parameter specified by the user at design time)

The training set memory can be accessed via two ports:

- **User Port** - Read/Write port accessed by the CPU via the AXI interface, 32-bit wide.
- **NTE Port** - Read port for the parallel read-out of the whole instance, :math:`R_{A}\cdot\NAM + R_{C}` bits wide.

The width of the NTE Port is determined at the design phase of the |cop|, and corresponds to the maximal size of the instance, i.e. the instance with the |NAM| number of attributes, that can be processed. When the co-processor is used for solving a problem with less attributes, the Training Set Memory fields of unused attributes need to be filled with zeros in order to obtain the correct calculation.

.. _fig-inst-mem-org:

.. bdp:: images/inst_mem.py
    :width: 80%

    The Training set memory organization

The instance attributes are encoded using an arbitrary fixed point number format, specified by the user. However, the same number format has to be used for all instances' attribute encodings. The total maximum number of instances (|NIM|), i.e. the size of the Training Set Memory, is selected by the user at the design phase of the |cop|, and determines the maximum possible training set size that can be stored inside the |cop| co-processor.

.. _sec-cop-dt-memory-array:

DT Memory Array
...............

DT Memory Array is composed of |DM| sub-modules used for storing the DT description, including the structural information and the coefficient values for every node test of the DT. Each sub-module of the DT Memory Array is a three-port memory with ports of different widths (as shown in the :num:`Figure #fig-dt-mem-array-org`) and is comprised of 32-bit wide stripes in order to be accessed by the host CPU via the 32-bit AXI interface.

.. _fig-dt-mem-array-org:

.. bdp:: images/dt_mem.py

    The DT memory organization

Each DT Memory Array sub-module contains a list of node descriptions as shown in the :num:`Figure #fig-dt-mem-array-org`, and has two parts. The CM part of the memory comprises the array of the node test coefficients: :math:`w_{i,1}` to :math:`w_{i,\NAM}`, each :math:`R_A` bits wide. The SM part of the memory contains the following fields:

- The node test threshold: :math:`\theta_{i}`, which is :math:`R_A` bits wide
- The ID of the left child: :math:`ChL_{i}`, which is |RN| bits wide
- The ID of the right child: :math:`ChR_{i}`, which is |RN| bits wide

An array of parameters, :math:`N^{M}_{n}(l), l \in (1, D^M)`, that can be specified by the user at the design stage, is used to control the size of the individual DT Memory Array sub-modules. These parameters impose a constraint on the maximum number of nodes that the induced DT can have on each level. The size of each DT Memory Array sub-module is configured separately, since the first DT level can only have one node (which is the root node). At the worst case, possible number of nodes per DT level increases exponentially with the depth of the DT level. However, in practice, the induced DTs are never full binary trees, hence the increase of the sub-modules' size with the corresponding DT level depth saturates quickly. To make the addressing of the DT Memory Array sub-modules of different size easier, every sub-module is given the address space of an identical size and it is up to the user to take care of how many DT node descriptions are actually available in each sub-module.

Since the fields :math:`ChL_{i}` and :math:`ChR_{i}` can either contain a leaf or a non-leaf ID, and the ID's MSB is used to discern the ID type, with their width of |RN|, they can encode :math:`2^{R_N - 1}` IDs. The value of the parameter |RN| is calculated at the design time so that the fields :math:`ChL_{i}` and :math:`ChR_{i}` can encode both the the maximum number of nodes per any DT level and the maximum number of leaves the induced DT can have, i.e.:

.. math:: R_N = 1 + \left \lceil ld(max(N^{M}_{n}(1), ..., N^{M}_{n}(D^M), N^{M}_{l})) \right \rceil
	:label: r_node_id_constraint

DT Memory Array sub-module can be accessed via three ports:

- **User Port** - The read/write port, accessed by the CPU via the AXI interface, 32-bit wide.
- **CM Port** - The read port for the parallel read-out of all node test coefficients for the addressed node, :math:`R_{A}\cdot\NAM` bit wide.
- **SM Port** - The read port for the parallel read-out of the node structural information for the addressed node, :math:`R_{A} + 2\cdot R_N` bit wide.

.. _sec-cop-accuracy-calc:

Accuracy Calculator
...................

This module calculates the accuracy of the DT by forming the distribution matrix as described by the :num:`Algorithm #fig-accuracy-calc-pca`. It monitors the classifications outputted by the Classifier for each instance in the training set, and based on its class (*C*) and the leaf in which it finished the traversal (*Leaf ID*), the appropriate element of the distribution matrix is incremented. The Accuracy Calculator block is shown in the :num:`Figure #fig-fit-calc-bd`.

.. _fig-fit-calc-bd:

.. bdp:: images/fitness_calc_bd.py
    :width: 85%

    The Accuracy Calculator block diagram

In order to speed up the dominant class calculation (second loop of the ``accuracy_calc()`` function in the :num:`Algorithm #fig-accuracy-calc-pca`), the Accuracy Calculator is implemented as an array of calculators, called Leaf Dominant Class Calculator - |LDCC|, whose each element keeps track of the distribution for the single leaf node. Hence, the dominant class calculation for a leaf (the ``dominant_class`` and the ``dominant_class_cnt`` variables from the :num:`Algorithm #fig-accuracy-calc-pca`) and counting the total number of instances that finished the traversal in the leaf, can be performed in parallel for each leaf node. In other words, each |LDCC| is responsible for maintaining one row of the distribution matrix from the :num:`Figure #fig-distribution-matrix`. The parameter |NlM|, which can be specified by the user during the design phase of the |cop| co-processor, determines the number of |LDCC| blocks available in the Accuracy Calculator module, and hence imposes a constraint on the maximum number of leaves in the induced DT. Each calculator comprises:

- **Class Distribution Memory** - For keeping track of the class distribution of the corresponding leaf node.
- **Incrementer** - Updates the memory based on the Classifier output.
- **Dominant Class Calculator** - Finds and outputs the following values: the dominant class for the leaf and the number of instances of the dominant class that were classified in the leaf, using the signals :math:`dominant\_class_{i}` and :math:`dominant\_class\_cnt_{i}` respectively, where :math:`i \in (1, N^{M}_{l})`, as shown in the :num:`Figure #fig-fit-calc-bd`.

For the leaf it is responsible for, each |LDCC| keeps track of how many instances of each of the training set classes were classified in the leaf. The parameter |NCM|, also specified by the user at the |cop| design time of the, determines the width of the Class Distribution Memory and hence the maximum number of classes of the training set the |cop| co-processor supports. It then finds a class that has the largest number of instances in the leaf (the dominant class corresponding to the ``dominant_class`` variable in :num:`Algorithm #fig-accuracy-calc-pca`), and outputs its ID via the *dominant_class* port. If the instance's class equals the dominant class of the leaf node it finished the traversal in, it is considered a hit, otherwise it is considered a miss. Hence, the value output to the *dominant_class_cnt* port represents the number of classification hits for the corresponding leaf node and corresponds to the ``dominant_class_cnt`` variable in :num:`Algorithm #fig-accuracy-calc-pca`. The total number of instances classified in the leaf is output via ``hits`` port.

When the classification of the training set is finished, the Accuracy Provider block performs the following:

- It sums the classification hits for all leaf nodes and outputs the sum as the number of hits for the whole DT (the *hits* port), which is then stored in the Classification Performance Register of the Control Unit.
- Gathers the information about dominant classes for each of the leaves and outputs this value via *dt_classes* port for storing it in Classes Register in Control Unit.

The Accuracy Calculator operation example
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

.. subfigstart::

.. _fig-acc-calc-demo1:

.. bdp:: images/acc_calc_demo1.py
    :width: 100%
    :align: center

    First instance :math:`I_0` of the training set arrives

.. _fig-acc-calc-demo2:

.. bdp:: images/acc_calc_demo2.py
    :width: 100%
    :align: center

    Instances continue to arrive and the matrix gets populated

.. _fig-acc-calc-demo3:

.. bdp:: images/acc_calc_demo3.py
    :width: 100%
    :align: center

    Distribution matrix almost complete, with only two instances left

.. _fig-acc-calc-demo4:

.. bdp:: images/acc_calc_demo4.py
    :width: 100%
    :align: center

    Distribution matrix complete, final results output

.. subfigend::
    :width: 0.49
    :label: fig-acc-calc-demo

    Demonstration of the Accuracy Calculator operation for the ``vene`` dataset classified by the DT from the :num:`Figure #fig-nte-example-dt`

In this subsection a demonstration of the Accuracy Calculator operation is given for the ``vene`` dataset classified by the DT from the :num:`Figure #fig-nte-example-dt`, and is depicted in the :num:`Figure #fig-acc-calc-demo`. The classification output from the Classifier module arrives each clock cycle for a different training set instance and is comprised from the leaf ID and the instance class pairs, as shown in the :num:`Figure #fig-acc-calc-demo` in the Classifier Output queue. The Accuracy Calculator is shown comprising the |LDCC| array of which only five active |LDCC| modules are shown, each responsible for one of the DT leaves :literal:`80` - :literal:`84`. The remaining :math:`N^{M}_{l} - 5` |LDCC| modules are inactive in this example, since there only five leaves in the DT. Each |LDCC| is shown comprising the Class Distribution Memory consisting of three elements, one for each of the classes (:math:`C_1`, :math:`C_2` and :math:`C_3`) occuring in the ``vene`` training set, while the remaining :math:`C^{M} - 3` elements are inactive and not shown in the figure. Together all |LDCC| modules with their Class Distribution Memories form the distribution matrix.

Based on the ID of the leaf the instance was classified into, the appropriate |LDCC| is activated. It then uses the instance class information to increment the corresponding item in the distribution matrix row it is responsible for. In the :num:`Figure #fig-acc-calc-demo1`, the first instance in the training set :math:`I_0` is shown arriving from the classifier module, prior to which the distribution matrix was empty. :math:`I_0` was classified into the leaf with the ID :literal:`83` for which the :math:`LDCC_3` module is responsible, and it belongs to the class :math:`C_1`, represented by the first column in the distribution matrix. Hence, the :math:`LDCC_3` module increments the first element of its class distribution row as shown in the figure. In the :num:`Figure #fig-acc-calc-demo2`, the instance :math:`I_2` of the class :math:`C_3`, which was classifed into the leaf :literal:`81`, acctivated :math:`LDCC_3` module to incement the item corresponding to the class :math:`C_3`.

The :num:`Figure #fig-acc-calc-demo3` displays the moment when the last two instances from the training set arrive, and the distribution matrix is almost complete. Finally, in the :num:`Figure #fig-acc-calc-demo4`, the complete distribution matrix is shown and its items corresponding to the dominant classes are highlighted in blue. The Accuracy Provider module then gathers the information from all |LDCC| modules about the dominant classes and combines them to get the total number of ``hits`` and the array of dominant classes that are sent to the Control Unit.

.. _sec-cop-control-unit:

Control Unit
............

Control Unit provides the AXI4 interface access to the configuration and the status registers, as well as to the DT Memory Array and the Training Set Memory by providing a unified memory space. Furthermore it generates an IRQ signal when the accuracy calculation is finished. The following registers are provided:

- **Operation Control** - Allows the user to start, stop and reset the |cop| co-processor.
- **Traning Set Configuration** - Allows the user to specify the relevant properties of the training set currently used: |NI| - the number of instances and |NC| the number of classes in the training set.
- **Classification Performance Register** - Informs the user when the accuracy evaluation task is done, and enables the user to read the calculated number of the classification hits.
- **Classes Registers** - Stores the dominant classes associated to each of the DT leaves, received form the Accuracy Calculator's *dt_classes* port.

.. _fig-efti-fsm:

.. bdp:: images/efti_fsm.py
    :width: 40%

    The Control Unit FSM that manages the whole accuracy calculation process of the |cop|  co-processor

The accuracy calculation process is performed automatically under the management of the Control Unit and is depicted by the diagram in the :num:`Figure #fig-efti-fsm`. The |cop| co-processor remains in the Idle state until the start signal is given via the Operation Control register. By that moment, both the Training Set Memory and the DT Memory Array should have been loaded with the training set instances and the desired DT description for the |cop| co-processor to use. The Control Unit then moves to the Enqueue state and starts issuing a sequence of read commands, one per clock cycle, to the Training Set Memory in order to retreive the intances of the training set and forward them to the Classifier module. This process is continued until all the instances have been read out of the Training Set Memory, when the Control Unit moves to the Flush state. In this state, the Control Unit waits for the Classifier to finish the classification of the last training set instance, after which the Accuracy Calculator is instructed to perform the dominant class calculation and the Control Unit enters the Calculate Accuracy state. After the Accuracy Calculator finished populating the Classification Performance Register and the Classes Register, the Control Unit returns to the Idle state once again, ready for the new accuracy calculation cycle.

Required Hardware Resources and Performance
-------------------------------------------

The |cop| co-processor is implemented as an IP core with many customization parameters discussed in the previous chapters that can be configured at the design phase. These parameters, listed in the :num:`Table #tbl-cop-params`, mainly impose constraints on the maximum size of the DT that can be induced, and the maximum size of the training set that can be used.

.. tabularcolumns:: c p{0.45\linewidth} p{0.4\linewidth}

.. _tbl-cop-params:

.. list-table:: The customization parameters that can be configured at the design phase of the |cop| co-processor
    :header-rows: 1
    :widths: 15 30 30

    * - Name
      - Description
      - Constraint
    * - |DM|
      - The number of NTEs in the Classifier
      - The maximum depth of the induced DT
    * - |NAM|
      - Determines: Training Set Memory width, :raw:`\newline`
        DT Memory Array sub-module width, :raw:`\newline`
        NTE adder tree size.
      - The maximum number of attributes training set can have
    * - |RA|
      - Determines: Training Set Memory width, :raw:`\newline`
        DT Memory Array sub-module width, :raw:`\newline`
        NTE adder tree size.
      - Resolution of induced DT coefficients
    * - |NCM|
      - Accuracy Calculator memory depth
      - The maximum number of training set and induced DT classes
    * - :math:`R_C`
      - Parameter must be at least :math:`log_{2}(N^M_C)`
      - --
    * - |NlM|
      - Number of Accuracy Calculator Elements
      - The maximum number of leaves of the induced DT
    * - |NIM|
      - Training Set Memory depth
      - The number of training set instances that can be stored in the |cop| co-processor
    * - |NnM_l|
      - DT Memory Array sub-modules' depths
      - The maximum number of nodes per level of the induced DT

The amount of hardware resources required to implement the |cop| co-processor is a function of the customization parameters given in the :num:`Table #tbl-cop-params` and is given in the :num:`Table #tbl-req-res`. Please note that :math:`R_{Node ID}` and |NP| parameter values cannot be selected independently, but are calculated based on parameters from the :num:`Table #tbl-cop-params`.

.. tabularcolumns:: p{0.2\linewidth} p{0.2\linewidth} p{0.5\linewidth}

.. _tbl-req-res:

.. list-table:: Required hardware resources for the |cop| architecture implementation
    :header-rows: 1

    * - Resource Type
      - Module
      - Quantity
    * - RAMs
      - Training Set Memory
      - :math:`\NIM\cdot (R_A*\NAM + R_C)`
    * - (total number of bits)
      - DT Memory Array
      - :math:`\sum_{i=l}^{D^M}(N^{M}_{n}(l)\cdot((R_A+1)*\NAM + 2*R_N))`
    * -
      - Accuracy Calculator
      - :math:`\NlM\cdot N^{M}_C\cdot \left \lceil log_{2}(N^{M}_{I})  \right \rceil`
    * -
      - NTE
      - :math:`\DM\cdot N_P\cdot (R_{A}\cdot\NAM + R_{C}) +` :raw:`\newline`
        :math:`\DM\cdot N_P\cdot R_N`
    * - Multipliers
      - NTE
      - :math:`\DM\cdot \NAM`
    * - Adders
      - NTE
      - :math:`\DM \left \lceil log_{2}(\NAM)  \right \rceil`
    * - Incrementers
      - Accuracy Calculator
      - :math:`\NlM`

Second, the number of clock cycles required to determine the DT accuracy will be discussed. The Classifier has a throughput of one instance per clock cycle, hence all instances are classified in :math:`N_I` cycles. However, there is an initial latency equal to the total length of the pipeline :math:`\DM\cdot N_{P}`. Furthermore, the Accuracy Calculator needs extra time after the classification has finished, in order to determine the dominant class which is equal to the total number of classes in the training set :math:`N_{C}`, plus the time to sum all dominant class hits, which is equal to the number of active leaves :math:`N_{l}`. Finally, the time required to calculate the DT accuracy, expressed in clock cycles, for a given training set can be calculated as follows:

.. math:: accuracy\ evaluation\ time = (N_{I} + \DM\cdot N_{P} + N_{C} + N_{l}) \ clock\ cycles,
	:label: accuracy_evaluation_time

and is thus dependent on the training set size.

.. _sec-cop-sw:

Software for the |cop| assisted DT induction
--------------------------------------------

With the |cop| co-processor performing the DT accuracy evaluation task, remaining functionality of the |algo| algorithm (:num:`Algorithm #fig-algorithm-pca`) is implemented in software. Furthermore, the software needs to implement procedures for interfacing the |cop| co-processor as well. The changes to the main function of the |algo| algorithm can be seen in the adapted pseudo-code of the ``efti()`` function given in the :num:`Algorithm #fig-co-efti-pca`. For the pure software implementation, the reference to the training set is passed as an argument, and can be readily accessed for the accuracy calculation task since it resides in the memory directly accessible to the CPU. However the |cop| co-processor has its own memory, the Training Set Memory, for storing the training set instances that needs to be loaded prior. The |algo| algorithm performs many fitness evaluations on the same dataset during the DT induction, hence the ``hw_load_train_set()`` function, given by the pseudo-code in the :num:`Algorithm #fig-co-hw-load-train-set-pca`, is used to load the training set instances to the |cop| co-processor only once at the beggining of the algorithm. Once stored in the Training Set Memory, the information about the training set instances will be reused in every iteration of the algorithm.

.. _fig-co-efti-pca:

.. literalinclude:: code/co_algorithm.py
    :caption: The pseudo-code of the |algo| algorithm using the |cop| co-processor

.. _fig-co-hw-load-train-set-pca:

.. literalinclude:: code/hw_load_train_set.py
    :caption: The pseudo-code of the ``hw_load_train_set()`` function that performs the transfer of the training set to the |cop| co-processor

After the initial DT individual is created, it needs to be transfered to the |cop| co-processor in order for its accuracy to be determined, which is performed by the ``hw_load_dt()`` function given by the pseudo-code in the :num:`Algorithm #fig-co-hw-load-dt-pca`. This is the recusive function that loads both coefficient and structural information about the DT node and all of its descendents to the corresponding CM and SM memory parts of the DT Memory Array of the |cop| co-processor. First, the ``pack_dt_node()`` function, whose implementation was omitted for brevity, packs the node's coefficients and structural information, in a list of 32-bit values in a way that the organization of SM and CM DT memory parts dictates (:num:`Figure #fig-dt-mem-array-org`). As it can be seen from the pseudo-code, the packing depends on the floating point format (Qx.y) used for the coefficients (the argument ``fp_format``) and the width of the node and leaf ID representation |RN| (the argument ``Rn``). The packed information is then written to the |cop| co-processor memories 32-bit at a time, at desired locations whose addresses are calculated by helper functions ``eftip_dt_cm_addr()`` and ``eftip_dt_sm_addr()`` whose implemetation is again omitted.

.. _fig-co-hw-load-dt-pca:

.. literalinclude:: code/hw_load_dt.py
    :caption: The pseudo-code of the ``hw_load_dt()`` function that performs the transfer of the DT individual coefficients and structural data to the |cop| co-processor

With both training set and the DT loaded to the co-processor, the accuracy calculation function needs only to send the start signal (the ``hw_start()`` helper function) and wait for the results (the ``hw_get_hits()`` helper function), as it can be seen from the :num:`Algorithm #fig-co-accuracy-calc-pca`.

.. _fig-co-accuracy-calc-pca:

.. literalinclude:: code/co_accuracy_calc.py
    :caption: The pseudo-code of the ``accuracy_calc()`` function adapted to use the |cop| co-processor

In the end of the |algo| algorithm the induction procedure settles for the best DT individual (variable ``dt_best``). However, the information about the dominant classes of the DT leaves is not retreived from the |cop| co-processor during each iteration to save time on data transfer since this information is not critical for the |algo| algorithm operation. Nevertheless, the induced DT returned by the algorithm needs to have classes assigned to all of its leaves, which is performed by the ``hw_populate_classes()`` function given by the pseudo-code in the :num:`Algorithm #fig-co-hw-populate-classes-pca`. This function invokes one last accuracy calculation on the best DT individual, which will in turn also populate the Classes Register of the Control Unit with the dominant classes for all the DT leaves, which can then be read by the software, at the address calculated by the ``eftip_cu_cls_addr()`` helper function in the pseudo-code, and assigned to the DT data structure.

.. _fig-co-hw-populate-classes-pca:

.. literalinclude:: code/co_hw_populate_classes.py
    :caption: The pseudo-code of the ``hw_populate_classes()`` function adapted to use the |cop| co-processor

Experiments
-----------

In this section, the results of the experiments designed to estimate DT induction speedup of the HW/SW implementation of the |algo| algorithm using the |cop| co-processor over pure software implementation of the |algo| algorithm are given.

Required Hardware Resources for the |cop| Co-Processor Used in Experiments
..........................................................................

The customization parameters of the |cop| co-processor, whose descriptions are given in the :num:`Table #tbl-cop-params`, have been set for the experiments to support all training sets from the :num:`Table #tbl-uci-datasets`. The values of the customization parameters are given in the :num:`Table #tbl-exp-params`.

.. tabularcolumns:: p{0.5\linewidth} p{0.2\linewidth}

.. _tbl-exp-params:

.. list-table:: The values of customization parameters of the |cop| co-processor instance used in the DT induction speedup experiments
    :header-rows: 1

    * - Parameter
      - Value
    * - DT Max. depth (|DM|)
      - 13
    * - Max. attributes num. (|NAM|)
      - 64
    * - Attribute encoding resolution (:math:`R_{A}`)
      - 16
    * - Class encoding resolution (:math:`R_{C}`)
      - 8
    * - Max. training set classes (:math:`C^{M}`)
      - 64
    * - Max. number of leaves (|NlM|)
      - 256
    * - Max. number of training set instances (|NIM|)
      - 65536
    * - Max. number of nodes per level (|NnM_l|)
      - (1, 2, 4, 8, 16, 16, 16, 32, 32, 32, 64, 64, 64)

The |cop| co-processor has been modeled in the VHDL hardware description language and implemented using the Xilinx Vivado Design Suite 2014.4 software for logic synthesis and implementation, with the default synthesis and P&R options. From the implementation report files, the device utilization data has been analyzed and the information about the number of used slices, BRAMs and DSP blocks has been extracted, and is presented in the :num:`Table #tbl-utilization`. The maximum operating frequency of 133 MHz of the system clock frequency for the implemented |cop| co-processor was attained.

.. tabularcolumns:: l l l l

.. _tbl-utilization:

.. list-table:: FPGA resources required to implement the |cop| co-processor for the DT induction with selected UCI datasets
    :header-rows: 1

    * - FPGA Device
      - Slices
      - BRAMs
      - DSPs
    * - XC7Z020
      - 6813 (57%)
      - 65 (47%)
      - 192 (87%)
    * - XC7Z100
      - 6806 (10%)
      - 65 (9%)
      - 192 (10%)
    * - XC7K325
      - 7052 (14%)
      - 65 (15%)
      - 192 (23%)
    * - XC7VX690
      - 6949 (6%)
      - 65 (4%)
      - 192 (5%)

Given in the brackets, along with each resource utilization number, is the percentage of used resources from the total resources available on the corresponding FPGA devices. :num:`Table #tbl-utilization` shows that implemented |cop| co-processor fits even into the entry level XC7Z020 Xilinx FPGA device of the Zynq series, and requires even smaller percentage of resources on entry- to mid-level Kintex7 and Virtex7 Xilinx FPGA devices (XC7K325 and XC7VX690).

The scallability of the HW/SW solution can be observed from the point of several customization parameters of the |cop| co-processor given in the :num:`Table #tbl-cop-params`. The :num:`Table #tbl-req-res` shows how some of these customization parameters influence the utilization of the hardware resources.

The number of instances the |cop| co-processor can store in its Training Set Memory is limited by the parameter |NIM|, selected at the design phase of the the |cop|. In case that the datasets which cannot fit into the Training Set Memory need to be used, either a double buffering approach could be used or |cop| could be used in the streaming mode. In the streaming mode, the data would be continuously streamed from the host CPU memory using the DMA transfer. In this case, there would be no Training Set Memory, as the instances would be supplied to the Classifier from the outside via the DMA. In the double buffering approach, the Training Set Memory would be used as a ring buffer. While the |cop| is using the NTE port to read the instance descriptions to the Classifier, the User port would be used to load new instances to the Training Set Memory. The DMA transfer from the main memory would be used here as well. |cop| reads instances from the data set in predictable, sequential order, so it is easy to setup the DMA transfer and execute it without the intervention of the software during the transfer. This means that the full bandwidth of the main memory can be used for the data without any overhead.

If the |cop| co-processor were to support the datasets with larger number of attributes, which results in wider training set instance encodings, the training set transfer time could impact the HW/SW implementation performance. In this case, again, the double buffering or the |cop| in streaming mode could be used. The throughput of the |cop| co-processor, i.e. the widest possible training set instance encoding that could be used without degrading the performance, would then be limited only by the bandwidth of the main memory, since there is no overhead to the training set data streaming. If the bandwidth of one main memory module is not enough, the |cop| could use several memory modules simultaneously to read the data out in parallel. The internal memory widths would also increase, but this would pose no significant problem either, because the internal FPGA memory primitives can be easily configured to have arbitrary data widths. Next, the number of attributes affects the size of the adder tree of the NTE module. However, by increasing the size and the depth of the adder tree, only the pipeline depth is increased, resulting only in the increase in the initial latency of the |cop| co-processor, without degrading the |cop| throughput.

If the attribute encodings (|RA|) were to be enlarged, other than increasing the encoding width of the training set instance, which was discussed above, the |cop| co-processor multipliers and adders would need to support wider operands. This would not pose a significant constraint for implementing both multipliers and adders, since the arbitrary width multipliers and adders can be built using a number of same blocks of smaller width connected in a pipeline. Hence, the increase in the data widths would not affect the HW/SW implementation performance, because only the pipeline depths would be increased, which would in turn increase the initial latency without affecting the throughput of the system. However, as far as the author is aware, the attribute encodings with more than 32 bits are rarely used in hardware acceleration of the machine learning algorithms, as discussed in :cite:`struharik2009intellectual,vranjkovic2015reconfigurable,anguita2008support`.

Finally, if the |cop| co-processor were to support the datasets with the larger number of classes |CM| and the larger number of the DT leaves |NlM|, the equation :eq:`accuracy_evaluation_time` shows that the |cop| latency would only linearly increase as a function of these two parameters.

Estimation of Induction Speedup
...............................

Three implementations of the |algo| algorithm have been developed for the experiments, all of them written in the C language:

- **SW-PC** - Pure software implementation for the PC discussed in the :num:`Section #sec-efti-experiments`.
- **SW-ARM** - Pure software implementation for the ARM Cortex-A9 processor.
- **HW/SW** - HW/SW co-design solution, where the |cop| co-processor implemented in the FPGA was used for the time critical fitness evaluation task. The remaining functionality of the |algo| algorithm (shown in the :num:`Algorithm #fig-co-design-sw-pca`) was left in software, and implemented for the ARM Cortex-A9 processor.

For the SW-ARM and the HW/SW implementations, the ARM Cortex-A9 667 MHz (Xilinx XC7Z020-1CLG484C Zynq-7000) platform has been used. The software was built using the Sourcery CodeBench Lite ARM EABI 4.8.3 compiler (from within the Xilinx SDK 2014.4) and the |cop| co-processor was built using the Xilinx Vivado Design Suite 2014.4. The experiments were structured following the description given in the :num:`Section #sec-exp-struct`, and the DT induction time has been measured. The software timing was obtained by different means for two target platforms:

- For the PC platform, the <time.h> C library was used and timing was output to the console,
- For the ARM and DSP platforms, hardware timer was used and the timing was output via the UART.

.. tabularcolumns:: L{0.08\linewidth} R{0.15\linewidth} R{0.18\linewidth} R{0.14\linewidth} R{0.18\linewidth} R{0.14\linewidth}

.. _tbl-results:

.. csv-table:: The DT induction times for various |algo| implementations and average speedups of HW/SW implementation over pure software implementations
    :header-rows: 1
    :file: scripts/cop-speedup.csv

All datasets from the :num:`Table #tbl-uci` were compiled together with the source code and were readily available in the memory. Therefore, the availability of the training set in the main memory was the common starting point for all three implementations, thus there was no training set loading overhead on the DT induction timings. However, in the HW/SW co-design implementation, the datasets need to be packed in the format expected by the Training Set Memory organization (shown in the :num:`Figure #fig-inst-mem-org`) and loaded to the |cop| co-processor via the AXI bus (performed by the *hw_load_training_set()* function). To make a fair comparison with the pure software implementations, time needed to complete these two operations was also included in the total execution time of the HW/SW implementation.

The results of the experiments are presented in the :num:`Table #tbl-results`. For each implementation and dataset, the average induction times of the five 5-fold cross-validation runs are given together with their 95% confidence intervals. The last row of the table provides the average speedup of the HW/SW implementation over the SW-ARM, SW-PC and SW-DSP implementations, together with the 95% confidence intervals.

The :num:`Table #tbl-results` indicates that the average speedup of the HW/SW implementation is 34.2 times over the SW-ARM, 3.4 times over the SW-PC implementation and 65.8 times over the SW-DSP implementation. The speedup varies with different datasets, which is expected since the |algo| algorithm computational complexity is dependent on the dataset as the equation :eq:`cplx_final` suggests. The computational complexity increases as |NI|, |NA|, *n* and |Nc| increase. The number of nodes in DT, *n*, is dependent on the training set instance attribute values, but can be expected to increase also with |NI|, |NA| and |Nc|. By observing the speedups of the HW/SW implementation over the pure software implementations shown in the :num:`Figure #fig-speedup`, for each dataset and the datasets' characteristics given in the :num:`Table #tbl-uci-datasets`, it can be seen that indeed, more speedup is gained for datasets with larger |NI|, |NA| and |Nc| values.

Datasets jvow, w21 and wfr are the largest of the datasets, and thus have some of the largest speedup gains. However, for example, the sick dataset which is almost as large as these ones, has noticeably smaller speedup gain. This is due to the fact that the DTs induced on the sick dataset have the depth of 1.2 levels on average, meaning that the instances of the sick dataset are obviously easily divisible into two classes by only one or two oblique tests. This means that the majority of instances gets classified within the first two NTE stages of the Classifier (with others only passing the result forward), which practically eliminates the benefits of pipelining the NTE modules inside the Classifier module. The only source of acceleration in this case, remains the parallel computation of the node test within the NTE. On the other hand, the datasets like ctg, seg and spf, which have only nearly half as many instances as the sick dataset, have much higher speedup gains, since deeper DTs are induced on them. This is in part because these datasets have more classes than the sick dataset, but it is also the consequence of the relative position of the dataset instances of different classes in the attribute space.

It can also be noticed that the confidence intervals of the pure software implementations are much wider than the ones of the HW/SW implementation. The reason for this is that during 25 cross-validation runs for a single dataset, the DT individuals of different depths get induced. For a single dataset, the |cop| co-processor has fixed execution time, regardless of the size of the DT individual. Hence, HW/SW implementation has rather constant execution time between the cross-validation runs, aside from the negligible variations caused by the variances in the mutation execution times. On the other hand, in the pure software implementations, with each level of depth added to the DT, there is an additional iteration of the ``find_dt_leaf_for_inst()`` function (from the :num:`Algorithm #fig-find-dt-leaf-for-inst-pca`), contributing to the execution time as given by the equation :eq:`find_dt_leaf`. Since this is one of the major components of the total execution time, given by the equation :eq:`cplx_final`, the execution time varies noticeably between the cross-validation runs, hence the bigger confidence intervals for the pure software implementations.

.. _fig-speedup:

.. plot:: images/speedup_plot.py
    :width: 100%

    The speedup of the HW/SW implementation over a) the SW-ARM implementation, b) the SW-PC implementation and c) the SW-DSP implementation, given for each dataset listed in the :num:`Table #tbl-uci-datasets`

The :num:`Figure #fig-speedup` and the :num:`Table #tbl-results` suggest that the HW/SW implementation using the |cop| co-processor offers a substantial speedup in comparison to the pure software implementations, for the ARM, PC and the DSP. This is mainly because all processors that were used in the experiments have a limited number of on-chip functional units that can be used for multiplication and addition operations, as well as the limited number of internal registers to store the node test coefficient values and instance attributes. This means that the loop from the equation :eq:`oblique-test` can only be partially unrolled, when targeting these processors, which would be the case for any processor type. On the other hand, the |cop| co-processor can be configured to use as many multiplier/adder units as needed, and as many internal memory resources for storing coefficient and attribute values which can be accessed in parallel. Because of this, in case of |cop|, the loop from the equation :eq:`oblique-test` can be fully unrolled, therefore gaining the maximum available performance. Furthermore, the |cop| implementation used in the experiments, operates at much lower frequency (133MHz) than ARM (667MHz), PC (3.4GHz) and DSP (225 MHz) platforms. If the |cop| co-processor were implemented in the ASIC, the operating frequency would be increased by an order of magnitude, and the DT induction speedups would increase accordingly.
