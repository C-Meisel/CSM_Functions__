''' This module contains functions to help format Electrohchemical Impedance Spectroscopy (EIS)
data. The data files are obtained by a Gamry potentiostat. The files are .DTA files
# C-Meisel
'''

'Imports'
import pandas as pd
import csv

def dta2csv(loc:str):
    '''
    Duplicates the .DTA files and converts it to a .CSV file
     
    param loc: str, location of dta file to convert to a csv

    return --> None 
    '''
    file = loc
    copyfile(file, file.replace('.DTA','')+'.csv')
    
def iv_data(area:float, loc:str) -> pd.DataFrame:
    '''
    Takes a .DTA file from an polarization curve (IV curve), extracts the voltage and amperage,
    and calculates the power density of each point. Then converts this data to a dataframe

    param area: float, active cell area for the cell that the data is from
    param loc: str, location of the .DTA file

    return --> Dataframe
    '''
    "Converts and finds CSV then turns it into a dataframe"
    dta2csv(loc)
    loc_csv = loc.replace('.DTA','')+'.csv'
    file = csv.reader(open(loc_csv, "r",encoding='latin1'), delimiter="\t") #I honestly dk what is going on here, but it works
    for row in file: #searches first column of each row in csv for "ZCURVE", then adds 1. This gives the right amount of rows to skip
        if row[0] == 'CURVE':
            skip = file.line_num+1
            break
    df = pd.read_csv(loc_csv,sep='\t',skiprows=skip,encoding='latin1')
    "calculations and only keeping the useful data"
    df['A'] = df['A'].div(-area)
    df['W'] = df['W'].div(-area)
    df_useful = df[['V','A','W']]

    return df_useful   
    
def ocv_data(loc:str):
    '''
    Takes a .DTA file that read the cell voltage, extracts the voltage and time,
    then converts this data to a dataframe.

    param loc: str, location of the .DTA file

    return --> none
    '''

    dta2csv(loc)
    loc_csv = loc.replace('.DTA','')+'.csv'
    file = csv.reader(open(loc_csv, "r",encoding='latin1'), delimiter="\t") #I honestly dk what is going on here
    skip = 0
    for row in file: #searches first column of each row in csv for "CURVE", then adds 1. This gives the right amount of rows to skip
        if row[0] == 'CURVE':
            skip = file.line_num+1
            print(skip)
            break
        if row[0] == 'READ VOLTAGE': #For whatever reason the DTA files are different if the data is aborted
            skip = file.line_num+1
            print(skip)
            break
    df = pd.read_csv(loc_csv,sep='\t',skiprows=skip,encoding='latin1')
    df_useful = df[['s','V']]
    df_useful.to_csv(loc_csv)

def peis_data(area:float,loc:str):
    '''
    Extracts area zreal and zimag .DTA file for potentiostatic eis. Converts z data to be area specific
    then places data in a pandas dataframe

    param loc: str, location of the .DTA file

    return --> none
    '''
    
    #Returns Zreal and Zimag from a DTA file of PotentiostaticEis in a CSV - not tested
    dta2csv(loc) #convert DTA to a CSV
    loc_csv = loc.replace('.DTA','')+'.csv' #access newly made file
    #find right amount of rows to skip
    file = csv.reader(open(loc_csv, "r",encoding='latin1'), delimiter="\t") #I honestly dk what is going on here
    for row in file: #searches first column of each row in csv for "ZCURVE", then adds 1. This gives the right amount of rows to skip
        if row[0] == 'ZCURVE':
            skip = file.line_num+1
            break
    df = pd.read_csv(loc_csv,sep= '\t',skiprows=skip,encoding='latin1')
    df['ohm.1'] = df['ohm.1'].mul(-1*area)
    df['ohm'] = df['ohm'].mul(area)
    df_useful = df[['ohm','ohm.1']]
    df_useful.to_csv(loc_csv)