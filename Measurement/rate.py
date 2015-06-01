#!/usr/bin/env python

# -------- rate.py --------------------------------
# Beschreibung: Skript zur Steuerung der Ratenmessung 
# Autor:      Dominik Haitz <dhaitz@cern.ch> 2014 https://github.com/dhaitz/muonrate
# last modified:  C. Theiß   Jun. 2015 - Auslagerung des Skriptes zur Ratenmessung in eine eigene Datei
#--------------------------------------------------------------
"""Diese Datei zeigt wie man mit der DAQ-Karte Messungen durchfuehrt.
   Inspired by muonic  http://code.google.com/p/muonic/
   DAQ Card Manual: http://physik-begreifen-zeuthen.desy.de/sites2009/site_PhyBegZ/content/e2198/e2451/e6374/e129804/e129813/infoboxContent129819/DAQ-KarteUserManual_ger.pdf
   2014 Dominik Haitz <dhaitz@cern.ch>
"""

import math
import matplotlib.pyplot as plt

def muonrate(opt,daqcard):
	# Schwellenspannungen und Trigger setzen
	daqcard.set_thresholds(*opt.schwellen)
	daqcard.set_trigger(opt.trigger)

	if not opt.graphical:
		# Messung starten
		t, outputlist = daqcard.measure(opt.time)

		# Ergebnisse ausgeben
		print "\nErgebnis nach %.2f Sekunden Messzeit:" % t
		for i in range(3):
			print "Kanal %s: %.0f Ereignisse" % (i+1, outputlist[i])
		print "Trigger:   %.0f Ereignisse" % outputlist[4], "  Stat. Fehler: %.0f Ereignisse" % math.sqrt(outputlist[4])
		print "\nTriggerrate: %.2f +- %.2f  Hz" % ((outputlist[4]/t), (math.sqrt(outputlist[4])/t))

	else:
		fig=plt.figure()
		plt.ion()
		plt.show()
		plt.xlabel("Messung")
		plt.ylabel("Triggerrate / Hz")

		x, y, yerr = [], [], []
		i = 0

		while True:
			i += 1
			t, outputlist = daqcard.measure(opt.time)

			x.append(i)
			y.append((outputlist[4]/t))
			yerr.append(math.sqrt(outputlist[4])/t)

			plt.axis([0,i+1,0,max(y)*1.2])
			plt.errorbar(x, y , yerr)
			plt.draw()

