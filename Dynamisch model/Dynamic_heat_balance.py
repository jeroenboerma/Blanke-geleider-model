# -*- coding: utf-8 -*-
"""
Created on Fri May  5 09:57:41 2023

@author: AL27397
"""

import Dyn_Heat_flows
import Dyn_Properties

Material, Shape, Core, Location, Painted = Dyn_Properties.Component()
M, Beta, Cpa, mu, labda, v = Dyn_Properties.ambient_parameters()
Mc, Cpc, V = Dyn_Heat_flows.Qabsorb()

def dynT(I, T, Te, dt): 
    Qemis = Dyn_Heat_flows.Qemis(T, Te)   #Calculated radiated heat
    Qirr = Dyn_Heat_flows.Qirr()          #Calculate solar irradiance
    Qgen, Rac = Dyn_Heat_flows.Qgen(I,T)       #Calculate Ohmic heat generated

    Qconv, h, Ra, Re, NuL, NuD = Dyn_Heat_flows.Qconv(T, Te, Shape, Location) #Calculate convective heat transfer

    #Calculate remaining heat absorbed by material
    Qres = Qgen + Qirr - Qconv - Qemis
    dTdt = Qres/(Mc*Cpc*V)        #Calculate temperature difference per timestep
    dT = dTdt*dt                  #Multiply by timestep to determine temperature difference
    
    T = T + dT
    return T, dT, Qemis, Qirr, Qgen, Qconv, Qres