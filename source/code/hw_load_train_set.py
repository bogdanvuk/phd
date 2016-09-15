def hw_load_train_set(train_set, fp_format):

    for i, instance in enumerate(train_set):
         pack_row = pack_instance(instance, fp_format)

         for e, elem in enumerate(pack_row):
              hw_write(eftip_train_mem_addr(i,e), elem)
