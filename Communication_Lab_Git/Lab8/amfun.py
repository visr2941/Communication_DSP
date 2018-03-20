from filtfun import *
from showfun import *
def amxmtr(tt, mt, xtype, fcparms, fmparms=[], fBparms=[]):
    """
    Amplitude Modulation Transmitter for suppressed ('sc')
    and transmitted ('tc') carrier AM
    >>>>> xt = amxmtr(tt, mt, xtype, fcparms, fmparms, fBparms) <<<<<
    where xt: transmitted AM signal
    tt: time axis for m(t), x(t)
    mt: modulating (wideband) message signal
    xtype: 'sc' or 'tc' (suppressed or transmitted carrier)
    fcparms = [fc, thetac] for 'sc'
    fcparms = [fc, thetac, alpha] for 'tc'
    fc: carrier frequency
    thetac: carrier phase in deg (0: cos, -90: sin)
    alpha: modulation index 0 <= alpha <= 1
    fmparms = [fm, km, alpham] LPF at fm parameters
    no LPF at fm if fmparms = []
    fm: highest message frequency
    km: LPF h(t) truncation to |t| <= km/(2*fm)
    alpham: LPF at fm frequency rolloff parameter, linear
    rolloff over range 2*alpham*fm
    fBparms = [fBW, fcB, kB, alphaB] BPF at fcB parameters
    no BPF if fBparms = []
    fBW: -6 dB BW of BPF
    fcB: center freq of BPF
    kB: BPF h(t) truncation to |t| <= kB/fBW
    alphaB: BPF frequency rolloff parameter, linear
    rolloff over range alphaB*fBW
    """
    Fs = int(len(tt)/(tt[-1]-tt[0]))                                        # sampling frequency
    fm = fmparms[0]                                                         # the cutoff frequency for LPF
    k = fmparms[1]                                                          # the truncation parameter of LPF
    alfa = fmparms[2]                                                       # frequency roll-off parameter of LPF
    fc = fcparms[0]                                                         # carrier frequency
    theta = fcparms[1]                                                      # phase of the carrier signal
    fBW = [fm,0]
    mt,n = trapfilt(mt, Fs, fBW, k, alfa)                                   # message signal after filtering out with LPF
    if xtype.lower() == 'sc':
        xt = mt*cos(2*pi*fc*tt + theta)
    else:
        mi = fcparms[2]                                                         # modulation index
        xt = (1+mi*mt)*cos(2*pi*fc*tt + theta)
    return xt


def amrcvr(tt, rt, rtype, fcparms, fmparms, fBparms):
    """
    Amplitude Modulation Receiver for coherent ('coh') reception,
    or absolute value ('abs'), or squaring ('sqr') demodulation,
    or I-Q envelope ('iqabs') detection, or I-Q phase ('iqangle')
    detection.
    >>>>> mthat = amrcvr(tt, rt, rtype, fcparms, fmparms, fBparms) <<<<<
    where mthat: demodulated message signal
    tt: time axis for r(t), mhat(t)
    rt: received AM signal
    rtype: Receiver type from list
    'abs' (absolute value envelope detector),
    'coh' (coherent),
    'iqangle' (I-Q rcvr, angle or phase),
    'iqabs' (I-Q rcvr, absolute value or envelope),
    'sqr' (squaring envelope detector)
    fcparms = [fc, thetac]
    fc: carrier frequency
    thetac: carrier phase in deg (0: cos, -90: sin)
    fmparms = [fm, km, alpham]
    LPF at fm parameters no LPF at fm if fmparms = []
    fm: highest message frequency
    km: LPF h(t) truncation to |t| <= km/(2*fm)
    alpham: LPF at fm frequency rolloff parameter, linear
    rolloff over range 2*alpham*fm
    fBparms = [fBW, fcB, kB, alphaB] BPF at fcB parameters
    no BPF if fBparms = []
    fBW: -6 dB BW of BPF
    fcB: center freq of BPF
    kB: BPF h(t) truncation to |t| <= kB/fBW
    alphaB: BPF frequency rolloff parameter, linear
    rolloff over range alphaB*fBW
    """
    Fs = int(len(tt)/(tt[-1]-tt[0]))                                        # sampling frequency
    fm = fmparms[0]                                                         # the cutoff frequency for LPF
    k = fmparms[1]                                                          # the truncation parameter of LPF
    alfa = fmparms[2]                                                       # frequency roll-off parameter of LPF
    fc = fcparms[0]                                                         # carrier frequency
    theta = fcparms[1]                                                      # phase of the carrier signal
    fBW = [fm,0]
    if rtype.lower() == 'coh' :
        vt = 2*rt*cos(2*pi*fc*tt + theta)
        mthat,n = trapfilt(vt, Fs, fBW, k, alfa)
    elif rtype.lower() == 'abs':
        vt = abs(rt)
        pt,n = trapfilt(vt, Fs, fBW, k, alfa)
        mthat = pt - mean(pt)
    elif rtype.lower() == 'iqangle':
        vit = rt*2*cos(2*pi*fc*tt)
        wit = trapfilt(vit, Fs, fBW, k, alfa)
        vqt = -rt*2*sin(2*pi*fc*tt)
        wqt,n = trapfilt(vqt, Fs, fBW, k, alfa)
        mthat = arctan(wqt/wit)
    elif rtype.lower() == 'iqabs':
        vit = rt*2*cos(2*pi*fc*tt)
        wit,n = trapfilt(vit, Fs, fBW, k, alfa)
        vqt = -rt*2*sin(2*pi*fc*tt)
        wqt,n = trapfilt(vqt, Fs, fBW, k, alfa)
        mthat = pow((pow(wit,2) + pow(wqt,2)), 0.5)
    elif rtype.lower() == 'sqr':
        vt = pow(rt,2)
        wt,n = trapfilt(vt, Fs, fBW, k, alfa)
        pt = pow(wt,2)
        mthat = pt - mean(pt)
    else:
        print("rtype is not valid")

    return mthat


def qamrcvr(tt, rt, fcparms, fmparms=[]):
    """
    Quadrature Amplitude Modulation (QAM) Receiver with
    complex-valued input/output signals
    >>>>> mthat = qamrcvr(tt, rt, fcparms, fmparms) <<<<<
    where mthat: complex-valued demodulated message signal
    tt:time axis for r(t), mhat(t)
    rt:received QAM signal (real- or complex-valued)
    fcparms = [fc thetac]
    fc:carrier frequency
    thetac: carrier phase in deg
    fmparms = [fm, km, alpham]
    for LPF at fm parameters
    fm:highest message frequency (-6 dB)
    fmparms = [fBW, fBc, km, alpham]
    for BPF at fm parameters
    fBW:BPF -6 dB bandwidth in Hz
    fBc:BPF center frequency (pos/neg) in Hz
    no LPF at fm if fmparms = []
    km:h(t) is truncated to
    |t| <= km/(2*fm) for LPF
    |t| <= km/fBW for BPF
    alpham: frequency rolloff parameter, linear
    rolloff over range
    (1-alpham)*fm <= |f| <= (1+alpham)*fm for LPF
    (1-alpham)*fBW/2 <= |f| <= (1+alpha)*fBW/2 for BPF
    """
    fc, theta = fcparms[0],fcparms[1]
    fBW,fbc, k, alfa = fmparms[0],fmparms[1],fmparms[2],fmparms[3]
    Fs = int(len(tt)/(tt[-1]-tt[0]))
    xut = rt * exp(-1j*(2*pi*fc*tt + theta))
    fparms = [fBW,fbc]
    xt = trapfilt_cc(xut, Fs, fparms, k, alfa)[0]
    return xt

def qamxmtr(tt, mt, fcparms, fmparms):
    """
    Quadrature Amplitude Modulation (QAM) Transmitter with
    complex-valued input/output signals
    >>>>> xt = qamxmtr(tt, mt, fcparms, fmparms) <<<<<
    where xt:complex-valued QAM signal
    tt:time axis for m(t), x(t)
    mt:complex-valued (wideband) message signal
    fcparms = [fc, thetac]
    fc:carrier frequency
    thetac: carrier phase in deg
    fmparms = [fm, km, alpham] for LPF at fm parameters
    fm:highest message frequency (-6dB)
    fmparms = [fBW, fBc, km, alpham] for BPF at fm parameters
    fBW:BPF -6dB bandwidth in Hz
    fBc:BPF center frequency (pos/neg) in Hz
    no LPF/BPF at fm if fmparms = []
    km:h(t) is truncated to
    |t| <= km/(2*fm) for LPF
    |t| <= km/fBW for BPF
    alpham: frequency rolloff parameter, linear
    rolloff over range
    (1-alpham)*fm <= |f| <= (1+alpham)*fm for LPF
    (1-alpham)*fBW/2 <= |f| <= (1+alpha)*fBW/2 for BPF
    """
    fc, theta = fcparms[0],fcparms[1]
    fBW,fbc, k, alfa = fmparms[0],fmparms[1],fmparms[2],fmparms[3]
    Fs = int(len(tt)/(tt[-1]-tt[0]))
    xut = mt * exp(1j*(2*pi*fc*tt+theta))
    fparms = [fBW,fbc]
    xt = trapfilt_cc(xut, Fs, fparms, k, alfa)[0]
    return xt