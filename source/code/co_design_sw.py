def efti(train_set, ensemble_size):
    task_train_sets = divide_train_set(train_set, ensemble_size)
    
    res = []
    initialize_result_array(res, ensemble_size)
    
    create_semaphores(ensemble_size)
    for t, r, smae_id in zip(task_train_sets, res, range(0,ensemble_size)):
        create_task(efti_task, t, r, smae_id)
    
    create_task(scheduler)
    
    wait_for_all_tasks()
    
    return res