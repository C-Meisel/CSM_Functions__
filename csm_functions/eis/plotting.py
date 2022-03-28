''' This module contains functions to help format and plot Electrohchemical Impedance Spectroscopy (EIS)
data. The data files are obtained by a Gamry potentiostat. The files are .DTA files
# C-Meisel
'''

'Imports'
import pandas as pd
import csv

def plot_ocv(loc : str):
    '''
    Plots OCV vs time from a .DTA file

    Param loc,str: Location of the .DTA file that contains the OCV data.

    returns: the plot of the figure
    '''
    dta2csv(loc)
    loc_csv = loc.replace('.DTA','')+'.csv'
    file = csv.reader(open(loc_csv, "r",encoding='latin1'), delimiter="\t") #I honestly dk what is going on here
    skip = 0
    for row in file: #searches first column of each row in csv for "CURVE", then adds 1. This gives the right amount of rows to skip
        if row[0] == 'CURVE':
            skip = file.line_num+1
            break
        if row[0] == 'READ VOLTAGE': #For whatever reason the DTA files are different if the data is aborted
            skip = file.line_num+1
            break
    df = pd.read_csv(loc_csv,sep='\t',skiprows=skip,encoding='latin1')
    df_useful = df[['s','V']]
    plot = plt.figure()
    plt.plot(df_useful['s'],df_useful['V'],'ko',)
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
    plt.tight_layout()
    return plot

def plot_peis(area:float,loc:str, ohmic_rtot:np.array = None, pro:bool = False,**plot_args):
    '''
    Plots Zreal and Zimag from a DTA file of Potentiostatic Eis

    param area,float: The active cell area in cm^2
    param loc,str: Location of the .DTA file that contains the EIS data.
    param ohmic_rtot,nnp.array: The first number is the ohmic resistance and the second is the total resistance.
    param pro,bool: If true, plots a dark mode EIS data.  If false, plots a light mode EIS data. The pro version
    has more experimental features.
    param plot_args,dict: Any arguments that are passed to the plot function.

    Return --> if False, the plot of the figure if True none but it plots the figure and shows it.
    '''
    
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
    #Plotting
    if pro == False:
        plot = plt.figure()
        plt.plot(df_useful['ohm'],df_useful['ohm.1'],'o',**plot_args,color = '#21314D') # #21314D is the color of Mines Navy blue
        plt.xlabel('Zreal (\u03A9*cm$^2$)')
        plt.ylabel('-Zimag (\u03A9*cm$^2$)')
        plt.axhline(y=0, color='#D2492A', linestyle='-.') # #D2492A is the color of Mines orange
        plt.rc('font', size=16)
        plt.axis('scaled')
        return plot

    elif pro == True: # Plot like a Pro breh. Just messing around at this point
        fig,ax = plt.subplots()
        ax.plot(df_useful['ohm'],df_useful['ohm.1'],'D',**plot_args,color = '#0c2d52',alpha=0.69,markeredgewidth=0.2,
            markeredgecolor='#cfcfcf',ms=8,antialiased=True) # #21314D is the color of Mines Navy blue ##09213c

        # --- Colors
        background = '#121212' # '#000023'
        fig.set_facecolor(background)
        ax.set_facecolor(background)
        frame_color = '#a0a0a0'
        ax.spines['bottom'].set_color(frame_color)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_color(frame_color)
        ax.spines['right'].set_visible(False)
        ax.tick_params(colors=frame_color, which='both')

        # --- Horozontal dashed line
        dashes = [6,2,2,2,6,2,2,4,6,2,6,4]
        ax.axhline(y=0, color='#c1741d',dashes=dashes) # #D2492A is the color of Mines orange #7f4c13 #c1741d #D98B21

        # --- cutting down the X and Y axis and adding a grid
        if ohmic_rtot is not None:
            ax.set_xticks(ohmic_rtot)
            ax.spines['bottom'].set_bounds(ohmic_rtot[0], ohmic_rtot[1])
            y_bottom = df_useful['ohm.1'].iloc[0]
            if ohmic_rtot[1]<=1: # --- Cutting out inductance effects
                y_bottom = -0.1
            ax.spines['left'].set_bounds(y_bottom,df_useful['ohm.1'].max())
            ax.spines['left'].set_capstyle('butt')
            ax.tick_params(axis='x',length=10,direction='inout')
            ax.grid(axis='x',linestyle='--',color='#a0a0a0',alpha=0.35) # visible=None

        # --- Labels
        font = 'Helvetica'
        ax.set_xlabel('Zreal (\u03A9*cm$^2$)',color=frame_color,fontsize='x-large',family=font)
        ax.set_ylabel('$\u2212$Zimag (\u03A9*cm$^2$)',color=frame_color,fontsize='x-large',family=font)
        ax.tick_params(axis='both', which='major', labelsize='large')
        ax.axis('scaled')
        if ohmic_rtot is not None and ohmic_rtot[1]<=1: # --- Cutting out inductance effects
            ax.set_ylim(y_bottom*1.01,df_useful['ohm.1'].max()*1.1)
        plt.tight_layout() 
        plt.show()

def plot_peiss(area:float, condition:str, loc:str, ncol:int=1,legend_loc:bool='best',**plot_args): #Enables multiple EIS spectra to be stacked on the same plot ,color=-1
    '''
    Enables multiple EIS spectra to be stacked on the same plot.
    
    param area,float: The active cell area in cm^2
    param condition,str: The condition of the EIS data. This is what will be in the legend.
    param loc,str: Location of the .DTA file that contains the EIS data.
    param ncol,int: The number of columns in the legend of the plot.
    param legend_loc,str: The location of the legend. Best is the best spot, Outside places the legend
    outside the plot.
    param plot_args,dict: Any arguments that are passed to the plot function.

    Return --> none but it plots the figure
    '''
    
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
    df_useful = df[['ohm','ohm.1']] #returns the useful information

    # ----- Plotting
    plt.plot(df_useful['ohm'],df_useful['ohm.1'],'o',**plot_args,label = condition) #plots data
    plt.xlabel('Zreal (\u03A9*cm$^2$)',size=14)
    plt.ylabel('$\u2212$Zimag (\u03A9*cm$^2$)',size=14)
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.axhline(y=0,color='k', linestyle='-.') # plots line at 0 #D2492A is the color of Mines orange
    plt.axis('scaled') #Keeps X and Y axis scaled 1 to 1
    # If statement determines legend loc
    if legend_loc == 'best': 
        plt.legend(loc='best',fontsize='large')
    elif legend_loc == 'outside':
        plt.legend(loc='upper left',bbox_to_anchor=(1,1),ncol=ncol)
    else: #this else statemnent is a default if one of the earlier statments causes an error
        plt.legend(loc='upper left',bbox_to_anchor=(1,1),ncol=ncol)

    plt.tight_layout()

def plot_eis_ocvs(loc:str,label:str,ymin:float=1.00,ymax:float=1.10,ncol:int=1):
    '''
    Plots the ocv that is taken right before the EIS data. This function can stack to plot
    multiple ocv files on the same plot. Same as peiss.

    param loc,str: Location of the .DTA file that contains the EIS data.
    param label,str: The label of the ocv data. this will be in the plot legend
    param ymin,float: The minimum y value of the plot. Defaults to 1.00.
    param ymax,float: The maximum y value of the plot. Defaults to 1.10.
    param ncol,int: The number of columns in the legend of the plot.

    Return --> none but it plots the figure
    '''
    dta2csv(loc) #convert DTA to a CSV
    loc_csv = loc.replace('.DTA','')+'.csv' #access newly made file
    #find right amount of rows to skip
    file = csv.reader(open(loc_csv, "r",encoding='latin1'), delimiter="\t") #I honestly dk what is going on here
    for row in file: #searches first column of each row in csv for "OCVCURVE", then adds 1. This gives the right amount of rows to skip to get to the OCV table
        if row[0] == 'OCVCURVE':
            skip = file.line_num+1
            break
    for row in file: #searches for end of the OCV table
        if row[0] == 'EOC':
            nrows = file.line_num-skip-2
            break
    df = pd.read_csv(loc_csv,sep= '\t',skiprows=skip,nrows=nrows,encoding='latin1', error_bad_lines=False)
    df_useful = df[['s','V vs. Ref.']] #returns the useful information
    plt.plot(df_useful['s'],df_useful['V vs. Ref.'],'o',label=label)
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
    plt.tight_layout()
    plt.legend(ncol=ncol)
    plt.ylim(ymin,ymax)

def plot_ivfc(area:float, loc:str):
    '''
    Plots an IV curve and power density curve with the Pmax listed on the plot for fuel cell mode operation.

    param area,float: The active cell area in cm^2
    param loc,str: Location of the .DTA file that contains the IV data.

    Return --> none but it plots the figure and shows it    
    '''
    
    dta2csv(loc) #Converts and finds CSV then turns it into a dataframe
    loc_csv = loc.replace('.DTA','')+'.csv'
    file = csv.reader(open(loc_csv, "r",encoding='latin1'), delimiter="\t") #I honestly dk what is going on here, but it works
    for row in file: #searches first column of each row in csv for "ZCURVE", then adds 1. This gives the right amount of rows to skip
        if row[0] == 'CURVE':
            skip = file.line_num+1
            break
    df = pd.read_csv(loc_csv,sep='\t',skiprows=skip,encoding='latin1')
    #calculations and only keeping the useful data
    df['A'] = df['A'].div(-area)
    df['W'] = df['W'].div(-area)
    df_useful = df[['V','A','W']]
    #Plotting
    fig, ax1 = plt.subplots()
    #IV plotting
    color = '#21314D' #Navy color
    ax1.set_xlabel('Current Density ($A/cm^2$)')
    ax1.set_ylabel('Voltage (V)', color=color)
    ax1.plot(df_useful['A'], df_useful['V'],'o', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    #Power density plotting
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color2 = '#D2492A' #orange color
    ax2.set_ylabel('Power Density ($W/cm^2$)', color=color2)  # we already handled the x-label with ax1
    ax2.plot(df_useful['A'], df_useful['W'], 'o',color=color2) 
    ax2.tick_params(axis='y', labelcolor=color2)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    #Calculating and printing max values onto the graph
    max_w = df_useful['W'].max() #finds maximum power density
    max_v = df.loc[df.index[df['W'] == max_w],'V'].item() #finds voltage of max power density
    max_ws = f'{round(max_w,3)}' #setts float to a string
    max_vs = f'{round(max_v,3)}'
    plt.figtext(0.28,0.21,r'$P_{max} = $'+max_ws+r' $W/cm^2 at$ '+max_vs+r'$V$',size='large',weight='bold')
    plt.tight_layout()
    plt.show()
    
def plot_ivfcs(curves_conditions:tuple):
    '''
    Plots multiple IV and power density curves, input is a tuple of (area,condition,location of IV curve)

    param curves_conditions,tuple: A tuple containing data to plot and label the curve.
    The order is: (area,condition,location of IV curve)

    Return --> none but it plots the figure and shows it
    '''
    
    fig,ax1 = plt.subplots() # Initializing plot
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    for iv in curves_conditions:
        ' Extracting data from DTA file to a dataframe'
        loc = iv[2]
        dta2csv(loc) #Converts and finds CSV then turns it into a dataframe
        loc_csv = loc.replace('.DTA','')+'.csv'
        file = csv.reader(open(loc_csv, "r",encoding='latin1'), delimiter="\t") #I honestly dk what is going on here, but it works
        for row in file: #searches first column of each row in csv for "ZCURVE", then adds 1. This gives the right amount of rows to skip
            if row[0] == 'CURVE':
                skip = file.line_num+1
                break
        df = pd.read_csv(loc_csv,sep='\t',skiprows=skip,encoding='latin1')
        #calculations and only keeping the useful data
        area = iv[0]
        df['A'] = df['A'].div(-area)
        df['W'] = df['W'].div(-area)
        df_useful = df[['V','A','W']]

        # --- IV plotting:
        label = iv[1]
        ax1.plot(df_useful['A'], df_useful['V'],'o',fillstyle='none',label=label)

        # --- Power Density plotting
        ax2.plot(df_useful['A'], df_useful['W'],'o',label=label)

    # ----- Plot Formatting:
    ax1.set_xlabel('Current Density (A/cm$^2$)',fontsize='x-large')
    ax1.set_ylabel('Voltage (V)',fontsize='x-large')
    ax1.tick_params(axis='both', which='major', labelsize='large')

    ax2.set_ylabel('Power Density (W/cm$^2$)',fontsize='x-large')  # we already handled the x-label with ax1
    ax2.tick_params(axis='both', which='major', labelsize='large')

    num_curves = len(curves_conditions)
    if num_curves <=4:
        ax2.legend(loc='lower center',bbox_to_anchor=(0.5,1.0),fontsize='large',ncol=num_curves,handletextpad=0.02,columnspacing=1)
    elif num_curves <=8:
        ncol = int(round(num_curves/2))
        ax2.legend(loc='lower center',bbox_to_anchor=(0.5,1.0),fontsize='large',ncol=ncol,handletextpad=0.02,columnspacing=1)
    elif num_curves <=12:
        ncol = int(round(num_curves/3))
        ax2.legend(loc='lower center',bbox_to_anchor=(0.5,1.0),fontsize='large',ncol=num_curves,handletextpad=0.02,columnspacing=1)
    plt.subplots_adjust(top=0.8)
    plt.tight_layout()
    plt.show()

def plot_ivec(area:float, loc:str):
    '''
    Plots IV curve in EC mode and displays the current density at 1.5V on the plot

    param area,float: The active cell area in cm^2
    param loc,string: The location .DTA file that contains the IVEC curve

    Return --> none but it plots the figure and shows it
    '''
    
    dta2csv(loc) #Converts and finds CSV then turns it into a dataframe
    loc_csv = loc.replace('.DTA','')+'.csv'
    file = csv.reader(open(loc_csv, "r",encoding='latin1'), delimiter="\t") #I honestly dk what is going on here, but it works
    for row in file: #searches first column of each row in csv for "ZCURVE", then adds 1. This gives the right amount of rows to skip
        if row[0] == 'CURVE':
            skip = file.line_num+1
            break
    df = pd.read_csv(loc_csv,sep='\t',skiprows=skip,encoding='latin1')

    # ------- calculations and only keeping the useful data
    df['A'] = df['A'].div(area)
    df_useful = df[['V','A']]
    'Plotting'
    fig, ax1 = plt.subplots()
    'IV plotting'
    color = '#21314D'
    ax1.set_xlabel('Current Density ($A/cm^2$)')
    ax1.set_ylabel('Voltage (V)')
    if df_useful['V'].loc[0] <= 0: #this is put in because the Gamry 3000 and 5000 have different signs on the voltage of IVEC curve
        sign = -1
    else:
        sign = 1
    ax1.plot(df_useful['A'], sign*df_useful['V'],'o', color=color)
    ax1.tick_params(axis='y')
    
    # ------- Calculating and printing current density at 1.5V
    current_density15 = -df_useful[abs(df_useful['V'])>=1.49].iloc[0,1] #finds the current density of the first Voltage value above 1.5V
    V15 = df_useful[abs(df_useful['V'])>=1.49].iloc[0,0] #same as before but returns the exact voltage value
    current_density15_string = f'{round(current_density15,3)}'
    V15_string = f'{round(-V15,3)}'
    plt.figtext(0.28,0.21,current_density15_string+r'$A/cm^2\:at$ '+V15_string+r'$V$',size='large',weight='bold') #placing value on graph
    plt.show()

def plot_ivecs(area:float,condition:str,loc:str):
    '''
    Plots multiple electrolysis cell mode IV curves on same plot. This function can stack to plot
    multiple IVEC files on the same plot. Same as peiss.

    param area,float: The active cell area in cm^2
    param condition,string: The condition of the IV curve. This will be the label of the curve in the legend
    param loc,string: The location .DTA file that contains the IVEC curve
    
    Return --> none but it plots the figure
    '''
    
    dta2csv(loc) #Converts and finds CSV then turns it into a dataframe
    loc_csv = loc.replace('.DTA','')+'.csv'
    file = csv.reader(open(loc_csv, "r",encoding='latin1'), delimiter="\t") #I honestly dk what is going on here, but it works
    for row in file: #searches first column of each row in csv for "ZCURVE", then adds 1. This gives the right amount of rows to skip
        if row[0] == 'CURVE':
            skip = file.line_num+1
            break
    df = pd.read_csv(loc_csv,sep='\t',skiprows=skip,encoding='latin1')

    # ------ calculations and only keeping the useful data
    df['A'] = df['A'].div(area)
    df_useful = df[['V','A']]
    if df_useful['V'].loc[0] <= 0: #this is put in because the Gamry 3000 and 5000 have different signs on the voltage of IVEC curve
        sign = -1
    else:
        sign = 1

    # ------- Plotting
    plt.plot(df_useful['A'], sign*df_useful['V'],'o', label=condition)
    plt.xlabel('Current Density ($A/cm^2$)', fontsize='x-large')
    plt.ylabel('Voltage (V)', fontsize='x-large')
    plt.legend(loc='best', fontsize = 'large')
    plt.xticks(fontsize = 'large')
    plt.yticks(fontsize = 'large')
    plt.tight_layout()

def plot_galvanoDeg(FolderLoc:str,fit:bool = True,fontsize:int = 16,smooth:bool=False,first_file:str = 'default'):
    '''
    #If you want to change the first file, put the loc in place of 'default
    '''
    
    files = os.listdir(FolderLoc)
    useful_files = [] #initializing a list for the useful files

    # ------- Taking out all of the galvanostatic files
    for file in files: #looping over all files in the folder Folderloc
        if (file.find('GS')!=-1) and (file.find('.DTA')!=-1):
            #Extracting the file number (used for sorting, yeah this is probably a roundabout way of doing it)
            start, end = file.rsplit('#',1)# cutting everything out before the # so only the number and file extension is left
            fnum, fileExt = end.rsplit('.',1) #cutting off the file extension leaving only the number as a string
            index = int(fnum) #Converts the file number to a string
            useful_file = (file,index)
            useful_files.append(useful_file)
    
    # ------- Sorting the files
    useful_files.sort(key=lambda x:x[1]) #Sorts by the second number in the tupple
    sorted_useful_files, numbers = zip(*useful_files) #splits the tupple
    sorted_useful_files = [FolderLoc + '/' + f for f in sorted_useful_files] #Turning all files from their relative paths to the absolute path

    # ------- Getting the first time
    if first_file == 'default':
        T0_stamp = fl.get_timestamp(sorted_useful_files[0]) #gets time stamp from first file
        t0 = T0_stamp.strftime("%s") #Conveting Datetime to seconds from Epoch
    else:
        T0_stamp = fl.get_timestamp(first_file) #gets time stamp from first file
        t0 = T0_stamp.strftime("%s") #Conveting Datetime to seconds from Epoch
    
    # ------- Combining all dataframes
    dfs = [] #Initializing list of dfs
    length = len(sorted_useful_files) #gets length of sorted useful files
    for i in range(0,length,1):
        loc = os.path.join(FolderLoc,sorted_useful_files[i]) #Creats a file path to the file of choice
        dta2csv(loc) #convert DTA to a CSV
        loc_csv = loc.replace('.DTA','')+'.csv' #access newly made file
        data = csv.reader(open(loc_csv, "r",encoding='latin1'), delimiter="\t") #I honestly dk what is going on here
        for row in data: #searches first column of each row in csv for "ZCURVE", then adds 1. This gives the right amount of rows to skip
            if row[0] == 'CURVE':
                skip = data.line_num+1
                break
        df = pd.read_csv(loc_csv,sep= '\t',skiprows=skip,encoding='latin1') #creat data frame for a file
        start_time = fl.get_timestamp(sorted_useful_files[i]).strftime("%s") #Find the start time of the file in s from epoch
        df['s'] = df['s'] + int(start_time)
        df_useful = df[['s','V vs. Ref.']]
        dfs.append(df_useful)
    cat_dfs = pd.concat(dfs,ignore_index=True)# (s) Combine all the dataframes in the file folder
    cat_dfs.sort_values(by=['s'])
    cat_dfs['s'] = (cat_dfs['s']-int(t0))/3600 #(hrs) subtracting the start time to get Delta t and converting time from seconds to hours and
    
    # ------- plotting:
    fig, ax = plt.subplots()
    ax.set_xlabel('Time (hrs)',fontsize = fontsize)
    ax.set_ylabel('Voltage (V)',fontsize = fontsize)
    ax.tick_params(axis='both', which='major', labelsize=12) #changing tick label size
    if smooth == False:
        ax.plot(cat_dfs['s'],cat_dfs['V vs. Ref.'],'.k')
    if smooth == True:
        bin_size = 50
        bins = cat_dfs['V vs. ef.'].rolling(bin_size)
        moving_avg_voltage = bins.mean()
        ax.plot(cat_dfs['s'],moving_avg_voltage,'k')
    ax.set_ylim(0,1.2)

    # ------- fitting and writting slope on graph:
    if fit == True:
        m,b = np.polyfit(cat_dfs['s'],cat_dfs['V vs. Ref.'],1)
        fit = m*cat_dfs['s']+b
        ax.plot(cat_dfs['s'],fit,'--r')
        mp = m*-100000 #Converting the slope into a % per khrs (*100 to get to %, *1000 to get to khrs,*-1 for degredation)
        ms = f'{round(mp,3)}'
        plt.figtext(0.27,0.17,'Degradation: '+ms+'% /khrs',weight='bold',size='xx-large')
    plt.tight_layout()
    plt.show()






