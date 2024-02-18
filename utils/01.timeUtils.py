# !wget http://download.csr.utexas.edu/outgoing/grace/RL0602_mascons/CSR_GRACE_GRACE-FO_RL0602_Mascons_all-corrections.nc

path = '/content/drive/MyDrive/Colab Notebooks/FAO Analysis/data/CSR_GRACE_GRACE-FO_RL0602_Mascons_all-corrections.nc'
ds = xr.open_dataset(path)

# Get the time and time_bounds variables and units
time = ds['time']
# print(time)
# Define a start date as July 2, 2014
timeDelta = datetime(2002, 1, 1, 0, 0, 0) - datetime(1970, 1, 1, 0, 0, 0)
first_day_ms = timeDelta.total_seconds()*1000

time_units = time.attrs['Units']
time_bound = ds['time_bounds']
time_bound_ar = time_bound.values

# the data is in format [[start, end], [start, end]....]
# first extract list as [start, start ...] and [end, end ...]
# and then convert the list back to xarray.DataArray type
time_bound_pre = time_bound_ar[:, :1]
time_bound_pre = xr.DataArray([float(sublist[0]) for sublist in time_bound_pre])

time_bound_post = time_bound_ar[:, 1:]
time_bound_post = xr.DataArray([float(sublist[0]) for sublist in time_bound_post])


# Decode time values into human-readable format
def timeToMs(t, time_units = time_units):
  datetime_ms = [int(first_day_ms+days*86400000)  for days in t.values]
  return datetime_ms

# Time conversion step
time            = timeToMs(time)
time_bound_pre  = timeToMs(time_bound_pre)
time_bound_post = [(excludeLastDay-86400000) for excludeLastDay in timeToMs(time_bound_post)]
time_bound_pre_date = [(datetime.utcfromtimestamp(x / 1000)).strftime('%Y-%m-%d').replace('-', '') for x in time_bound_pre]
time_bound_post_date = [(datetime.utcfromtimestamp(x / 1000)).strftime('%Y-%m-%d').replace('-', '') for x in time_bound_post]

# get the final list of time, time_bound_pre, and time_bound_post
time_time_bounds = list(zip(time, time_bound_pre, time_bound_pre_date, time_bound_post, time_bound_post_date))
time_time_bounds = pd.DataFrame.from_records(time_time_bounds, columns =['time', 'time_beginning_ms', 'time_beginning_YMD', 'time_end_ms', 'time_end_YMD'])
time_time_bounds["id"] = time_time_bounds.index + 1

# Export id to csv
time_time_bounds.to_csv('/content/GRACE_CSV/id_info.csv', index=False)