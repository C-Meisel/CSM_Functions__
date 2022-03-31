''' 
This module contains all other functions that I made for analyzing data.
They mostly pertain to random charactarization techniques or software.

# C-Meisel
'''

'Imports'
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
import cmasher as cmr
import numpy as np
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
"Mass Spec functions"
'Functions to help me format data from the Prima DB mass spec in GRL241'
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
def ms_df_tc(loc:str)->pd.DataFrame: 
    '''
    Takes a CSV file from the prima DB and turnes it into a df with the useful materials and
    converts time into relative time from the first measurement taken
    ms = mass spec, df = dataframe, tc = time converter
    
    Param loc, str: (path to a file)
        Location of the CSV file containing the mass spec data

    Return --> a dataframe containing the desired time values
    '''
    # Time conversion
    df = pd.read_csv(loc)
    t_init = int(pd.to_datetime(df.at[0,'Time&Date']).strftime("%s")) #converts excel time into something more useable and sets this as the initial time
    df['Time&Date'] = pd.to_datetime(df['Time&Date']).apply(lambda x: x.strftime('%s')) #-t_init#.dt.strftime("%s")-t_init #converts absolute time to relative time
    t_values = [int(t) for t in df['Time&Date'].to_numpy()]
    df['Time&Date'] = [t-t_init for t in t_values]
    return df

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
"Drycal Functions"
'Functions to help me format data from the Drycals used to calculate gas flow'
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
def plot_drycal_flow(loc_excel:str, sheet:str): 
    '''
    Plots drycal flow from a specific sheet in a specific file in excel

    Param loc_excel, str: (path to a file)
        Location of the excel file containing the drycal data
    Param sheet, str:
        Name of the sheet in the excel file to be plotted
    
    Return --> none but a plot is generated and shown
    '''
    
    df = pd.read_excel(loc_excel,sheet,skiprows=3)
    flow = df['DryCal scc/min ']
    time= [int(t.strftime('%s')) for t in df['Time'].to_numpy()] #Converts the date time into an integer array of seconds from epoc
    #Each time in df_dc_c1['Time'] is converted into seconds from epoc and then converted into an integer. 
    # df_dc_c1['Time'] is first converted into an array in numpy
    
    t0 = time[0] #Gets first time
    test_time = [t-t0 for t in time] #Getting delta t from start of test
    
    # - Plotting
    fig, ax = plt.subplots()
    ax.plot(test_time,flow,'b',linewidth=2.5)
    ax.set_xlabel('Time (s)',weight='bold')
    ax.set_ylabel('Flow (SCCM)',weight='bold')
    plt.tight_layout()
    plt.show()

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
"Gas Chromatography Functions"
'Functions to help me format data from the gas chromatagropher (GC) and plot it'
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
def plot_gc(loc_excel:str, sheet:str):
    '''
    Plots GC data from a specific sheet in a specific file in excel
    It is currently set to plot the Hydrogen, Nitrogen, and Methane Data

    Param loc_excel, str: (path to a file)
        Location of the excel file containing the GC data
    Param sheet, str:
        Name of the sheet in the excel file to be plotted

    Return --> none but a plot is generated and shown
    '''
    df= pd.read_excel(loc_excel,sheet,skiprows=3,usecols=[1,2,3,4])
    fig,ax = plt.subplots()

    # - Plotting
    ax.plot(df['Run'],df['Hydrogen (%)'],label='H$_2$')
    ax.plot(df['Run'],df['Nitrogen (%)'],label='N$_2$')
    ax.plot(df['Run'],df['Methane (%)'],label='CH$_4$')
    ax.set_xlabel('GC run',weight='bold')
    ax.set_ylabel('Gas Concentration (%)',weight='bold')
    plt.legend()
    plt.tight_layout()
    plt.show()

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
"SEM Functions"
'Functions to help me format and plot Scanning Electron Microscope (SEM) data'
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
def eds_line_plot(loc_csv:str, only:list = [''], no_O2:bool = False, reverse:bool = False,
                    sort_bczyyb:bool = False, dp:bool = False):
    '''
    Plots EDS line scan data from the Apex EDAX software from the Tescan SEM

    Param loc_csv, str: (path to a file)
        Path to the CSV file containing the EDS line scan data
    Param only, list: (Default = [''])
        List of elements that you want to plot. If empty, all elements are plotted
    Param no_O2, bool: (Default = False)
        If True, the O2 data is thrown out of the dataset and the at% values are re-calculated
    Param reverse, bool: (Default = False)
        If True, the data is plotted with the distance reversed
    Param sort_bczyyb, bool: (Default = False)
        If True, the data is sorted by the order of the elements in BCZYYb for the plot legend
    Param dp, bool: (Default = False)
        If True, this lets the function know it is plotting a depth profile which will just
        change the plot formatting

    Return --> None but a plot is generated and shown
    '''
    
    
    file = csv.reader(open(loc_csv, "r",encoding='latin1'),delimiter=',') #enables the file to be read by pytoh
    for row in file: #searches for start of data
        if row[0] == 'Point': #string in first column in the row where the data starts
            skip = file.line_num-1
            break
    df = pd.read_csv(loc_csv,sep= ',',skiprows=skip,encoding='latin1',index_col=False) #creates dataframe, in this case sep needs to be ,
    df.drop(columns=['Point',' Image',' Frame'],inplace=True) #Drops values that are not needed 

    if sort_bczyyb == True:
        Ba_column = df.pop(' Ba L') # Barium to first spot
        df.insert(1, ' Ba L', Ba_column)
        Ce_column = df.pop(' Ce L') # Cerium to second spot
        df.insert(2, ' Ce L', Ce_column)
        if ' Zr L' in df.columns: # Zirconium to third spot
            Zr_column = df.pop(' Zr L') 
            df.insert(3, ' Zr L', Zr_column)
        else:
            Zr_column = df.pop(' Zr K') 
            df.insert(3, ' Zr K', Zr_column)  
        if ' Y L' in df.columns:
            Y_column = df.pop(' Y L') 
            df.insert(4, ' Y L', Zr_column)
        else:
            Y_column = df.pop(' Y K') # Yttrium
            df.insert(4, ' Y K', Y_column)
        if ' Yb M' in df.columns: #ytterbium, checking to see which band is being plotted
            Yb_column = df.pop(' Yb M')
            df.insert(5, ' Yb M', Yb_column)
        else:
            Yb_column = df.pop(' Yb L')
            df.insert(5, ' Yb L', Yb_column)
        if ' Ni K' in df.columns:
            Ni_column = df.pop(' Ni K')
            df.insert(6, ' Ni K', Ni_column)

    cols = list(df.columns.values) #Makes list of cols
    cols.pop(0) #Drops Distance from cols list

    if no_O2 == True:
        df.pop(' O K') # Gets rid of Oxygen column
        cols = list(df.columns.values)
        df.loc[:,cols[1]:cols[len(cols)-1]] = df.loc[:,cols[1]:cols[len(cols)-1]].div(df.sum(axis=1), axis=0)
        df.loc[:,cols[1]:cols[len(cols)-1]] = df.loc[:,cols[1]:cols[len(cols)-1]]*100
        cols.pop(0) #Drops Distance from cols list
        
    if reverse == True:
        df[" Distance (um)"] = df[" Distance (um)"].values[::-1]

    # Plotting
    fig, ax = plt.subplots() #Starts Plot
    if len(only[0])==0: #If there are no specified elements in only, then all elements will be plotted
        for col in cols: #Plots all of the columns
            ax.plot(df[' Distance (um)'],df[col],label = col,linewidth=2)

    elif len(only[0])>=1: #if certain elements are speficied then those elemens will be
        col_new = []
        for atom in cols: #Seraches through all the elements
            for element in only: #searches through all the selected elements
                if atom.find(element+' ')!=-1: #if the selected element matches with one of the elements in the datatset
                    col_new.append(atom) # appending the matching element to a new element list
                    break

        for col in col_new: #Plots the columns for the selected elements only 
            ax.plot(df[' Distance (um)'],df[col],label = col,linewidth=2)

    # --- Plot formatting
    plt.legend()
    if dp == True:
        ax.annotate("Positrode", xy=(0,0), xycoords="axes fraction",
                        xytext=(-11,-21), textcoords="offset points",
                        ha="left", va="top",size='large') # Places "Positrode" in a certain spot
    ax.spines['left'].set_bounds(0,df.to_numpy().max()*1.07)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    if reverse == False:
        ax.spines['bottom'].set_bounds(0, round(df[' Distance (um)'].iloc[-1],0))
    elif reverse == True:
        ax.spines['bottom'].set_bounds(0, round(df[' Distance (um)'].iloc[0],0))
    plt.legend(loc='upper left',bbox_to_anchor=(0.97,1),ncol=1,fontsize='large')
    ax.set_xlabel('Distance ($\mu$m)',size='x-large')
    ax.set_ylabel('Atomic %',size='x-large')
    ax.tick_params(axis='both', which='major', labelsize='large')
    plt.tight_layout()
    plt.show()


#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
"Particle size analyzer (PSA) functions"
'Functions to help me format and plot data from the PSA in Hill Hall 375'
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
def psa_d50(loc:str)->float: 
    '''
    Takes in a PSA excel sheet and returns the D50 of the sample (float)
    D50 is the diameter of a particle in the 50th percentile of size

    Param loc, str: (path to a file)
        Location of the excel file containing the PSA data
    
    Return --> D50, float
    '''
    
    # --- Making a dataframe for the useful data
    df = pd.read_excel(loc,'Sheet1',skiprows=25,nrows=10) #The percentiles alwayas start at row 26 and will only need 10 rows
    
    # --- returning the D50
    d50 = df[df['%Tile']==50].iloc[0,2] #This returns a float. Looks through df %tile column for 50 then returns the value in column 3 (2+1)
    
    return d50

def psa_plot(loc:str, plot_d50:bool=True):
    '''
    Plots Particle size analyzer data and shows the D50 on the plot if plot_d50 is True

    Param loc, str: (path to a file)
        Location of the excel file containing the PSA data
    Param plot_d50, bool: (Default = True)
        If True, the D50 will be plotted on the plot as a verticle line
    
    Return --> None but a plot is created and shown
    '''
    
    df = pd.read_excel(loc,'Sheet1',skiprows=68) #the sheet will always be called sheet 1 and the data will always start at row 69 (nice)
    d50 = psa_d50(loc) # retreives d50

    # --- Plotting
    fig,ax = plt.subplots()
    ax.plot(df['Size(um)'],df['%Chan'],'k',linewidth=4)

    # --- plotting D50 and printing value
    if plot_d50==True:
        ax.axvline(d50,color='#D2492A')
        d50s = f'{d50}' #converting the int to a string so I can print it on the figure
        ax.text(d50,0.1,r'$D50 =$'+d50s+r' $\mu m$',ha='left',size='large',weight='bold',color='#D2492A')

    # - Misc plot formatting
    ax.set_xscale('log')
    ax.set_ylabel('% Chance (%)',size=16)
    ax.set_xlabel('Particle Diameter ($\mu$m)',size=16)
    ax.tick_params(axis='both', which='major', labelsize=14)
    plt.tight_layout()

def psa_plots(list:list):
    '''
    Plots multiple PSA data sets on the same plot

    Param list, list of strs:
        List of paths to the PSA files to be plotted

    Return --> None, but a plot is created and shown
    '''
    
    # --- Plotting
    fig,ax = plt.subplots()
    for psa in list:
        df = pd.read_excel(psa[0],'Sheet1',skiprows=68) #the sheet will always be called sheet 1 and the data will always start at row 69 (nice)
        ax.plot(df['Size(um)'],df['%Chan'],label=psa[1],linewidth=4)
    # - Mist plotting stuff
    ax.set_xscale('log')
    ax.set_ylabel('% Chance (%)',size=16)
    ax.set_xlabel('Particle Diameter ($\mu$m)',size=16)
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.legend()
    plt.tight_layout()
    plt.show()

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
"EPMA"
'Functions to help me format and plot Electron Probe Microanalyzer (EPMA) data taken at KICET in South Korea'
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
def epma_plots(folder:str, sem:bool = True):
    '''
    Plots EPMA elemental maps from a folder of EPMA files. Each EPMA scan data is in its own distinct folder.
    If sem = True then the SEM images of the cells are plotted as well.

    Param folder, str: (path to directory)
        Location of the file containing the EPMA data for a sample
    Param sem, bool: (Default = True)
        Plots the Secendary Electron (SEI) and Back Scattered Electron (COMPO) images of the cell
        where the elemental data was taken.

    Return --> None, but a plot of plots is created and shown
    '''

    # --- Extracting all datafiles from the folder:
    if sem == False:
        data = [file for file in os.listdir(folder) if file.endswith('La.csv')]
    elif sem == True:
        data = [file for file in os.listdir(folder) if file.endswith('.csv')]

    # ----- Sorting the datafiles:
    i = 0
    for file in data:
        if file.find('Ba') != -1:
            data.remove(file)
            data.insert(i,file)
            i = i + 1

    for file in data:
        if file.find('Ce') != -1:
            data.remove(file)
            data.insert(i,file)
            i = i + 1

    for file in data:
        if file.find('Zr') != -1:
            data.remove(file)
            data.insert(i,file)
            i = i + 1

    for file in data:
        if file.find('Y') != -1:
            data.remove(file)
            data.insert(i,file)
            i = i + 1

    for file in data:
        if file.find('Yb') != -1:
            data.remove(file)
            data.insert(i,file)
            i = i + 1

    for file in data:
        if file.find('Ni') != -1:
            data.remove(file)
            data.insert(i,file)
            i = i + 1

    if sem == True:
        for file in data:
            if file.find('SEI') != -1:
                data.remove(file)
                data.insert(i,file)
                i = i + 1
        for file in data:
            if file.find('COMPO') != -1:
                data.remove(file)
                data.insert(i,file)
                i = i + 1

    # ---- Plotting data
    if len(data) > 4 and len(data) <= 6:
        fig, axs = plt.subplots(2,3)
        fig.set_size_inches(11, 7)
    if len(data) >6 and len(data) <=8:
        fig, axs = plt.subplots(2,4)
        fig.set_size_inches(10, 5)
    if len(data) == 9:
        fig,axs = plt.subplots(3,3)

    for idx, ax in enumerate(axs.reshape(-1)):
        if idx <= len(data)-1 and data[idx].find('SEI')==-1 and data[idx].find('COMPO')==-1:
            element_data = os.path.join(folder,data[idx])

            # --- Converting the data to a dataframe and obtaining the element name
            df = pd.read_csv(element_data,header=None,encoding='latin1')
            element = os.path.basename(element_data).split("_", 2)[1]

            # --- Initializing the plot
            cmap = cmr.get_sub_cmap('cmr.chroma', 0.10, 0.95) #cmr.chroma cmr.rainforest
            im = ax.imshow(df.values,cmap=cmap,vmin=0,vmax=100)
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.05)
            cbar = plt.colorbar(im,cax=cax)

            # --- Formatting the plot
            font = 'Helvetica'
            df_len = len(df.index)
            xticks = [0,df_len-1]
            yticks = [0,df_len-1]
            labels = [0,25]
            ax.xaxis.set_ticks(xticks)
            ax.set_xticklabels(labels)
            ax.yaxis.set_ticks(yticks)
            ax.set_yticklabels(np.flip(labels))
            ax.tick_params(axis='both', which='major', labelsize='large')
            ax.set_ylabel('\u03BCm',size='x-large',family=font)
            ax.yaxis.labelpad = -15
            ax.set_xlabel('\u03BCm',size='x-large',family=font)
            ax.xaxis.labelpad = -15

            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            cbar.ax.tick_params(labelsize=12)
            cbar.ax.yaxis.set_ticks([0,100])

            ax.set_title(element,family=font,size='xx-large')

            fig.tight_layout()

        elif idx <= len(data)-1 and sem == True and (data[idx].find('SEI')!=-1 or data[idx].find('COMPO')!=-1):
            image = os.path.join(folder,data[idx])

            # --- Converting the data to a dataframe and obtaining the element name
            df = pd.read_csv(image,header=None,encoding='latin1')
            if data[idx].find('SEI')!=-1:
                image_type = os.path.basename(image).split("_", 1)[1].replace('.csv','')
            elif data[idx].find('COMPO')!=-1:
                image_type = 'BSE'
            max = df.max().max()
            im = ax.imshow(df.values,cmap='gray', vmin=0, vmax=max)
            cbar = fig.colorbar(im,ax=ax)
            cbar.remove()
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title(image_type,family=font,size='xx-large')
            plt.tight_layout()

        elif idx > len(data)-1:
            ax.set_visible(False)

    plt.show()