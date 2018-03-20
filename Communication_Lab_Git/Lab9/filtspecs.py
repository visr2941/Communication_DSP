from numpy import *
from scipy.signal import butter
def trapfilt_taps(N, phil, alfa):
    """
    Returns taps for order N FIR LPF with trapezoidal frequency
    response, normalized cutoff frequency phiL = fL/Fs, and rolloff
    parameter alfa.
    >>>>> hLn = trapfilt_taps(N, phiL, alfa) <<<<<
    where N: filter order
    phiL: normalized cutoff frequency (-6 dB)
    alfa: frequency rolloff parameter, linear rolloff
    over range (1-alfa)phiL <= |f| <= (1+alfa)phiL
    """

    tt = arange(-N/2,N/2 + 1)                                    # Time axis for h(t)    
    # ***** Generate impulse response ht here *****
    ht = zeros(len(tt))
    ix = where(tt != 0)[0]
    if alfa != 0:
        ht[ix] = ((sin(2*pi*phil*tt[ix]))/(pi*tt[ix]))*((sin(2*pi*alfa*phil*tt[ix]))/(2*pi*alfa*phil*tt[ix]))
    else:
        ht[ix] = (sin(2*pi*phil*tt[ix]))/(phil*pi*tt[ix])
    ix0 = where(tt == 0)[0]
    ht[ix0] = 2*phil

    return ht
