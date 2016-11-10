def eefti(train_set, ensemble_size):
    train_par = divide_train_set(train_set, ensemble_size)

    res = []
    tasks = []
    for i in range(ensemble_size):
        r = {}
        t = create_task(efti, train_par[i], r)
        res.append(r)
        tasks.append(t)

    while(not all_finished(tasks)):
        pass

    return res
