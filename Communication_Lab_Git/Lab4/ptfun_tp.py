# File: pamfun.py
# Functions for pulse amplitude modulation (PAM)
from numpy import *
def pampt(an,sps, ptype, pparms=[]):
	Fs=44100
	FB=100
	N = len(an)    		# Number of data symbols
	TB = 1/float(FB)    	# Time per symbol
	ixL = ceil(-Fs*0.5*TB)    	# Left index for time axis
	ixR = ceil(Fs*(N-0.5)*TB)     # Right index for time axis
	tt = arange(ixL,ixR)/float(Fs)     # Time axis for s(t)
    
    	# ***** Conversion from DT a_n to CT a_s(t) *****
	ast = zeros(len(tt))    	# Initialize a_s(t)
	ix = array(around(Fs*arange(0,N)*TB),int)    # Symbol center indexes
	ast[ix-int(ixL)] = Fs*an    # delta_n -> delta(t) conversion
	# ***** Set up PAM pulse p(t) *****
	ptype = ptype.lower()	# Convert ptype to lowercase
	
	# Set left/right limits for p(t)
	if (ptype=='rect' or ptype == 'man'):
		kL = -0.5; kR = -kL
	else:
		kL = -1.0; kR = -kL
	
	# Default left/right limits
	ixpL = ceil(sps*kL)		# Left index for p(t) time axis
	ixpR = ceil(sps*kR)		# Right index for p(t) time axis
	ttp = arange(ixpL,ixpR)	        # Time axis for p(t)
	pt = zeros(len(ttp))		# Initialize pulse p(t)
	max_ttp = max(ttp)
	if (ptype=='rect'):		# Rectangular p(t)
		pt = ones(len(ttp))
	elif (ptype == 'tri'):
		pt = array([(1+i/max_ttp) if i/max_ttp+1 < 1.0 else (1-i/max_ttp) for i in list(ttp)])
	elif (ptype=='sinc'):
		k=pparms[0]
		kL = -1.0*k; kR = -kL
		ixpL = ceil(sps*kL)		# Left index for p(t) time axis
		ixpR = ceil(sps*kR)		# Right index for p(t) time axis
		ttp = arange(ixpL,ixpR)	 # Time axis for p(t)
		pt = zeros(len(ttp))
		beta=pparms[1]
		pt = array([sin(pi*t/max_ttp)/(pi*t/max_ttp) if t!= 0  else  1.0 for t in list(ttp)])
		pt=pt*kaiser(len(pt), beta)
	elif (ptype=='man'):
		ix = where(logical_and(ttp>=kL, ttp<kR))[0]
		pt[ix] = hstack((ones(int(len(ix)/2))-2, ones(len(pt)-int(len(pt)/2))))
	elif (ptype=='rcf'):
		k=pparms[0]
		alpha=pparms[1]
		kL = kL*k; kR = -kL
		ixpL = ceil(sps*kL)		# Left index for p(t) time axis
		ixpR = ceil(sps*kR)		# Right index for p(t) time axis
		ttp = arange(ixpL,ixpR)	        # Time axis for p(t)
		pt = zeros(len(ttp))
		pt=[(sin(pi*t/max_ttp)/(pi*t/max_ttp))*(cos(pi*alpha*t/max_ttp)/(1-pow(2*alpha*t/max_ttp,2))) \
		if t!= 0 and (1-pow(2*alpha*t/max_ttp,2))!=0  else  1.0 for t in list(ttp)]
	else:
		print("ptype '%s' is not recognized" % ptype)
	
	# ***** Filter with h(t) = p(t) *****
	st = convolve(ast,pt)/float(Fs)     # s(t) = a_s(t)*p(t)
	st = st[-ixpL:ixR-ixL-ixpL]     	# Trim after convolution
	return tt, st
