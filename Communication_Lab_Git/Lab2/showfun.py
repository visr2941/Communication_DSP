# File: showfun.py
# "show" functions like showft, showpsd, etc
from pylab import *
def showft(tt, xt, ff_lim):
	"""
	Plot (DFT/FFT approximation to) Fourier transform of x(t)
	Displays magnitude |X(f)| either linear and absolute or
	normalized (wrt to maximum value) in dB. Phase of X(f) is
    	shown in degrees.
    	>>>>> showft(tt, xt, ff_lim) <<<<<
    	where tt:time axis (increments Ts=1/Fs) for x(t)
            xt:sampled CT signal x(t))
            ff_lim = [f1,f2,llim]
            f1:lower frequency limit for display
            f2:upper frequency limit for display
            llim = 0: display |X(f)| linear and absolute
            llim > 0: same as llim = 0 but phase is masked
                      (set to zero) for |X(f)| < llim
            llim < 0: display 20*log_{10}(|X(f)|/max(|X(f)|))
                      in dB with lower display limit llim dB,
                      phase is masked (set to zero) for f
                      with magnitude (dB, normalized) < llim
    	"""
	# ***** Prepare x(t), swap pos/neg parts of time axis *****
	n = len(tt)
	fs = int((n-1)/float(tt[-1]-tt[0])) 	# Sampling rate
	ixp = where(tt>=0)[0]			# Indexes for t>=0
	ixn = where(tt<0)[0]			# Indexes for t<0
	tlen = tt[-1]	
	xt = hstack((xt[ixp],xt[ixn])) 		# Swap pos/neg time axis parts
	llim = ff_lim[2]

	
	
	# ***** Compute X(f), make frequency axis *****
	Xf = fft(xt)/float(fs)			# DFT/FFT of x(t),
    
	# scaled for X(f) approximation
	ff = fs*arange(n)/float(n) 		# Frequency axisi
	if ff_lim[0] < 0:
		ixp = where(ff < fs/2)[0]
		ixn = where(ff >= fs/2)[0]
		ff = hstack((ff[ixn]-fs,ff[ixp]))
		Xf = hstack((Xf[ixn],Xf[ixp]))

	# ***** Compute |X(f)|, arg[X(f)] *****
	absXf = abs(Xf)				# Magnitude |X(f)|
	argXf = angle(Xf)			# Phase arg[X(f)]
	
	if llim < 0:
		absXf = 20*log10((absXf)/max(absXf))
		ix = where(absXf < ff_lim[2])[0]
		argXf[ix] = zeros(len(ix))
		absXf[ix] = ff_lim[2]*ones(len(ix))
	else:
		ix = where(absXf < ff_lim[2])[0]
		argXf[ix]=zeros(len(ix))
        
	ix = where(logical_and(ff>= ff_lim[0], ff < ff_lim[1]))[0]
	ff = ff[ix]
	absXf=absXf[ix]
	argXf=argXf[ix]

	# ***** Plot magnitude/phase *****
	f1 = figure()
	af11 = f1.add_subplot(211)
	af11.plot(ff,absXf)
	af11.grid()
	if llim >= 0:
		af11.set_ylabel('|X(f)|')
	else:
		af11.set_ylabel('|X(f)| in dB')
	strgt = 'FT Approximation, $F_s=$' + str(fs) + ' Hz'
	strgt = strgt + ', N=' + str(n)
	strgt = strgt + ', $\Delta_f$={0:3.2f}'.format(fs/float(n)) + ' Hz'
	af11.set_title(strgt)
	af12 = f1.add_subplot(212)
	af12.plot(ff,180/pi*argXf) 		# Plot phase in degrees
	af12.grid()
	af12.set_ylabel('arg[X(f)] [deg]')
	af12.set_xlabel('f [Hz]')
	show()
