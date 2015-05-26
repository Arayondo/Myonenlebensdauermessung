#!/usr/bin/env python

import time, math
			
def dpmessung(opt,daqcard):			
	runtime=opt.time

	# Schwellenspannungen und Trigger setzen
	daqcard.set_thresholds(*opt.schwellen)
	daqcard.set_trigger(1)
	daqcard.write("CE",0.1) #Counter enable, da wir ja den ganzen Output wollen
	
	start_time=int(time.time())
	t=0
	counter=0
	temp=0
	print("Starte Messung")
	filename="Lebensdauermessung_"+time.strftime("%Y_%m_%d_%H_%M")+".dat"
	with open(filename,"a") as datafile:
		while t<runtime:
			datafile.write(daqcard.read()+"\n")
			t=int(time.time())-start_time
			temp=t-counter*3600
			if temp > 3600:
				counter=counter+1
				print('Messung laeuft seit %s Stunden, verbleibende Messzeit: %s s' %(counter,runtime-counter*3600))

	print("Messung beendet")
	print("Daten gespeichert in "+filename)
