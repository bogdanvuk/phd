def select(dt, dt_mut, dt_best):
    if dt_mut.fit > dt.fit:
        stagnation_duration = 0
        dt = dt_mut

        if dt_mut.fit > dt_best.fit:
            dt_best = dt_mut
    else:
        stagnation_duration += 1
        diff = (dt.fit - dt_mut.fit)/dt.fit
        search_probability = stagnation_duration * rho_0 * \
                             exp(-diff/S_T);
        if random() < restart_probability:
            stagnation_duration = 0
            dt = dt_best
        elif random() < search_probability:
            dt = dt_mut

    return dt, dt_best
