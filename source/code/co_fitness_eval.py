def hw_fitness_eval(train_set):
    hw_write(eftip_operation_control_addr(), EFTIP_START)

    eftip_res = 0
    while not eftip_done(eftip_res):
        eftip_res = hw_read(eftip_result_addr())

    accuracy = eftip_accuracy(eftip_res)

    Nc = train_set.cls_num()
    oversize = (len(dt.leaves()) - Nc)/Nc

    fitness = accuracy * (1 - Ko*oversize)
    return fitness
