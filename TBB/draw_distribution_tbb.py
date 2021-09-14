#!/home/fengxiang/anaconda3/envs/wrfout/bin/python
# -*- encoding: utf-8 -*-
'''
Description:
画TBB分布单个图
-----------------------------------------
Time             :2021/09/13 11:39:04
Author           :Forxd
Version          :1.0
'''

# %%
import xarray as xr
import cmaps
import numpy as np
import xesmf as xe
import os
import wrf
import netCDF4 as nc
import pandas as pd

import salem
import cartopy.crs as ccrs
import cartopy.feature as cfeat
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.io.shapereader import Reader, natural_earth
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.gridspec as gridspec
import geopandas
import cmaps
from multiprocessing import Pool
from global_variable import station_dic

plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']


# %%
def get_cmap():
    ccc = cmaps.precip3_16lev_r
    colors = mpl.cm.get_cmap(ccc)
    col = colors(np.linspace(0, 1, 18))
    cccc = mpl.colors.ListedColormap([
        col[0],
        col[1],
        col[2],
        (231 / 250, 177 / 250, 22 / 250),
        col[4],
        col[6],
        '#85f485',
        '#16c516',
        'white',
    ])
    cmap = cccc
    return  cmap

class Draw(object):

    
    def __init__(self) -> None:
        super().__init__()
        self.path_province = '/mnt/zfm_18T/fengxiang/DATA/SHP/Map/cn_shp/Province_9/Province_9.shp'
        self.path_city = '/mnt/zfm_18T/fengxiang/DATA/SHP/Map/cn_shp/City_9/City_9.shp'
        self.path_tibet = '/mnt/zfm_18T/fengxiang/DATA/SHP/shp_tp/Tibet.shp'
        self.picture_path = '/mnt/zfm_18T/fengxiang/Asses_PBL/Rain/picture'
        # self.levels = np.arange(0,561,35) 
        # self.levels = [0, 10, 25, 50, 100, 250,500,]
        self.levels = np.linspace(0,660,16)

    def draw_station(self, ax):
        pass
        # station = station_dic
        # station = {
        #     'ZhengZhou': {
        #         'abbreviation':'郑州',
        #         'lat': 34.75,
        #         'lon': 113.62
        #     },
        # }
        station = station_dic
        values = station.values()
        station_name = list(station.keys())
        station_name = []
        x = []
        y = []
        for i in values:
            y.append(float(i['lat']))
            x.append(float(i['lon']))
            station_name.append(i['abbreviation'])

        # 标记出站点
        ax.scatter(x,
                   y,
                #    color='black',
                   color='black',
                   transform=ccrs.PlateCarree(),
                   alpha=1.,
                   linewidth=5,
                   s=30,
                   )
        # 给站点加注释
        for i in range(len(x)):
            # print(x[i])
            ax.text(x[i]-0.4,
                    y[i] + 0.4,
                    station_name[i],
                    transform=ccrs.PlateCarree(),
                    alpha=1.,
                    fontdict={
                    'size': 28,
            })

    def draw_patch(self, ax):
        """画矩形框
        """
        area = [None] * 3  # 设置一个维度为8的空列表
        area[0] = {"lat1": 33.5, "lat2": 40, "lon1": 80, "lon2": 90}  # north
        area[1] = {"lat1": 28, "lat2": 33,
                   "lon1": 83, "lon2": 94}  # south left
        area[2] = {"lat1": 26, "lat2": 33,
                   "lon1": 95, "lon2": 103}  # south right
        for i in range(3):
            lon = np.empty(4)
            lat = np.empty(4)
            lon[0], lat[0] = area[i]['lon1'], area[i]['lat1']
            lon[1], lat[1] = area[i]['lon2'], area[i]['lat1']
            lon[2], lat[2] = area[i]['lon2'], area[i]['lat2']
            lon[3], lat[3] = area[i]['lon1'], area[i]['lat2']
            x, y = lon, lat
            xy = list(zip(x, y))
            poly = plt.Polygon(xy, edgecolor="red", fc="none", lw=.9, alpha=1)
            ax.add_patch(poly)

    def create_map(self, ax):
        """创建地图对象
        ax 需要添加底图的画图对象

        Returns:
            ax: 添加完底图信息的坐标子图对象
        """
        proj = ccrs.PlateCarree()
        # --设置地图属性
        # 画省界
        provinces = cfeat.ShapelyFeature(
            Reader(self.path_province).geometries(),
            proj,
            edgecolor='k',
            facecolor='none')
        
        city = cfeat.ShapelyFeature(
            Reader(self.path_city).geometries(),
            proj,
            edgecolor='k',
            facecolor='none')

        Tibet = cfeat.ShapelyFeature(
            Reader(self.path_tibet).geometries(),
            proj,
            edgecolor='k',
            facecolor='none')


        # --设置图像刻度
        ax.set_xticks(np.arange(70, 130 + 2, 5))
        ax.coastlines(resolution='110m')
        # ax.gridlines()
        
        # ax.add_feature(provinces, linewidth=1, zorder=2)
        ax.add_feature(Tibet, linewidth=2, zorder=2)  # 添加青藏高原区域
        ax.add_feature(provinces, linewidth=1, zorder=10)
        # ax.add_feature(city, linewidth=1, zorder=2)  # 添加青藏高原区域
        ax.set_yticks(np.arange(10, 55 + 2, 5))
        ax.xaxis.set_major_formatter(LongitudeFormatter())
        ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
        ax.yaxis.set_major_formatter(LatitudeFormatter())
        ax.yaxis.set_minor_locator(plt.MultipleLocator(1))
        ax.tick_params(which='major',length=8,width=1.0) # 控制标签大小 
        ax.tick_params(which='minor',length=4,width=0.5)  #,colors='b')
        ax.xaxis.set_tick_params(labelsize=10)
        ax.yaxis.set_tick_params(labelsize=10)
        ax.tick_params(axis='both', labelsize=20, direction='out')
        # -- 设置图像范围
        # ax.set_extent([78, 98, 26, 38], crs=ccrs.PlateCarree())
        return ax

    def draw_contourf_single(self, data, ax, dic):
        """画填色图
        """

        x = data.lon
        y = data.lat

        
        
        # levels = [220,230, 240, 250, 260, 270, 280, 290, 300]  # 需要画出的等值线
        # levels = [205,210, 215,220, 225,235,245]  # 需要画出的等值线
        levels = [205, 210, 215, 220, 225, 235, 245]  # 需要画出的等值线
        
        crx = ax.contourf(x,
                          y,
                          data,
                          cmap=get_cmap(),
                        #   norm=norm,
                          extend='both',
                        #   extend='max',
                          levels=levels,
                        #   levels=self.levels,
                          transform=ccrs.PlateCarree())
        box = [80, 115, 20, 40]
        ax.set_extent(box, crs=ccrs.PlateCarree())
        # ax.set_title(title[2], loc='left',  fontsize=12)
        # ax.set_title(dic['name'], loc='left',  fontsize=12)
        # ax.set_extent([70, 105, 25, 41], crs=ccrs.LambertConformal())
        # ax.xaxis.set_tick_params(labelsize=10)
        # ax.yaxis.set_tick_params(labelsize=10)
        # ax.text(99.5, 38.5, title[1])
        # ax.set_title(title[1], loc='right',  fontsize=12)
        # ax.set_tilte(title[1], loc='right')
        # ax.text(78,26.2,title[0], fontsize=12)
        self.draw_station(ax)
        return crx

    def draw_single(self, da, date):
        """画单个的那种图

        Args:
            da (DataArray): 单个时次的降水
        """
        print("画%s"%date)
        fig = plt.figure(figsize=(12, 9), dpi=600)
        # proj = ccrs.LambertConformal()  # 创建坐标系
        proj = ccrs.PlateCarree()  # 创建坐标系
        ax = fig.add_axes([0.1,0.1,0.85,0.85], projection=proj)
        dic = {'name':'HeNan',
               'cmap':cmaps.precip3_16lev,
            #    'cmap':get_cmap_rain2(),
               'time':str(date)}
        ax = self.create_map(ax)
        ax.set_title(date, fontsize=30)
        # ax.set_extent([])
        cf = self.draw_contourf_single(da, ax, dic)
        ax6 = fig.add_axes([0.15, 0.05, 0.7, 0.02])  # 重新生成一个新的坐标图


        cmap = get_cmap()
        # bounds = [220,230, 240,250, 260,270,280,290]  # 需要画出的等值线
        bounds = [205, 210, 215,220, 225,235,245]  # 需要画出的等值线
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend='both')
        cb = fig.colorbar(
            cf,
            cax=ax6,
            orientation='horizontal',
            ticks=bounds,
            fraction=0.05,  # 色标大小
            pad=0.1,  # 透明度
        )
        fig_name = '/mnt/zfm_18T/fengxiang/SWV/picture/'+date+'.png'
        # fig.savefig('/mnt/zfm_18T/fengxiang/HeNan/Draw/test.png')
        fig.savefig(fig_name)


fl = '/mnt/zfm_18T/fengxiang/DATA/FY_TBB/TBB_FY2G_201607.nc'
ds = xr.open_dataset(fl)
# da = ds['tbb'].isel(time=0)

# %%
# dr = Draw()
# tt = ds.time
# for t in tt:
#     da = ds['tbb'].sel(time=t)
#     title = t.dt.strftime('%d_%H').values
#     dr.draw_single(da.T, title)
#     # print(aa.time)
#     # i = aa.time


# %%

## 多进程
if __name__ == "__main__":

    pool = Pool(12)
    # result = []
    dr = Draw()
    tt = ds.time
    for t in tt:
        da = ds['tbb'].sel(time=t)
        title = t.dt.strftime('%d_%H').values
        tr = pool.apply_async(dr.draw_single, args=(da.T,title,))
        # print("计算%d"%i)
        # result.append(tr)
    pool.close()
    pool.join()


