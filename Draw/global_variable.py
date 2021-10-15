#!/home/fengxiang/anaconda3/envs/wrfout/bin/python
# -*- encoding: utf-8 -*-
'''
Description:
存储全局变量的
-----------------------------------------
Time             :2021/07/26 13:46:13
Author           :Forxd
Version          :1.0
'''

area = {"lat1": 24.875, "lat2": 40.125, "lon1": 69.875, "lon2": 105.125}

station_dic = {
    'ShiQuanhe': {
        'abbreviation':'SQH',
        'lat': 32.4,
        'lon': 80.1,
        'name': 'ShiQuanhe',
        'number': '55228',
        'height': 4280
    },
    'GaiZe': {
        'abbreviation':'Gz',
        'lat': 32.3,
        'lon': 84.0,
        'name': 'GaiZe',
        'number': '55248',
        'height': 4400,
    },
    'ShenZha': {
        'abbreviation':'SZ',
        'lat': 30.9,
        'lon': 88.7,
        'name': 'ShenZha',
        'number': '55472',
        'height': 4672
    },
    'TingRi': {
        'abbreviation':'TR',
        'lat': 28.63,
        'lon': 87.08,
        'name': 'TingRi',
        'number': '55664',
        'height': 4302
    },
    'LaSa': {
        'abbreviation':'LS',
        'lat': 29.66,
        'lon': 91.14,
        'name': 'LaSa',
        'number': '55591',
        'height': 3648.8999
    },
    'NaQu': {
        'abbreviation':'NQ',
        'lat': 31.48,
        'lon': 92.06,
        'name': 'NaQu',
        'number': '55299',
        'height': 4508
    },
    'LinZhi': {
        'abbreviation':'LZ',
        'lat': 29.65,
        'lon': 94.36,
        'name': 'LinZhi',
        'number': '56312',
        'height':2991.8 
    },
    'ChangDu': {
        'abbreviation':'CD',
        'lat': 31.15,
        'lon': 97.17,
        'name': 'ChangDu',
        'number': '56137',
        'height': 3315
    },
    'BaTang': {
        'abbreviation':'BT',
        'lat': 30,
        'lon': 99.1,
        'name': 'BaTang',
        'number': '56247',
        'height': 2589.2
    },
    'TuoTuohe': {
        'abbreviation':'TTH',
        'lat': 34.22,
        'lon': 92.44,
        'name': 'ChangDu',
        'number': '56004',
        'height': 4542.5
    },
    'MangYa': {
        'abbreviation':'MY',
        'lat': 38.25,
        'lon': 90.85,
        'name': 'MangYa',
        'number': '51886',
        'height': 2951.2
    },
    'GeErmu': {
        'abbreviation':'GEM',
        'lat': 36.42,
        'lon': 94.91,
        'name': 'GeErmu',
        'number': '52818',
        'height': 2812.3
    },
    'DuLan': {
        'abbreviation':'DL',
        'lat': 36.30,
        'lon': 98.10,
        'name': 'DuLan',
        'number': '52836',
        'height': 3197.7
    },
    'YuShu': {
        'abbreviation':'YS',
        'lat': 33.00,
        'lon': 96.96,
        'name': 'YuShu',
        'number': '56029',
        'height': 3723.3999
    },
    'DaRi': {
        'abbreviation':'DR',
        'lat': 33.76,
        'lon': 99.65,
        'name': 'DaRi',
        'number': '56046',
        'height': 3967.6001
    },
    'JiuLong': {
        'abbreviation':'JL',
        'lat': 29.0,
        'lon': 101.5,
        'name': 'JiuLong',
        'number':56462,
        'height':2919},
    'JingChuan': {
        'abbreviation':'JC',
        'lat': 31.29,
        'lon': 102.04,
        'name': 'JiuLong',
        'number': '56168',
        'height': 2165
    },
    'GanZi': {
        'abbreviation':'GZ',
        'lat': 31.62,
        'lon': 100,
        'name': 'GanZi',
        'number': '56146',
        'height': 3393.5
    },
    'GanZi': {
        'abbreviation':'GZ',
        'lat': 31.62,
        'lon': 100,
        'name': 'GanZi',
        'number': '56146',
        'height': 3393.5
    },
    
    'LiJiang': {
        'abbreviation':'LJ',
        'lat': 26.85,
        'lon': 100.22,
        'name': 'LiJiang',
        'number': '56651',
        'height':2380.899 
    },
    'KunMing': {
        'abbreviation':'KM',
        'lat': 25.01,
        'lon': 102.65,
        'name': 'KunMing',
        'number': '56778',
        'height':1888.1
    },
    'XiChang': {
        'abbreviation':'XC',
        'lat': 27.90,
        'lon': 102.27,
        'name': 'XiChang',
        'number': '56571',
        'height':1590.9
    },
    'WenJiang': {
        'abbreviation':'WJ',
        'lat': 30.75,
        'lon': 103.87,
        'name': 'WenJiang',
        'number': '56187',
        'height':547.7
    },
    'WenJiang': {
        'abbreviation':'WJ',
        'lat': 30.75,
        'lon': 103.87,
        'name': 'WenJiang',
        'number': '56187',
        'height':547.7
    },
    'HongYuan': {
        'abbreviation':'HY',
        'lat': 32.8,
        'lon': 102.55,
        'name': 'HongYuan',
        'number': '56173',
        'height':3491.6001
    },
    'WuDu': {
        'abbreviation':'WD',
        'lat': 33.4,
        'lon': 104.92,
        'name': 'WuDu',
        'number': '56096',
        'height':1079.1
    },
    'YiBing': {
        'abbreviation':'YB',
        'lat': 28.77,
        'lon': 104.61,
        'name': 'YB',
        'number': '56492',
        'height':502.8
    },
    'XianNing': {
        'abbreviation':'XN',
        'lat': 26.86,
        'lon': 104.28,
        'name': 'XN',
        'number': '56691',
        'height':2237.5
    },
}

