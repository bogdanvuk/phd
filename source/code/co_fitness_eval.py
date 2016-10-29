def hw_fitness_eval(train_set):
    hw_write(eftip_operation_control_addr(), EFTIP_START)

    eftip_res = 0
    while not eftip_done(eftip_res):
        hits = hw_read(eftip_result_addr())

    accuracy = hits/len(train_set)

    Nc = train_set.cls_num()
    oversize = (len(dt.leaves()) - Nc)/Nc
    fitness = accuracy * (1 - Ko*oversize*oversize)

    return fitness
