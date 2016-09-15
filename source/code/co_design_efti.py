def efti(train_set, smae_id):
    hw_load_training_set(smae_id, train_set)
    
    initialize(dt)
    
    best_fit = fitness_eval(dt, train_set)
    
    for iter in range(max_iter):
        
        dt_mut, dt_diff = mutate(dt)
        hw_load_dt_diff(smae_id, dt_diff)
        
        cur_fit = fitness_eval(dt_mut, dt_diff, train_set, smae_id)
        
        if cur_fit > best_fit:
            best_fit = cur_fit
            dt = dt_mut
        else:
            hw_revert_dt_diff(smae_id, dt, dt_diff)
            
    return dt
