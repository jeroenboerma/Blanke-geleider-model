"""
In this script the nominal current for various final temperatures 
for multiple dimensions of the same conductor is calculated. Specify
the conductor in Properties_fun.py and run this script for output.
"""
import numpy as np
import Properties_fun
import Det_Imax_fun
import pandas as pd
pd.options.display.float_format = '{:,.1f}'.format

Width, Thickness, Diameter, Wall_Thickness = Properties_fun.dimensions()
Material, Shape, Core, Location, Painted = Properties_fun.Component()

#Input values for Tmax. Input Tfinal of nominal current and the maximum allowed
#final temperature for comparison. 
Tmax = np.array([65, 80]) + 273.15          #Maximum permissible conductor temperature [K]

if Shape == "Rectangular":
    index_name = [str(Width[i]*1e3) + ' x ' + str(Thickness[i]*1e3) + ' mm' for i in range(len(Width))]
    I = np.zeros([len(Width), len(Tmax)])
    
    for ii in range(len(Tmax)):
        for i in range(len(Width)):
            I[i, ii] = Det_Imax_fun.Imax(Material, Shape, Core, Location, Painted, Width[i], Thickness[i], 0, 0, Tmax[ii])
    
elif Shape == "Cylindrical" and Core == "Solid":
    index_name = [str(Diameter[i]*1e3) + 'mm \u2300' for i in range(len(Diameter))]
    I = np.zeros([len(Diameter), len(Tmax)])
    
    for ii in range(len(Tmax)):
        for i in range(len(Diameter)):
            I[i, ii] = Det_Imax_fun.Imax(Material, Shape, Core, Location, Painted, 0, 0, Diameter[i], 0, Tmax[ii])

elif Shape == "Cylindrical" and Core == "Hollow":
    index_name = [str(Diameter[i]*1e3) + ' \u2300 x ' + str(Wall_Thickness[i]*1e3) + ' mm'  for i in range(len(Diameter))]
    I = np.zeros([len(Diameter), len(Tmax)])
    
    for ii in range(len(Tmax)):
        for i in range(len(Diameter)):
            I[i, ii] = Det_Imax_fun.Imax(Material, Shape, Core, Location, Painted, 0, 0, Diameter[i], Wall_Thickness[i], Tmax[ii])


column_name = ['Nominale stroom', 'Verhoogde belastbaarheid']

Load_capacity = pd.DataFrame(I, index=index_name, columns=column_name)