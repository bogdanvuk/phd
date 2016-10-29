def efti(train_set, max_iter):
    dt_best = dt = initialize(train_set)
    fitness_eval(dt, train_set)

    for iter in range(max_iter):
        dt_mut  = mutate(dt)
        fitness_eval(dt_mut, train_set)

        dt, dt_best = select(dt, dt_mut, dt_best)

    return dt_best
