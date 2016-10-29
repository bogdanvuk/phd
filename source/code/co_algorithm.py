def efti(train_set, max_iter):
    hw_load_train_set(train_set, fp_format)

    dt_best = dt = initialize(train_set)
    hw_load_dt(dt.root)
    fitness_eval(dt, train_set)

    for iter in range(max_iter):
        dt_mut  = mutate(dt)
        hw_load_dt_diff(dt_mut)

        fitness_eval(dt_mut, train_set)

        dt, dt_best = select(dt, dt_mut, dt_best)

        if dt != dt_mut:
            if dt == dt_best:
                hw_load_dt(dt.root)
            else:
                hw_revert_dt_diff(dt_mut)


    hw_load_dt(dt_best.root)
    hw_populate_classes(dt_best)

    return dt_best
