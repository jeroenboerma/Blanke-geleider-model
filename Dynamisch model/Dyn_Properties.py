# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 10:47:37 2023

@author: AL27397
"""
import numpy as np
import math as mt
import cmath
import scipy.special as ss

#Define component
def Component():
    Material = "Copper"  #Choose "Copper" or "Aluminium"
    Shape = "Rectangular"      #Choose "Cylindrical", "Rectangular" or "Stranded"
    Core = "Solid"          #Choose "Solid", "Hollow" or "Steel"
    Location = "Inside"    #Choose "Inside" or "Outside"
    Painted = "No"          #Choose "Yes" of "No"
    return Material, Shape, Core, Location, Painted

#List of properties and constants                                                   #Units:
def select_material(Material, Shape, Painted, Location):
    if Material == "Copper":
    #Material properties
        Mc = 8960                   #Mass density copper                            [kg/m3]
        Cpc = 0.385e3               #Specific heat                                  [J/Kg*K]
        rho = 1.78e-8               #Electical resistivity  at 20 centrigrade       [Ohm m]
        alpha = 4.04e-3             #Thermische weerstand coefficient               [1/K]
        rho0 = rho/(1-alpha*20)     #Resistivity at 0 degree celsius                [Ohm m]
        if Painted == "No":
            epsilon = 0.4           #Emissivity from DIN 43671   
        elif Painted == "Yes":                
            epsilon = 0.9

    elif Material == "Aluminium" or "Al. alloy":
        #Material properties
        Mc = 2700                    #Mass density Aluminium                         [kg/m3]
        Cpc = 0.897e3                #Specific heat                                  [J/Kg*K]
        rho = 2.82e-8                #Electical resistivity at 20 centigrade         [Ohm m]
        alpha = 4.03e-3              #Thermische weerstand coefficient               [1/K]
        if Material == "Al. alloy":
            rho = 3.3e-8
            alpha = 3.7e-3
        rho0 = rho/(1-alpha*20)     #Resistivity at 0 degree celsius                [Ohm m]
        if Painted == "No" and Location == "Outside":
            epsilon = 0.50          #Emissivity from ABB Pocket book acc. to DIN 43670   
        elif Painted == "No" and Location == "Inside":
                epsilon = 0.35      #Emissivity from ABB Pocket book acc. to DIN 43670    
        elif Painted == "Yes":                
            epsilon = 0.9                                                  

    
    return Mc, Cpc, rho, rho0, alpha, epsilon

def component_parameters(Shape, Core, rho0, epsilon):
    #Component properties
    L = 2                        #Length of conductor                            [m]
    if Shape == "Cylindrical":
        if Core == "Solid":
            Dh = 40*(1/1000)      #Outer diameter                                 [m]
            ID = 0                #Inner diameter
            B = 2*np.pi*(Dh/2)    #Circumference                                  [m]
            S = np.pi*(Dh/2)**2   #Cross section                                  [m2]
            w = 0                 #Width not applicable
            
        elif Core == "Hollow":
            Dh = 80*(1/1000)            #Outer diameter
            WD = 8*(1/1000)             #Wall thickness                                [m]
            ID = Dh - 2*WD              #Inner diameter                                 [m]
            B = 2*np.pi*(Dh/2)          #Circumference                                  [m]
            S = (np.pi/4)*(Dh**2-ID**2) #Cross section                                  [m2]
            w = 0                       #Width not applicable
        
    elif Shape == "Rectangular":
        Dh = 80*(1/1000)           #Height                                         [m]
        ID = 0                     #Inner diameter
        w = 10*(1/1000)            #Width                                          [m]  
        B = 2*(Dh+w)               #Circumference                                  [m]
        S = Dh*w                   #Cross section                                  [m2]
        
    elif Shape == "Stranded":        
        SN = 48                 #Number of strands
        Dw = 3.5*(1/1000)       #Wire diameter  [m]
        Dh = 29*(1/1000)        #Outer diameter [m]
        ID = 0                  #Inner diameter [m]
        B = 2*np.pi*(Dh/2)      #Circumference (maybe multiply with factor due to strandedness)
        S = SN*np.pi*(Dw/2)**2  #Current carrying cross-section
        w = 0                   #Width not applicable
        
    A = B*L             #Outer surface                                  [m2]
    V = S*L             #Volume                                         [m3]
    Ro = rho0*L/S       #Resistance of conductor at 0 degree celsius    [Ohm]
    Sr = 0.5*A          #Solar irradiance receptive surface area        [m2]

    return Dh, ID, w, B, L, A, S, V, Ro, Sr

def ambient_parameters():
    #Surrounding fluid properties, air in this case
    M = 1.225           #Mass density                                   [kg/m3]
    Beta = 3.69e-3      #thermal expansion coefficient                  [1/K]
    Cpa = 1.01e3        #Specific heat                                  [J/Kg K]
    mu = 1.68e-5        #Dynamic viscosity                              [Pa*s]
    labda = 2.61e-2     #Thermal conductivity                           [W/m*K]
    v = 0.6             #Air velocity                                   [m/s]

    return M, Beta, Cpa, mu, labda, v

def PhyCo():
    #Physics constants
    g = 9.81            #Gravitational acceleration                     [m/s2]
    sigma = 5.67e-8     #Boltzmann constant                             [W/m2*K4]
    
    return g, sigma

def Wheather(Material):
    #Weather conditions
    phis = 900         #Solar flux density                                 [W/m2]
    if Material == "Copper":
        r = 0.64           #Solar absorption coefficient
    elif Material == "Aluminium":
        r = 0.3            #Solar absorption coefficient
    
    return phis, r


def Rac(Rdc, Shape, Core, Dh, ID, rho0, L, alpha, T, w):
    Ks = 1
    f = 50                                  #AC frequency of grid in [Hz]
    omega = 2*np.pi*f                       #Radial frequency
    mur = 1.2566e-6                         #Magnetic permeability of copper and aluminium (almost equal to mu_0)
    cond = 1/(rho0*(1+alpha*(T-273.15)))    #Conductivity [Sm]
    SD = np.sqrt(2/(2*np.pi*f*cond*mur))    #Skin depth
    RdcL = Rdc/L                            #Resistance per unit length (very important for following formulas)

    if Shape == "Stranded":
        Xs = np.sqrt((8*np.pi*f*1e-7*Ks)/RdcL)        #From IEC 60287 Skin effect
        if Xs > 0 and Xs <= 2.8:
            Ys = Xs**4/(192 + 0.8*Xs**4)
        elif Xs > 2.8 and Xs <= 3.8:
            Ys = -0.136 - 0.0177*Xs + 0.0563*Xs**2
        elif Xs > 3.8:
            Ys = 0.354*Xs - 0.733

        Rac = Rdc*(1+Ys) 
        
    if Shape == "Rectangular":     
        SD = np.sqrt(2/(omega*cond*mur))    #Skin depth
        A = Dh*w                            #Cross-sectional area
        Rdc = L/(Dh*w*cond)                 #DC resistance
        #Next formulas are from: "The AC resistance of Rectangular Conductors" by Alan Payne
        x = (2*(SD/w)*(1+(w/Dh) + 8*((SD/w)**3)/(Dh/w)))/((Dh/w)**(0.33)*mt.exp(-3.5*(w/SD) + 1))
        p = np.sqrt(A*1e6)/(1.26*(SD*1000))
        F = 1 - mt.exp(-0.026*p)
        K = 1 + F*(1.2/mt.exp(2.1*(Dh/w)) + 1.2/mt.exp(2.1*(w/Dh)))

        Rac = Rdc*(K/(1-mt.exp(-x)))
        
        Ys = 0  #Keep zero as not applicable
        Xs = 0  #Keep zero as not applicable

    if Shape == "Cylindrical" and Core == "Hollow":
        #From CIGRÉ: "Basic principles and practical methods to measure the AC and DC resistance of conductors of power cables"
        Re = Dh/2    #External radius
        Ri = ID/2    #Internal radius
        k = np.sqrt(omega*mur*cond)
        ke = k*Re*cmath.exp((np.pi/4)*1j)
        ki = k*Ri*cmath.exp((np.pi/4)*1j)
        kc = k*cmath.exp((np.pi/4)*1j)
        #ss.jv and ss.yv are Bessel functions, Rcomp is the complex resistance per unit length
        Rcomp = (kc/(2*np.pi*cond*Re))*((ss.jv(1, ki)*ss.yv(0, ke) - ss.yv(1, ki)*ss.jv(0, ke))/(ss.jv(1, ki)*ss.yv(1, ke) - ss.yv(1, ki)*ss.jv(1, ke)))
        Rac = Rcomp.real*L #Take the real part and multiply with length to find resistance
        #Rac = Rdc
        Ys = 0  #Keep zero as not applicable
        Xs = 0  #Keep zero as not applicable
        
    elif Shape == "Cylindrical" and Core == "Solid":
        #From Cigré report on AC resistance
        x = np.array([np.sqrt(omega*mur/(np.pi*RdcL))])
        #The functions below are Kelvin functions
        Ys = (x/2)*(ss.ber(x)*ss.beip(x) - ss.bei(x)*ss.berp(x))/(ss.berp(x)**2 + ss.beip(x)**2) - 1
        Rac = Rdc*(1+Ys)

        Xs = 0  #Keep zeros as not applicable

    return Rac, Ys, Xs
    

    
    
