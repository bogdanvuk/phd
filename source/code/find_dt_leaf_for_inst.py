def find_dt_leaf_for_inst(dt, instance):

    cur_node = dt.root

    while (not cur_node.is_leaf):
        psum = dot_product(instance.x, cur_node.w)

        if psum < cur_node.thr:
            cur_node = cur_node.left
        else:
            cur_node = cur_node.right

    return cur_node
