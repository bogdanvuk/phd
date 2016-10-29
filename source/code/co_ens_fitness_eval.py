def fitness_eval(dt, dt_diff, eftip_id, semaphore):
    hw_write(eftip_operation_control_addr(eftip_id), EFTIP_START)
    semaphore_wait(semaphore)
    hits = hw_read(eftip_result_addr())

    accuracy = hits/len(train_set)
    Nc = train_set.cls_num()
    oversize = (len(dt.leaves()) - Nc)/Nc
    fitness = accuracy * (1 - Ko*oversize*oversize)

    return fitness
