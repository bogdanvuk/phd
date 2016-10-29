def eefti(train_set, ensemble_size):
    task_train_sets = divide_train_set(train_set, ensemble_size)

    res = []
    tasks = []
    for i in range(ensemble_size):
        r = {}
        t = create_task(efti, task_train_sets[i], r)
        res.append(r)
        tasks.append(t)

    while(not all_finished(tasks)):
        pass

    return res
