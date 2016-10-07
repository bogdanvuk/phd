def find_dt_leaf_for_inst(dt, instance, store_paths, recalc_all):

    path_diverged = recalc_all
    cur_node = dt.root

    while not cur_node.is_leaf:
        # if the memorized path is still followed
        if not path_diverged:
            # have we crossed the topologicaly mutated node
            if dt.is_topo_mutated(cur_node):
                psum = dot_product(instance.x, cur_node.w)
                path_diverged = True
            # or only coefficients have mutated
            elif dt.is_coeff_mutated(cur_node):
                # get stored dot product and apply the changes
                psum = get_stored_psum(instance, cur_node)
                for i in dt.mutated_coeff_index(cur_node):
                    psum += (cur_node.w[i] - cur_node.w_orig[i]) \
                            * instance.x[i]

                path_diverged = True
        # else, path has diverged and no testing for crossing
        # mutated nodes is needed
        else:
            psum = dot_product(instance.x, cur_node.w)

        # still have not diverged, look-up the stored next node
        if not path_diverged:
            cur_node = get_stored_next_node(instance, cur_node)
        # path has diverged and the node test needs to be performed
        else:
            if psum < cur_node.thr:
                cur_node = cur_node.left
            else:
                cur_node = cur_node.right

            # has the instance stayed on the path in spite mutation
            if cur_node == get_stored_next_node(instance, cur_node):
                path_diverged = False

        # should the path be memorized
        if store_paths:
            store_node_to_path(instance, cur_node, psum)

    return cur_node
