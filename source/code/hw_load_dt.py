def hw_load_dt(node):
    if not node.is_leaf:
        cm_pack, sm_pack = pack_dt_node(node, fp_format, Rn)

        for e, elem in enumerate(cm_pack):
            hw_write(eftip_dt_cm_addr(node.level, node.id, e), elem)

        for e, elem in enumerate(sm_pack):
            hw_write(eftip_dt_sm_addr(node.level, node.id, e), elem)

        hw_load_dt(node.left)
        hw_load_dt(node.right)
