def hw_populate_classes(dt):
    hw_start()

    hits = 0
    while hits == 0:
        hits = hw_get_hits()

    for leaf in dt.leaves():
        leaf.cls = hw_read(eftip_cu_cls_addr(leaf.id))

