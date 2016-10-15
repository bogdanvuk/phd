
Co-processor for the DT induction - the |cop|
=============================================

In this section, the |cop| co-processor is presented...

.. _profiling-results:

Profiling results
-----------------

To confirm the results obtained by the computational complexity analysis, the software profiling was performed on the |algo| algorithm's C implementation. The software implementation was developed using many optimization techniques:

- arithmetic operation on 64-bit operands only (optimized for the 64-bit CPU),
- loop unfolding for the node test evaluation loop,
- maximum compiler optimization settings, etc.

To perform the experiments 21 datasets, presented in the :num:`Table #tbl-uci-datasets`, were selected from the UCI benchmark datasets database :cite:`newman1998uci`. The UCI database is commonly used in the machine learning community to estimate and compare the performance of different machine learning algorithms.

The software implementation of the |algo| algorithm was compiled using the GCC 4.8.2 compiler, run on the AMD Phenom(tm) II X4 965 (3.4 GHz) computer and profiled using the GProf performance analysis tool for each of the tests listed in the :numref:`tbl-uci-datasets`. The results obtained by profiling were consistent with the algorithm complexity analysis performed in the previous chapter and are shown in the :numref:`fig-profiling-plot`. The :numref:`fig-profiling-plot` shows the percentage of time spent in the *fitness_eval()* function and its subfuctions for each dataset. On average, |algo| spent 99.0% of time calculating the fitness of the individual.

.. subfigstart::

.. _fig-profiling-plot1:

.. plot:: images/profiling_plot1.py
    :align: center

    The percentage of time spent in the *fitness_eval()* function and its subfuctions for each dataset listed in the :numref:`tbl-uci`

.. _fig-profiling-plot2:

.. plot:: images/profiling_plot2.py
    :align: center

    The percentage of time spent in the *fitness_eval()* function and its subfuctions for each dataset listed in the :num:`Table #tbl-uci-datasets`

.. _fig-profiling-plot3:

.. plot:: images/profiling_plot3.py
    :align: center

    The percentage of time spent in the *fitness_eval()* function and its subfuctions for each dataset listed in the :num:`Table #tbl-uci-datasets`

.. subfigend::
    :width: 1
    :label: fig-profiling-plot

    The percentage of time spent in the *fitness_eval()* function and its subfuctions for each dataset listed in the :num:`Table #tbl-uci-datasets`

.. raw:: latex

   \begingroup
   \small
   \renewcommand{\arraystretch}{0.8}

.. tabularcolumns:: L{0.12\linewidth} | R{0.17\linewidth} R{0.17\linewidth} R{0.17\linewidth} R{0.17\linewidth} R{0.17\linewidth}

.. _tbl-profiling:
.. csv-table:: List of datasets (and their characteristics) from the UCI database, that are used in the experiments throughout this thesis
    :header-rows: 1
    :file: scripts/profiling.csv

.. raw:: latex

    \endgroup

The results of one example profiling experiment on the *veh* dataset are shown in the :numref:`fig-profiling`. The results are given in tabular fashion, with each row providing the profiling data for one function. The following data are given for each function:

- **Name** - The name of the function.
- **Time** - Total amount of time spent in the function.
- **Calls** - Total number of calls to the function.
- **% Time** - Percentage of time spent in the function relative to the total execution time.

.. _fig-profiling:

.. figure:: images/profiling.png

    The profiling results of the |algo| algorithm's C implementation.

The execution times shown for the functions represent only self times, i.e. the execution times of its subfunctions are subtracted from their total execution time. The functions *fitness_eval()*, *find_dt_leaf_for_inst()* and *find_node_distribution()* from the table in the :num:`Figure #fig-profiling` (which was sorted by the execution times) belong to the fitness evaluation task. By summing the execution times of these four functions, we obtain that the fitness evaluation task takes about 99.41% of the total time for this particular test.

Hence, the |algo| algorithm has obvious computational bottleneck in the fitness evaluation task, which takes 99.0% of the computational time on average, which makes it an undoubtful candidate for the hardware acceleration. Since the DT mutation task takes insignificant amount of time to perform, it was decided to be left in software. Further advantage of leaving the mutation task in software, is the ease of changing and experimenting with this task. Many other evolutionary algorithms for optimizing the DT structure can then be implemented in software and make use of the hardware accelerated fitness evaluation task, like: Genetic Algorithms (GA), Genetic Programming (GP), Simulated Annealing (SA), etc. This fact significantly expands the potential field of use for the proposed EFTIP co-processor core.

.. _classifier-arch-overview:

Architectures for hardware implementation of DT accuracy calculation
--------------------------------------------------------------------

The accuracy of a DT is calculated by letting the DT classify the instances of a training set. The results of the DT classification are then compared with the known classification of the training set and the accuracy is calculated as a number of the correct classifications to the total number of instances in the training set. A sequential algorithm for performing this task is employed by the |algo| algorithm and is described in the :num:`Section #accuracy-calculation`.

First attempt in developping a hardware implementation of this procedure might be to implement every DT node as a separate hardware module, and connect the modules in the form of the DT. The hardware architecture based on this idea is proposed in :cite:`lopez2006decision`, and shown in the :num:`Figure #fig-dt-class-arch-ex1`.

.. _fig-dt-class-arch-ex1:

.. bdp:: images/dt_class_arch_ex1.py
    :width: 60%

    The DT classification hardware implementation using one hardware module per DT node

The instance that is to be classified is sent to each of the hardware DT nodes where the node test is evaluated. All the DT classes are made available on the inputs of the Demultiplexer (:num:`Figure #fig-dt-class-arch-ex1`). Depending on the classification result, one of the classes will be passed by the Demultiplexer to the output of the classifier. Starting from the root, the node tests' are evalulated sequentially along the classification path of the instance, and based on their results  the correct class for the output by the Demultiplexer is selected.

The hardware architecture proposed in :cite:`lopez2006decision` has two major drawbacks, one regarding the amount of hardware resources needed and the other regarding the time needed to perform the classification. First, the architecture needs one hardware module per DT node, which in turn requires a significant amount of resources in order to be able to perform the dot product calculation of the node test (equation :eq:`oblique-test`). Second, the time needed to perform the classification is proportional to the depth of the DT and to the time needed to perform the node test calculation. In other words, this architecture does not scale well with the size of the DT.

One possible way of decreasing the classification time using this architecture is to perform all the node tests in parallel. This is akin to what has been suggested in :cite:`bermak2003compact`, where an equivalence between decision trees and threshold networks is used to devise a hardware architecture for decision tree classification, where all of the node tests are performed in parallel. Once all of the node tests have been evaluated, their results can be combined using a boolean function in order to determine in which node the instance finished the classification, and hence to which class it should be classified into. This way, the time needed to perform the classification equals the time needed to evaluate one node test, plus the time needed to evaluate the output boolean function. Still, the issue with number of node hardware modules remains.

The architecture that remedies both resource and timing problems and was adapted for the |cop| co-processor, is proposed in :cite:`struharik2009intellectual` and called *SMPL* (Single Module Per Layer). Instead of implementing each DT node in hardware separately, this architecture requires only one universal node per DT level, which is associated to all the DT nodes at that level and is able to evaluate all the test assigned to these nodes. The idea behind this solution lies in the fact that a single instance never visits two nodes on the same DT level during its traversal.

.. _fig-smpl-dt:

.. bdp:: images/smpl_dt.py
    :width: 100%

    The idea behind *SMPL* (Single Module Per Layer) architecture. There is one universal hardware module (Universal nodes :math:`L_1 - L_3`) per DT level that implements all the DT nodes on the level.

The :num:`Figure #fig-smpl-dt` shows the structure of the *SMPL* architecture implementation for the same example DT used in :num:`Figure #fig-dt-class-arch-ex1`. The architecture implementation consists of three universal nodes :math:`L_1` through :math:`L_3`, one for each of the DT levels that contain nonleaf nodes. The instance starts its traversal of the DT by being input to the :math:`L_1` module, which implements the root DT node in every *SMPL* architecture implementation. The universal node :math:`L_1` evaluates the root node test and passes the instance along with the test results to the :math:`L_2` module, which is akin to the instance continuing its traversal to the level 2 of the DT. Based on the root node test results received from :math:`L_1`, the :math:`L_2` module knows to which root child the instance has been passed (either node ID 2 or 3), and thus the appropriate level 2 node test is evaluated. Then the universal node :math:`L_2` passes the instance and the test results to its successor and this process is continued until one of the unicersal nodes detects that the instance has arrived to a leaf node, i.e. it has been classified. Thereafter, the information about the class is passed onwards and following universal nodes perform no test evaluations on this instance. Finally, the last module of the *SMPL* architecture outputs the class of the instance.

The *SMPL* is a pipelined architecture, hence the instances can be effectively classified in parallel on all universal nodes, with the small cost of an initial pipeline latency. The node test evaluation results calculated by an universal node, that are to be made available to the next universal node in pipeline, are stored in the register available between every two nodes (blocks named *reg* in the :num:`Figure #fig-smpl-dt`). That way, once the node test is evaluated for an instance and stored in the output register, the universal node is free to start processing the following instance from the dataset, while the next universal node in pipeline consumes the stored results from the register.

The |cop| co-processor classification module is based on *SMPL* architecture as it requires significantly less hardware resources for the implementation then architectures :cite:`lopez2006decision` and :cite:`bermak2003compact`. In order to evalate oblique DT node tests, the addition, multiplication and comparison operations are needed. Hence, the *SMPL* architecture requires notably less adders, multipliers and comparators then architectures proposed in :cite:`lopez2006decision` and :cite:`bermak2003compact`. However, the memory resources requirements for storing the node test coefficients and leaf classes are identical between all three given architectures.

Overview
--------

In this section, an overview of the |cop| co-processor is given. As it was discussed in the section :num:`Section #profiling-results`, the |cop| is designed to accelerate the most time consuming task of the evolutionary DT induction algorithms, which is the task of determining the accuracy of the DT individual, which is in turn needed for the fitness evaluation of the DT (the :num:`Algorithm #fig-fitness-eval-pca`). More precisely, the |cop| co-processor calculates the number of successfull classifications, i.e. the number of classifications hits - the *hits* variable of the :num:`Algorithm #fig-accuracy-calc-pca`.

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

- **Classifier** - Performs the DT traversal for each training set instance, i.e. implements the *find_dt_leaf_for_inst()* function from the :num:`Algorithm #fig-find-dt-leaf-for-inst-pca`. The classification process is pipelined using a number of Node Test Evaluator modules (*NTEs*), with each NTE performing the DT node test calculations for one DT level. The parameter |DM| is the number of pipeline stages and thus the maximum supported depth of the induced DT. For each instance in the training set, the Classifier outputs the ID assigned to the leaf in which the instance finished the traversal (please refer to the *fitness_eval()* function from the :num:`Algorithm #fig-fitness-eval-pca`).
- **Training Set Memory** - The memory for storing all training set instances that should be processed by the |cop| co-processor.
- **DT Memory Array** - The array of memories used for storing the DT description, composed of sub-modules :math:`L_{1}` through :math:`L_{D^{M}}`. Each Classifier pipeline stage requires its own memory that holds the description of all nodes at the DT level it is associated with. Each DT Memory sub-module is further divided into two parts: the CM (Coefficient Memory - memory for the node test coefficients) and the SM (Structural Memory - memory for the DT structural information).
- **Accuracy Calculator** - Based on the classification data received from the Classifier, calculates the accuracy and the impurity of the DT and keeps track of which training set classes were found as dominant for at least one DT leaf. For each instance of the training set, the Classifier supplies the ID of the leaf in which the instance finished the DT traversal. Based on this information, the Accuracy Calculator updates the distribution matrix, calculates the results, which are then forwarded to the Control Unit, ready to be read by the user.
- **Control Unit** - Acts as a bridge between the AXI4 interface and the internal protocols. It also controls the accuracy evaluation process.

Hardware description
--------------------

Classifier
..........

The classifier module performs the classification of an arbitrary set of instances on an arbitrary binary oblique DT. As it was already discussed in the :num:`Section #classifier-arch-overview`, the Classifier module was implemented by modifying the *SMPL* architecture described in :cite:`struharik2009intellectual`. The original architecture from :cite:`struharik2009intellectual` was designed to perform the classification using already induced DTs, hence it was adapted so that it could be used with the |algo| algorithm for the DT induction as well.

.. _fig-dt-classifier-bd:

.. bdp:: images/classifier.py

    The architecture of the Classifier module consisting of the |NTE| modules connected in an array.

In order for the |cop| co-processor to calculate the accuracy of a DT on a dataset, the Classifier needs to perform the DT traversal for each instance of the dataset, i.e. it needs to implement the *find_dt_leaf_for_inst()* function from the :num:`Algorithm #fig-find-dt-leaf-for-inst-pca` in hardware. As it was discussed in the :num:`Section #classifier-arch-overview`, during the traversal of an instance, only one node per DT level is visited, i.e. only one node test is performed per DT level for a single instance. Hence, a single module that implements the evaluation of the oblique node test (equation :eq:`oblique-test`), could be used to incorporate the test evaluations for all nodes on one DT level. Naturally, this module would have to be programmable in that it would have to support the node test evaluation with different coefficient vectors in order to be able to evaluate tests for all nodes residing at same DT level. However, this would need to be the case even if one module was used to implement each DT node, since the |cop| co-processor is used for the DT induction so the node test coefficients are not known in advance.

The :num:`Figure #fig-dt-classifier-bd` shows the Classifier module as being composed from |NTE| modules, each of which is associated with one DT level, and implements the node test evaluation procedure for all nodes on that DT level. The |NTE| modules correspond to the universal nodes of the *SMPL* architecture. During the traversal of the DT, an instance always descends one DT level at the time, and never returns to the levels it already visited. The |NTE| modules are thus connected into a chain, where an instance is transfered from the first |NTE| to the last one in the chain in order to calculate its DT traversal path. The number of *NTEs* the Classifier comprises - |DM|, determines the maximum depth of the DT whose accuracy can be calculated by that hardware instance of the |cop| co-processor. The |DM| value can be specified by the user during the design phase of the |cop| co-processor.

Since an instance always travels down the |NTE| chain, one |NTE| at a time, there is no reason why multiple instances could not traverse the chain simultaneously. The moment the :math:`NTE_1` evaluated the node test for the first instance of the dataset and the instance was transferred to the :math:`NTE_2`, the :math:`NTE_1` is free to evaluate the node test for next instance in dataset. In other words, the |NTE| modules can form the pipeline, with one stage per DT level, capable of accomodating |DM| instances in parallel after the initial latency.

The :math:`NTE_1` always processes the root DT node, however, which nodes are processed by other stages, depends on the path of the traversal for each individual instance. Hence, each |NTE| module needs to have access to the descriptions of all the nodes on the DT level assosicated with it. Since each stage of the |NTE| pipeline needs to operate in parallel (in a distributed manner), the node description data need to be distributed as well and thus each stage has one sub-module of the DT Memory Array assigned to it, that holds the descriptions of all the nodes on the DT level associated with that stage. Furthermore, each DT Memory Array sub-module is divided in two parts, namely |CM| and *SM*, in order to save on some |NTE| hardware resources, because the data from these two memomory parts are needed at different times in the node test evaluation, which will be discussed in more detail in the following text. Therefore, each |NTE| contains interfaces, comprising the address and data buses, for accessing the |CM| and *SM* parts of the assigned DT Memory Array sub-module: *CM addr*, *CM data*, *SM addr* and *SM data*.

When an instance is transferred from one |NTE| module to the next, along with it the decision via which node the traversal continues (made by evaluating the node test) needs to be communicated too. There are two major cases that need to be handled differently:

1. the instance continues the traversal via one of the children of the node whose test has been evaluated by the current |NTE| module. In this case, the next |NTE| in the chain is sent the ID of the child (non-leaf) node to which the instance should descend.

2. the instance has already been classified, in which case the traversal is finished. However, in order not to disturbe the filled pipeline, the instance is nevertheless transfered down the |NTE| chain. In this case, the next |NTE| in the chain is sent the ID of the leaf in which the instances finished its traversal. Based on that, the next |NTE| will recognize that no further calculation needs to be done for this instance and simply pass this information onward.

The inter-NTE interface comprises the following buses:

- **Instance bus** - Passes the instance to the next |NTE|, as the instance traverses the DT.
- **Node ID bus** - Passes to the next |NTE| either the ID of a non-leaf node, through which the traversal is to be continued, or the ID of a leaf node into which the instance has already been classified in some of the previous pipeline stages. The leaf and the non-leaf IDs are distinguished by the value of the node ID's MSB. If the value of the MSB is zero, the node ID is a non-leaf ID, otherwise it is a leaf ID.

For each instance, received at the Classifier input, the first NTE block processes the calculation given by the equation :eq:`oblique-test` using the attributes of received instance |x| and the root node coefficients |w|. Based on the result, it then decides on how to proceed with the DT traversal: via the left or via the right child. The ID of the selected child node, which can either be a leaf or a non-leaf, is output via the *Node ID Output* port. If the selected child is a leaf node, the classification is done and the next stages will perform no further calculations, but only pass forward the ID of the leaf into which the instance has been classified. On the other hand, if the selected child is a non-leaf node, the next stage will continue the traversal through the selected child by calculating the node test associated to it. The calculation of each NTE corresponds to one iteration of the *find_dt_leaf_for_inst()* function loop (:num:`Algorithm #fig-find-dt-leaf-for-inst-pca`), and NTE output *Node ID* corresponds to the *cur_node* variable, more specifically to its attribute *id* needed for the formation of the distribution matrix in the function *accuracy_calc()* of the :num:`Algorithm #fig-accuracy-calc-pca` (*leaf.id*). The node ID is output synchronously with the instance via the *Instance Output* port.

All subsequent stages operate in a similar manner, except that in addition, they also receive the calculation results from their predecessor stage. Somewhere along the NTE chain, all instances will have finished into some leaf. This information is output from the Classifier module via the *Node ID Output* port of the last |NTE| in the chain to the Accuracy Calculator module (together with the corresponding instance description via the *Instance Output* port) in order to update the distribution matrix and calculate the final number of classification hits.

The dot product parallelism
;;;;;;;;;;;;;;;;;;;;;;;;;;;

To evaluate a DT node test, each |NTE| needs to evaluate the dot product between node test coefficient vector |w| and instance attribute vector |x|, which is at the same time by far the most complex operation of the |NTE| module. By extracting the parallelism from the dot product operation, additional speedup could be gained. The :num:`Figure #fig-node-test-parallelism` shows which parts of the dot product calculation can be performed in parallel on an example where :math:`N_A=7`. If we are only allowed to perform binary addition (which is usually the case when the addition is performed by hardware), the calculation could be performed in 4 steps, with all the operations that could be executed in parallel in each step circled with dashed line. In Step 1 all the multiplications could be performed in parallel, while in later steps the |NA|-ary addition is broken down into the sequence of binary addition operations, where some of them could be executed in parallel in each of the remaining steps to obtain the final dot product result value.

.. _fig-node-test-parallelism:

.. bdp:: images/node_test_parallelism.py
    :width: 100%

    The figure shows which parts of the dot product calculation can be performed in parallel on an example where :math:`N_A=7`. If we are only allowed to perform binary addition (which is usually the case when the addition is performed by hardware), the calculation could be performed in 4 steps, with all the operations that could be executed in parallel in each step circled with dashed line.

To take advantage of this parallelism of the dot product calculation, the |NTE| module could be again pipelined internally for the maximal throughput. Each of the steps (:num:`Figure #fig-node-test-parallelism`) of the dot product calculation could be mapped into one internal pipeline stage. The number of stages needed for the dot product pipeline equals 1 for the multiplication step, plus
:math:`\left \lceil ld(\NA)  \right \rceil` for |NA|-ary addition to be performed via binary addition operations. Finally, there is no additional overhead that could come from the need of pipeline flushing, since for this application of the DT accuracy calculation, the instances enter the pipeline in predefined order, one by one, until whole dataset is classified.

Node Test Evaluator - NTE
;;;;;;;;;;;;;;;;;;;;;;;;;

The block diagram in the :num:`Figure #fig-dt-test-eval-bd` shows the architecture of the |NTE| module. When the value received at the *Node ID Input* of an |NTE| contains a non-leaf node ID, it selects the node whose test is to be evaluated, among all the nodes at the DT level associated with the |NTE| module, for the current dataset instance received at the same time with the node ID. Please notice, that |NTE| expects the ID of a node within its associated level (in other words, the ID needs to be unique only within the level), and not the global node ID, which is unique accross the whole DT. Hence, for each DT level, the node numbering starts from 0. On the other hand, the non-leaf node IDs need to be global, i.e. unique accross the whole DT, since one of them will be output from the Classifier as a classification result. The following is thus performed by the Classifier:

1. the test coefficients vector |w| of the selected node is fetched from the CM part of the DT Memory Array sub-module via the *Coefficient Memory Interface*. The selected node's ID is used to calculate the address of the node's coefficient vector in the CM memory, which is communicated via the *CM addr* port,
2. the node test calculation is performed according to the equation :eq:`oblique-test` on the vector |w| and the attribute vector |x| of the current instance,
3. the current node's test threshold (|th|) and the information about the current node's children is retrieved from the SM part of the DT Memory Array sub-module, again using the current node ID to calculate the address where this information is stored in the SM memory,
4. the decision on where to proceed with the DT traversal is made, and the result is output to the next NTE via the *Node ID Output* port, along with the current dataset instance.

On the other hand, when the value received at the *Node ID Input* of an |NTE| contains a leaf node ID, this signals the |NTE| that the corresponding instance has already been classified, hence the dot product calculation is not performed (more precisely, in order to simplify the design it is still performed, but the results are discarded). The received node ID value is simply output verbatim via the "Node ID Output" port along with the corresponding dataset instance.

.. _fig-dt-test-eval-bd:

.. bdp:: images/nte.py

    The NTE (Node Test Evaluator) block architecture

**Nisu dobro numerisane instance u queue-ovima. Instance sa manjim indeksom su napred - pre su krenule. Treba ovo prokomentarisati u textu**

The main parameter that needs to be specified by the user during the design phase of the |cop| is the maximum supported number of attributes per instance - |NAM|, i.e. the maximum supported sizes of the vectors |w| and |x|. This parameter affects the size and latency of the |NTE| module as it will be explained in the text that follows.

The |NTE| module's main task is the dot product calculation of the vectors |w| and |x|. By using only two input multipliers and adders, this computation is parallelized and pipelined as much as possible as discussed in the :num:`Section #the-dot-product-parallelism`. The multiplications are all performed in parallel, for all |NAM| coefficient and attribute pairs. Since, usually, two input adders are used in hardware design, and the |NAM|-ary sum is needed, the tree of two input adders is necessary, that is :math:`\left \lceil ld(\NAM)  \right \rceil` deep. In order to acheive higher operating frequency of the implemented |cop| co-processor, the dot product calculation datapath is broken in stages, with one stage per calculation step, that comprises multiplications or additions that can be performed in parallel. Hence, the outputs of each of the adders and multipliers are registered to form the pipeline.

One more important parameter, besides |NAM|, that needs to be specified by the user during the design phase of the |cop| is |RA| - the number of bits used for the signed fixed point representation of the elements of the vectors |w| and |x| in the |cop| co-processor. Hence, the elements of |w| and |x| are considered to be in Q0.(:math:`R_A-1`) format. For an example, if 16 bits are used for the representation of the vector elements, they are considered to be in Q0.15 format. After the multiplication stage, the products will thus be in Q0.(:math:`2R_A-2`) signed fixed point format. The value of the sum output by each adder is 1 bit larger than the value of its operands, hence the registers increase in size by 1 integer bit per pipeline stage. After the final addition the sum representation will have reached the size of: :math:`2R_A-1+\NPADD` bits in Q(|NPADD|).(:math:`2R_A-2`) format. Finally, the value of the finall sum is truncated to the width of |RA| bits in format Q(|NPADD|).(:math:`R_A-1-\NPADD`), which are hence the representation size and format of the node test threshold |th|.

The necessary number of bits used to encode the non-leaf node and leaf IDs - |RN|, can be calculated based on the parameter |DM|. Since the non-leaf node IDs are unique only accross one DT level, of which the last level can have the largest number of nodes, and the |DM| parameter limits the number of levels the induced DT can have, there is a maximum of :math:`2^{D^M-1}` different non-leaf node IDs to be encoded for the selected value of the parameter |DM|. On the other hand, the leaf IDs need to be globaly unique, hence there needs to be one leaf ID available for each leaf in the DT. The number of leaves is also related to the parameter |DM|: :math:`2^{D^M}`. Additionaly, the MSB of the ID representation needs is reserved for differentiating between the leaf and non-leaf node IDs. Finally, the total number of bits for encoding IDs should be :math:`R_N \ge D^M+1`.

The |NTE| architecture displayed in the :num:`Figure #fig-dt-test-eval-bd` is partitioned in |NP| pipeline stages by the vertical dotted lines and each part is labeled by the stage ID: Stage 1, Stage 2, ... Stage |NP|. The total number of pipeline stages needed (|NP|), equals the depth of the adder tree, plus the multiplication stage and the decision stage in the end where node test results are intepreted:

.. math:: N_{P}=\NPADD + 2
	:label: np

The |NTE| module also supports the datasets with less than |NAM| number of instance attributes, :math:`\NA < \NAM`. In this case, the surpluss coefficients :math:`w_{\NA+1}, w_{\NA+2}, ... w_{\NAM}` should be all set to zero, in order not to affect the calculation of the sum.

Treba ovde ispricati da vise instanci moze biti napunjeno u pipeline i da se zbog toga oznake na Queue-ovima na razlicitim stagevima nazivaju kao na slici.

The Instance Queue and the Node Queue delay lines are necessary due to the pipelining. Each |NTE| performs calculations only for a single DT level, hence once the calculations is finished the instance needs to be transferred to the next |NTE| module in the Classifier chain. This transfer needs to correlate in time with the output of the node test evaluation results via the *Node ID output* port. Hence, the Instance Queue has to have the length equal to |NP|, since it needs to delay the output of the instance to the next |NTE| module for |NP| clock cycles.

The Node Queue is necessary for preserving the selected node's ID (the signal *Node ID* in the :num:`Figure #fig-dt-test-eval-bd`). In the pipeline Stage :math:`N_P-1`, this ID will be used to calculate the address of the node's structural description in the SM part of the DT Memory Array sub-module, comprising three values: the ID of the left child - |ChL|, the ID of the right child - |ChR| and the node test threshold value - |th|. These values are needed in the last pipeline stage, where a decision on how to continue the traversal will be made. The comparator compares the dot product sum value and |th|, and based on the result signals the MUX1 to select either |ChL| or |ChR|, i.e. to decide where the traversal will continue. However, if the selected node ID is a leaf ID, the node test evaluation results should be discarded since the instance has already been classified. This decision is made by the MUX2, based on the MSB value of the selected node ID. As it was already mentioned the MSB value of the leaf IDs is always 1, while the MSB value of the non-leaf node IDs is always 0. Hence, if the selected node ID is a leaf ID, it is passed verbatim to the *Node ID Output* port, otherwise the output of the MUX1 multiplexer is passed. Also, since the selected node ID value is used in the last pipeline stage, the Node Queue also has to have the length equal to |NP|.

The Classifier operation example
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

Once again, lets use the example DT whose induction by the |algo| algorithm was discussed in :num:`Section #the-algorithm-overview` and shown in :num:`Figure #fig-efti-overview` and :num:`Figure #fig-efti-overview-dot`. First, the parameters of the Classifier module need to be selected. Since the training set used to induce the example DT (shown in the :num:`Figure #fig-efti-overview`) is described by two attributes, :math:`N_A=2`, the minimum value that can be chosen for |NAM| is :math:`\NAM=N_A=2`. For the sake of simplicity, in this example, |NAM| will be set to this minimum value of 2. The value of |RA| can be chosen freely, and here it will be set to 16, which will provide high enough representation precision to obtain correct classification results. The example DT is 3 levels deep, hence |DM| parameter needs to be set to at least that value. Even though the Classifier would provide correct results even if it contained more levels than that, for the sake of simplicity |DM| will be set 3. Although, it would suffice to select :math:`R_N=D^M + 1=4`, |RN| will be set to 8 for visually clearer leaf ID representation.

Once more, the parameters were set to the following values: :math:`D^M=3`, :math:`\NAM=2`, :math:`R_A=16` and :math:`R_N=8`. Based on these settings, the other parameters can be calculated: |NPADD| = 1, |NP| = 3, |w| and |x| elements format is Q0.15, and |th| format is Q1.14.

The :num:`Figure #fig-nte-example-dt` shows the induced DT with |th| and |w| displayed for all nodes, first in decimal format and then in the fixed point representation immediately below. Please notice that

.. _fig-nte-example-dt:

.. bdp:: images/nte_example_dt.py
    :width: 100%

    The example DT used to discuss the |NTE| operation. |th| and |w| are displayed for all nodes, first in decimal format and then in the fixed point representation immediately below.

**Naglasiti da Instance Queue nosi i informaciju o classi instance, ali da ovde nije prikazana jer nije relevantna**

It will be shown now, how a single instance gets classified by the example DT using the Classifier module. For this example, the instance :math:`\mathbf{x}=[0.5156,0.2031]` will be classified, which encoded to Q0.15 becomes :math:`\mathbf{x}=[\mathtt{41FF},\mathtt{19FF}]`. As the :num:`Figure #fig-dt-classifier-bd` shows, the instance is first input to the :math:`\textrm{NTE}_1`. The :math:`\textrm{NTE}_1` module always has the node ID 0 selected, since the root node is the only possible choice for the first DT level.

.. _fig-classifier-example-nte1-pre:

.. bdp:: images/classifier_example_nte1_pre.py
    :width: 100%

    The preparation for the first pipeline stage, where the loading of the coefficient vector for the selected node from the CM memory is performed. All the blocks and the signal paths active in this phase are marked in the figure.

Before the first pipeline stage, the coefficient vector needs to be loaded from memory for the selected node. The read from CM memory is performed asynchronously, and the coefficients are readied to be registered in order to be used in the first pipeline stage, that performs the multiplication operation. The instance attribute vector is led to the Instance Queue and the selected node ID to the Node Queue.  All blocks and signal paths active in this phase are marked in the figure :num:`Figure #fig-classifier-example-nte1-pre`. Next, in the first pipline stage, the elementwise multiplication between vectors |w| and |x| is performed. The instance and the selected node ID are now stored in the first elements of the Instance and Node queues respectively. The :num:`Figure #fig-classifier-example-nte1-stage1` shows all the blocks and the signal paths active in the first pipeline stage. The vector |w| and |x| element values are shown in the figure, as well as the multiplication results which are in Q0.30 fixed point format as it was already described. Please notice, that |NTE| preforms signed additions and multiplications, hence the sign extension is needed for all operands, but this is not shown in the following figures.

.. _fig-classifier-example-nte1-stage1:

.. bdp:: images/classifier_example_nte1_stage1.py
    :width: 100%

    The first pipeline stage, where the elementwise multiplication between vectors |w| and |x| is performed. All the blocks and the signal paths active in this stage are marked in the figure.

Next, in the pipeline stage 2, the addition of the elementwise products is performed. Since there the |NAM| paremeter was set to support only two instance attributes, the addition can be performed within the single pipeline stage. If a higher value was selected for the |NAM| parameter, multiple stages would be needed in order to calculate the dot product sum. The instance and the selected node ID are now stored in the second elements of the Instance and Node queues respectively. The :num:`Figure #fig-classifier-example-nte1-stage2` shows all the blocks and the signal paths active in the second pipeline stage. The vector elementwise products are shown in the figure, as well as the addition result, that is also the dot product result, which is in Q1.30 fixed point format. Additionally, the information needed for the final decision on where the traversal will continue is fetched from the SM and prepared for the last pipeline stage. The fetched values for |th|, |ChL| and |ChR| for this example are shown in the figure.

.. _fig-classifier-example-nte1-stage2:

.. bdp:: images/classifier_example_nte1_stage2.py
    :width: 100%

    The second pipeline stage, where the final evaluation of the node test is performed and the decision on where the traversal will continue is made. All the blocks and the signal paths active in this stage are marked in the figure.

Finally, in the pipeline stage 3, the dot product calculation results are compared to the value of |th|, to determine that the node test yielded the value **true**. Based on that the ID of the left child - 0, |ChL|, will be output by MUX1, which will be also passed by MUX2 to the *Node ID Output*, since the instance was not already classified (the MSB of the current node ID is 0). Hence, the DT traversal for this instance will continue via node with ID 0 on the second DT level, which will be performed by the :math:`NTE_2` module. The :num:`Figure #fig-classifier-example-nte1-stage3` shows all the blocks and the signal paths active in the pipeline stage 3.

.. _fig-classifier-example-nte1-stage3:

.. bdp:: images/classifier_example_nte1_stage3.py
    :width: 100%

    The third pipeline stage, where the addition of the elementwise products is performed. All the blocks and the signal paths active in this stage are marked in the figure.

The outputs: *Instance Output* = :math:`[\mathtt{41FF},\mathtt{19FF}]` and *Node ID Output* = 0, as shown in the :num:`Figure #fig-classifier-example-nte1-stage3`, are then passed to the :math:`NTE_2` module where the traversal of the instance continues. The :math:`NTE_2` module performs the exact same 3 stages as the :math:`NTE_1` module did, but on a different DT node. The :num:`Figure #fig-classifier-example-nte2` combines the results of all the computations from all 3 stages of :math:`NTE_2` module in one image. This time the value passed from the previous |NTE| (the value 0 in this example), is used to select the node for the test evaluation, among the two possible nodes on the DT level 2. As it is shown in the figure, the test evaluates to **false** and hence the traversal should be continued via the right child. In this case, the right child is a leaf with the id :math:`\mathtt{80}`, hence the instance's classification has been determined. Nevertheless, the instance is passed to the next (and also the last) |NTE| module, which will recognize that no further computation is needed for the instance, and simply pass the results to the Classifier output. The :num:`Figure #fig-classifier-example-nte3` shows the relevant computation results from all 3 stages of :math:`NTE_3` module in one image. The MUX2 component of the |NTE| module recognizes that it has received a leaf ID on its *Node ID Input* port (node ID's MSB value is 1), hence it disregards all the computation (whose results are omitted from the figure because of this reason) and simply outputs the same leaf ID value for the instance on the *Node ID Output* port, which is at the same time the output of the whole Classifier module too.

**Povezati ovo sa plotom dataseta i pokazati da je klasifikacija tacna**

.. _fig-classifier-example-nte2:

.. bdp:: images/classifier_example_nte2.py
    :width: 100%

    The results of the node test evaluation on the second DT level by the :math:`NTE_2` module.

.. _fig-classifier-example-nte3:

.. bdp:: images/classifier_example_nte3.py
    :width: 100%

    The results of the node test evaluation on the third DT level by the :math:`NTE_3` module.

The :num:`Figure #fig-pipeline-demo` shows the pipeline processing of the dataset instances. In this figure, only the contents of the Instance and Node queues are shown, depicting which instance is being processed by which stage of which |NTE|. Each pipeline stage is represented by a pair of Instance and Node queue elements which are shown horizontally aligned in the figure. The Instance Queue element of the pair shows the attribute vector and the class assigned to the instance it contains, while the Node Queue element shows the current ID of the node this instance is at.

At the beginning, the queues are empty and the first instance :math:`I_0` is received from the Training Set Memory as shown in the :num:`Figure #fig-pipeline-demo1`. The node test evaluation computation is carried out stage by stage, and :math:`I_0` instance is transfered to the :math:`NTE_1` module, shown in the :num:`Figure #fig-pipeline-demo2`, and its traversal is continued via the node with ID 0 on the DT level 1 (:num:`Figure #fig-nte-example-dt`). By this time, three more instances have been loaded from the Training Set Memory, and are in the process of the node test evaluation in three stages of the :math:`NTE_0` module. Since they all need to start from the root node, their selected node IDs are all 0. Finally, the :num:`Figure #fig-pipeline-demo3` shows the moment in the classification where the first instance of the dataset :math:`I_0` has reached the end of the pipeline and is output to the Accuracy Calculator module, along with its classification into the leaf node with ID :math:`\mathtt{83}`.

**Povezati rezultat sa slikom dataseta u attribute space-u**

.. subfigstart::

.. _fig-pipeline-demo1:

.. bdp:: images/pipeline_demo1.py
    :width: 100%
    :align: center

    iter: 000000, fit: 0.602, size: 2, acc: 0.600

.. _fig-pipeline-demo2:

.. bdp:: images/pipeline_demo2.py
    :width: 100%
    :align: center

    iter: 000013, fit: 0.629, size: 2, acc: 0.627

.. _fig-pipeline-demo3:

.. bdp:: images/pipeline_demo3.py
    :width: 100%
    :align: center

    iter: 000013, fit: 0.629, size: 2, acc: 0.627

.. subfigend::
    :width: 0.99
    :label: fig-pipeline-demo

    Caption

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

Accuracy Calculator
...................

This module calculates the accuracy of the DT via the distribution matrix, as described by the :num:`Algorithm #fig-fitness-eval-pca`. It monitors the output of the Classifier module, i.e the training set classification, and for each instance in the training set, based on its class (*C*) and the leaf in which it finished the traversal (*Leaf ID*), the appropriate element of the distribution matrix is incremented. The Accuracy Calculator block is shown in the :num:`Figure #fig-fit-calc-bd`.

.. _fig-fit-calc-bd:

.. bdp:: images/fitness_calc_bd.py
    :width: 85%

    The Accuracy Calculator block diagram

In order to speed up the dominant class calculation (second loop of the *fitness_eval()* function in the :num:`Algorithm #fig-fitness-eval-pca`), the Accuracy Calculator is implemented as an array of calculators, called Leaf Dominant Class Calculator - |LDCC|, whose each element keeps track of the distribution for the single leaf node. Hence, the dominant class calculation for a leaf (the *dominant_class* and the *dominant_class_cnt* variables from the :num:`Algorithm #fig-fitness-eval-pca`) and counting the total number of instances that finished the traversal in the leaf, can be performed in parallel for each leaf node. The number of elements in the array equals the value of the maximum number of leaf nodes parameter - |NlM|, which can be specified by the user during the design phase of the |cop| co-processor. This value imposes a constraint on the maximum number of leaves in the induced DT. Each calculator comprises:

- **Class Distribution Memory** - For keeping track of the class distribution of the corresponding leaf node.
- **Incrementer** - Updates the memory based on the Classifier output.
- **Dominant Class Calculator** - Finds and outputs the following values: the dominant class for the leaf, the number of instances of the dominant class that were classified in the leaf and the total number of instances that were classified in the leaf, using the signals :math:`dominant\_class_{i}`, :math:`dominant\_class\_cnt_{i}` and :math:`total\_cnt_{i}` respectively, where :math:`i \in (1, N^{M}_{l})`, shown in the :num:`Figure #fig-fit-calc-bd`.

For the leaf it is responsible for, each |LDCC| keeps track of how many instances of each of the training set classes were classified in the leaf. It then finds a class that has the largest number of instances in the leaf (the dominant class corresponding to the *dominant_class* variable in :num:`Algorithm #fig-fitness-eval-pca`), and outputs its ID via the *dominant_class* port. If the instance's class equals the dominant class of the leaf node it finished the traversal in, it is considered a hit, otherwise it is considered a miss. Hence, the value output to the *dominant_class_cnt* port represents the number of classification hits for the corresponding leaf node and corresponds to the *dominant_class_cnt* variable in :num:`Algorithm #fig-fitness-eval-pca`. The total number of instances classified in the leaf is output via *hits* port.

The Accuracy Provider then performs the following:

- It sums the classification hits for all leaf nodes and outputs the sum as the number of hits for the whole DT (the *hits* port), which is then stored in the Classification Performance Register of the Control Unit.
- Forms a bit vector that represents which training set classes have been found as dominant by any of the Fitness Calculators, and which ones are missing. This value is output via *dt_classes* port for storing in Classes Register in Control Unit.

The Accuracy Calculator operation example
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


.. subfigstart::

.. _fig-acc-calc-demo1:

.. bdp:: images/acc_calc_demo1.py
    :width: 100%
    :align: center

    iter: 000000, fit: 0.602, size: 2, acc: 0.600

.. _fig-acc-calc-demo2:

.. bdp:: images/acc_calc_demo2.py
    :width: 100%
    :align: center

    iter: 000013, fit: 0.629, size: 2, acc: 0.627

.. _fig-acc-calc-demo3:

.. bdp:: images/acc_calc_demo3.py
    :width: 100%
    :align: center

    iter: 000013, fit: 0.629, size: 2, acc: 0.627

.. _fig-acc-calc-demo4:
    
.. bdp:: images/acc_calc_demo4.py
    :width: 100%
    :align: center

    iter: 000013, fit: 0.629, size: 2, acc: 0.627
    
.. subfigend::
    :width: 0.49
    :label: fig-acc-calc-demo

    Caption

Control Unit
............

Control Unit provides the AXI4 interface access to the configuration and the status registers, as well as to the DT Memory Array and the Training Set Memory. The following registers are provided:

- **Operation Control** - Allows the user to start, stop and reset the |cop| co-processor.
- **Traning Set Size** - Allows the user to specify the number of instances in the training set.
- **Classification Performance Register** - Informs the user when the accuracy evaluation task is done, and enables the user to read the calculated number of the classification hits.
- **Classes Register** - Stores the bit vector output via Accuracy Calculator's *dt_classes* port.
- **Leaf Impurity Registers** - Stores the impurity measures output via Accuracy Calculator's *dt_impurity* port.

.. _fig-efti-fsm:
    
.. bdp:: images/efti_fsm.py
    :width: 45%

    iter: 000013, fit: 0.629, size: 2, acc: 0.627
  
**Opisati proces evaluacije, koji registri sta, kako ide registar mapa, proci kroz FSM, koje memorije treba napuniti**
  
Required Hardware Resources and Performance
-------------------------------------------

The |cop| co-processor is implemented as an IP core with many customization parameters that can be configured at the design phase and are given in the :num:`Table #tbl-cop-params`. These parameters mainly impose constraints on the maximum size of the DT that can be induced, and the maximum size of the training set that can be used.

.. tabularcolumns:: c p{0.4\linewidth} p{0.4\linewidth}

.. _tbl-cop-params:

.. list-table:: The customization parameters that can be configured at the design phase of the |cop| co-processor
    :header-rows: 1
    :widths: 15 30 30

    * - Parameter
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
    * - :math:`C^M`
      - Accuracy Calculator memory depth
      - The maximum number of training set and induced DT classes
    * - :math:`R_C`
      - Parameter must be at least :math:`log_{2}(C^M)`
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
      - :math:`\NlM\cdot C^{M}\cdot \left \lceil log_{2}(N^{M}_{I})  \right \rceil`
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

.. math:: accuracy\_evaluation\_time = (N_{I} + \DM\cdot N_{P} + N_{C} + N_{l}) \ clock\ cycles,
	:label: accuracy_evaluation_time

and is thus dependent on the training set size.

Software for the |cop| assisted DT induction
--------------------------------------------

With the |cop| co-processor performing the DT accuracy evaluation task, remaining functionality of the |algo| algorithm (:num:`Algorithm #fig-algorithm-pca`) is implemented in software. Furthermore, the software needs to implement procedures for interfacing the |cop| co-processor as well. The pseudo-code for the software used in the co-design is given by the :num:`Algorithm #fig-co-design-sw-pca`.

.. _fig-co-design-sw-pca:

.. literalinclude:: code/co_algorithm.py
    :caption: The pseudo-code of the |algo| algorithm using the |cop| co-processor

.. literalinclude:: code/hw_load_train_set.py
    :caption: The pseudo-code of the *hw_load_train_set()* function that performs the transfer of the training set to the |cop| co-processor

.. literalinclude:: code/hw_fitness_eval.py
    :caption: The pseudo-code of the *hw_fitness_eval()* function that performs the fitness evaluation calculation using the |cop| co-processor

.. literalinclude:: code/hw_load_whole_dt.py
    :caption: The pseudo-code of the *hw_load_whole_dt()* function that performs the transfer of the DT individual coefficients and structural data to the |cop| co-processor

The only difference to the pure software solution of the main *efti()* function, is that the training set needs to be transfered to the |cop| co-processor, which is performed by the *hw_load_training_set()* function. Since the |cop|'s memory space is mapped to the host CPU's memory space via the AXI bus, this function simply copies the instances to the memory region corresponding to the Training Set Memory of the |cop|.

The *fitness_eval()* function performs the following:

- uploads the new (mutated) DT description (by changing only the mutated parts of the DT) to the |cop|'s DT Memory Array, using the *hw_load_dt_diff()* function,
- initiates the DT accuracy evaluation by writing to the Operation Control register of the |cop|, using the *hw_start_accuracy_eval()* function,
- waits for the DT accuracy evaluation results to become available, by polling the |cop| Classification Performance Register, using the *hw_finished_accuracy_eval()* function,
- fetches the number of classification hits (*hits* variable), the list of classes that were assigned to a leaf (*dt_classes* variable) and the list of leaf impurity measures (*dt_impurity* variable), from the |cop| Classification Performance Register, using the *hw_get_hits()*, and calculates the fitness in the same manner as in the :num:`Algorithm #fig-fitness-eval-pca`.

The hardware interface functions pseudo-codes were omitted for brevity. It should be noted, however, that the descriptions of the training set instances in the Training Set Memory and the DT node descriptions in the DT Memory Array are stored compacted to save the memory resources, as opposed to their storage in the host CPU memory, where they are word aligned to gain the maximum execution speed on the CPU. Hence, before sending either the instance or node description data to the |cop| internal memories, the data needs to be packed in chunks of 32 bits in the manner showed in the :num:`Figure #fig-inst-mem-org` for the Training Set Memory, and in the :num:`Figure #fig-dt-mem-array-org` for the DT Memory Array. Each instance description slot in the Training Set Memory and each node description slot in the DT Memory Array can be individually addressed, read and written to, in chunks of 32 bits, via their User Ports.

Regarding the accessing of the DT Memory Array, every memory sub-module from the array is assigned its own address space. All address spaces assigned to the sub-modules are equal in size and are big enough to accommodate the largest sub-module. When the host CPU wants to update the description of a certain node, it needs to pack the coefficients and the structural information into an array of 32 bit values, so that the fields have the same layout as shown in the :num:`Figure #fig-dt-mem-array-org`. Next, it can update a DT Memory Array sub-module's node description by writing this array into the successive memory locations assigned to the node. This operation is repeated sequentially, for every EFTIP pipeline stage requiring the DT Memory Array sub-module update.

Optimizations:

- vektor koeficijenata u dt strukturi stoji upakovan sve vreme, da se ne bi stalno prepakivalo
- accuracy and finished status are combined in single register to save on access time
- loads and reverst only parts of dt that were mutated

Experiments
-----------

In this section, the results of the experiments designed to estimate DT induction speedup of the HW/SW implementation of the |algo| algorithm using the |cop| co-processor over pure software implementation of the |algo| algorithm are given.

Required Hardware Resources for the |cop| Co-Processor Used in Experiments
..........................................................................

The customization parameters of the |cop| co-processor, whose descriptions is given in the :num:`Table #tbl-cop-params`, have been set for the experiments to support all training sets from the :num:`Table #tbl-uci-datasets`. The values of the customization parameters are given in the :num:`Table #tbl-exp-params`.

.. tabularcolumns:: p{0.5\linewidth} p{0.2\linewidth}

.. _tbl-exp-params:

.. list-table:: The values of customization parameters of the |cop| co-processor instance used in the DT induction speedup experiments
    :header-rows: 1

    * - Parameter
      - Value
    * - DT Max. depth (|DM|)
      - 6
    * - Max. attributes num. (|NAM|)
      - 32
    * - Attribute encoding resolution (:math:`R_{A}`)
      - 16
    * - Class encoding resolution (:math:`R_{C}`)
      - 8
    * - Max. training set classes (:math:`C^{M}`)
      - 16
    * - Max. number of leaves (|NlM|)
      - 16
    * - Max. number of training set instances (|NIM|)
      - 4096
    * - Max. number of nodes per level (|NnM_l|)
      - (1, 2, 4, 8, 16, 16)

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

The number of instances the |cop| co-processor can store in its Training Set Memory is limited by the parameter |NIM|, selected at the design phase of the the |cop|. In case that the datasets, which cannot fit into the Training Set Memory, need to be used, either a double buffering approach could be used or the |cop| could be used in the streaming mode. In the streaming mode, the data would be continuously streamed from the host CPU memory using the DMA transfer. In this case, there would be no Training Set Memory, as the instances would be supplied to the Classifier from the outside via the DMA. In the double buffering approach, the Training Set Memory would be used as a ring buffer. While the |cop| is using the NTE port to read the instance descriptions to the Classifier, the User port would be used to load new instances to the Training Set Memory. The DMA transfer from the main memory would be used here as well. |cop| reads instances from the data set in predictable, sequential order, so it is easy to setup the DMA transfer and execute it without the intervention of the software during the transfer. This means that the full bandwidth of the main memory can be used for the data without any overhead.

If the |cop| co-processor were to support the datasets with larger number of attributes, which results in wider training set instance encodings, the training set transfer time could impact the HW/SW implementation performance. In this case, again, the double buffering or the |cop| in streaming mode could be used. The throughput of the |cop| co-processor, i.e. the widest possible training set instance encoding that could be used without degrading the performance, would then be limited only by the bandwidth of the main memory, since there is no overhead to the training set data streaming. If the bandwidth of one main memory module is not enough, the |cop| could use several memory modules simultaneously to read the data out in parallel. The internal memory widths would also increase, but this would pose no significant problem either, because the internal FPGA memory primitives can be easily configured to have arbitrary data widths. Next, the number of attributes affects the size of the adder tree of the NTE module. However, by increasing the size and depth of the adder tree, only the pipeline depth is increased, resulting only in the increase in the initial latency of the |cop| co-processor, without degrading the |cop| throughput.

If the attribute encodings (|RA|) were to be enlarged, other than increasing the encoding width of the training set instance, which was discussed above, the |cop| co-processor multipliers and adders would need to support wider operands. Regarding the multipliers, this would not pose a significant constraint, since the arbitrary width multipliers can be build using a number of DSP blocks connected in a pipeline. The similar pipelining approach can be used if the width of adders needs to be enlarged. Hence, all this increase in data widths would not affect the HW/SW implementation performance, because only the pipeline depths would be increased, increasing the initial latency, but not affecting the throughput of the system. However, as far as authors are aware, attribute encodings  with more than 32 bits are rarely used in hardware acceleration of the machine learning algorithms, please refer to :cite:`struharik2009intellectual,vranjkovic2015reconfigurable,anguita2008support`.

If the |cop| co-processor were to support the datasets with larger number of classes |NlM|, only the depth of the Fitness Calculators' memories needs to be enlarged without any effect on the HW/SW implementation performance.

Estimation of Induction Speedup
...............................

Four implementations of the |algo| algorithm have been developed for the experiments, all of them written in the C language:

- **SW-PC** - Pure software implementation for the PC.
- **SW-ARM** - Pure software implementation for the ARM Cortex-A9 processor.
- **SW-DSP** - Pure software implementation for the TI TMS320C6713 DSP processor. Since the calculations from the equation :eq:`oblique-test` resemble the MAC operation of the DSPs, it was decided to include the DSP implementation into the experiments, to investigate its performance.
- **HW/SW** - HW/SW co-design solution, where the |cop| co-processor implemented in the FPGA was used for the time critical fitness evaluation task. The remaining functionality of the |algo| algorithm (shown in the :num:`Algorithm #fig-co-design-sw-pca`) was left in software, and implemented for the ARM Cortex-A9 processor.

For the PC implementation, the AMD Phenom(tm) II X4 965 (3.4 GHz) platform was used, and the software was built using the GCC 4.8.2 compiler. For the SW-ARM and the HW/SW implementations, the ARM Cortex-A9 667 MHz (Xilinx XC7Z020-1CLG484C Zynq-7000) platform has been used. The software was built using the Sourcery CodeBench Lite ARM EABI 4.8.3 compiler (from within the Xilinx SDK 2014.4) and the |cop| co-processor was built using the Xilinx Vivado Design Suite 2014.4. For the SW-DSP implementation, Texas Instruments TMS320C6713 (225 MHz) DSP processor was used, and the software was built using TMS320C6x C/C++ Compiler v7.4.4.

Care was taken when writing the software and many optimization techniques were employed, as described in the section `Profiling results`_, in order to create the fastest possible software implementation and have a fair comparison with the HW/SW solution. For the SW-DSP implementation all data structures used in the |cop| implementation and the executable code have been stored in the DSP's on-chip memory to maximize the performance. Furthermore, the number representations for the instance attributes and the node test coefficients have been set to 16-bit fixed point, to optimize them for the 16x16 bit multipliers that are available on the DSP used.

For each of the datasets from the :num:`Table #tbl-uci-datasets`, an experiment consisting of five 5-fold cross-validation runs has been performed for all three |algo| algorithm implementations. For each cross-validation run, 500000 iterations were performed (the *max_iter* variable from the :num:`Algorithm #fig-algorithm-pca` has been set to 500000) and the DT induction time has been measured. The software timing was obtained by different means for two target platforms:

- For the PC platform, the <time.h> C library was used and timing was output to the console,
- For the ARM and DSP platforms, hardware timer was used and the timing was output via the UART.

.. tabularcolumns:: l R{0.15\linewidth} R{0.15\linewidth} R{0.15\linewidth} R{0.15\linewidth}

.. _tbl-results:

.. csv-table:: The DT induction times for various |algo| implementations and average speedups of HW/SW implementation over pure software implementations
    :header-rows: 1
    :file: scripts/results.csv

All datasets from the :num:`Table #tbl-uci-datasets` were compiled together with the source code and were readily available in the memory. Therefore, the availability of the training set in the main memory was the common starting point for all three implementations, thus there was no training set loading overhead on the DT induction timings. However, in the HW/SW co-design implementation, the datasets need to be packed in the format expected by the Training Set Memory organization (shown in the :num:`Figure #fig-inst-mem-org`) and loaded to the |cop| co-processor via the AXI bus (performed by the *hw_load_training_set()* function). To make a fair comparison with the pure software implementations, time needed to complete these two operations was also included in the total execution time of the HW/SW implementation.

The results of the experiments are presented in the :num:`Table #tbl-results`. For each implementation and dataset, the average induction times of the five 5-fold cross-validation runs are given together with their 95% confidence intervals. The last row of the table provides the average speedup of the HW/SW implementation over the SW-ARM, SW-PC and SW-DSP implementations, together with the 95% confidence intervals.

The :num:`Table #tbl-results` indicates that the average speedup of the HW/SW implementation is 34.2 times over the SW-ARM, 3.4 times over the SW-PC implementation and 65.8 times over the SW-DSP implementation. The speedup varies with different datasets, which is expected since the |algo| algorithm computational complexity is dependent on the dataset as the equation :eq:`cplx_final` suggests. The computational complexity increases as |NI|, |NA|, *n* and |Nc| increase. The number of nodes in DT, *n*, is dependent on the training set instance attribute values, but can be expected to increase also with |NI|, |NA| and |Nc|. By observing the speedups of the HW/SW implementation over the pure software implementations shown in the :num:`Figure #fig-speedup`, for each dataset and the datasets' characteristics given in the :num:`Table #tbl-uci-datasets`, it can be seen that indeed, more speedup is gained for datasets with larger |NI|, |NA| and |Nc| values.

Datasets jvow, w21 and wfr are the largest of the datasets, and thus have some of the largest speedup gains. However, for example, the sick dataset which is almost as large as these ones, has noticeably smaller speedup gain. This is due to the fact that the DTs induced on the sick dataset have the depth of 1.2 levels on average, meaning that the instances of the sick dataset are obviously easily divisible into two classes by only one or two oblique tests. This means that the majority of instances gets classified within the first two NTE stages of the Classifier (with others only passing the result forward), which practically eliminates the benefits of pipelining the NTE modules inside the Classifier module. The only source of acceleration in this case, remains the parallel computation of the node test within the NTE. On the other hand, the datasets like ctg, seg and spf, which have only nearly half as many instances as the sick dataset, have much higher speedup gains, since deeper DTs are induced on them. This is in part because these datasets have more classes than the sick dataset, but it is also the consequence of the relative position of the dataset instances of different classes in the attribute space.

It can also be noticed that the confidence intervals of the pure software implementations are much wider than the ones of the HW/SW implementation. The reason for this is that during 25 cross-validation runs for a single dataset, the DT individuals of different depths get induced. For a single dataset, the |cop| co-processor has fixed execution time, regardless of the size of the DT individual. Hence, HW/SW implementation has rather constant execution time between the cross-validation runs, aside from the negligible variations caused by the variances in the mutation execution times. On the other hand, in the pure software implementations, with each level of depth added to the DT, there is an additional iteration of the *find_dt_leaf_for_inst()* function (from the :num:`Algorithm #fig-find-dt-leaf-for-inst-pca`), contributing to the execution time as given by the equation :eq:`find_dt_leaf`. Since this is one of the major components of the total execution time, given by the equation :eq:`cplx_final`, the execution time varies noticeably between the cross-validation runs, hence the bigger confidence intervals for the pure software implementations.

.. _fig-speedup:

.. plot:: images/speedup_plot.py
    :width: 100%

    The speedup of the HW/SW implementation over a) the SW-ARM implementation, b) the SW-PC implementation and c) the SW-DSP implementation, given for each dataset listed in the :num:`Table #tbl-uci-datasets`

The :num:`Figure #fig-speedup` and the :num:`Table #tbl-results` suggest that the HW/SW implementation using the |cop| co-processor offers a substantial speedup in comparison to the pure software implementations, for the ARM, PC and the DSP. This is mainly because all processors that were used in the experiments have a limited number of on-chip functional units that can be used for multiplication and addition operations, as well as the limited number of internal registers to store the node test coefficient values and instance attributes. This means that the loop from the equation :eq:`oblique-test` can only be partially unrolled, when targeting these processors, which would be the case for any processor type. On the other hand, the |cop| co-processor can be configured to use as many multiplier/adder units as needed, and as many internal memory resources for storing coefficient and attribute values which can be accessed in parallel. Because of this, in case of |cop|, the loop from the equation :eq:`oblique-test` can be fully unrolled, therefore gaining the maximum available performance. Furthermore, the |cop| implementation used in the experiments, operates at much lower frequency (133MHz) than ARM (667MHz), PC (3.4GHz) and DSP (225 MHz) platforms. If the |cop| co-processor were implemented in the ASIC, the operating frequency would be increased by an order of magnitude, and the DT induction speedups would increase accordingly.
