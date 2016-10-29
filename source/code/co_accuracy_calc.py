def accuracy_calc(train_set):
    hw_start()

    hits = 0
    while hits == 0:
        hits = hw_get_hits()

    return hits / len(train_set)
