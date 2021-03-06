def eefti(train_set, ensemble_size):
    train_par = divide_train_set(train_set, ensemble_size)

    res = []
    semaphores = []
    tasks = []
    for eftip_id in range(ensemble_size):
        r = {}
        s = create_semaphore()
        t = create_task(efti, train_par[eftip_id], r, eftip_id, s)
        res.append(r)
        semaphores.append(s)
        tasks.append(t)

    scheduler(tasks, semaphores)

    return res
