def scheduler():
    while(tasks_exist()):
        status = hw_get_status()
        
        for smae_id, smae_stat in enumerate(binary(status)):
            if smae_stat == 1:
                semaphore_give(smae_id)