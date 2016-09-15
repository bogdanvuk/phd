def fitness_eval(dt, dt_diff):
    hw_start_fitness_eval(smae_id)

    wait(semaphore(smae_id))
    
    accuracy = hw_get_hits(smae_id) / len(train_set)
    oversize = leaves_cnt(dt) / class_cnt(train_set) - 1
    fitness = w_a * accuracy - w_s * oversize
    
    return fitness
