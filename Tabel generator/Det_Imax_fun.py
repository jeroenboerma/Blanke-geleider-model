# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 14:17:12 2023

@author: AL27397
"""

import Properties_fun
import Heat_flows_fun
import numpy as np
import matplotlib.pyplot as plt


#Material, Shape, Core, Location, Painted = Fun_total.Parm()
#Mc, Cpc, rho, rho0, alpha, epsilon = Properties_fun.select_material(Material, Shape, Painted, Location)
#Dh, ID, w, B, L, A, S, V, Ro, Sr = Properties_fun.component_parameters(Shape, Core, rho0, epsilon, Dh, w)
#M, Beta, Cpa, mu, labda, v = Properties_fun.ambient_parameters()
#g, sigma = Properties_fun.PhyCo()
#phis, r = Properties_fun.Wheather(Material)

def Imax(Material, Shape, Core, Location, Painted, Dh, w, Diameter, Wall_Thickness, Tmax):

    Mc, Cpc, rho, rho0, alpha, epsilon = Properties_fun.select_material(Material, Shape, Painted, Location)
    Dh, ID, w, B, L, A, S, V, Ro, Sr = Properties_fun.component_parameters(Shape, Core, rho0, epsilon, Dh, w, Diameter, Wall_Thickness)
    M, Beta, Cpa, mu, labda, v = Properties_fun.ambient_parameters()
    g, sigma = Properties_fun.PhyCo()
    phis, r = Properties_fun.Wheather(Material, Painted)
    
    if Shape == "Cylindrical":
        Dh = Diameter
        
    #Define maximum temperature conductor may reach
    Te = np.array([35])+273.15              #Ambient temperature [K]
    #Te = np.arange(0,36,1) + 273.15        #Ambient temperature [K]
    #Tmax = np.arange(65,101,1) + 273.15    #Maximum permissible conductor temperature [K]
    #Tmax = np.array([80]) + 273.15          #Maximum permissible conductor temperature [K]
    Tmax = np.array([Tmax])
    Inom = 1100 #Fill in the nominal current, which is listed in the tables

    """ 
    If you want to express the new load capacity in percentage of the nominal current,
    type "YES" behind the next line. Otherwise type "NO"
    """
    I_want_the_load_capacity_in_percent_of_Inom = "NO"  #"NO" or "YES"

    if len(Te) > 1:
        leng = len(Te)
    elif len(Te) == 1:
        leng = len(Tmax)
            
    Qconv = np.zeros(leng)
    Qemis = np.zeros(leng)
    h = np.zeros(leng)
    I = np.zeros(leng)

    for i in range(len(Te)):
        for j in range(len(Tmax)):
            y = i + j
            #Heat transfer coefficient for cylinder natural convection
            Qconv[y], h[y], Ra, Re, NuL, NuD = Heat_flows_fun.Qconv(Tmax[j], Te[i], Shape, Location, Dh, A, L) #Calculate convective heat transfer
    
            Qemis = Heat_flows_fun.Qemis(Tmax[j], Te[i], A)
            #Calculate AC resistance
            Rdc = Ro*(1+alpha*(Tmax[j]-273.1))
            Rac, Ys, Xs = Properties_fun.Rac(Rdc, Shape, Core, Dh, ID, rho0, L, alpha, Tmax[j], w)
            #Determine current needed to reach Tmax
            if Location == "Inside":
                I[y] = np.sqrt((A*(h[y]*(Tmax[j]-Te[i]) + sigma*epsilon*(Tmax[j]**4 - Te[i]**4)))/(Rac))      
            elif Location == "Outside":
                I[y] = np.sqrt((A*(h[y]*(Tmax[j]-Te[i]) + sigma*epsilon*(Tmax[j]**4 - Te[i]**4)) - r*phis*Sr)/(Rac))
    

    Tmax = Tmax - 273.15
    Te = Te - 273.15

    if I_want_the_load_capacity_in_percent_of_Inom == "YES":
        I = ((I)/Inom)*100

    #The graph shows the relation between I and Tmax at constant Te
    if len(Tmax) > 1:
        plt.plot(Tmax,I)
        #plt.plot(I,Te1)
        plt.title("$T_{max}$ vs I for " + Shape + " " + Material + " " + Location + " at Tamb = " + str(int(Te)) +  "$^\circ$C")
        plt.xlabel("$T_{max}$ [$^\circ$C]")
        plt.ylabel("$I$ [A]")
    if I_want_the_load_capacity_in_percent_of_Inom == "YES":
        plt.ylabel("$I_{max}/I_{nom}$ [%]")
        plt.gcf().set_dpi(300)
        plt.grid(True)
        plt.show()

    #This graph shows the relation between I and Te at constant Tmax
    if len(Te) > 1:
        plt.plot(Te,I)
        plt.title("Maximum allowed current at $T_{max}$ = " + str(int(Tmax)) +  "$^\circ$C for " + Shape + " " + Material + " " + Location)
        plt.xlabel("$T_{ambient}$ [$^\circ$C]")
        plt.ylabel("$I$ [A]")
    if I_want_the_load_capacity_in_percent_of_Inom == "YES":
        plt.ylabel("$I_{max}/I_{nom}$ [%]")
        plt.gcf().set_dpi(300)
        plt.grid(True)
        plt.show()

    #Output single current value at constant Te and Tmax
    if len(Te) < 2 and len(Tmax) < 2:
        if I_want_the_load_capacity_in_percent_of_Inom == "YES":
            print("The ambient temperature is " + str(int(Te)) + " degrees celsius")
            print("The maximum permissible temperature is " + str(int(Tmax)) + " degrees celsius")
            print("The load capacity of the " + str(Material) + " " + str(Core) + " " + str(Shape) + " " + "conductor " + str(Location) + " = " + str(int(I)) + " [% of Inom]" )
        elif I_want_the_load_capacity_in_percent_of_Inom == "NO":
            print("The ambient temperature is " + str(int(Te)) + " degrees celsius")
            print("The maximum permissible temperature is " + str(int(Tmax)) + " degrees celsius")
            print("The load capacity of the " + str(Material) + " " + str(Core) + " " + str(Shape) + " " + "conductor " + str(Location) + " = " + str(int(I)) + " [A]" )
        
    if len(Tmax) > 1 and len(Te) > 1:
        print("Both Te and Tmax have length > 1, keep one constant!")
        
    return I