
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 15:26:37 2023

@author: AL27397
"""

### Define final temperature and time constant


import Temperature_profile_fun
import math as mt


#Function that calculates the time constant and maximum temperature per current
#With timesteps and temperature profile as input
def T_tau(lent, Te, I, T, Tfinal, t, tfinal, tau):

    t, T, Qemis, Qirr, Qconv, Qgen, Ra, Re, NuL, NuD, h, dT, Rac = Temperature_profile_fun.Temp_profile(I, Te) #Load time and temperature profile from Temp_profile function
    T = T - T[0]
    power = 2                                #Highest average accuracy for both low and high time constants, found by trial and error
    fx = 1-(1/mt.e)**power                   #Raise accuracy to certain power, higher power --> higher accuracy

    for i in range(len(t)-2):          #Iterate over timesteps
           
       if T[-1] - T[i] <= 0.01 and tfinal == 0:      #Define maximum temperature by minimum change  
           Tfinal = T[i]               #Assign value for Tmax
           tfinal = t[i]

           for j in range(len(t[:])-2):  #If Tmax is found, find time it takes to reach Tmax
                   
               if T[j] >= T[-1]*fx and tau == 0:   #If T is bigger than assigned accuracy
                   tau = t[j]/power  #Time constant is total time divided by the number of 1/e increases
                   #break                    #If found, break out of loop 

    Tfinal = Tfinal + (Te - 273.15)             #Convert to degree celsius
    #Temperature difference between start and and point
    delT = T[-1]
    return delT, Tfinal, tfinal, tau, Ra, Re, NuL, NuD, h, t, T, lent, dT, Qemis, Qirr, Qconv, Qgen, Rac  

