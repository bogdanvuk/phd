
Co-processor for the DT ensemble induction - |ecop|
===================================================

.. _fig-system-bd:
.. bdp:: images/system_bd.py
    :width: 70%

    The |ecop| co-processor structure and integration with the host CPU

Proposed |ecop| co-processor performs the task of determining the accuracies of the DT individuals for the fitness evaluation tasks used in the DT ensemble induction. The |ecop| can calculate DT accuracies, i.e. the number of hits accumulated in the *hits* variable of the :num:`Algorithm #fig-fitness-eval-pca`, for all ensemble members in parallel. The co-processor is connected to the CPU via the AXI4 AMBA bus, which can be used by the software to completely control the |ecop| operation:

- Download of the training sets for each ensemble member
- Download of DT descriptions, including structural organization and coefficient values for all node tests present in the DTs
- Start of the accuracy evaluation process for each of the ensemble members individually
- Read-out of the vector of combined statuses of the accuracy evaluation processes for all ensemble members
- Read-out of the classification performance results for each of the ensemble members

The |ecop| co-processor structure and integration with the host CPU is depicted in the :num:`Figure #fig-system-bd`. The |ecop| consists of an array of DT accuracy evaluators: :math:`SMAE_1` (Single Member Accuracy Evaluator) to :math:`SMAE_{S^M}`, each of which can be used to evaluate the accuracy of the DT for a single ensemble member. Parameter |SM| represents the total number of |smae| units in the |ecop| and thus the maximal number of ensemble member accuracy evaluations that can be performed in parallel. Furthermore, the co-processor features the IRQ Status block that allows the user to read-out the operation status of all |smae|.

Single Member Accuracy Evaluator
--------------------------------

.. _fig-eftip:
.. bdp:: images/ensemble/eftip.py

    The |smae| module structure

The |smae| block evaluates the accuracy of the single DT individual. The major components of the |smae| block and their connections are depicted in the :num:`Figure #fig-eftip`:

- **Control Unit**: Provides AXI4 interface for the user to access the |smae| block. It acts as a gateway and demultiplexes and relays the read and write operations to the internal modules of the |smae| block. Furthermore, it implements the control logic of the accuracy evaluation flow and contains control registers for starting, stopping and restarting the accuracy evaluation process, as well as reading out the current evaluation status. When instructed by the user via the AXI4 interface to initiate the accuracy evaluation process, it signals the Training Set Memory to start to output the instances to the Classifier, waits for the instance classification to finish and the accuracy to be calculated by the Accuracy Calculator block, then generates the pulse on the *IRQ* output and stores the accuracy result for user to read it.
- **Classifier**: Implements the *find_dt_leaf_for_inst()* function from the :num:`Algorithm #fig-find-dt-leaf-for-inst-pca`, i.e. performs the DT traversal for each training set instance. Classifier comprises an array of *TLE* (Tree Level Evaluator) modules, which calculate instance traversal paths in parallel by pipelining the process. Each pipeline stage calculates the node test given by the equation :eq:`oblique-test` for one level of the DT, since the instance can only visit one node per level during the DT traversal. Based on the node test calculation result, it then passes the instance to the next *TLE* stage, i.e. next DT level, and informs the stage whether the traversal is to be continued via the right or the left child. The block for the node test calculation inside *TLE* is once again pipelined using the multipliers in parallel and the tree of adders. Maximum supported depth of the induced DT depends on the number of pipeline stages (|LM|). At the end of the pipeline, Classifier outputs for each instance the ID assigned to the leaf (variable *leaf_id* from the :num:`Algorithm #fig-fitness-eval-pca`) in which the instance finished the DT traversal (please refer to *fitness_eval()* function from the :num:`Algorithm #fig-fitness-eval-pca`).
- **Training Set Memory**: The memory for storing all training set instances that participate in the classification accuracy estimation for the single ensemble member. The memory is accessible via the AXI4 bus for the user to upload the training set to the |smae|.
- **DT Memory Array**: Comprises the array of memories, :math:`DTD_{1}` (DT Description) through :math:`DTD_{L_m}`, one per each DT level, i.e. one per each Classifier pipeline stage, to hold the description of the DT. Each Classifier pipeline stage requires its own *DTD* memory that holds the description of all nodes at the DT level the stage is associated with, since all calculations are performed in parallel.
- **Accuracy Calculator**: Implements the calculation of the class distribution matrix, dominant class and accuracy calculations described by the :num:`Algorithm #fig-fitness-eval-pca`. The *leaf_id* is received from the Classifier together with the known target class (variable *instance_class* from the the :num:`Algorithm #fig-fitness-eval-pca`) for each instance in the training set. Accuracy Calculator module comprises an array of *ACEs* (Accuracy Calculator Elements) with each of them associated to the specific leaf. Each *ACE* updates the part of the distribution matrix for the corresponding leaf and calculates its dominant class. After all instances are classified, the number of hits is calculated as the sum of the dominant classes hits calculated by the individual *ACEs*, and the result is sent to the Control Unit.

IRQ Status module
-----------------

IRQ Status module has been implemented in order to provide the user with the means of reading the statuses of all |smae| units with only one AXI4 read operation and thus optimize the AXI bus traffic. Each |smae| unit comprises an *IRQ* (interrupt request) signal used to inform the IRQ Status block that the |smae| unit has finished the accuracy evaluation. The IRQ Status block comprises an array of IRQ Status Word Registers which can all be read in a single burst via the AXI bus. Each IRQ Status Word is a 32-bit register (since |ecop| was optimized for 32-bit AXI) packed from the bits representing the statuses of up to 32 |smae| units. Each bit is called :math:`SMAE_i` Status Bit, where *i* denotes the ID of the |smae| unit whose status the bit is tracking, as shown in the :num:`Figure #fig-irq-status`. The figure shows IRQ Status register space for one specific |SM| value, but there are no limitations on the number of |smae| units that can be connected to the IRQ Status block. The bits of the IRQ Status Word Register are sticky, i.e. set each time the *IRQ* is signaled from the corresponding |smae| and cleared when the register is read by the user.

.. _fig-irq-status:
.. bdp:: images/ensemble/irq_status.py

    IRQ Status register space

Required Hardware Resources and Performance
-------------------------------------------

The |ecop| co-processor is implemented as an IP core with many customization parameters that can be configured at the design phase and are given in the :num:`Table #tbl-ens-cop-params`. These parameters mainly impose constraints on the maximum number of ensemble members that can be induced in parallel, the maximum size of the DT individual and the maximum size of the training set that can be used.

.. tabularcolumns:: c p{0.4\linewidth} p{0.4\linewidth}

.. _tbl-ens-cop-params:

.. list-table:: Customization parameters that can be configured at the design phase of the |ecop| co-processor
    :header-rows: 1
    :widths: 15 30 30

    * - Parameter
      - Description
      - Constraint
    * - |SM|
      - The number of |smae| units
      - The maximum number of ensemble members that can be induced in parallel
    * - |LM|
      - The number of *TLEs* in the |smae| block
      - The maximum depth of the induced DT
    * - |AM|
      - Determines: Training Set Memory width, :raw:`\newline`
        *DTD* width, :raw:`\newline`
        *TLE* multipliers count and adder tree size.
      - The maximum number of attributes training set can have
    * - :math:`R_A`
      - Determines: Training Set Memory width, :raw:`\newline`
        *DTD* memory width, :raw:`\newline`
        *TLE* adder tree size.
      - Resolution of induced DT coefficients
    * - :math:`R_C`
      - Parameter must be at least :math:`log_{2}(C_m)`
      - Resolution of the class ID
    * - :math:`C_m`
      - Accuracy Calculator memory depth
      - The maximum number of training set and induced DT classes
    * - |ACEM|
      - Number of Accuracy Calculator Elements
      - The maximum number of leaves of the induced DT
    * - |IM|
      - Training Set Memory depth
      - The number of training set instances that can be stored in |ecop| co-processor
    * - :math:`N_{lm}`
      - *DTD* memory depth
      - The maximum number of nodes per level of the induced DT

The amount of hardware resources required to implement the |ecop| co-processor is a function of the customization parameters given in the :num:`Table #tbl-ens-cop-params` and is given in the :num:`Table #tbl-ens-req-res` for various types of hardware resources. The :math:`N_{P}=\left \lceil log_{2}(\AM) + 2 \right \rceil` is the length of the *TLE* pipeline.

.. tabularcolumns:: p{0.2\linewidth} p{0.2\linewidth} p{0.5\linewidth}

.. _tbl-ens-req-res:

.. list-table:: Required hardware resources for the |ecop| architecture implementation
    :header-rows: 1

    * - Resource Type
      - Module
      - Quantity
    * - RAMs
      - Training Set Memory
      - :math:`\SM\cdot\IM\cdot (R_A*\AM + R_C)`
    * - (total number of bits)
      - *DTD* memory
      - :math:`\SM\cdot\LM\cdot N_{lm} \cdot (R_{A}\cdot(\AM + 1) + 2\cdot\LM + 2\cdot\left \lceil log_{2}(N_{lm}) \right \rceil)`
    * -
      - Accuracy Calculator
      - :math:`\SM\cdot ACE_m \cdot C_{m}\cdot \left \lceil log_{2}(\IM) \right \rceil`
    * -
      - *TLE*
      - :math:`\SM\cdot\LM\cdot N_P\cdot (R_{A}\cdot\AM + R_{C}) +` :raw:`\newline`
        :math:`\SM\cdot\LM\cdot N_P\cdot (R_{A} + 2\cdot\LM + 2\cdot\left \lceil log_{2}(N_{lm}) \right \rceil`
    * - Multipliers
      - *TLE*
      - :math:`\SM\cdot\LM\cdot \AM`
    * - Adders
      - *TLE*
      - :math:`\SM\cdot\LM \left \lceil log_{2}(\AM)  \right \rceil`
    * - Incrementers
      - Accuracy Calculator
      - :math:`\SM\cdot ACE_m`

As for the the number of clock cycles required to determine the accuracy for the single DT ensemble member, the Classifier has a throughput of one instance per clock cycle with the initial latency equal to the length of the pipeline :math:`N_{P}` and the Accuracy Calculator post-processing latency equals :math:`N_{C} + N_{l}`, i.e.:

.. math:: accuracy\_evaluation\_time = N_{Iass} + N_{P} + N_{C} + N_{l} \ clock\ cycles,

where, |NIass| designates the number of instances in the training set associated with the single DT ensemble member, |Nc| the total number of classes in the training set and |Nl| the number of leaves in the DT. Therefore, the accuracy evaluation time is dependent on the training set size.

.. _ens-hw-sw-speedup-estim:

Theoretical estimation of the acheivable speedup of the proposed HW/SW system
-----------------------------------------------------------------------------

In this section the speedup of the HW/SW implementation over the pure software implementation of the |ealgo| algorithm will be calculated as a function of the number of the ensemble members, |ne|:

.. math:: speedup(n_e) = \frac{\Tsw(n_e)}{\Ths(n_e)}
    :label: m-speedup-function

where |Tsw| and |Ths| denote the run times of the pure software and HW/SW implementations respectively. As discussed in the previous section, the good candidate for the hardware acceleration of the |ealgo| algorithm is the accuracy calculation task, while leaving the mutation to be implemented in the software. Hence, we will observe separately the contributions of these two parts to the total algorithm runtime. Furthermore, the hardware accelerator for the accuracy calculation task can be easily made to calculate the accuracy for each ensemble member in parallel, since there is no coupling between different members' induction processes. Runtime of the pure software implementation can be calculated as:

.. math:: \Tsw(n_e) = \Tswmut + \Tswacc
    :label: m-tsw-breakdown

where |Tswmut| and |Tswacc| denote the amount of time pure software implementation spends on the mutation and accuracy calculation tasks respectively. |Tswmut| is a linear function of |ne|, since the mutation is performed once per iteration per ensemble member. Hence, if the number of iterations is kept constant, we obtain:

.. math:: \Tswmut(n_e) = \Tswmut(1) \cdot n_e
    :label: m-tswmut-func

In this paper, the |ealgo| algorithm uses random sampling without replacement to generate the training sets for individual ensemble members. Hence, |Tswacc| is constant with respect to the |ne|, since the training set is divided amongst ensemble members, making the number of instances being classified and thus the amount of computation, constant. For the HW/SW implementation we obtain:

.. math:: \Ths(n_e) = \Thsmut(1) \cdot n_e + \Thsacc
    :label: m-ths-breakdown

where |Thsmut| and |Thsacc| denote the amount of the time HW/SW implementation spends on the mutation and accuracy calculation tasks respectively. |Thsmut| is implemented in the software and is a linear function of |ne| for the same reasons given for the |Tswmut|. Please observe that the |Thsmut| is somewhat greater than the |Tswmut| (:math:`\Thsmut = \Tswmut + \Delta_t`) since it also comprises the latency of the hardware accelerator interface operations, which is not present in the pure software implementation.

Because the HW/SW accuracy calculation is performed in parallel for all ensemble members, the calculation time is proportional to the size of the training set allocated for each ensemble member. Since the training set is divided equally among the ensemble members (using the DTEEP co-processor), |Thsacc| is inversely proportional to the |ne|:

.. math:: \Thsacc(n_e) = \frac{\Thsacc(1)}{n_e}
    :label: m-thsacc-func

By substituting equations :eq:`m-tsw-breakdown`, :eq:`m-tswmut-func`, :eq:`m-ths-breakdown` and :eq:`m-thsacc-func` into the :eq:`m-speedup-function`, we obtain:

.. math:: speedup(n_e) = \frac{\Tswmut(1) \cdot n_e + \Tswacc}{\Thsmut(1) \cdot n_e + \frac{\Thsacc(1)}{n_e}} = \frac{\Tswmut(1) \cdot n_e^{2} + \Tswacc \cdot n_e}{\Thsmut(1) \cdot n_e^{2} + \Thsacc(1)}
    :label: m-speedup-func-subst

|Tswacc| term was shown in the :num:`Section #eefti-profiling-res` to take almost all of the computational time. This parameter is heavily influenced by the amount of the computation needed to calculate the instance traversal (:num:`Algorithm #fig-find-dt-leaf-for-inst-pca`). Time needed to perform the DT traversal for all instances is proportional to the number of instances in the training set (|NI|), number of attributes |x| (equation :eq:`oblique-test`) and the depth of the DT. Depth of the DT is determined by the complexity of the training set data, but the larger training sets with higher |Nc| and |x| tend to require larger trees. The datasets that can be of interest to run DT ensemble induction on using the |ecop| are the ones that require significant time to execute in the software on the CPU. For these datasets :math:`\Tswacc \gg \Tswmut` and thus :math:`\Tswacc \gg \Thsmut`. By using the hardware acceleration and massive parallelism, :math:`\Tswacc \gg \Thsacc` is accomplished as well. By taking these parameter relationships into the account, :math:`speedup(n_e)` function given by the equation :eq:`m-speedup-func-subst` takes shape depicted in the :num:`Figure #fig-speedup-func-plot`.

.. _fig-speedup-func-plot:
.. plot:: images/ensemble/speedup_func_plot.py
    :width: 100%

    The shape of the :math:`speedup(n_e)` function given by the equation :eq:`m-speedup-func-subst`.

The plot in the :num:`Figure #fig-speedup-func-plot` suggests that accelerating the |ealgo| by a co-processor that performs the DT accuracy calculation in parallel for all ensemble members, will in the beginning provide increase in the speedup as the number of ensemble members increase. Then, after a speedup maximum has been reached, it will slowly degrade, but continue to offer a substantial speedup for all reasonable ensemble sizes. The maximum of the speedup can be found by seeking the maximum of the function given by the equation :eq:`m-speedup-func-subst`. By taking into the account parameter relationships, the point of the maximum of the :math:`speedup(n_e)` function can be expressed as follows:

.. math:: max(speedup(n_e))\approx\frac{\Tswacc}{2\sqrt{\Thsacc(1)\Thsmut(1)}}\ at\ n_e \approx \sqrt{\frac{\Thsacc(1)}{\Thsmut(1)}}
	:label: m-speedup-maximum

Furthermore, the :num:`Figure #fig-speedup-func-plot` shows that even though the speedup starts declining after reaching its maximum value for certain |ne|, the downslope is slowly flattening, and the significant speedup is achieved even for large ensemble sizes.

Software for the |ecop| assisted DT ensemble induction
------------------------------------------------------

.. _fig-ens_scheduling:
.. bdp:: images/ens_scheduling.py
    :caption: The pseudo-code of the |ealgo| algorithm using the |ecop| co-processor

.. _fig-ens_scheduling_parallel:
.. bdp:: images/ens_scheduling_parallel.py
    :caption: The pseudo-code of the |ealgo| algorithm using the |ecop| co-processor

As it was described in the previous chapters, the |ecop| co-processor can perform accuracy evaluation task in parallel for as many ensemble members as there are |smae| units within. Hence, in the HW/SW implementation of the |ealgo| algorithm, each of the |algo| tasks is assigned one |smae| unit to use exclusively for the acceleration of the accuracy evaluation for its DT individual. Since there is a single AXI bus connecting the CPU to the |ecop| co-processor, no two |algo| tasks can access it in the same time. Hence, a Scheduler task is needed to manage the access rights by using semaphores of the underlying operating system to signal that the access to the |ecop| has been granted to some task. The |ealgo| top level pseudo-code with added instantiation of the synchronization mechanism in the form of the Scheduler task and the semaphores is presented in the :num:`Algorithm #fig-co-design-sw-pca`.

.. _fig-co-design-sw-pca:
.. literalinclude:: code/co_design_sw.py
    :caption: The pseudo-code of the |ealgo| algorithm using the |ecop| co-processor

Furthermore, each of the tasks is assigned a unique ID (variable *smae_id* in the :num:`Algorithm #fig-co-design-efti-pca`), which serves as a handle to the semaphore and the |smae| unit of the |ecop| co-processor assigned to the task. Please notice that the hardware interface function pseudo-codes were omitted for brevity.

First let us show how each |algo| task (shown in the :num:`Algorithm #fig-algorithm-pca`) needs to be changed in order to support the use of the |ecop| co-processor. New |algo| pseudo-code for the HW/SW co-design is given by the :num:`Algorithm #fig-co-design-efti-pca`. Because the |ecop|'s memory space is mapped to the main CPU's memory space via the AXI4 bus, the *hw_load_training_set()* function simply copies all instances of the training set to the Training Set Memory address space of the assigned |smae| unit. The *smae_id* is used by all hardware interface functions to select the correct address space, i.e. to calculate the hardware addresses belonging to the assigned |smae| unit.

First, the training set needs to be loaded into the |smae| unit, since it will be needed to perform the accuracy calculation. Each time the DT individual is mutated its description needs to be reloaded into the DT Memory Array of the assigned |smae| unit. Since only small parts of the DT individuals are mutated in each iteration, only the changed parts can be loaded to the co-processor in order to optimize the AXI-bus traffic. Hence, the *mutate()* function is slightly changed to return the list of all changes it made to the DT individual into the *dt_diff* variable. The function *hw_load_dt_diff()* is then called to copy only these changes to the appropriate DT Memory Array locations of the assigned |smae| unit. Furthermore, if the new DT individual does not get selected for a new current best, the mutations need to be discarded. This is executed by the *hw_revert_dt_diff()* function, which undoes all the changes applied by the *hw_load_dt_diff()* function.

.. _fig-co-design-efti-pca:
.. literalinclude:: code/co_design_efti.py
    :caption: The pseudo-code of the modified |algo| task algorithm used in the HW/SW co-design implementation

The pseudo-code for the *fitness_eval()* function used in the HW/SW co-design implementation is shown in the :num:`Algorithm #fig-co-design-fitness-eval-pca`. With the training set and the DT description readily loaded into the co-processor, signal is sent to the the assigned |smae| unit to start the accuracy evaluation. After that, the task waits for the semaphore signal from the Scheduler task to indicate that the accuracy has been calculated and the access to the |ecop| has been granted to it. The call is issued to the function for waiting on semaphores of the underlying operating system, which suspends the task and performs the task switch to some other |algo| task which is ready for execution.

.. _fig-co-design-fitness-eval-pca:
.. literalinclude:: code/co_design_fitness_eval.py
    :caption: The pseudo-code of the fitness evaluation function used in the HW/SW co-design implementation

The pseudo-code of the Scheduler task is given in the :num:`Algorithm #fig-co-design-scheduler-pca`. The main function of the scheduler task is to monitor the IRQ Status Registers of the |ecop| co-processor and, based on its value, signal the semaphores assigned to the corresponding |algo| tasks. The Scheduler task reads the |ecop| co-processor status via the *hw_get_status()* function into the variable *status*. It then iterates over all bits of the variable *status* that correspond to the SMAE Status Bits, and checks which of them have the value of 1, meaning the corresponding |smae| unit has reported the end of the accuracy evaluation process. The corresponding |algo| task is then invoked by signaling the appropriate semaphore.

.. _fig-co-design-scheduler-pca:
.. literalinclude:: code/co_design_scheduler.py
    :caption: The pseudo-code of the Scheduler task used in the HW/SW co-design implementation

Experiments
-----------

To estimate the DT ensemble induction speedup of the HW/SW over the pure software implementation of the |ealgo| algorithm, the datasets listed in the :num:`Table #tbl-uci-datasets` were used and the results are given in this section. Ensembles of up to 25 members were induced from the datasets in the experiments.

Required Hardware Resources for the |ecop| co-processor
.......................................................

For the experiments, five different instances of the |ecop| co-processor were generated, one for each of the ensemble sizes used in the experiments: 2, 4, 8, 16 and 25. The values of the customization parameters, given in the :num:`Table #tbl-exp-params`, were chosen so that the generated co-processors could support the DT ensemble induction from all datasets of the :num:`Table #tbl-uci-datasets`. The datasets *mushroom*, *w21* and *wfr* were preprocessed using the PCA (Principal Component Analysis) to reduce their number of attributes to 16. This was done so that all datasets could fit in the |ecop| co-processor with parameter |AM| set to 16, in order to have smaller |ecop| footprint for the experiments.

.. tabularcolumns:: p{0.4\linewidth} *{5}{R{0.08\linewidth}}
.. _tbl-exp-params:
.. list-table:: Values of the customization parameters of the |ecop| co-processor instances, one for each of the ensemble sizes used in the experiments.
    :header-rows: 1

    * - Parameter
      - |SM| = 2
      - |SM| = 4
      - |SM| = 8
      - |SM| = 16
      - |SM| = 25
    * - DT max. depth (|LM|)
      - 5
      - 5
      - 5
      - 5
      - 5
    * - Max. attributes num. (|AM|)
      - 16
      - 16
      - 16
      - 16
      - 16
    * - Attribute encoding resolution (:math:`R_{A}`)
      - 16
      - 16
      - 16
      - 16
      - 16
    * - Class encoding resolution (:math:`R_{C}`)
      - 8
      - 8
      - 8
      - 8
      - 8
    * - Max. training set classes (:math:`C_{M}`)
      - 64
      - 64
      - 64
      - 64
      - 64
    * - Max. number of leaves (|ACEM|)
      - 16
      - 16
      - 16
      - 16
      - 16
    * - Max. number of training set instances (|IM|)
      - 24000
      - 12000
      - 6000
      - 4096
      - 2048
    * - Max. number of nodes per level (:math:`N_{lm}`)
      - 16
      - 16
      - 16
      - 16
      - 16

The VHDL language has been used to model the |ecop| co-processor and it was implemented using the Xilinx Vivado Design Suite 2015.2 software for the logic synthesis and implementation with the default synthesis and P&R options. From the implementation report files, device utilization data has been analyzed for the |ecop| co-processor instance with |SM| = 25 (:num:`Table #tbl-exp-params`), which has the largest footprint. The information about the number of used slices, BRAMs and DSP blocks has been extracted, and is presented in the :num:`Table #tbl-ens-utilization`, for different target FPGA devices. The operating frequency of 100 MHz of the system clock frequency was attained for all the implemented |ecop| co-processor instances from the :num:`Table #tbl-exp-params`.

.. tabularcolumns:: p{0.3\linewidth} *{3}{p{0.2\linewidth}}
.. _tbl-ens-utilization:
.. list-table:: FPGA resources required to implement the |ecop| co-processor with 25 |smae| units and the configuration given in the :numref:`tbl-exp-params`.
    :header-rows: 1

    * - FPGA Device
      - Slices/CLBs
      - BRAMs
      - DSPs
    * - xc7z100
      - 62091 (89%)
      - 412.5 (55%)
      - 2000 (99%)
    * - xcku115
      - 33231 (40%)
      - 412.5 (19%)
      - 2000 (36%)
    * - xc7vx690
      - 63885 (59%)
      - 412.5 (28%)
      - 2000 (56%)

Given in the brackets along with each resource utilization number is a percentage of used resources from the total resources available in the corresponding FPGA devices. :num:`Table #tbl-ens-utilization` shows that the implemented |ecop| co-processor fits into xc7z100 Xilinx FPGA device of the Zynq series, and into mid- to high-level Virtex7 and UltraScale Kintex7 Xilinx FPGA devices (xc7vx690 and xcku115).

Estimation of the Induction Speedup
...................................

For the experiments, the |ealgo| algorithm was implemented for three platforms (all software was written in the C programming language):

- **SW-PC**: Pure software implementation for the PC
- **SW-ARM**: Pure software implementation for the ARM Cortex-A9 processor
- **HW/SW**: The |ecop| co-processor implemented in the FPGA was used for the fitness evaluation, while all other tasks of the |ealgo| algorithm (shown in the :num:`Algorithm #fig-co-design-sw-pca`) were implemented in software for the ARM Cortex-A9 processor.

For the software implementations of the |ealgo| algorithm on the ARM platform, at first the FreeRTOS was used as the operating system since it has a port for the ARM Cortex-A9 and it is open source. However, experiments showed that it has rather high task switching latency, which degraded the execution speed of the HW/SW implementation. In lack of other open source RTOSes ported for the ARM Cortex-A9 that we could find, we developed a simple cooperative scheduler to be used for the SW-ARM and HW/SW implementations.

For the PC implementation, AMD Phenom(tm) II X4 965 (3.4 GHz) platform was used and the software was built using the GCC 4.8.2 compiler. For the SW-ARM and HW/SW implementations, ARM Cortex-A9 was used running at 667MHz. The software was built using the Sourcery CodeBench Lite ARM EABI 4.9.1 compiler (from within the Xilinx SDK 2015.2) and the |ecop| co-processor was built using the Xilinx Vivado Design Suite 2015.2.

Many optimization techniques were used for writing the software as described in the :num:`Section #eefti-profiling-res` in order to create the fastest possible software implementation and have a fair comparison with the HW/SW solution.

For all three |ealgo| algorithm implementations, experiments were carried out on all datasets from the :num:`Table #tbl-uci-datasets`. For each of the datasets, five experiments were performed in which the ensembles were induced with: 2, 4, 8, 16 and 25 members. For each of these experiments five 5-fold cross-validations has been carried out and the DT ensemble classifier induction times have been measured.

The results of the experiments are presented in the :num:`Table #tbl-ens-results`. The table contains the speedups of the HW/SW implementation over the SW-ARM and SW-PC implementations for each dataset and the ensemble size. At the bottom of the table, the average speedups are given for each ensemble size.

.. tabularcolumns:: l || *{5}{R{0.07\linewidth}} || *{5}{R{0.07\linewidth}}
.. _tbl-ens-results:
.. csv-table:: The speedups of the HW/SW implementation over the SW-ARM and SW-PC implementations for each dataset and ensemble size.
    :header-rows: 1
    :file: scripts/results.csv

:num:`Table #tbl-ens-results` indicates that the average speedup of the HW/SW implementation is between 65 and 130 times over the SW-ARM and between 5 and 10 times over the SW-PC implementation, depending on the number of the ensemble members induced. It can be seen that the speedups follow the theoretical curve from the :num:`Figure #fig-speedup-func-plot` shown in the Section `Theoretical estimation of the acheivable speedup of the proposed HW/SW system`_, which is also visible in the :num:`Figure #fig-speedup`. In the :num:`Figure #fig-speedup` each bar represents the speedup for one ensemble size, hence the envelope of the bar graph for each dataset correlates with the theoretical speedup curve. It should be noted that the envelopes appear distorted, since ensemble sizes for which the speedups are drown as bars are not equidistant, but follow the exponential function. By observing the speedup of the HW/SW implementation over the pure software implementations shown in the :num:`Table #tbl-ens-results` for each dataset and the datasets' characteristics given in the :num:`Table #tbl-uci-datasets`, it can be seen that more speedup is gained for datasets with larger |NI|, |NA| and |Nc|.

.. _fig-speedup:
.. plot:: images/ensemble/speedup_plot.py
    :width: 100%

    Speedup of the HW/SW implementation over a)
    SW-ARM implementation and b) SW-PC implementation, given for each dataset listed in the :num:`Table #tbl-uci-datasets`. Each bar represents a speedup for one ensemble size.

:num:`Figure #fig-speedup` and :num:`Table #tbl-ens-results` suggest that the HW/SW implementation using |ecop| co-processor offers a substantial speedup in comparison to pure software implementations for both PC and ARM. Furthermore, |ecop| implementation used in the experiments operates at much lower frequency (100MHz) than both ARM (667MHz) and PC(3.4GHz) platforms. If |ecop| co-processor were implemented in ASIC, the operating frequency would be increased by an order of magnitude, and the DT induction speedup would increase accordingly.
