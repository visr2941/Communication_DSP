# File: ftpam_rcvr01.py
# Script file that accepts a binary unipolar flat top PAM
# signal r(t) with bitrate fb and sampling rate fs
# as input and decodes it into a received text string.
# The PAM signal r(t) is received from a wav-file with
# sampling rate fs. First r(t) is sampled at the right DT sequence 
# sampling times, spaced tb = 1/fb apart. The result is then 
# quantized to binary (0 or 1) to form the 
# estimated received sequence dnhat which is subsequently
# converted to 8 bit ASCII text.

from pylab import *
import ascfun as af
import wavfun as wf
#filename = input("Enter the file name (wav): ")
rt, fs = wf.wavread("ftpam_sig01.wav")

fb = 100 
tb = 1/float(fb)

bits = 8
n = int(floor(len(rt)/float(fs)/tb)) 	# number of received bits

rt = list(rt)  	# changing rt into list type

######### getting sample of rt signal #######

dnhat=[]
for i in range(n):
	d_prime = rt[i*round(fs*tb):(i+1)*round(fs*tb)]
	avg = sum(d_prime) / round(fs*tb)     # averaging out the one bit window and the comapring
	if avg > 0.5:
		dnhat = dnhat + [1]
	else:
		dnhat = dnhat + [0]

#####################################################
dnhat = array(dnhat,int8)	 # converting list into binary array

print("")
print('The content of the wav file is "%s"' %af.bin2asc(dnhat))
print("")
