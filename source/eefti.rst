
|ealgo| algorithm
=================

In this section, the |ealgo| algorithm for the induction of the DT ensembles which uses Bagging on top of the |algo| algorithm is proposed. The ability of the |algo| algorithm to operate on a single individual and induce small DTs is even more important for the ensembles, since all the operations, be it induction or classification of new instances, are performed on all the DT members of the ensemble at once. The following topics will be covered in this section:

- :num:`Section #sec-bagging` - Description of the Bagging algorithm
- :num:`Section #classifier-arch-overview` - Description of the |ealgo| algorithm
- :num:`Section #sec-ens-advantages` - Experiments showing the superior performance of the ensembles induced by the |ealgo| algorithm over single classifiers in terms of the classification accuracy

.. _sec-bagging:

Bagging Algorithm
-----------------

The choice of the Bagging algorithm was made mainly because it generates one subset of the training set for each ensemble member, hence completely decoupling the induction of the individual members from each other, which in turn makes the algorithm suitable for the parallelization and hardware acceleration. Furthermore, the Bagging algorithm was reported to reduce the accuracy variance and help avoid overfitting. Two common ways of forming the subsets are:

- **random sampling without replacement** - forms disjoint subsets of size :math:`N_{IS}=\frac{N_I}{n_e}`, and
- **random sampling with replacement** - forms overlapping subsets of size :math:`N_{IS} \leq N_I`,

where :math:`N_{IS}` is the size of the subsets, |NI| the size of the whole training set and |ne| the number of subsets, i.e. the number of the ensemble members. The most important feature of the sampling procedure is the diversity of the ensemble members it helps induce. This is especially important for the deterministic induction algorithms, since given the same training subset they would induce identical DT individual each time. In case of stochastic algorithms on the other hand, this is less of a problem. Hence, the |ealgo| algorithm can be used even when :math:`N_{IS} = N_I`.

.. _sec-ealgo:

|ealgo| Description
-------------------

The :num:`Algorithm #fig-algorithm-pca` shows the |ealgo| algorithm pseudo-code. |ealgo| first partitions the training set in the subsets using the ``divide_train_set()`` function that implements one of the techniques discussed in the :num:`Subsection #sec-bagging`. Next, for each member of the ensemble an |algo| tasks is created and assigned its corresponding training subset (``train_par[i]``). In addition, the reference to the result object ``r`` is passed to the |algo| task, to which it can assign the resulting DT and any additional information about the induction, like inference time, etc. All result objects are gathered in the ``res`` array and are returned to the user when the induction is finished. Handles to the created tasks are gathered in the ``tasks`` array, which is used by the ``all_finished()`` helper function, which in turn checks the statuses of the running |algo| tasks and returns ``true`` when all of them have finished the induction and exited. Once all the individual tasks have finished and thus populated their corresponding result objects, the |ealgo| algorithm exits by returning the ``res`` array to the user.

.. _fig-ens-algorithm-pca:
.. literalinclude:: code/ens_algorithm.py
    :caption: The main functino of the |ealgo| algorithm

.. _sec-ens-advantages:

Advantages of the DT ensembles
------------------------------

As it was already said, the ensemble classifier systems were shown to provide improvement to the classification performance over a single classifier :cite:`rokach2010ensemble`. In order to test whether |ealgo| algorithm is capable of inducing an ensemble that has superior accuracy than the individual classifier induced by the |algo| algorithm, an experiment has been conducted whose results are shown in this subsection. The ensembles of sizes 3, 5, 9, 17 and 33 were induced on all datasets from the :num:`Table #tbl-uci` using five 5-fold cross-validation techinique together with the Tukey multiple comparisons test as described in the :num:`Section #sec-exp-struct`. The induced ensembles' accuracies were measured by performing the classification of the test set using the majority voting technique. In the :num:`Table #tbl-ens-vs-single` the average accuracies of the single classifier and the ensembles of five different sizes used in this experiment are given for each dataset together with their 95% confidence intervals. The accuracy rankings of the induced classifiers are given in the :num:`Table #tbl-ens-vs-single-rank` for each dataset, together with the average rank for each classifier used.

.. raw:: latex

   \begingroup
   \setlength{\tabcolsep}{.3em}

.. tabularcolumns:: p{0.09\linewidth} *{6}{R{0.13\linewidth}}
.. _tbl-ens-vs-single:
.. csv-table:: The accuracies of the ensembles with various numbers of elements
    :header-rows: 1
    :file: scripts/ens-vs-single-acc.csv

The results show that an ensemle of classifiers almost always has superior accuracy over the single classifier, with few exceptions with ``bank``, ``page``, ``sb`` and ``thy`` datasets. Also, it can be seen that increasing the number of ensemble members helps the performance until a certain point of saturation, which is different for different datasets. The accuracy on some datasets could not be improved by using ensembles of sizes beyond 3, like ``adult``, ``bcw``, ``ca``, ``eye``, ``hep``, ``irs``, ``lym``, ``magic`` and ``zoo``, while for some datasets progressively larger ensembles continued to steadily advance in terms of the accuracy, like ``bch``, ``jvow``, ``letter`` and ``vow``. Nevertheless, the results in the :num:`Table #tbl-ens-vs-single` show that the accuracy variance decreases the larger the ensembles are used, even when the average value shows no improvement, which is exactly what was expected. Finally, the average ranks in the :num:`Table #tbl-ens-vs-single-rank` show indeed that larger ensembles show statistically significant improvement in the classification accuracy.

.. tabularcolumns:: p{0.08\linewidth} *{6}{R{0.05\linewidth}} | p{0.08\linewidth} *{6}{R{0.05\linewidth}}
.. _tbl-ens-vs-single-rank:
.. csv-table:: The accuracies of the ensembles with various numbers of elements
    :header-rows: 1
    :file: scripts/ens-vs-single-rank-acc.csv

.. raw:: latex

    \endgroup

