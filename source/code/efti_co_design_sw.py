def efti(train_set, max_iter):
    initialize(dt)
    hw_load_training_set()
    fit = fitness_eval(dt, train_set)

    for iter in range(max_iter):
        dt_mut  = mutate(dt)
        fit_mut = fitness_eval(dt_mut, train_set)

        dt = select(dt, dt_mut, fit, fit_mut)

    return dt

def efti():
    initialize(dt)
    hw_load_training_set()
    best_fit, impurity = fitness_eval(dt, train_set)

    for iter in range(max_iter):

        dt_mut = mutate(dt, impurity)
        cur_fit, impurity = fitness_eval(dt_mut, train_set)

        if cur_fit > best_fit:
            best_fit = cur_fit
            dt = dt_mut

    return dt

def fitness_eval(dt):
    hw_load_dt_diff(dt)

    hw_start_accuracy_eval()

    while (not hw_finished_accuracy_eval()):
        pass

    Nc = class_cnt(train_set)

    hits, dt_classes, dt_impurity = hw_get_results()

    accuracy = hits / len(train_set)
    oversize = w_s*(leaves_cnt(dt) - Nc)/Nc
    missing  = w_m*(Nc - len(dt_classes))/Nc

    fitness = accuracy * (1 - oversize) * (1 + missing)

    return fitness, dt_impurity
