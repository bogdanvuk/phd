def select(dt, dt_mut):
    if dt_mut.fit > dt.fit:
        return dt_mut
    else:
        return dt
