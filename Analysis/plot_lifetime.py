###########
# Header  #
###########




###########
# Imports #
###########

import argparse

# import everything we need from kafe
from kafe import *
from kafe.function_library import exp_2par, exp_3par

from numpy import exp, cos

###################
# Argument-Parser #
###################

def argumente():
	"""Diese Funktion liest Argumente von der Kommandozeile ein."""
	parser = argparse.ArgumentParser()

	parser.add_argument('-f', '--filename', type=str, default=" ",
	help="Name of the file to analyze.")
			
	return parser.parse_args()


################
# Fit-Function #
################

############
# Workflow #
############

opt=argumente()

# load the experimental data from a file
my_dataset = parse_column_data(
    opt.filename,
    field_order="x,y,yabserr",
    title="Anzahl der Ereignisse"
)
# Create Fit-Object
my_fit = Fit(my_dataset,
             exp_2par)

# Create first to find the splitting point
print 'Creating logarithmic plot to analyse and finding the splitting point\n'

my_plot = Plot(my_fit,ylog=True, )
my_plot.axis_labels = ['$ \Delta t / \mu s$', 'Ereignisse']
my_plot.plot_all(show_function_for=None)
my_plot.show()

#Ask for the splitting point
print 'Enter the point of the time-axis, where the the slope gets smaller:'
splitter=float(input())

#Generating data set with selected data
secondobj=open("selected_data.dat", "w")

with open(opt.filename,"r") as data:
	linecounter=0
	for line in data:
		linecounter=linecounter+1
		line.strip()
		spl=line.split('\t')
		if linecounter == 1:
			secondobj.write(str(line))
		elif float(spl[0]) > splitter:
			secondobj.write(str(line))

secondobj.close()

#####################################
# Creating dataset-objects for fits #
#####################################

selected_dataset = parse_column_data(
    'selected_data.dat',
    field_order="x,y,yabserr",
    title="Anzahl der Ereignisse"
)

############################################
# Creating Fit-objects and performing fits #
############################################

 
second_fit = Fit(selected_dataset,
             exp_2par)
            
second_fit.do_fit()


###########################################
# Creating Plot-Object with data and fits #
###########################################

final_plot =Plot(my_fit,second_fit,ylog=True) 
final_plot.axis_labels = ['$\Delta t / \mu s$', 'Ereignisse']
final_plot.plot(0,show_function=False)
final_plot.plot(1,show_data=False)
final_plot.show()
final_plot.save("lifetime_plot.pdf")
