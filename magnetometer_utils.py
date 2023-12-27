import matplotlib.pyplot as plt
import numpy as np
import datetime
from datetime import timedelta
from matplotlib.ticker import FormatStrFormatter
import os
import pandas as pd
import re
import glob

#colors = ['tab:cyan','tab:blue','tab:green', 'tab:orange', 'tab:gray']





def GetIndices_v0(magData):
    YYYY = magData['YYYY']
    MM = magData['MM']
    DD = magData['DD']
    hh = magData['hh']
    mm = magData['min']#magData['min']
    #print(magData['YYYY'].dtype)
    fechas = []
    for Y, M, D, h, m in zip(YYYY, MM, DD, hh, mm):
        fecha = datetime.datetime(Y, M, D, h, m, 0)
        #print(fecha)
        fechas.append(fecha)
    #    print(pd.to_datetime(Y,M,D,h,m,0,format='%Y-%m-%d %H:%M'))#, M, D, h, m)
    dates = pd.to_datetime(fechas)
    #print(dates.dtype)
    #magData.index = dates
    return dates


def GetIndices(magData):
    YYYY = magData['YYYY']
    MM = magData['MM']
    DD = magData['DD']
    hh = magData['hh']
    mm = magData['mm']#magData['min']
    #print(magData['YYYY'].dtype)
    fechas = []
    for Y, M, D, h, m in zip(YYYY, MM, DD, hh, mm):
        fecha = datetime.datetime(Y, M, D, h, m, 0)
        #print(fecha)
        fechas.append(fecha)
    #    print(pd.to_datetime(Y,M,D,h,m,0,format='%Y-%m-%d %H:%M'))#, M, D, h, m)
    dates = pd.to_datetime(fechas)
    #print(dates.dtype)
    #magData.index = dates
    return dates

def GetTimesSeriesD(magData):
    dates = GetIndices(magData)
    magData.index = dates
    h_field = pd.Series(magData['D(nT)'], index=dates)
    return d_field

def GetTimesSeriesXYZ_v0(magData):
    dates = GetIndices_v0(magData)
    magData.index = dates
    I = (np.pi/180)*magData['I(Deg)'].values
    H = magData['H(nT)'].values
    X = np.multiply(H,np.cos(I))
    Y = np.multiply(H,np.sin(I))
    Z = magData['Z(nT)'].values
    x_field = pd.Series(X, index=dates)
    y_field = pd.Series(Y, index=dates)
    z_field = pd.Series(Z, index=dates)
    return x_field, y_field, z_field

def GetTimesSeriesXYZ(magData):
    dates = GetIndices(magData)
    magData.index = dates #- timedelta(hours=5)
    I = (np.pi/180)*magData['I(deg)'].values
    H = magData['H(nT)'].values
    X = np.multiply(H,np.cos(I))
    Y = np.multiply(H,np.sin(I))
    Z = magData['Z(nT)'].values
    x_field = pd.Series(X, index=dates)
    y_field = pd.Series(Y, index=dates)
    z_field = pd.Series(Z, index=dates)
    return x_field, y_field, z_field


def GetTimesSeriesH_v0(magData):
    dates = GetIndices_v0(magData)
    magData.index = dates 
    h_field = pd.Series(magData['H(nT)'], index=dates)
    return h_field

def GetTimesSeriesH(magData):
    dates = GetIndices(magData)
    magData.index = dates #- timedelta(hours=5)
    h_field = pd.Series(magData['H(nT)'], index=dates)
    return h_field


def GetDeltaH(magFile_roj, magFile_piura):
    print(magFile_roj)
    print(magFile_piura)
    #print(magFile[5:-4])
    #'''
    #JRO files:
    magData_roj = pd.read_csv(magFile_roj,delimiter=r"\s+", skiprows=2,usecols= ["DD","MM","YYYY", "hh", "mm", "D(deg)","H(nT)","Z(nT)"])                     #parse_dates=[["YYYY","MM", "DD", "hh", "mm"]])
    h_field_roj = GetTimesSeriesH(magData_roj)# - baseline_series
    time1 = datetime.datetime(h_field_roj.index.year[0], h_field_roj.index.month[0], h_field_roj.index.day[0], 3, 0, 0) #- pd.Timedelta(hours=5)
    time2 = datetime.datetime(h_field_roj.index.year[0], h_field_roj.index.month[0], h_field_roj.index.day[0], 7, 0, 0) #- pd.Timedelta(hours=5)
    #print(time1)
    #print(time2)
    #h_field_roj.index = h_field_roj.index #- pd.Timedelta(hours=5)
    baseline_roj = h_field_roj[time1:time2].mean()
    print(baseline_roj)
    h_series_baseline_roj = pd.Series(baseline_roj*np.ones(h_field_roj.shape[0]),index=h_field_roj.index)
    h_field_sub_roj = h_field_roj - h_series_baseline_roj
    #h_field_sub_roj.index = h_field_roj.index - pd.Timedelta(hours=5)
    
    #Piura files:
    
    magData_piura = pd.read_csv( magFile_piura,delimiter=r"\s+", skiprows=2,usecols= ["DD","MM","YYYY", "hh", "mm", "D(deg)","H(nT)","Z(nT)"])                     #parse_dates=[["YYYY","MM", "DD", "hh", "mm"]])
    h_field_piura = GetTimesSeriesH(magData_piura)# - baseline_series
    time_i = datetime.datetime(h_field_piura.index.year[0], h_field_piura.index.month[0], h_field_piura.index.day[0], 3, 0, 0) #- pd.Timedelta(hours=5)
    time_f = datetime.datetime(h_field_piura.index.year[0], h_field_piura.index.month[0], h_field_piura.index.day[0], 7, 0, 0) #- pd.Timedelta(hours=5)
    #print(time1)
    #print(time2)
    baseline_piura = h_field_piura[time_i:time_f].mean()
    print(baseline_piura)
    h_series_baseline_piura = pd.Series(baseline_piura*np.ones(h_field_piura.shape[0]),index=h_field_piura.index)
    h_field_sub_piura = h_field_piura - h_series_baseline_piura
    #h_field_sub_piura.index = h_field_piura.index - pd.Timedelta(hours=5)
    time_inic = datetime.datetime(h_field_piura.index.year[0], h_field_piura.index.month[0], h_field_piura.index.day[0], 15, 0, 0) #- pd.Timedelta(hours=5)
    time_final = datetime.datetime(h_field_piura.index.year[0], h_field_piura.index.month[0], h_field_piura.index.day[0], 21, 0, 0) #- pd.Timedelta(hours=5) 
    delta_H = h_field_roj - h_field_piura
    #delta_H.index =  delta_H.index# - pd.Timedelta(hours=5)
    #delta_H_5min = delta_H.loc[time_inic:time_final].resample('5T').mean()
    #delta_H_5min.index =  delta_H_5min.index - pd.Timedelta(hours=5)
    #print('Tamaño de la serie: ', delta_H_5min.shape)
    #plt.figure(figsize=(7,6))

    #delta_H_5min.plot(marker='o')
    #plt.ylabel(r'$\Delta H(nT)$')
    #plt.xlabel('h (LT)')
    #plt.title(r'$\Delta H$ = $\bar{H}_{JRO} - \bar{H}_{Piura}$ (nT)')
    #str_fig = 'delta-H-component-%s-LT.png' % (magFile_roj[5:-4])
    #plt.savefig(str_fig)
    #i = i + 1
    #plt.close()
    return delta_H
