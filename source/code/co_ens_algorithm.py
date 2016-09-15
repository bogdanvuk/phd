def efti(train_set, ensemble_size):
    task_train_sets = divide_train_set(train_set, ensemble_size)
    
    res = []
    initialize_result_array(res, ensemble_size)
    
    for t, r in zip(task_train_sets, res):
        create_task(efti_task, t, r)
    
    wait_for_all_tasks()
    
    return res
