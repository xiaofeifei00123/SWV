#!/home/fengxiang/anaconda3/envs/wrfout/bin/python
# -*- encoding: utf-8 -*-
'''
Description:
画2016年7月西南地区500hPa高度场和风速
fnl资料
-----------------------------------------
Time             :2021/09/14 16:29:30
Author           :Forxd
Version          :1.0
'''

# %%
import xarray as xr
# %%
flnm = '/mnt/zfm_18T/fengxiang/DATA/FNL/fnl_2016.nc'
ds = xr.open_dataset(flnm)

# %%
# ds['height'].sel([pressure=500, time='2016-07-01 0000'])
da = ds['height'].sel(pressure=500, time='2016-07-01 1200')
# da.plot()

