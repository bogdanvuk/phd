def efti(train_set, max_iter):
    initialize(dt)
    fit = fitness_eval(dt, train_set)

    for iter in range(max_iter):
        dt_mut  = mutate(dt)
        fit_mut = fitness_eval(dt_mut, train_set)

        dt, fit = select(dt, dt_mut, fit, fit_mut)

    return dt
