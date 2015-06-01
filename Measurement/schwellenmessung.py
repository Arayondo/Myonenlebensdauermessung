#!/usr/bin/env python

# -------- schwellenmessung.py --------------------------------
# Beschreibung:  Skript zur Steuerung der Pulshöhenspektrumsmessung
# Autor:      C. Theiß   Jun. 2015
# last modified: 
#--------------------------------------------------------------

"""Diese Datei beinhaltet das Skript zur Durchführung einer Pulshöhenspektrumsmessung
"""

import os
import time

def condition(current,end,sign):
	if sign > 0:
		return end >= current
	else:
		return current >= end


def schwellenmessung(opt,daqcard):
	
	# Schwellenspannungen und Trigger setzen
	daqcard.set_trigger(1)

	if (opt.end >= opt.start):
		sign=1
	else:
		sign=-1
	current=opt.start #current threshhold
	with open("Schwellenmessung_"+time.strftime("%Y_%m_%d_%H_%M")+".dat","a") as datei:
		datei.write('Parameter:'+str(opt)+'\n')
		datei.write('#Schwelle\tMesszeit\tEreignisse\n')
		while(condition(current,opt.end,sign)):
			daqcard.set_thresholds(current,1000,1000)
			t,output=daqcard.measure(opt.time,opt.events)
			datei.write('%s\t\t%s\t\t%s\n'% (current,t,output[0]))
			current=current+sign*opt.interval

