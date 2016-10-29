def scheduler(tasks, semaphores):
    while(not all_finished(tasks)):
        status = hw_read(eeftip_irq_status_addr())

        for eftip_id, eftip_stat in enumerate(status):
            if eftip_stat == 1:
                semaphore_give(semaphores[eftip_id])

        context_switch()
