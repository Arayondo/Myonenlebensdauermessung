#!/usr/bin/env python

# -------- extract_pulses.py --------------------------------
# Beschreibung:  Dieses Skript untersucht die Ausgabe der DAQ-Karte auf Pulse, welche in eine separate Datei gechrieben werden.
# Autor:      C. Theiß   Jun. 2015
# last modified: 
#--------------------------------------------------------------


# Main routine
# 1. Search for Trigger-Flag
# 2. Copy all lines until next Trigger-Flag to buffer line
# 3. Analyze Data in buffer line and write all time stamps with absolute time in external file
#
# Line-Analysing function:
# 0. Creating 8-int (or float?) array temp, initialize with 0
# 1. Splitting lines
#   Iterating over lines:
#     0.? Computing and writing absolute time?
#     1. from right to left: check for valid rising or falling edges
#       -> if valid edge: try to copy content (timestamp?) into temp
#            if current array-element == 0 -> overwrite
#            else exeption handling (e.g. fluctuations, falling and rising edge in same line ,etc.)
#     2. checking after each line for valid pulses
#     3. writing pulses to output file

import argparse
import numpy as np
import matplotlib.pyplot as plt

def argumente():
	"""Diese Funktion liest Argumente von der Kommandozeile ein."""
	parser = argparse.ArgumentParser()

	parser.add_argument('-f', '--filename', type=str, default=" ",
	help="Name of the file to analyze.")
	parser.add_argument('-o', '--output', type=str, default=" ",
	help="Name of the output file.")
			
	return parser.parse_args()
	
def analyze_lines(data,output):
	"""Analysiert eingelesene Linien und schreibt Daten in die dafuer vorgesehene Datei"""
	
	datafile=open("FD_"+output,"a")	
	temp=[0.,0.,0.,0.,0.,0.,0.,0.]
	for line in data:
		line=line.split(' ')
		time=int(line[0],16)*0.00000004 #25 MHz
		for i in range(4):
			if (int(line[(i+1)*2],16) & 0x20) !=0: #valid rising edge signal (3.)
				if (temp[i*2+1]) == 0.: #no entries till now, so write down
					tmp=int(line[(i+1)*2],16) & 0x1F #save time bits
					temp[i*2+1]=time+tmp*0.00000000125 #(3.y.1.n.)
				#else: yeah, what if there is already an entry???
		for i in range(4):
			if (int(line[i*2+1],16) & 0x20) !=0: #valid rising edge signal (3.)
				if (temp[i*2]) == 0.: #no entries till now, so write down
					tmp=int(line[i*2+1],16) & 0x1F #save time bits
					temp[i*2]=time+tmp*0.00000000125 #(3.y.1.n.)
				else: #there is still a signal from a previous rising adge
					if temp[i*2+1] !=0: #if there is also a falling edge, write out and clear the pulse
						datafile.write('%s\t%.11f\t%.11f\n' %(str(i),temp[i*2],temp[i*2+1]))
						temp[i*2+1] = 0.
						tmp=int(line[i*2+1],16) & 0x1F #save time bits
						temp[i*2]=time+tmp*0.00000000125 #(3.y.1.n.)
					else: #yeah? overwriting seems appropriate
						tmp=int(line[i*2+1],16) & 0x1F #save time bits
						temp[i*2]=time+tmp*0.00000000125 #(3.y.1.n.)
		for i in range(4):
			if (temp[i*2] != 0.) and (temp[i*2+1] != 0.):
				datafile.write('%s\t%.11f\t%.11f\n' %(str(i),temp[i*2],temp[i*2+1]))
				temp[2*i] = 0.
				temp[i*2+1] = 0.	
	datafile.write("#EndEvent\n")
	datafile.close()

opt=argumente()

if opt.output == " ":
	opt.output = opt.filename

channel=0 #channel of the can at the Daq-card (0-3)
channel_r=channel*2+1 #rising edge word of the channel 



with open(opt.filename,"r") as datafile: #2014-06-03_15-29-27_RAW_1.01_ct
	print("Successfully openend "+opt.filename)

	line_counter=0
	temp=[]
	
	for line in datafile:
		#print line
		line_counter=line_counter+1
		if (line_counter%1000000==0):
			print("%s lines already read" %line_counter) #is it alive???
		line=line.strip()
		splitter=line.split(' ')
		if len(splitter)==16: #valid DAQ-Card-Word? (1.)
			if (int(splitter[1],16) & 0x80)!=0 : #valid trigger signal (2.)
				if len(temp) > 0:
					analyze_lines(temp,opt.output)
					temp=[]
					temp.append(line)
			else:
				temp.append(line)
	analyze_lines(temp,opt.output) #analyze last lines too
			

print ("All %s lines read " %(line_counter))

