# -*- coding: utf-8 -*-
"""
Created on Fri May  5 13:17:45 2023

@author: AL27397
"""
import pandas as pd
import datetime

#### INSTELLINGEN ####

# specificeer start en einddatum voor knmi data
startdate = "20220101"
enddate = "20221231"

# plek waar KNMI en EMS data staan
Bronmap = r"C:\Users\AL27397\OneDrive - Alliander NV\Documents\Ketenbelastbaarheidstudie\Blanke geleiders\Thermische modellen\Belasting en weer data"

# definieer pad naar knmi bestand (.txt)
knmifile = r"KNMI_uurgeg_Voorschoten_215_2021-2030.txt"
knmifilepath = Bronmap + "\\" + knmifile

# definieer pad naar EMS bestand (.csv)
emsfile = r"EMS KAW 10 kV TR2+TR3 INS2 en TR1+TR3 INS3.csv"
emsfilepath = Bronmap + "\\" + emsfile

# specificeer de kolomnaam in het csv bestand waarin de stroom waardes staan die gebruikt moeten worden
belastingkolom = "INS2"

# Instellingen filepaths standaard profielen - pas het pad aan naar waar je de .vud bestanden neerzet
profielbelastingfilepath = (
    r"C:\Users\AL27397\OneDrive - Alliander NV\Documents\Ketenbelastbaarheidstudie\Blanke geleiders\Thermische modellen\Belasting en weer data\Belastingprofiel.vud")
profielzonfilepath = (
    r"C:\Users\AL27397\OneDrive - Alliander NV\Documents\Ketenbelastbaarheidstudie\Blanke geleiders\Thermische modellen\Belasting en weer data\Zon 100% profiel 1 dag.vud")
profielwindfilepath = (
    r"C:\Users\AL27397\OneDrive - Alliander NV\Documents\Ketenbelastbaarheidstudie\Blanke geleiders\Thermische modellen\Belasting en weer data\Windprofiel 3 dagen 100% 4 dagen 25%.vud")
profielzonwindfilepath = (
    r"C:\Users\AL27397\OneDrive - Alliander NV\Documents\Ketenbelastbaarheidstudie\Blanke geleiders\Thermische modellen\Belasting en weer data\50% wind + 50% Zon profiel 7 dagen.vud")

############################
### HOOFDFUNCTIES ##########

# importeert de standaard profielen in python
def import_profielen():
    #import profielen
    profiel_belasting = pd.read_csv(profielbelastingfilepath)
    profiel_zon = pd.read_csv(profielzonfilepath)
    profiel_wind = pd.read_csv(profielwindfilepath)
    profiel_zon_wind = pd.read_csv(profielzonwindfilepath)

    #Creer datum/tijd kolom voor dataframe en voeg samen met bovenstaande profielen kolom in tabel (dataframe). 
        # LET OP! Profielwaarden zijn % Belasting (K), niet belasting in I. 
        # Compenseer door te vermenigvuldigen met Inom/100
        # Temperatuur = 20 graden celcius.
    Inom = 1240
    datetime = pd.date_range("2020-01-01", periods=168, freq = "H")
    df_profielen = pd.DataFrame(datetime, columns=["Datetime"])
    df_profielen["Continu"] = Inom
    df_profielen["Belasting"] = profiel_belasting.values*Inom/100
    df_profielen["Zon"] = profiel_zon.values*Inom/100
    df_profielen["Wind"] = profiel_wind.values*Inom/100
    df_profielen["Zon_Wind"] = profiel_zon_wind.values*Inom/100
    df_profielen["Temp"] = 20
    
    return df_profielen

# hoofdfunctie die de EMS data en KNMI data in 1 tabel zet
def create_final_import_table():
    df_invoer = get_data_ems()
    df_temp_hour = get_data_knmi()
    df_final = pd.merge(left=df_invoer, right=df_temp_hour, how="left", left_on=["Datum","Uur"], right_on=["Datum","Uur"])
    
    return df_final

####################################
#### KNMI DATA IMPORT FUNCTIES ######

### eindfunctie om data van KNMI in te lezen ###
def get_data_knmi():

    df_temp_hour = import_knmi()
    print("import")
    
    #Datatransformaties
        #Bereken juiste temp (in 1 C ipv 0.1C) en uren (24-->23)
    df_temp_hour["Temp"] = df_temp_hour["T"]/10 + 273.15 # T is in 0.1C, zet om naar Temp in C
    df_temp_hour["Uur"] = df_temp_hour["Uur"]-1
    
#     df_temp_hour[["T", "Temp"]] = df_temp_hour[["T", "Temp"]].apply(pd.to_numeric)
        
    return df_temp_hour

#Import KNMI data
def import_knmi():
    # Import data
    df_temp_hour = pd.read_csv(
        knmifilepath, 
        sep = ",", 
        skiprows = 31, 
        header = 0, 
        usecols = [0,1,2,7], 
        names = ["Station","Datum","Uur","T"], 
        dtype = {"Uur":int}, 
        parse_dates=['Datum']
    )
    
    # Datatransformaties
    startdate_datetime = datetime.datetime.strptime(startdate, "%Y%m%d")
    enddate_datetime = datetime.datetime.strptime(enddate, "%Y%m%d")
    
    print(startdate_datetime)
    print(enddate_datetime)

#     df_temp_hour = df_temp_hour[(
#         df_temp_hour['Datum'] >= startdate_datetime
#     )]
#     df_temp_hour = df_temp_hour[(
#         df_temp_hour['Datum'] <= enddate_datetime
#     )]
    
    return df_temp_hour


#################################
### EMS DATA IMPORT FUNCTIES ####

def get_data_ems():

    df_invoer = import_ems_csv()
        
    # Tabeltransformaties:
        # Hernoem belastinkolom naar "Belasting"
        # Creer 'Datetime_shifted' kolom (type datetime) met offset van -15 minuten (om te matchen met KNMI data)
        # Creer 'Uur' kolom (type int) als key-kolom voor datum-uur koppeling tussen KNMI en df_invoer
        # Creer 'Datum' kolom (type datetime) voor datum-uur koppeling tussen KNMI en df_invoer
    df_invoer.rename(columns={belastingkolom:"Belasting"},inplace=True) #verander kolomnaam Totaal naar Belasting
    df_invoer["Belasting"] = df_invoer["Belasting"]
    df_invoer["Datetime_shifted"] = df_invoer["Datetime"] - pd.Timedelta(minutes=15)
    df_invoer["Uur"] = df_invoer["Datetime_shifted"].dt.strftime('%H').astype(int)
    df_invoer["Datum"] = df_invoer["Datetime_shifted"].dt.date.astype('datetime64')
    
    return df_invoer

def import_ems_csv():
    #functie om datum/tijd op een goede manier te creeren in df_invoer
    dateparse = lambda x: datetime.datetime.strptime(x, '%d-%m-%Y %H:%M')
    
    df_invoer = pd.read_csv(
        emsfilepath, 
        usecols = [' Datum','Tijd', belastingkolom], 
        parse_dates = {'Datetime': [' Datum', 'Tijd']}, 
        date_parser=dateparse,
        sep = ";",
        decimal=",", 
        dtype = {belastingkolom:float}
    )
    
    return df_invoer