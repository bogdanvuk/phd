def accuracy_calc(train_set, eftip_id, semaphore):
    hw_write(eftip_operation_control_addr(eftip_id), EFTIP_START)
    semaphore_wait(semaphore)
    hits = hw_read(eftip_result_addr(efipt_id))

    return hits/len(train_set)
