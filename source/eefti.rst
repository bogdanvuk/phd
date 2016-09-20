.. include:: conf.rst

|ealgo| algorithm
=================

In this section, the |ealgo| algorithm for the induction of DT ensembles using the full DT induction approach based on the EA is described. Only one individual per ensemble member is required for the induction by the |algo| algorithm. Each individual represents the best DT evolved up to the current iteration for its corresponding ensemble member. Because |algo| uses supervised learning, the training set used to induce the ensemble consists of the problem instances together with their corresponding class memberships. Since the |ealgo| uses the Bagging algorithm, one subset of the training set is generated for each ensemble member which will be used to induce it. Two common ways of forming the subsets are:

- **random sampling without replacement** - formed subsets are disjoint sets of size :math:`N_{Iass}=\frac{N_I}{n_e}`, and
- **random sampling with replacement** - formed subsets are of size :math:`N_{Iass} \leq N_I`,

where |NI| is the size of the training set and |ne| the number of subsets, i.e. ensemble members. Each ensemble member starts off as a randomly generated one-node DT and the algorithm iteratively tries to improve on it. DT is slightly changed, i.e. mutated, in each iteration, and let to perform classification of its corresponding subset of the training set. The known training set classification is then used to calculate the quality of the classification results. When the newly mutated DT performs better at the classification than its predecessor, it is promoted to the new current best individual for its ensemble member and will become the base for the mutations in the following iterations, until a better one is found. After the desired number of iterations, the algorithm exits and returns the set of best DT individuals, one for each ensemble member.

.. _fig-algorithm-pca:
.. literalinclude:: code/algorithm.py
    :caption: Overview of the |ealgo| algorithm

The :num:`Algorithm #fig-algorithm-pca` shows the |ealgo| algorithm. Please note that all algorithms in this paper are described in the Python language style and that many details have been omitted for the sake of clarity. The |algo| algorithm is used for the induction of each ensemble member since it is suitable for the hardware acceleration (it uses only one individual for the induction and creates smaller DTs with no loss of accuracy compared to many other well-known algorithms :cite:`vukobratovic2015evolving`). It was decided to implement the Bagging algorithm for the |ealgo|, since the induction process of one ensemble member is then uninfluenced by the induction processes of other ensemble members in any way, hence they can be performed in separate tasks, created by a successive calls to the *create_task* function in the :num:`Algorithm #fig-algorithm-pca`. These tasks implement the |algo| algorithm whose pseudo-code is shown in the :num:`Algorithm #fig-task-pca`. The |ealgo| first divides the training set in the subsets using the *divide_train_set()* function and stores them in the array *task_train_sets*. The result array is then created using the *initialize_result_array()* function and stored in the *res* variable. The *res* array contains one item for each ensemble member, to which the corresponding |algo| will output induced DTs and various miscellaneous corresponding statistical data. Next, the |algo| tasks are created, assigned their corresponding *task_train_sets* and *res* items, and started. The |ealgo| waits for the completion of all |algo| tasks and returns the *res* array populated by them.

.. tabularcolumns:: l p{30pt} p{40pt} p{40pt} p{40pt}
.. _tbl-ens-vs-single:
.. csv-table:: The accuracies of the ensembles with various numbers of elements
    :header-rows: 1
    :file: scripts/ens_vs_single.csv

**Ubaci ANOVA rankove takodje, da se vidi da su ansambli konzistentiniji**

.. _eefti-profiling-res:

EEFTI algorithm profiling results
---------------------------------

In order to decide which part of the |ealgo| algorithm should be accelerated in the hardware, the profiling was performed on the |ealgo| algorithm software implementation. The software implementation of the |ealgo| algorithm was realized in the C programming language, with many optimization techniques employed:

- node test evaluation loop (within *evaluate_node_test()* function in :num:`Algorithm #fig-find-dt-leaf-for-inst-pca`) has been unfold
- all arithmetic operation were performed using 64-bit operands (optimized for the 64-bit CPU which was used for profiling),
- compiler optimization settings were set to maximum for speed, etc.

To perform the experiments, 18 datasets, presented in the :num:`Table #tbl-uci-datasets`, were selected from the UCI benchmark datasets database :cite:`newman1998uci`. UCI database is commonly used database in the machine learning community to estimate and compare performance of different machine learning algorithms.

.. tabularcolumns:: l p{30pt} p{40pt} p{40pt} p{40pt}
.. _tbl-uci-datasets:
.. list-table:: Characteristics of the UCI datasets used in the experiments
    :header-rows: 1

    * - Dataset Name
      - Short Name
      - No. of attributes
      - No. of instances
      - No. of classes
    * - Adult
      - adult
      - 14
      - 48842
      - 2
    * - Bank Marketing
      - bank
      - 16
      - 45211
      - 2
    * - Bach Choral Harmony
      - bch
      - 16
      - 5665
      - 60
    * - Clave Vectors Firm Teacher Model
      - cvf
      - 15
      - 10800
      - 7
    * - Tamilnadu Electricity Board Hourly Readings
      - eb
      - 4
      - 45781
      - 31
    * - EEG Eye State
      - eye
      - 14
      - 14980
      - 2
    * - Japanese Vowels
      - jvow
      - 14
      - 4274
      - 9
    * - White King and Rook against Black King
      - kpt
      - 6
      - 28056
      - 18
    * - Letter Recognition
      - ltr
      - 16
      - 20000
      - 26
    * - MAGIC Gamma Telescope
      - magic
      - 10
      - 19020
      - 2
    * - Mushroom
      - msh
      - 22
      - 8124
      - 2
    * - Nursery
      - nrs
      - 8
      - 12960
      - 5
    * - Page Block Classification
      - page
      - 10
      - 5473
      - 5
    * - Pen Based Recognition of Handwritten Digits
      - pen
      - 16
      - 10992
      - 10
    * - Statlog Shuttle
      - sht
      - 9
      - 58000
      - 7
    * - Waveform Database Generator
      - w21
      - 21
      - 5000
      - 3
    * - Wall Following Robot Navigation
      - wfr
      - 24
      - 5456
      - 4
    * - Wine Quality
      - wine
      - 11
      - 4898
      - 7

GCC 4.8.2 compiler was used to compile the software implementation of the |ealgo| algorithm and GProf to profile it on each of the UCI datasets listed in the :num:`Table #tbl-uci-datasets`. It was run on the AMD Phenom(tm) II X4 965 (3.4 GHz) based computer and the results obtained by the profiling are shown in the :num:`Figure #fig-profiling-plot`. All tests were performed by inducing a single member ensemble, since the results obtained in this way are then convenient for conducting the calculation of the arbitrary size ensemble induction performance as discussed in the :num:`Figure #ens-hw-sw-speedup-estim`. The figure shows percentage of the total execution time spent in the *fitness_eval()* function and its subfuctions for each dataset. On average, |ealgo| spent 98.9% of time calculating the fitness of the individuals.

.. _fig-profiling-plot:
.. plot:: images/ensemble/profiling_plot.py
    :width: 100%

    Percentage of time spent in the *fitness_eval()* function and its subfuctions for each dataset listed in the :num:`Table #tbl-uci-datasets`

The results for one example profiling experiment on the *magic* dataset are given in the :num:`Figure #fig-profiling`. Each row in the table provides the profiling data for one function with the following data:

- **Name** - The name of the function
- **Time** - Total amount of time spent in the function
- **Calls** - Total number of calls to the function
- **% Time** - Percentage of time spent in the function relative to the total execution time.

.. _fig-profiling:
.. figure:: images/profiling.png

    Profiling results of the |ealgo| algorithm's C implementation.

Fitness evaluation task comprises the following functions from the table : *evaluate node test()*, *find_dt_leaf_for_inst()* and *find_node_distribution()*. The percentage of execution time spent in the fitness evaluation task can be obtained by summing the execution times of these three functions, which adds up to 98.7% of total time for this particular dataset.

The certain candidate for the hardware acceleration is thus the fitness evaluation operation, since it takes 98.9% of the total computational time on average. All other operations (DT initialization, DT mutation and individual selection) were decided to be left in the software, since they require significantly less amount of time to complete. On the other hand, by leaving these operations in the software the design remains flexible for experimenting with different algorithms for DT mutation, Bagging and individual selection. Furthermore, many other algorithms based on the EA like: Simulated Annealing (SA), Genetic Algorithms (GA), Genetic Programming (GP) etc., can be employed to perform the DT induction instead of the |algo| algorithm and still benefit from the co-processor performing the fitness evaluation operation, which significantly expands the scope of use of the proposed |cop| co-processor.
