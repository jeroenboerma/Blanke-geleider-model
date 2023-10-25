# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 14:29:57 2023

@author: AL27397
"""

import Heat_flows_fun
import Properties_fun
import numpy as np

Material, Shape, Core, Location, Painted = Properties_fun.Component()
M, Beta, Cpa, mu, labda, v = Properties_fun.ambient_parameters()

def Times():
    #Define time frame for warm up curve
    hours = 6                   #Choose time frame in hours
    seconds = hours*3600        #Convert hours to seconds
    dt = 1                      #Time step size in [s]
    t = np.arange(0,seconds,dt) #Make array from t = 0 to t = t_final
    lent = len(t)
    return dt, t, lent

def Temp_profile(I, Te,):

    dt, t, lent = Times()

    #Make temperature arrays
    T = np.zeros(len(t))    #Make array with length of timesteps
    dT = np.zeros(len(t))   #Make array for temperature difference after each timestep

    #dT[0] = T0-Te           #Define first element of 

    #Define empty arrays to fill in for loop
    #Qemis = Heat_flows.Qemis(T)
    Mc, Cpc, V = Heat_flows_fun.Qabsorb()
    Qirr = Heat_flows_fun.Qirr()
    Qirr = np.ones(len(t))*Qirr
    Qemis = np.zeros(len(t))
    Qgen = np.zeros(len(t))
    Qconv = np.zeros(len(t))
    Qres = np.zeros(len(t))
    dTdt = np.zeros(len(t))
    #NuD = np.zeros(len(t))
    #NuL = np.zeros(len(t))
    
    for i in range(len(t)):
        if i == 0:
            T[i] = Te               #Initial temperature is T0
        else:
            T[i] = T[i-1] + dT[i-1] #After first iteration take last updated temperature
                
        Qemis[i] = Heat_flows_fun.Qemis(T[i], Te)   #Calculated radiated heat
        Qirr[i] = Heat_flows_fun.Qirr()         #Calculate solar irradiance
        Qgen[i], Rac = Heat_flows_fun.Qgen(I,T[i])   #Calculate Ohmic heat generated
    
        Qconv[i], h, Ra, Re, NuL, NuD = Heat_flows_fun.Qconv(T[i], Te, Shape, Location) #Calculate convective heat transfer
    
        #Calculate remaining heat absorbed by material
        Qres[i] = Qgen[i] + Qirr[i] - Qconv[i] - Qemis[i]
        dTdt[i] = Qres[i]/(Mc*Cpc*V)        #Calculate temperature difference per timestep
        dT[i] = dTdt[i]*dt                  #Multiply by timestep to determine temperature difference

    return t, T, Qemis, Qirr, Qconv, Qgen, Ra, Re, NuL, NuD, h, dT, Rac     

