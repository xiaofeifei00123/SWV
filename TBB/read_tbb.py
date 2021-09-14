#!/home/fengxiang/anaconda3/envs/wrfout/bin/python
# -*- encoding: utf-8 -*-
'''
Description:
读取FY-2G卫星 全圆盘标称格式  TBB数据
另外处理了hdf文件的处理问题
参考:python处理卫星云图获取亮温值(小朱小朱绝不服输)
https://blog.csdn.net/weixin_44052055/article/details/116273068
具体操作步骤:
    1. 读单个文件
    2. 添加描述文件和维度
    3. 合并数据
    4. 插值

xesmf库重投影对大范围的数据选择出现问题
不规则数据的投影转换， 尝试使用pyinterp
-----------------------------------------
Time             :2021/09/11 10:37:17
Author           :Forxd
Version          :1.0
'''

# %%
import numpy as np
from numpy.core.defchararray import count
from multiprocessing import Pool
import xarray as xr
import re
import os
import pandas as pd
from multiprocessing import Pool
import xesmf as xe
import matplotlib.pyplot as plt
import xesmf as xe

import cartopy as ca
import cartopy
import cartopy.crs
import pyinterp
import pyinterp.tests
import pyinterp.backends.xarray



# %%

## -- 获取卫星资料的描述文件,就是对应的格点数据的经纬度
class GetTBB():

    def __init__(self) -> None:
        pass
        self.path_TBB = '/mnt/zfm_18T/fengxiang/DATA/FY_TBB/TBB_FY2G_201607/'
        self.lonlatfile  = '/mnt/zfm_18T/fengxiang/DATA/FY_TBB/NOM_ITG_2288_2288(0E0N)_LE/NOM_ITG_2288_2288(0E0N)_LE.dat'

    def get_lat_lon(self,):
        """获得卫星数据的经纬度
        """
        with open(self.lonlatfile, 'r') as f:
            lon_fy = np.fromfile(f, count=2288*2288, dtype=np.float32)+104.5
            lat_fy = np.fromfile(f, count=2288*2288, dtype=np.float32)
        lon = lon_fy.reshape([2288,2288]) ## south_north, west_east
        lat = lat_fy.reshape([2288,2288])  ## 这里也就是和C的存储顺序一致, 不用order的结果一致
        dic ={
            'lat':lat,
            'lon':lon,
        }
        return dic
        
    def get_tbb_one(self, flnm, dic):
        """获得单个时次的，tbb数据，并转成daset格式
        """
        ## 获得时间戳
        pattern = '\d{8}_\d{4}'
        aa = re.search(pattern, flnm)
        bb = aa.group()
        cc = re.sub('_', ' ',bb)
        tt = pd.Timestamp(cc)
        print("读%s时次的数据"%tt)
        ## 读单个时次的数据
        da = xr.open_dataarray(flnm)
        ## 将单个时次的数据转为nc格式
        ds = xr.Dataset(
                        {
                            'tbb':(['south_north', 'west_east'], da.values)
                        },
                        coords={
                            'lat':(['south_north','west_east'], dic['lat']),
                            'lon':(['south_north','west_east'], dic['lon']),
                            'time':tt,
                            },
                            attrs={'variable_name':'TBB' },)
        return ds

    def regrid_pyinterp(self, ds):
        """目前只会重新投影二维的场
        ds含有一个时次的TBB场[nx,ny]
        """
        lons = ds.lon
        lats = ds.lat
        da = ds['tbb']
        tt = ds.time
        # da = ds['tbb'].isel(time=0)
        mesh = pyinterp.RTree()
        mesh.packing(
            np.vstack((lons.values.flatten(), lats.values.flatten())).T,
            da.values.flatten())
        x0, x1 = 69.05, 150.1
        # y0, y1 = -40, 40
        y0, y1 = 0, 55.1 
        # res = 1 / 32.0
        res = 1 / 10  # 0.1°
        mx, my = np.meshgrid(np.arange(x0, x1, res),
                                np.arange(y0, y1, res),
                                indexing="ij")
        idw_eta, neighbors = mesh.inverse_distance_weighting(
            np.vstack((mx.flatten(), my.flatten())).T,
            within=True,  # Extrapolation is forbidden
            radius=55000,  # In a radius of 5.5 Km
            k=8,  # We are looking for at most 8 neighbours
            num_threads=0)
        idw_eta = idw_eta.reshape(mx.shape)

        lon = np.arange(x0,x1,res)
        lat = np.arange(y0,y1,res)
        # lat
        # lona
        tbb_return = xr.Dataset(
                        {
                            'tbb':(['lon', 'lat'], idw_eta)
                        },
                        coords={
                            'lat':lat,
                            'lon':lon,
                            'time':tt,
                            },
                        attrs={'var_name':'tbb' },)
        return tbb_return

    def get_one(self, flnm = '/mnt/zfm_18T/fengxiang/DATA/FY_TBB/TBB_FY2G_201607/FY2G_TBB_IR1_NOM_20160701_0100.hdf'):
        # flnm = '/mnt/zfm_18T/fengxiang/DATA/FY_TBB/TBB_FY2G_201607/FY2G_TBB_IR1_NOM_20160701_0100.hdf'
        dic_latlon = self.get_lat_lon()
        ds = self.get_tbb_one(flnm, dic_latlon)
        ds_regrid = self.regrid_pyinterp(ds)
        # ds
        return ds_regrid
    
    def get_dual(self):
        pass
        # dic_latlon = self.get_lat_lon()
        fl_list = os.popen('ls {}/FY2G_*00.hdf'.format(self.path_TBB))  # 打开一个管道
        fl_list = fl_list.read().split()
        # print(fl_list)
        ## 单进程
        # ds_list = []
        # for fl in fl_list:
        #     print(fl)
        #     ds = self.get_tbb_one(fl, dic_latlon)
        #     ds_list.append(ds)
        # ds_return = xr.concat(ds_list,dim='time')
        # return ds_return
        ## 单进程结束
        
        ## 多进程
        pool = Pool(10)
        result = []
        for fl in fl_list:
            # tr = pool.apply_async(self.get_tbb_one, args=(fl,dic_latlon,))
            tr = pool.apply_async(self.get_one, args=(fl,))
            
            result.append(tr)
        pool.close()
        pool.join()

        ds_list = []
        for j in result:
            ds_list.append(j.get())
        ds_return = xr.concat(ds_list,dim='time')
        ds_return.to_netcdf('/mnt/zfm_18T/fengxiang/DATA/FY_TBB/TBB_FY2G_201607.nc')
        # return ds_return

    def read_tbb_temp(self,):
        fl = '/mnt/zfm_18T/fengxiang/DATA/FY_TBB/TBB_FY2G_201607.nc'
        ds = xr.open_dataset(fl)
        return ds
        

        

rd = GetTBB()    
rd.get_dual()
# ds = rd.read_tbb_temp()
# %%
# ds['tbb'].max()
# ds['tbb'].plot()
# ds['tbb'].T.isel(time=10).plot()

# %%





    # import cartopy
    # fig = plt.figure(figsize=(18, 9))
    # ax = fig.add_subplot(111, projection=cartopy.crs.PlateCarree())
    # cc = ax.pcolormesh( mx,
    #                     my,
    #                     idw_eta,
    #                     cmap='terrain',
    #                     transform=cartopy.crs.PlateCarree())
    # ax.coastlines()
    # ax.set_xticks(np.arange(x0, x1, 10.0))
    # ax.set_yticks(np.arange(y0, y1, 10))
    # ax.set_title("Eta (IDW)")
    # fig.colorbar(cc)
    # plt.show()