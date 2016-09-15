def accuracy_calc(dt, train_set):

    distribution = [[0] * train_set.cls_num()
                    for i in range(len(dt.leaves))]

    for instance in train_set:
        leaf = find_dt_leaf_for_inst(dt, instance)
        distribution[leaf.id][instance.cls] += 1

    hits = 0
    for leaf in dt.leaves:
        dominant_class_cnt = max(distribution[leaf.id])
        hits += dominant_class_cnt

    return hits / len(train_set)
