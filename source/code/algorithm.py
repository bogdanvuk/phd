def efti(train_set, max_iter):
    dt = initialize()
    fitness_eval(dt, train_set)

    for iter in range(max_iter):
        dt_mut  = mutate(dt)
        fitness_eval(dt_mut, train_set)

        dt = select(dt, dt_mut)

    return dt
