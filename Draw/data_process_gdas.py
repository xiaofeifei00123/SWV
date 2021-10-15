#!/home/fengxiang/anaconda3/envs/wrfout/bin/python
# -*- encoding: utf-8 -*-
'''
Description:
读取gdas数据，
将相对湿度转为比湿保存
5月和7月所有湿度数据保存为一个文件
这个fnl资料里面有
gh, t, r, u, v
fnl 资料是从1000hPa开始的，全球资料
gh是海拔高度
要想得到区域平均的值
我觉得区域平均的值，不应该用高度坐标来表示
因为一个区域内高度差很多
fnl 是 1° x 1° 的数据
需要先插值

同时将其插值到站点上
-----------------------------------------
Author           :Forxd
Version          :1.0
Time：2021/07/12/ 15:28
'''
# %%
import os
import xarray as xr
import numpy as np



# %%
class GetFnl():
    
    def __init__(self,) -> None:
        pass
        # self.path = '/mnt/zfm_18T/fengxiang/DATA/FNL/FNL_2016/*20160701*00.grib2'  

        # self.path = '/mnt/zfm_18T/fengxiang/DATA/FNL/FNL_2016/*20160[5,7]*00.grib2'  
        self.path = '/mnt/zfm_18T/fengxiang/DATA/FNL/GDAS_2016/gdas1.fnl0p25.2016071000.f00.grib2'  
        # self.path = '/mnt/zfm_18T/fengxiang/DATA/FNL/GDAS_2016/gdas1*grib2'  

        self.fnl_file = "/mnt/zfm_18T/fengxiang/DATA/FNL/fnl_2016.nc"
        # self.pressure_level = np.arange(570, 280, -5)
        self.pressure_level = np.arange(800, 100, -1)

    def concat_fnl(self,):
        """获取相对湿度等fnl变量
        将它们聚合成一个ds文件
        """
        ## 这个支持正则表达式
        # path = '/mnt/zfm_18T/fengxiang/DATA/FNL/FNL_2016/*20160701*00.grib2'  
        # path = '/mnt/zfm_18T/fengxiang/DATA/FNL/FNL_2016/*201605*00.grib2'  
        # path = '/mnt/zfm_18T/fengxiang/DATA/FNL/FNL_2016/*20160[5,7]*00.grib2'  
        path = self.path
        fl_list = os.popen('ls {}'.format(path))  # 打开一个管道
        fl_list = fl_list.read().split()
        # print(fl_list)

        rh_list = []
        for fl in fl_list:
            ds = xr.open_dataset(fl, engine='cfgrib',
                                backend_kwargs={'filter_by_keys':
                                    {'typeOfLevel': 'isobaricInhPa'}})
            # ds = xr.open_dataset(fl, engine='cfgrib',
            #                     backend_kwargs={'filter_by_keys':
            #                         {'typeOfLevel': 'planetaryBoundaryLayer'}})
            # ds = xr.open_dataset(fl, engine='cfgrib')
            # return ds
            # ds = ds.rename({'r':'rh', 't':'temp'})  # 统一变量名称
            # rh = ds[var]
            rh = ds['r']
            t = ds['t']
            u = ds['u']
            v = ds['v']
            gh = ds['gh']
            dds = xr.Dataset()
            dds['rh'] = rh
            dds['temp'] = t
            dds['U'] = u
            dds['V'] = v
            dds['height'] = gh
            
            # rh = ds
            rh_list.append(dds)
        # ds = xr.concat(rh_list, dim='time')

        # ds = ds.rename({'isobaricInhPa': 'pressure',
        #                 'latitude': 'lat', 'longitude': 'lon'})
        # ds.attrs['description'] = 'the combine of all time rh, full grid'
        # # print(ds)
        return ds




# %%
if __name__ == '__main__':
    pass
    ### 对fnl数据进行聚合
    gf = GetFnl()
    ds = gf.concat_fnl()
    # %%
    ds
    # %%
    ds.to_netcdf('/mnt/zfm_18T/fengxiang/DATA/FNL/gdas_2016_0710_20.nc')