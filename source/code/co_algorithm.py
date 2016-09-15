def efti(train_set, max_iter):
    hw_load_train_set(train_set, fp_format)

    initialize(dt)
    hw_load_whole_dt(dt)
    fit = fitness_eval(dt, train_set)

    for iter in range(max_iter):
        dt_mut  = mutate(dt)
        hw_load_dt_diff(dt_mut)

        fit_mut = hw_fitness_eval(train_set)

        dt = select(dt, dt_mut, fit, fit_mut)
        if dt != dt_mut:
           hw_revert_dt_diff(dt_mut)

    return dt
