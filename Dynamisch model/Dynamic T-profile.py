# -*- coding: utf-8 -*-
"""
Created on Fri May  5 10:52:36 2023

@author: AL27397
"""
import Import_EMS_and_KNMI
import Dynamic_heat_balance
import Dyn_Heat_flows
import Dyn_Properties
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

Table = Import_EMS_and_KNMI.create_final_import_table()
df_profielen = Import_EMS_and_KNMI.import_profielen()   #Vul zelf Inom in in andere file

I = Table["Belasting"]*5
Te = Table["Temp"]
Datetime = Table["Datetime"]
length = len(Datetime)
dt = 60*15              #Amount of seconds in 15 minutes

Inom = df_profielen["Continu"]
Belasting = df_profielen["Belasting"]
Te1 = (df_profielen["Temp"])*0+35+273.155
Datetime1 = df_profielen["Datetime"]
length = len(Datetime1)

Qirr = Dyn_Heat_flows.Qirr()
Qirr = np.ones(length)*Qirr
Qemis = np.zeros(length)
Qgen = np.zeros(length)
Qconv = np.zeros(length)
Qres = np.zeros(length)

#T0 = 30 + 273.15   #Initial conductor temperature, fill in first number in celsius
T0 = Te1[0]          #Initial conductor temperature, set equal to ambient temperature
T = np.zeros(length+1)
dT = np.zeros(length)
T[0] = T0

for i in range(length):
    
    #T[i+1], dT[i], Qemis[i], Qirr[i], Qgen[i], Qconv[i], Qres[i] = Dynamic_heat_balance.dynT(I[i], T[i], Te[i], dt)
    T[i+1], dT[i], Qemis[i], Qirr[i], Qgen[i], Qconv[i], Qres[i] = Dynamic_heat_balance.dynT(Belasting[i], T[i], Te1[i], dt)  #df_profielen
    

Material, Shape, Core, Location, Painted = Dyn_Properties.Component()      
    
T = T - 273.15      #Convert to degree celsius
Te = Te - 273.15  #Convert to degree celsius
"""
#Year profile
plt.plot(Datetime,T[0:-1])
plt.plot(Datetime,Ted)
plt.plot(Datetime,Id)
plt.title('Temperature profile of ' + Shape + ' ' + Material + ' ' + Location)
plt.xlabel("Time [s]")
plt.ylabel("T [C]")
plt.legend(["Tconductor","Tambient"])
plt.show() 

plt.plot(Datetime,Id)
plt.title('Load profile of ' + Shape + ' ' + Material + ' ' + Location)
plt.xlabel("Time [s]")
plt.ylabel("I [A]")
plt.show() 
"""

"""
#Day profile
plt.plot(Datetime[0:93],T[0:93])
plt.plot(Datetime[0:93],Ted[0:93])
#plt.plot(Datetime[0:93],Id[0:93])
plt.title('Temperature profile of ' + Shape + ' ' + Material + ' ' + Location)
plt.xlabel("Time [s]")
plt.ylabel("T [C]")
plt.legend(["Tconductor","Tambient"])
plt.show()    

plt.plot(Datetime[0:93],Id[0:93])
plt.title('Load profile of ' + Shape + ' ' + Material + ' ' + Location)
plt.xlabel("Time [s]")
plt.ylabel("I [A]")
plt.show() 
"""

"""
a = 0
b = 93

#Day profile
ax1 = plt.plot()
plt.plot(Datetime[a:b],T[a:b])
plt.plot(Datetime[a:b],Te[a:b])
plt.legend(["Tconductor","Tambient"])
plt.xlabel("Time [s]")
plt.ylabel("T [C]")

ax2 = plt.gca().twinx()
ax2.plot(Datetime[a:b],I[a:b], color='r')
plt.ylabel("I [A]")
#plt.legend(["Tconductor","Tambient","Current"])
plt.title('Temperature profile of ' + Shape + ' ' + Material + ' ' + Location)
plt.show() 
"""
a = 0
b = 168

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
fig, ax1 = plt.subplots()
line1 = ax1.plot(Datetime1[a:b],Inom[a:b],  label = 'Inom')
line2 = ax1.plot(Datetime1[a:b],Belasting[a:b],  label = 'Belasting')
plt.gcf().autofmt_xdate()
#plt.legend(["Inom","Belasting"], loc=4)


plt.xlabel("Time [days]")
plt.ylabel("I [A]")

ax2 = ax1.twinx()
#ax2 = plt.gca().twinx()
line3 = ax2.plot(Datetime1[a:b], T[0:-1], color='r',  label = 'Tconductor')
plt.ylabel("T [C]")
#ax1.legend(handles=[line1, line2, line3])
ax1.legend( handles=line1+line2+line3, loc=4 )
plt.title('Temperature profile of ' + Shape + ' ' + Material + ' ' + Location)
plt.show() 
