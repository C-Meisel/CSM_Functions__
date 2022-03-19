''' This module contains functions to help format and plot XRD files from
the bruker xrd in Toberer's lab
# C-Meisel
'''

'Imports'
import matplotlib.pyplot as plt
from zipfile import ZipFile #needed for the Bruker XRD functions
import csv
from shutil import copyfile
import pandas as pd

def brml2csv(loc):
    loc = '/Users/Charlie/Documents/CSM/XRD_Data/7Jul21_Bruker_BCFZYESB/80BCFZY_20ESB_18min.brml'
    copyfile(loc, loc.replace('.brml','')+'.zip') #Creating a new file that is a .zip
    loc_zip = loc.replace('.brml','')+'.zip' #Access new zip file
    zip = ZipFile(loc_zip, 'r') #Creats a new zipfile object
    loc_data = zip.extract('Experiment0/RawData0.xml') #accesing the data we want
    copyfile(loc_data, loc_data.replace('.xml','')+'.csv') #Creating a new file that is a .csv
    return loc_data

def bruker_xrd_format(loc):
    loc_data = brml2csv(loc)
    loc_csv = loc_data.replace('.xml','')+'.csv' #Access new csv
    file = csv.reader(open(loc_csv, "r",encoding='latin1'), delimiter=",") #I honestly dk what is going on here, but it works
    for row in file: #Finding where the data we want starts so I can cut extra stuff out of the Dataframe
        if '      </SubScans>' in row:
            skip = file.line_num
            break
    for row in file: #Finding the line with the last data point
        if '      <ExtLocations />' in row:
            last_data = file.line_num
            break
    end = last_data-skip-2 #Calculating which index I should stop the dataframe at the -2 is to account for indexing starting at 0
    df = pd.read_csv(loc_csv,sep= ',',skiprows=skip,encoding='latin1')[:end] # Making a dataframe that is a relavent size
    df.columns = ['datum','idk','2theta','theta','intensity'] #labeling columns
    df['intensity'] = df['intensity'].str.replace(r'\D', '',regex=True).astype(int) #chops off random words after intensity and saves as an int. idk man
    #The stacked overflow was pretty good https://stackoverflow.com/questions/13682044/remove-unwanted-parts-from-strings-in-a-column
    df.drop(labels=['datum','idk','theta'], axis=1,inplace=True) #Drops randon ass columns that no one needs. wont work w/o inplace=True
    return df

def plot_xrds_bruker(loc, material='',y_offset=0,normalize=True):
    df = bruker_xrd_format(loc)
    # /\/\/\/\/\/\/\/\ Normalizing the data to 1 /\/\/\/\/\/\/\/\ #
    if normalize==True:
        maximum = df['intensity'].max() #finds the highest intensity value
        df['intensity'] = df['intensity']/maximum #normalizes data by dividing all intensity values by the max
        
    # [][][][][][][] Plotting [][][][][][][] #
    # fig, ax = plt.subplots() #Creates figure
    # ax.plot(df['2theta'],df['intensity']+y_offset,label = material) #Plotts Intensity as a function of 2theta
    plt.plot(df['2theta'],df['intensity']+y_offset,label = material)
    plt.xlabel('2\u03B8')
    plt.ylabel('Intensity')
    if normalize == True: #if the data is normalized the ylabel will let you know that it is
        plt.ylabel('Relative Intensity')
    plt.legend()
    plt.tight_layout()
    plt.show()