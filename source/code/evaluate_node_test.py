def evaluate_node_test(cur_node, instance):

    sum = 0
    
    for coef, attr in zip(cur_node.coefficients, instance):
        sum += coef*attr
        
    sum += cur_node.threshold
    
    return sum < 0 