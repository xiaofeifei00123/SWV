#!/home/fengxiang/anaconda3/envs/wrfout/bin/python
# -*- encoding: utf-8 -*-
'''
Description:
用来读取需要的数据的模块
改用站点插值和cmorph融合的降水数据
-----------------------------------------
Time             :2021/06/04 14:47:01
Author           :Forxd
Version          :1.0
'''
# %%

import xarray as xr
import pandas as pd
# import salem  # 过滤高原外的数据, 滤出地形外的数据
# import geopandas
import xesmf as xe  # 插值
import numpy as np
import os
## 读grd文件的库
from xgrads import CtlDescriptor
from xgrads import open_CtlDataset


# %%

def get_rain_obs():
    """格点降水和CMORPH降水融合数据
    """
    # elif self.month == 'Jul':
    flnm = '/mnt/zfm_18T/fengxiang/DATA/PRECIPTATION/CMORPH_STATION_RAIN/07/CHN_PRCP_HOUR_MERG_DISPLAY_0.1deg.lnx.ctl'
    ds = open_CtlDataset(flnm)
    da = ds.crain.squeeze(drop=True)
    da = da.where(da.values>=0, np.nan)

    ds_in = da.to_dataset()
    # ds_in = ds_in.drop_dims('time')

    path_main = '/mnt/zfm_18T/fengxiang/SWV/Data/'
    path_out = path_main+'rain_obs.nc'
    ds_in.to_netcdf(path_out)
    return ds_in

def regrid():
    pass


# flnm = '/mnt/zfm_18T/fengxiang/SWV/Data/rain_obs.nc'
# ds = xr.open_dataset(flnm)


# %%
if __name__ == '__main__':

    pass
    get_rain_obs()
    
