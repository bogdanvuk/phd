def select(dt, dt_mut, fit, fit_mut):
   if fit_mut > fit:
       return dt_mut, fit_mut
   elif random() < search_probability:
       return dt_mut, fit_mut
   else:
       return dt, fit
