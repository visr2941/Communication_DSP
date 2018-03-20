# Module for filter functions
from pylab import *
from scipy.signal import butter, lfilter
def trapfilt(xt, Fs, fL, k, alfa):
    """
    Delay compensated FIR LPF with trapezoidal frequency response.
    >>>>> yt, n = trapfilt(xt, Fs, fL, k, alfa) <<<<<
    where yt: filter output y(t), sampling rate Fs
    n:  filter order
    xt: filter input x(t), sampling rate Fs
    Fs: sampling rate of x(t), y(t)
    fL: cutoff frequency (-6 dB) in Hz
    k:  h(t) is truncated to |t| <= k/(2fL)
    alfa: frequency rolloff parameter, linear rolloff
    over range (1-alfa)fL <= |f| <= (1+alfa)fL
    """
    ixk = round(Fs*k/float(2*fL))                                # Tail cutoff index
    tt = arange(-ixk,ixk+1)/float(Fs)                            # Time axis for h(t)
    n = len(tt)-1                                                # Filter order
    
    # ***** Generate impulse response ht here *****
    ht = zeros(len(tt))                                          # Initializing ht
    ix = where(tt != 0)[0]
    if alfa != 0:
        ht[ix] = ((sin(2*pi*fL*tt[ix]))/(pi*tt[ix]))*((sin(2*pi*alfa*fL*tt[ix]))/(2*pi*alfa*fL*tt[ix]))
    else:
        ht[ix] = (sin(2*pi*fL*tt[ix]))/(pi*tt[ix])
    ix0 = where(tt == 0)[0]
    ht[ix0] = 2*fL
    yt = lfilter(ht, 1, hstack((xt, zeros(ixk))))/float(Fs)      # Compute filter output y(t)
    yt = yt[ixk:]                                                # Filter delay compensation
    return yt, n                                                 # Return y(t) and filter order
