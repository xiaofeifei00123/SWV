#!/home/fengxiang/anaconda3/envs/wrfout/bin/python
# -*- encoding: utf-8 -*-
'''
Description:
在地图上画图的模板
# cartopy库
地图上的等值线、填色、风矢图
-----------------------------------------
Time             :2021/09/13 11:39:04
Author           :Forxd
Version          :1.0
'''

# %%
import xarray as xr
import cmaps
import numpy as np
# import xesmf as xe
# import netCDF4 as nc
# import pandas as pd

# import salem
import cartopy.crs as ccrs
import cartopy.feature as cfeat
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.io.shapereader import Reader, natural_earth
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.gridspec as gridspec
# import geopandas
import cmaps
from multiprocessing import Pool
from global_variable import station_dic
from get_cmap import get_cmap_tbb

plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

fl = '/mnt/zfm_18T/fengxiang/DATA/FY_TBB/TBB_FY2G_201607.nc'
ds_tbb = xr.open_dataset(fl)


# %%
# fl_fnl = '/mnt/zfm_18T/fengxiang/DATA/FNL/fnl_2016.nc'
fl_gdas = '/mnt/zfm_18T/fengxiang/DATA/FNL/gdas_2016_0710_20.nc'
ds_fnl = xr.open_dataset(fl_gdas)
# fl_era5 = '/mnt/zfm_18T/fengxiang/DATA/ERA5/ERA5_201607.nc'
# fl_era5 = '/mnt/zfm_18T/fengxiang/DATA/ERA5/2016_07/ERA5_202107.nc'
# fl_era5 = '/mnt/zfm_18T/fengxiang/DATA/ERA5/2016_07/ERA5_201607.nc'

# ds_era5 = xr.open_dataset(fl_era5)
# %%
# ds_gdas['height'].sel(pressure=500).isel(time=0).plot()
# ds_era5['z']
# ds_era5['z'].sel(level=1000).max()/10
# ds_era5['z'].sel(level=700).max()/10
# ds_era5['z'].sel(level=500).min()/10


# %%



# ds_fnl = xr.open_dataset(fl_gdas)
# ds_fnl['height']
# ds_fnl 


# %%
class Map():
    """控制地图的类
    """
    def __init__(self, ax):
        self.path_province = '/mnt/zfm_18T/fengxiang/DATA/SHP/Map/cn_shp/Province_9/Province_9.shp'
        self.path_city = '/mnt/zfm_18T/fengxiang/DATA/SHP/Map/cn_shp/City_9/City_9.shp'
        self.path_tibet = '/mnt/zfm_18T/fengxiang/DATA/SHP/shp_tp/Tibet.shp'
        self.ax = ax

    def draw_station(self, ):
        """在地图上标记站点
        """
        pass
        # station = station_dic
        station = {
            'ZhengZhou': {
                'abbreviation':'郑州',
                'lat': 34.75,
                'lon': 113.62
            },
        }
        # station = station_dic
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
        self.ax.scatter(x,
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
            self.ax.text(x[i]-0.4,
                    y[i] + 0.4,
                    station_name[i],
                    transform=ccrs.PlateCarree(),
                    alpha=1.,
                    fontdict={
                    'size': 28,
            })

    def draw_patch(self, ):
        """在地图上绘制画矩形框
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
            self.ax.add_patch(poly)

    def create_map(self,):
        """在底图上添加底图的要素, 省界等
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
        ax = self.ax
        ax.set_xticks(np.arange(70, 130 + 2, 5))
        ax.coastlines(resolution='110m')
        # ax.gridlines()
        
        # ax.add_feature(provinces, linewidth=1, zorder=2)
        ax.add_feature(Tibet, linewidth=2, zorder=2)  # 添加青藏高原区域
        # ax.add_feature(provinces, linewidth=1, zorder=10)
        # ax.add_feature(city, linewidth=1, zorder=2)  # 添加青藏高原区域
        ax.set_yticks(np.arange(10, 55 + 2, 5))
        ax.xaxis.set_major_formatter(LongitudeFormatter())
        ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
        ax.yaxis.set_major_formatter(LatitudeFormatter())
        ax.yaxis.set_minor_locator(plt.MultipleLocator(1))
        ax.tick_params(which='major',length=8,width=1.0) # 控制标签大小 
        ax.tick_params(which='minor',length=4,width=0.5)  #,colors='b')
        # ax.xaxis.set_tick_params(labelsize=8)
        # ax.yaxis.set_tick_params(labelsize=8)
        ax.tick_params(axis='both', labelsize=13, direction='out')
        # -- 设置图像范围
        # ax.set_extent([78, 98, 26, 38], crs=ccrs.PlateCarree())
        return ax

class DataShow():

    def draw_contourf(self, da, ax):
        """在地图上绘制填色图
        """
        x = da.lon
        y = da.lat
        # levels = [220,230, 240, 250, 260, 270, 280, 290, 300]  # 需要画出的等值线
        # levels = [205,210, 215,220, 225,235,245]  # 需要画出的等值线
        levels = [205, 210, 215, 220, 225, 235, 245]  # 需要画出的等值线
        # levels = np.arange(3000, 3300,50)
        
        crx = ax.contourf(x,
                          y,
                          da,
                          cmap=get_cmap_tbb(),
                        #   norm=norm,
                          extend='both',
                        #   extend='max',
                          levels=levels,
                        #   levels=self.levels,
                          transform=ccrs.PlateCarree())
                          

        # box = [80, 115, 20, 40]
        # ax.set_extent(box, crs=ccrs.PlateCarree())
        # ax.set_title(title[2], loc='left',  fontsize=12)
        # ax.set_title(dic['name'], loc='left',  fontsize=12)
        # ax.set_extent([70, 105, 25, 41], crs=ccrs.LambertConformal())
        # ax.xaxis.set_tick_params(labelsize=10)
        # ax.yaxis.set_tick_params(labelsize=10)
        # ax.text(99.5, 38.5, title[1])
        # ax.set_title(title[1], loc='right',  fontsize=12)
        # ax.set_tilte(title[1], loc='right')
        # ax.text(78,26.2,title[0], fontsize=12)
        # self.draw_station(ax)
        return crx

    def draw_contour(self, da, ax):
        """在地图上绘制等值线
        """
        x = da.lon
        y = da.lat
        # levels = [220,230, 240, 250, 260, 270, 280, 290, 300]  # 需要画出的等值线
        # levels = [205,210, 215,220, 225,235,245]  # 需要画出的等值线
        # levels = [205, 210, 215, 220, 225, 235, 245]  # 需要画出的等值线
        # levels = np.arange(5000, 5800, 10)
        levels = np.arange(3000, 3200,50)
        
        
        crx = ax.contour(x,
                          y,
                          da,
                          colors = 'blue',
                        #   cmap=get_cmap_tbb(),
                        #   norm=norm,
                        #   extend='both',
                        #   extend='max',
                          levels=levels,
                        #   levels=self.levels,
                          transform=ccrs.PlateCarree())
        return crx

    def draw_barbas(self,u,v):
        '''
        绘制风羽图图
        '''
        u = u[::4,::4]
        v = v[::4,::4]
        y = u.coords['lat']
        x = u.coords['lon']
        
        # emptyarb设置风旋转的那一点的大小;spacing是F的两条线之间的距离;height:F的横线长短
        self.ax.barbs(x, y, u, v,length=5,pivot='middle',
            sizes=dict(emptybarb=0, spacing=0.3, height=0.5))


    def draw_quiver(self,u,v):
        '''
        绘制风矢图
        '''
        u = u[::6,::6]
        v = v[::6,::6]
        y = u.coords['lat']
        x = u.coords['lon']
        ax = self.ax
        Q = ax.quiver(x,y,u,v,units='inches',scale=18,pivot='middle')  # 绘制风矢
        # qk = ax.quiverkey(Q, 0.9, 0.9, 1, r'$1\ m/s$', labelpos='E',coordinates='figure')   # 设置参考风矢


class Picture(Map, DataShow):
    """绘图的主类
    """

    def __init__(self, ax):
        super().__init__(ax)

    def draw_single(self, fig, dict, picture_dic):
        """绘制单幅图
        设置它的属性之类的

        Args:
            ax ([type]): [画纸对象]
            ds ([Dataset]): [数据]
            picture_dic ([dict]): [图片属性，标注的字典]
        """

        ## 设置地图的范围
        lat = ds_tbb.lat
        lon = ds_tbb.lon
        ax = self.ax
        ax.set_extent([lon.min(), lon.max(), lat.min(), lat.max()], crs=ccrs.PlateCarree())
        box = [80, 115, 20, 40]
        ax.set_extent(box, crs=ccrs.PlateCarree())

        ## 设置图片标题
        self.create_map()
        ax.set_title(picture_dic['title'], fontsize=30)
        ax.set_title(picture_dic['pressure'], fontsize=20,loc='right')
        # cf = self.draw_contourf_single(da, ax, dic)
        
        ## 绘制云顶亮温
        cs = self.draw_contourf(dict['tbb'], ax)
        ccc = self.draw_contour(dict['height'], ax)
        ax.clabel(ccc,inline=1, fontsize=20)
        
        # cccc = self.draw_barbas(dict['u'], dict['v'])
        cccc = self.draw_quiver(dict['u'], dict['v'])
        
        
        return cs
        # fig_name = '/mnt/zfm_18T/fengxiang/SWV/picture/'+date+'.png'
        # fig.savefig(fig_name)

class Draw():

    def draw_one_subplot(self,dict):
        pass 
        fig = plt.figure(figsize=(12, 9), dpi=600)
        proj = ccrs.PlateCarree()  # 创建坐标系
        ax = fig.add_axes([0.1,0.1,0.85,0.85], projection=proj)
        pr = Picture(ax, )
        # da_input = ds_tbb['tbb'].isel(time=0).T
        # dict = {}
        # dict['tbb'] = ds_tbb['tbb'].sel(time='2016-07-11 1200').T
        # dict['height'] = ds_fnl['height'].sel(pressure=500, time='2016-07-11 1200')
        # dict['u'] = ds_fnl['U'].sel(pressure=500, time='2016-07-11 1200')
        # dict['v'] = ds_fnl['V'].sel(pressure=500, time='2016-07-11 1200')
        # ds_input =da_input.to_dataset()
        
        # cs = pr.draw_single(ds_input, picture_dic)
        tt = dict['tbb'].time
        titile = str(tt.dt.strftime('%Y-%m-%d %H').values)
        pressure = str(int(dict['height'].pressure.values))+' hPa'
        picture_dic = {'pressure':pressure, 'time':'111111', 'title':titile}
        
        

        cs = pr.draw_single(fig, dict, picture_dic)

        cb = fig.colorbar(
            cs,
            # cax=ax6,
            orientation='horizontal',
            # ticks=bounds,
            fraction=0.05,  # 色标大小
            pad=0.1,  # 透明度
        )
        figpath = '/mnt/zfm_18T/fengxiang/SWV/picture_tbb_wind/'
        fig_name = str(tt.dt.strftime('%Y-%m-%d_%H').values)+"_"+pressure
        fig.savefig(figpath+fig_name)



def main():
    dr = Draw()
    pre = 700
    
    for t in ds_fnl.time:
        dict = {}
        ds_fnl.sel(pressure=pre, time=t)
        dict['tbb'] = ds_tbb['tbb'].sel(time=t).T
        dict['height'] = ds_fnl['height'].sel(pressure=pre, time=t)
        dict['u'] = ds_fnl['U'].sel(pressure=pre, time=t)
        dict['v'] = ds_fnl['V'].sel(pressure=pre, time=t)
    dr.draw_one_subplot(dict)
main()

# %%

# dict['height']
# pp = dict['height'].pressure
# tt = dict['tbb'].time
# ccc = str(tt.dt.strftime('%Y-%m-%d %H').values)
# ccc








# %%


# tt = ds.time
# da = ds['tbb'].isel(time=0)
# title = tt[0].dt.strftime('%d_%H').values
# dr.draw_single(da.T, title)
        # print(aa.time)
        # i = aa.time







# %%
def single_process_draw():
    """单进程绘图
    """
    fl = '/mnt/zfm_18T/fengxiang/DATA/FY_TBB/TBB_FY2G_201607.nc'
    ds = xr.open_dataset(fl)
# da = ds['tbb'].isel(time=0)
    dr = Draw()
    tt = ds.time
    for t in tt:
        da = ds['tbb'].sel(time=t)
        title = t.dt.strftime('%d_%H').values
        dr.draw_single(da.T, title)
        # print(aa.time)
        # i = aa.time

def multi_process_draw():
    """多进程绘图
    """
    fl = '/mnt/zfm_18T/fengxiang/DATA/FY_TBB/TBB_FY2G_201607.nc'
    ds = xr.open_dataset(fl)
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


if __name__ == "__main__":
    pass
    main()
    # multi_process_draw()



