def hw_load_whole_dt(node):
    if not node.is_leaf:
        pack_row = pack_dt_node(node, fp_format, Rn)

        for e, elem in enumerate(pack_row):
            hw_write(eftip_dt_mem_addr(node.level, node.id, e), elem)

        hw_load_whole_dt(node.left)
        hw_load_whole_dt(node.right)
