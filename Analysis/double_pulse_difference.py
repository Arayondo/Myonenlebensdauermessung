#!/usr/bin/env python

import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mlp

def argumente():
	"""Diese Funktion liest Argumente von der Kommandozeile ein."""
	parser = argparse.ArgumentParser()

	parser.add_argument('-f', '--filename', type=str, default=" ",
	help="Name of the file to analyze.")
	parser.add_argument('-n', '--bins', type=int, default=100,
	help="Number of bins. Default is 100.")
			
	return parser.parse_args()

opt=argumente()

time_diff=[]
first_pulse=0
second_pulse=0
eventcounter=0
channel=0  

datafile=open(opt.filename,"r")
line=datafile.readline()
while line != "":
	line=line.strip()
	if line != "#EndEvent":
		splitter=line.split("\t")
		if splitter[0] == str(channel):
			if first_pulse == 0:
				first_pulse = float(splitter[1]) 
			elif second_pulse == 0:
				second_pulse = float(splitter[1])				
		line=datafile.readline()
	else:
		eventcounter=eventcounter+1
		time_diff.append((second_pulse-first_pulse)*1000000)
		first_pulse=0
		second_pulse=0
		line=datafile.readline()

print "Read %i events, selecting %i double pulses" %(eventcounter,len(time_diff))

# getting number of events per bin

y,edges=np.histogram(time_diff,opt.bins,(0.1,10.))

# calculating error 

yerror=[]
for i in range(len(y)):
	yerror.append(np.sqrt(y[i]))

# calculating x-values from bin edges

x=[]
for i in range(len(edges)-1):
	mid=edges[i]+(edges[i+1]-edges[i])/2
	x.append(mid)
	
# writing data to output file

name="Kafe_"+opt.filename
with open(name,"w") as plotfile:
        plotfile.write("#time\tevents\tevents_error\n")
        for i in range(len(x)):
			text=str(x[i])+"\t"+str(y[i])+"\t"+str(yerror[i])+"\n"
			plotfile.write(text)


