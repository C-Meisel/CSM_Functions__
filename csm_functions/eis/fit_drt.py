''' This module contains functions to help it distribution of relaxation time (DRT) spectra to 
potentiostatic electrochemical impedance spectroscopy data taken with a Gamry potentiostat
All of the actual DRT fitting and analysis is done in the bayes_drt module made by Jake Huang
# C-Meisel
'''

'Imports'
import os
from bayes_drt.inversion import Inverter#inverter class in inversion module
from bayes_drt.stan_models import save_pickle #useful for saving a fit for later (saves whole inverter object)
from bayes_drt import file_load as fl
from bayes_drt import plotting as bp #Imports new plotting module (bp = bayes plotting)


# ---------- Functions for saving a DRT fit for one spectra ----------
def bayes_drt_save(loc_eis,fit_path,fit_name):
    '''
    Takes a potentiostatic EIS spectra, fits it using a Baysian model,
    and saves it to a certain fit path (directory) with a file name

    Made on 18May21, this is how I currently use Jake's Bayes fit function to fit eis spectra
    Changes will likely be made in the future as I learn more about DRT and Jakes Modules

    param loc_eis, string: location of the EIS spectra
    param fit_path, string: path to save the fit. This will be the directory, or "Jar", that the fit
    will be saved in.
    param fit_name: string, The name of the fit. This will be the file name

    Return --> None
    '''
    df = fl.read_eis(loc_eis)
    freq,z = fl.get_fZ(df)
    inv = Inverter() #new DRT package can figure out the right basis frequency to use
    inv.fit(freq,z,init_from_ridge=True,mode='sample',chains=2,samples=200) #Bayes fitting DRT
    #Chains=2 and samples=200
    save_pickle(inv,os.path.join(fit_path,fit_name))


def map_drt_save(loc_eis,fit_path,fit_name,which='core',init_from_ridge=True,outliers=False):
    '''
    Takes a potentiostatic EIS spectra, fits it using a mapping model,
    and saves it to a certain fit path (directory) with a file name.

    Made on 18May21, this is how I currently use Jake's Bayes fit function to fit eis spectra
    Changes will likely be made in the future as I learn more about DRT and Jakes Modules

    param loc_eis, string: location of the EIS spectra
    param fit_path, string: path to save the fit. This will be the directory, or "Jar", that the fit
    will be saved in.
    param fit_name, string: The name of the fit. This will be the file name
    param which, string: which data to store. 'core' or 'sample'. Core file sizes are smaller
    param init_from_ridge, boolean: whether to use ridge regression to initialize the fit.
    param outliers, boolean: whether to use outliers to initialize the fit.
    '''
    
    #Made on 18May21, this is how I currently use Jake's Bayes fit function to fit eis spectra
    #Changes will likely be made in the future as I learn more about DRT and Jakes Modules
    df = fl.read_eis(loc_eis)
    freq,z = fl.get_fZ(df)
    inv = Inverter()
    inv.fit(freq,z,init_from_ridge=init_from_ridge,outliers=outliers) #If the data is not taken from 1e6hz init_from_ridge should be true
    inv.save_fit_data(os.path.join(fit_path,fit_name),which=which) #main thing that core doesnt save is the matricies (a lot of data)