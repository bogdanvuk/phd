
Co-processor for the DT ensemble induction - |ecop|
===================================================

.. _fig-ens-cop-system-bd:
.. bdp:: images/ens_cop_system_bd.py
    :width: 80%

    The |ecop| co-processor structure and integration with the host CPU

For the induction of a single DT, it was already demonstrated that the |cop| co-processor can be used in a HW/SW architecture to achieve substantial speedups over the pure software implementation of the |algo| algorithm. Furthermore, it was explained in the :num:`Section #profiling-results` what was behind the decision to accelerate only the accuracy calculation task in hardware. Hence, in an attempt to achieve the same benefits for the DT ensemble induction, the |ecop| co-processor proposed in this section was implemented using |cop| as a module for the accuracy calculation. However, the |ecop| co-processor also takes advantage of the intrinsic parallelism of the Bagging algorithm to achieve even higher speedups when compared to the pure software implementation of the |ealgo| algorithm.

The |ecop| co-processor structure and integration with the host CPU is depicted in the :num:`Figure #fig-ens-cop-system-bd`. The |ecop| consists of an array of |cop| modules, described in the :num:`Section #sec-cop`, :math:`\textit{EFTIP}_1` to :math:`\textit{EFTIP}_{S^M}`, each of which can be used to evaluate the accuracy of the DT individual for the induction of one ensemble member. Each |cop| has its own address space and can be individually accessed for all operation described in the :num:`Section #sec-cop`. In addition, the co-processor features the IRQ Status (Interrupt Request Status) block that allows the user to read-out the operation status of all |cop| units. The maximal number of ensemble member accuracy calculations that can be performed in parallel equals the total number of the |cop| units in the |ecop| co-processor, which is a parameter that can be set during the design time of the |cop| co-processor, and is called |SM|.

IRQ Status module
-----------------

IRQ Status module has been implemented in order to provide the user with the means of reading the statuses of all |cop| units with only one AXI4 read operation and thus optimize the AXI bus traffic. Each |cop| unit comprises an IRQ (Interrupt Request) port for signaling the end of the accuracy calculation, which was in turn connected to the IRQ Status block of the |ecop| co-processor. The IRQ Status block comprises an array of IRQ Status Word Registers representing the statuses of all |cop| units, which can all be read in a single burst via the AXI bus. Additionally, the IRQ Status block provides a combined IRQ signal, which is triggered each time any of the |cop| units signal their corresponding IRQ outputs, i.e. each time any of the |cop| units finish the accuracy calculation.

Each IRQ Status Word is a 32-bit register (since |ecop| was optimized for 32-bit AXI) packed from the bits representing the statuses of up to 32 |cop| units each. Each bit is called :math:`\textit{EFTIP}_i` Status Bit, where *i* denotes the ID of the |cop| unit whose status the bit is tracking, as shown in the :num:`Figure #fig-irq-status`. The figure shows IRQ Status register space for one specific |SM| value, but there are no limitations on the number of |cop| units that can be connected to the IRQ Status block. The bits of the IRQ Status Word Register are sticky, i.e. set each time the IRQ is signaled from the corresponding |cop| and cleared when the register is read by the user.

.. _fig-irq-status:
.. bdp:: images/ensemble/irq_status.py

    IRQ Status register space

.. _ens-hw-sw-speedup-estim:

Theoretical estimation of the acheivable speedup of the proposed HW/SW system
-----------------------------------------------------------------------------

In this section the speedup of the HW/SW implementation over the pure software implementation of the |ealgo| algorithm will be calculated as a function of the number of the ensemble members, |ne|:

.. math:: \text{speedup}(n_e) = \frac{\Tsw(n_e)}{\Ths(n_e)}
    :label: m-speedup-function

where |Tsw| and |Ths| denote the run times of the pure software and HW/SW implementations respectively. As already discussed, the good candidate for the hardware acceleration of the |ealgo| algorithm is the accuracy calculation task, while leaving the mutation and selection to be implemented in software has some flexibility benefits. Hence, the contributions of these two parts to the total algorithm runitme will be observed separately:

.. math:: \text{speedup}(n_e) = \frac{\Tswms(n_e) + \Tswacc(n_e)}{\Thsms(n_e) + \Thsacc(n_e)}
    :label: m-t-breakdown

where |Tswms| and |Tswacc| denote the amount of time pure software implementation spends on the mutation/selection and the accuracy calculation tasks respectively, while |Thsms| and |Thsacc| represent the same values for the HW/SW implementation. |Tswms| and |Thsms| are linear functions of |ne|, since the mutation is performed once per iteration per ensemble member. Hence, if the number of iterations is kept constant, we obtain:

.. math::
    :label: m-tms-func

    \begin{aligned}
    \Tswms(n_e) &= \Tswms(1) \cdot n_e, \\
    \Thsms(n_e) &= \Thsms(1) \cdot n_e,
    \end{aligned}

which when combined with the equation :eq:`m-t-breakdown` yield the following:

.. math:: \text{speedup}(n_e) = \frac{\Tswms(1)\cdot n_e + \Tswacc(n_e)}{\Thsms(1)\cdot n_e + \Thsacc(n_e)}
    :label: m-speedup-breakdown

Please observe that the |Thsms| is somewhat greater than the |Tswms| (:math:`\Thsms = \Tswms + \Delta_t`) since it also comprises the latency of the hardware accelerator interface operations, which is not present in the pure software implementation.

Depending on which approach to forming the training subsets is used, |Tswacc| and |Thsacc| will behave differently with respect to |ne|. When random sampling without replacement is used, |Tswacc| and |Thsacc| are constant with respect to |ne|, since the training set is partitioned amongst ensemble members, making the number of instances being classified and thus the amount of computation, constant. However, when random sampling with replacement is used, these times will tend to grow with |ne| with the worst case being when :math:`N_{IS} = N_I`, i.e. when whole training set is used for each individual. Hence, the behavior of the speedup for these two corner cases will be discussed next.

Random sampling without replacement
...................................

Because the HW/SW accuracy calculation is performed in parallel for all ensemble members, the calculation time is proportional to the size of the training subset allocated for each ensemble member. Since the training set is divided equally among the ensemble members (using the |ecop| co-processor), |Thsacc| is inversely proportional to the |ne|:

.. math:: \Thsacc(n_e) = \frac{\Thsacc(1)}{n_e}
    :label: m-thsacc-func

By incorporating the fact that |Tswacc| is constant in this case and substituting equation :eq:`m-thsacc-func` into the :eq:`m-speedup-function`, we obtain:

.. math:: \text{speedup}(n_e) = \frac{\Tswms(1) \cdot n_e + \Tswacc}{\Thsms(1) \cdot n_e + \frac{\Thsacc(1)}{n_e}} = \frac{\Tswms(1) \cdot n_e^{2} + \Tswacc \cdot n_e}{\Thsms(1) \cdot n_e^{2} + \Thsacc(1)}
    :label: m-speedup-func-subst

|Tswacc| term was shown in the :num:`Section #sec-complexity` and the :num:`Section #profiling-results` to take almost all of the computational time. The datasets that can be of interest to run DT ensemble induction on using the |ecop| are the ones that require significant time to execute in the software on the CPU. For these datasets :math:`\Tswacc \gg \Tswms` and thus :math:`\Tswacc \gg \Thsms`. By using the hardware acceleration and massive parallelism, :math:`\Tswacc \gg \Thsacc` is accomplished as well. By taking these parameter relationships into the account, :math:`\text(speedup)(n_e)` function given by the equation :eq:`m-speedup-func-subst` takes shape depicted in the :num:`Figure #fig-speedup-func-plot`.

.. _fig-speedup-func-plot:
.. plot:: images/ensemble/speedup_func_plot.py
    :width: 100%

    The shape of the :math:`\text{speedup}(n_e)` function given by the equation :eq:`m-speedup-func-subst`.

The plot in the :num:`Figure #fig-speedup-func-plot` suggests that accelerating the |ealgo| by a co-processor that performs the DT accuracy calculation in parallel for all ensemble members, will in the beginning provide increase in the speedup as the number of ensemble members increase. Then, after a speedup maximum has been reached, it will slowly degrade, but continue to offer a substantial speedup for all reasonable ensemble sizes. The maximum of the speedup can be found by seeking the maximum of the function given by the equation :eq:`m-speedup-func-subst`. By taking into the account parameter relationships, the point of the maximum of the :math:`\text{speedup}(n_e)` function can be expressed as follows:

.. math:: max(\text{speedup}(n_e))\approx\frac{\Tswacc}{2\sqrt{\Thsacc(1)\Thsms(1)}}\ at\ n_e \approx \sqrt{\frac{\Thsacc(1)}{\Thsms(1)}}
	:label: m-speedup-maximum

Furthermore, the :num:`Figure #fig-speedup-func-plot` shows that even though the speedup starts declining after reaching its maximum value for certain |ne|, the downslope is slowly flattening, and the significant speedup is achieved even for large ensemble sizes.

Whole training set for each member
..................................

In this case, the total number of instances in the ensemble rises linearly with the number of ensemble members. This means that |Tswacc| will rise linearly and |Thsacc| will remain constant being that it is performed in parallel. This yield the following form for the speedup function:

.. math:: \text{speedup}(n_e) = \frac{\Tswms(1) \cdot n_e + \Tswacc(1) \cdot n_e}{\Thsms(1) \cdot n_e + \Thsacc(1)}
    :label: m-speedup-whole-subst

Taking into the account that :math:`\Tsw = \Thsms + \Tswacc`, and rearanging the equation :eq:`m-speedup-whole-subst`, the following is obtained:

.. math:: \text{speedup}(n_e) = \frac{\Tsw(1)}{\Thsms(1)}\cdot\frac{1}{1 + \frac{\Thsacc(1)}{\Thsms(1) \cdot n_e}}
    :label: m-speedup-whole-rearange

The equation :eq:`m-speedup-whole-rearange` shows that the speedup increases with the number of ensemble members induced and asymptotically converges to the ratio of the total time needed for the single member induction in software (:math:`\Tsw(1)`) to the time needed for the mutation/selection tasks in the HW/SW co-design implementation (:math:`\Thsms(1)`), which basically means that the speedup can be increased by optimizing the execution time of the mutation/selection tasks and the communication with the co-processor.

Software for the |ecop| assisted DT ensemble induction
------------------------------------------------------

As it was described in the previous chapters, the |ecop| co-processor can perform accuracy evaluation task in parallel for as many ensemble members as there are |cop| units within. Hence, in the HW/SW implementation of the |ealgo| algorithm, each of the |algo| tasks is assigned one |cop| unit to use exclusively for the acceleration of the accuracy evaluation for its DT individual. Since there is a single AXI bus connecting the CPU to the |ecop| co-processor, no two |algo| tasks can access it in the same time.

The |algo| tasks could be left alone to compete for the rights to use |ecop| and check whether their corresponding |cop| unit has finished computing the accuracy, but there is a more economical approach that utilizes the IRQ Status module of the |ecop| co-processor. In this approach, the |algo| tasks are disallowed to poll the status registers of their |cop| units. Their responsibility is to load the DT individuals and start the accuracy calculation process. On the other hand a management task, called the Scheduler, is introduced to exclusively monitor the registers of the IRQ Status module and inform the individual |algo| tasks about the completion of their accuracy calculation processes. This is done by using semaphores of the underlying operating system, which are used to signal the |algo| tasks that the accuracy calculation has been completed and the access to the |ecop| has been now granted to them, so that they can update the DT information and start the new calculation cycle. As soon as the accuracy calculation on their corresponding |cop| unit is started, the control is given back to the Scheduler task and |algo| waits for the new completion signal via semphore.

.. _fig-co-ens-scheduler-pca:
.. literalinclude:: code/co_ens_scheduler.py
    :caption: The pseudo-code of the Scheduler task used in the HW/SW co-design implementation

The pseudo-code for the Scheduler task is given in the :num:`Algorithm #fig-co-ens-scheduler-pca`. The main task of the Scheduler task is to poll the IRQ Status register (whose address is returned by the ``eeftip_irq_status_addr()`` helper function) of the |ecop| co-processor in a loop. It then iterates through the received status value to check which |cop| units have reported to have finished the accuracy calculation, and activates the correponding |algo| tasks. After all the required tasks have been informed, the Scheduler issues a call to the ``context_switch()`` function of the underlying OS, so that the OS can serve the other tasks that have been activated via emited semaphores. The loop ends when all the tasks have finished the induction and exited, which is monitored by the ``all_finished()`` helper function.

.. _fig-co-ens-algorithm-pca:
.. literalinclude:: code/co_ens_algorithm.py
    :caption: The pseudo-code of the |ealgo| algorithm using the |ecop| co-processor

The |ealgo| top level pseudo-code with the added instantiation of the synchronization mechanism in the form of the Scheduler task and the semaphores is presented in the :num:`Algorithm #fig-co-ens-algorithm-pca`. In addition to the training set and the reference to the result object ``r``, each of the |algo| tasks created is assigned a semaphore handle, and the unique ID (variable ``eftip_id``) that serves as a handle to the |cop| unit of the |ecop| co-processor assigned to the task. After all the |algo| tasks have been created, the control is transfered to the Scheduler task until all ensemble members have been induced.

The HW/SW implementation of almost all of the |algo| tasks, which were described in the :num:`Section #sec-cop-sw`, is used almost verbatim for the HW/SW implementation of the |ealgo| algorithm. One difference is that here a co-processor with multiple |cop| units is accessed by the software. Hence, all the helper functions of the HW/SW implementation of the |algo| algorithm for calculating the appropriate hardware memory addresses, need now to take into the account the ID of the |cop| unit (``eftip_id``) they are interfacing. The second change needed was to adapt the code from the :num:`Algorithm #fig-accuracy-calc-pca` for the ``accuracy_calc()`` function to support the described protocol for the access rights delegation using semaphores. The adapted function pseudo-code is shown in the :num:`Algorithm #fig-co-ens-accuracy-calc-pca`.

.. _fig-co-ens-accuracy-calc-pca:
.. literalinclude:: code/co_ens_accuracy_calc.py
    :caption: The pseudo-code of the fitness evaluation function used in the HW/SW co-design implementation

The :num:`Figure #fig-ens-scheduling` shows the benefits of careful scheduling scheme over the naive solution where each |algo| task is let to finish whole iteration before the other is let to start. The diagram in the figure shows how occupied with different |algo| tasks is the CPU and the |ecop| co-processor for these two different scenarios, where the operations related to the different |algo| tasks are given in different colors. Time periods marked with letters M and S represent the mutation and selection tasks respectively, and the idle periods of the CPU are showed hatched in figure.

With the naive approach shown in the :num:`Figure #fig-ens-scheduling-sequential`, a lot of CPU time is waisted on waiting for the accuracy calculation to finish, and the potential of the parallel |cop| units is not exploited. By introducing the Scheduler task and making the ``accuracy_calc()`` function suspend its execution and return the control back as soon as it finishes with the mutation task, sets and starts the accuracy calculation on its corresponding |cop| unit, the HW/SW architecture that uses the |ecop| co-processor can be exploited to its full potential, which leads to the timing diagram shown in the :num:`Figure #fig-ens-scheduling-parallel`.

.. subfigstart::

.. _fig-ens-scheduling-sequential:
.. bdp:: images/ens_scheduling.py

    Sequential operation

.. _fig-ens-scheduling-parallel:
.. bdp:: images/ens_scheduling_parallel.py

    Interlaced operation

.. subfigend::
    :width: 1
    :label: fig-ens-scheduling

    Achieving the maximum CPU utilization by interlacing the inducion operations of different ensemble members **(b)**, as opposed to performing these operations sequentially **(a)**. Time periods marked with letters M and S represent mutation and selection tasks respectively, and the idle periods of the CPU are showed hatched in figure. The operations related to the different |algo| tasks are given in different colors.

Experiments
-----------

To estimate the DT ensemble induction speedup of the HW/SW implementation over the pure software implementation of the |ealgo| algorithm, the experiments have been performed on the induction of the ensembles of up to 25 members and the results are given in this section. In order to support the datasets with higher number of intances, the random sampling without replacement was used to form the training subsets, in order to make them smaller.

Required Hardware Resources for the |ecop| co-processor
.......................................................

For the experiments, five different instances of the |ecop| co-processor were generated, one for each of the ensemble sizes used in the experiments: 2, 4, 8, 16 and 25. The values of the customization parameters, given in the :num:`Table #tbl-ens-exp-params`, were chosen so that the generated co-processors could fit inside the xc7z100 Xilinx Zynq device that was used for testing.

.. raw:: latex

   \begingroup
   \setlength{\tabcolsep}{.2em}

.. tabularcolumns:: p{0.44\linewidth} *{5}{R{0.1\linewidth}}
.. _tbl-ens-exp-params:
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

.. raw:: latex

   \endgroup

The VHDL language has been used to model the |ecop| co-processor and it was implemented using the Xilinx Vivado Design Suite 2015.2 software for the logic synthesis and implementation with the default synthesis and P&R options. From the implementation report files, device utilization data has been analyzed for the |ecop| co-processor instance with |SM| = 25 (:num:`Table #tbl-exp-params`), which has the largest footprint. The information about the number of used slices, BRAMs and DSP blocks has been extracted, and is presented in the :num:`Table #tbl-ens-utilization`, for different target FPGA devices. The operating frequency of 100 MHz of the system clock frequency was attained for all the implemented |ecop| co-processor instances from the :num:`Table #tbl-exp-params`.

.. tabularcolumns:: p{0.3\linewidth} *{3}{p{0.2\linewidth}}
.. _tbl-ens-utilization:
.. list-table:: FPGA resources required to implement the |ecop| co-processor with 25 |cop| units and the configuration given in the :numref:`tbl-exp-params`.
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

For the software implementations of the |ealgo| algorithm on the ARM platform, at first the FreeRTOS was used as the operating system since it has a port for the ARM Cortex-A9 and it is open source. However, experiments showed that it has rather high task switching latency, which degraded the execution speed of the HW/SW implementation. In lack of other open source RTOSes ported for the ARM Cortex-A9 that we could find, a simple simple cooperative scheduler was developped to be used for the SW-ARM and HW/SW implementations.

For the PC implementation, a 64-bit, 4-core, Intel i5-2500K CPU operating at approximately 3.5GHz, with 8GB or RAM, running Ubuntu 16.04 operating system platform was used and the software was built using the GCC 5.4.1 compiler. For the SW-ARM and HW/SW implementations, ARM Cortex-A9 was used running at 667MHz. The software was built using the Sourcery CodeBench Lite ARM EABI 4.9.1 compiler (from within the Xilinx SDK 2015.2) and the |ecop| co-processor was built using the Xilinx Vivado Design Suite 2015.2.

Not all of the datasets from the :num:`Table #tbl-uci` were used in these experiments for two different reasons. Some of the datasets, like ``ausc``, ``bc``, ``bcw``, ``ger``, ``gls``, ``hep``, ``hrtc``, ``hrts``, ``ion``, ``irs``, ``liv``, ``lym``, ``pid``, ``son``, ``ttt``, ``veh``, ``vote``, ``vow`` and ``zoo``, have too few instances to support induction of up to 25 members using training set partitioning by sampling without replacement. On the other hand, some datasets like ``sick`, ``spf``, ``thy`` and ``w40`` had too many attributes to fit into the implemented co-processors. The others, like ``mushroom``, ``w21`` and ``wfr`` were preprocessed using the PCA (Principal Component Analysis) to reduce their number of attributes to 16, what the implemented co-processors support. For each of the datasets, five experiments were performed in which the ensembles were induced with: 2, 4, 8, 16 and 25 members. For each of these experiments five 5-fold cross-validations has been carried out and the DT ensemble classifier induction times have been measured.

The results of the experiments are presented in the :num:`Table #tbl-ens-results`. The table contains the speedups of the HW/SW implementation over the SW-ARM and SW-PC implementations for each dataset and the ensemble size. At the bottom of the table, the average speedups are given for each ensemble size.

.. raw:: latex

   \begingroup
   \setlength{\tabcolsep}{.2em}

.. tabularcolumns:: p{0.1\linewidth} || *{5}{R{0.082\linewidth}} || *{5}{R{0.07\linewidth}}
.. _tbl-ens-results:
.. csv-table:: The speedups of the HW/SW implementation over the SW-ARM and SW-PC implementations for each dataset and ensemble size.
    :header-rows: 2
    :file: scripts/co_ens_results.csv

.. raw:: latex

   \endgroup

:num:`Table #tbl-ens-results` indicates that the average speedup of the HW/SW implementation is between 26 and 52 times over the SW-ARM and between 10 and 20 times over the SW-PC implementation, depending on the number of the ensemble members induced. It can be seen that the speedups follow the theoretical curve from the :num:`Figure #fig-speedup-func-plot` shown in the Section `Theoretical estimation of the acheivable speedup of the proposed HW/SW system`_, which is also visible in the :num:`Figure #fig-ens-speedup`. In the :num:`Figure #fig-ens-speedup` each bar represents the speedup for one ensemble size, hence the envelope of the bar graph for each dataset correlates with the theoretical speedup curve. It should be noted that the envelopes appear distorted, since ensemble sizes for which the speedups are drown as bars are not equidistant, but follow the exponential function. By observing the speedup of the HW/SW implementation over the pure software implementations shown in the :num:`Table #tbl-ens-results` for each dataset used in the experiments, it can be seen that more speedup is gained for datasets with larger |NI|, |NA| and |Nc|.

.. _fig-ens-speedup:
.. plot:: images/ensemble/speedup_plot.py
    :width: 100%

    Speedup of the HW/SW implementation over a)
    SW-ARM implementation and b) SW-PC implementation, given for each dataset listed in the :num:`Table #tbl-uci-datasets`. Each bar represents a speedup for one ensemble size.

:num:`Figure #fig-speedup` and :num:`Table #tbl-ens-results` suggest that the HW/SW implementation using |ecop| co-processor offers a substantial speedup in comparison to the pure software implementations for both PC and ARM. Furthermore, the |ecop| implementation used in the experiments operates at much lower frequency (100MHz) than both ARM (667MHz) and PC(3.4GHz) platforms. If |ecop| co-processor were implemented in ASIC, the operating frequency would be increased by an order of magnitude, and the DT induction speedup would increase accordingly.
