# Module for filter functions
from pylab import *
from scipy.signal import butter, lfilter
def trapfilt(xt, Fs, fBW, k, alfa):
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
    fL = fBW[0]
    fc = fBW[-1]
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
    if fc != 0:
        ht = 2*ht*cos(2*pi*fc*tt)
    yt = lfilter(ht, 1, hstack((xt, zeros(ixk))))/float(Fs)      # Compute filter output y(t)
    yt = yt[ixk:]                                                # Filter delay compensation
    return yt, n                                                 # Return y(t) and filter order


def trapfilt_cc(xt, Fs, fparms, k, alfa):
    """
    Delay compensated FIR LPF/BPF filter with trapezoidal
    frequency response, complex-valued input/output and
    complex-valued filter coefficients.
    >>>>> yt, n = trapfilt_cc(xt, Fs, fparms, k, alfa) <<<<<
    where yt:complex filter output y(t), sampling rate Fs
    n:filter order
    xt:complex filter input x(t), sampling rate Fs
    Fs:sampling rate of x(t), y(t)
    fparms = fL for LPF
    fL:LPF cutoff frequency (-6 dB) in Hz
    fparms = [fBW, fBc] for BPF
    fBW: BPF -6dB bandwidth in Hz
    fBc: BPF center frequency (pos/neg) in Hz
    k:h(t) is truncated to
    |t| <= k/(2*fL) for LPF
    |t| <= k/fBW for BPF
    alfa: frequency rolloff parameter, linear
    rolloff over range
    (1-alfa)*fL <= |f| <= (1+alfa)*fL for LPF
    (1-alfa)*fBW/2 <= |f| <= (1+alfa)*fBW/2 for BPF
    """
    fL = fparms[0]
    fc = fparms[-1]
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
    if fc != 0:
        ht = 2*ht*exp(1j*2*pi*fc*tt)
    yt = lfilter(ht, 1, hstack((xt, zeros(ixk))))/float(Fs)      # Compute filter output y(t)
    yt = yt[ixk:]                                                # Filter delay compensation
    return yt, n                                                 # Return y(t) and filter order
