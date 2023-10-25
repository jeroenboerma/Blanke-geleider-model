# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 10:01:52 2023

@author: AL27397

Determine the temperature profile for different ambient temperatures.
"""

import numpy as np
import Properties
import Tfinal_and_tau as Tt
import Temperature_profile
import matplotlib.pyplot as plt
import math as mt
    
Material, Shape, Core, Location, Painted = Properties.Component()   
Mc, Cpc, rho, rho0, alpha, epsilon = Properties.select_material(Material, Shape, Painted, Location)
Dh, ID, w, B, L, A, S, V, Ro, Sr = Properties.component_parameters(Shape, Core, rho0, epsilon)
dt, t, lent = Temperature_profile.Times()

#Take single ambient temperature(Te) and vary the current or take constant current and vary Tambient
#Te = np.arange(20,36,1) + 273.15          #Ambient temperature [K]
Te = np.array([35]) + 273.15               #Ambient temperature [K]
I = np.array([1240])                       #Current [A] 
#I = np.array(np.arange(1240,1841,100))       #Make array of different currents

if len(Te) > 1 and len(Te) > 1:
    print("WARNING: Both Te and I have length > 1, keep one constant!")

if len(Te) > 1:
    leng = len(Te)
elif len(Te) == 1:
    leng = len(I)

t = np.zeros([leng,lent])     #Assign element per current and timestep
T = np.zeros([leng,lent])     #Assign element per current and timestep
Tfinal = np.zeros(leng)       #Assign element per current
tfinal = np.zeros(leng)       #Assign element per current
tau = np.zeros(leng)          #Assign element per current
Qemis = np.zeros([leng,lent]) #Assign element per current and timestep
Qirr = np.zeros([leng,lent])  #Assign element per current and timestep
Qconv = np.zeros([leng,lent]) #Assign element per current and timestep
Qgen = np.zeros([leng,lent])  #Assign element per current and timestep


for jj in range(len(Te)):
    for ii in range(len(I)):
        #Calculate temperature profile for constant current
        yy = jj + ii
        delT, Tfinal[yy], tfinal[yy], tau[yy], Ra, Re, NuL, NuD, h, t[yy,:], T[yy,:], lent, dT, Qemis[yy,:], Qirr[yy,:], Qconv[yy,:], Qgen[yy,:], Rac = Tt.T_tau(lent, Te[jj], I[ii], T[yy,:], Tfinal[yy], t[yy,:], tfinal[yy], tau[yy])
        T[yy,:] = T[yy,:] + (Te[jj] - 273.15)
        t = t/60
        plt.plot(t[yy,:],T[yy,:])



plt.title('Temperature profile of ' + Shape + ' ' + Material + ' ' + Location)
plt.xlabel("Time [min]")
plt.ylabel("T [$^\circ$C]")
plt.gcf().set_dpi(300)
plt.grid(True)
plt.show()

if len(I) > 1:
    plt.plot(I,Tfinal)
    plt.title('I vs Tfinal of ' + Shape + ' ' + Material + ' ' + Location)
    plt.xlabel("I [A]")
    plt.ylabel("T [$^\circ$C]")
    plt.gcf().set_dpi(300)
    plt.grid(True)
    plt.show()

#Calculate the total temperature difference between the first and final point of the curve
delT = T[:,-1] - (Te - 273.15)

#When plotting multiple curves, k refers to the curve number. For example, if I = np.arange([10,20,1])
#then k = 0 refers to I = 10, k = 1 to I = 11, etc.
k = 0
plt.plot(T[k,:], Qemis[k,:]) # plot 2D data
plt.plot(T[k,:], Qirr[k,:]) # plot 2D data
plt.plot(T[k,:], Qconv[k,:]) # plot 2D data
plt.plot(T[k,:], Qgen[k,:]) # plot 2D data
#plt.title("Heat transfer at Ta = 35 C") # Set title of plot
plt.xlabel("T [$^\circ$C]") # Set label for x-axis
plt.ylabel("P [W]") # Set label for y-axis
plt.legend(["Radiation","Irradiation","Convection","Generation"])
plt.gcf().set_dpi(300)
plt.grid(True)
plt.show()

Rdc = Ro*(1+alpha*(T[-1]))
#Rac, Ys, Xs = Properties.Rac(Rdc, Shape, Core, Dh, ID, rho0, L, alpha, T, w)

