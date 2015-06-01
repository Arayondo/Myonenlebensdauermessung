#!/usr/bin/python -tt

##########
# Header #
##########

# -------- plot_threshold.py --------------------------------
# Beschreibung: Analyse-Skript für die Daten einer Pulshöhenspektrumsmessung
# Autor:      C. Theiß   Jun. 2015
# last modified: 
#--------------------------------------------------------------


###########
# Imports #
###########

import argparse

# import everything we need from kafe
from kafe import *
from kafe.function_library import exp_2par

import os
import numpy as np

###################
# Argument-Parser #
###################

def argumente():
	"""Diese Funktion liest Argumente von der Kommandozeile ein."""
	parser = argparse.ArgumentParser()

	parser.add_argument('-f', '--filled', type=str, default=" ",
	help="Name of the file with the data from the filled can.")
	parser.add_argument('-e', '--empty', type=str, default=" ",
	help="Name of the file with the data from the empty can.")
	parser.add_argument('-x', '--xaxe', type=int, nargs="*", default=[0, 700],
    help="Start- und Endpunkt der x-Achse (Schwellenspannung). Default ist %(default)s")

			
	return parser.parse_args()
	
###############################################################
# Function to extract data from files and returns Fit-Objects #
###############################################################
	
def extract_data(filename,name):
	threshhold=[]
	rate_int=[]
	error_rate_int=[]
	with open(filename,"r") as datafile:
		counter=0
		for line in datafile:
			counter=counter+1
			if counter == 2 : #check if datafile is from threshold measurement
				if line.strip() != "#Schwelle\tMesszeit\tEreignisse":
					break
			if counter > 2: #read thresholds and calculate rate and the error of the rate
				splitter=(line.strip()).split()
				threshhold.append(float(splitter[0]))
				rate_int.append(float(splitter[2])/float(splitter[1]))
				error_rate_int.append(np.sqrt(float(splitter[2]))/float(splitter[1]))

	#sort arrays for further calculating from lowest to highest threshold
	index=np.lexsort((rate_int,threshhold))
	threshhold=[threshhold[n] for n in index]
	rate_int=[rate_int[n] for n in index]
	error_rate_int=[error_rate_int[n] for n in index]
	
	#normalizing to 1
	rate_0=rate_int[0]
	for i in range(len(rate_int)):
		rate_int[i]=rate_int[i]/rate_0
		error_rate_int[i]=error_rate_int[i]/rate_0	

	#differetiating rates...
	rate_diff=[(-1)*(rate_int[n+1]-rate_int[n]) for n in range(len(threshhold)-1)]

	#calculating mean points between thresholds for plotting the differentiated rate
	threshhold_diff=[]
	for n in range(len(threshhold)-1):
		threshhold_diff.append(threshhold[n]+(threshhold[n+1]-threshhold[n])/2)

	#calculating error for rate_diff
	error_rate_diff=[]
	for n in range(len(threshhold)-1):
		error_rate_diff.append(np.sqrt(error_rate_int[n+1]**2+error_rate_int[n]**2))
	
	tmp1=build_dataset(threshhold, rate_int, yabserr=error_rate_int, title="Integrale Rate der "+name)
	tmp2=build_dataset(threshhold_diff, rate_diff, yabserr=error_rate_diff, title="Differentielle Rate der "+name)
	
	
	return [tmp1,tmp2,error_rate_int,error_rate_diff]

############
# Workflow #
############

	
opt=argumente()

# Getting Data of the measurements from files

filled_data=extract_data(opt.filled,"vollen Kanne")
empty_data=extract_data(opt.empty,"leeren Kanne")
filled_fits=[Fit(filled_data[0], exp_2par),Fit(filled_data[1], exp_2par)]
empty_fits=[Fit(empty_data[0], exp_2par),Fit(empty_data[1], exp_2par)]

# Calculating noise ratio

noise_int=[]
error_noise_int=[]
for i in range(len(filled_data[0].get_data('y'))):
	noise_int.append(empty_data[0].get_data('y')[i]/filled_data[0].get_data('y')[i])
	error_noise_int.append(noise_int[i]*np.sqrt((empty_data[2][i]/empty_data[0].get_data('y')[i])**2+(filled_data[2][i]/filled_data[0].get_data('y')[i])**2))

noise_diff=[]
error_noise_diff=[]
for i in range(len(filled_data[1].get_data('y'))):
	noise_diff.append(empty_data[1].get_data('y')[i]/filled_data[1].get_data('y')[i])
	error_noise_diff.append(noise_diff[i]*np.sqrt((empty_data[3][i]/empty_data[1].get_data('y')[i])**2+(filled_data[3][i]/filled_data[1].get_data('y')[i])**2))

noise_data=[build_dataset(filled_data[0].get_data('x'),noise_int,yabserr=error_noise_int,title="Rauschanteil"),build_dataset(filled_data[1].get_data('x'),noise_diff,yabserr=error_noise_diff,title="Rauschanteil")]
noise_fits=[Fit(noise_data[0],exp_2par),Fit(noise_data[1],exp_2par)]

##################
# Creating Plots #
##################

final_plot_int=Plot(filled_fits[0],empty_fits[0],noise_fits[0],ylog=True)
final_plot_int.plot_range={ 'x':(opt.xaxe[0],opt.xaxe[1]), 'y':None}
final_plot_int.axis_labels=['$U_S / mV$','Normierte Rate / Rauschanteil']
final_plot_int.plot_all(show_function_for= None )
final_plot_int.show()

final_plot_diff=Plot(filled_fits[1],empty_fits[1],noise_fits[1],ylog=True)
final_plot_diff.plot_range={ 'x':(opt.xaxe[0],opt.xaxe[1]), 'y':(0.00001,10)}
final_plot_diff.axis_labels=['$U_S / mV$','Normierte Rate / Rauschanteil']
final_plot_diff.plot_all(show_function_for= None )
final_plot_diff.show()
