# File: keyfun.py
# Functions for amplitude/frequency/phase shift keying
# ASK, FSK, PSK and hybrid APSK
from pylab import *
import pamfun
def askxmtr(anthcn,FB,Fs,ptype,pparms,xtype,fcparms):
    """
    Amplitude Shift Keying (ASK) Transmitter for
    Choherent ('coh') and Non-coherent ('noncoh') ASK Signals
    >>>>> tt,xt,st = askxmtr(anthcn,FB,Fs,ptype,pparms,xtype,fcparms) <<<<<
    where tt:time axis for x(t), starts at t=-TB/2
    xt:transmitted ASK signal, sampling rate Fs
    x(t) = s(t)*cos(2*pi*fc*t+(pi/180)*thetac)
    tt:time axis for x(t), starts at t=-TB/2
    st:baseband PAM signal s(t) for 'coh'
    st = sit + 1j*sqt for 'noncoh'
    sit:PAM signal of an*cos(pi/180*thetacn)
    sqt:PAM signal of an*sin(pi/180*thetacn)
    xtype:Transmitter type from list {'coh','noncoh'}
    anthcn = [an]    for {'coh'}
    anthcn = [[an],[thetacn]]  for {'noncoh'}
    an:N-symbol DT input sequence a_n, 0<=n<N
    thetacn: N-symbol DT sequence theta_c[n] in degrees,
    used instead of thetac for {'noncoh'} ASK
    FB:baud rate of a_n (and theta_c[n]), TB=1/FB
    Fs:sampling rate of x(t), s(t)
    ptype:pulse type from list ['man','rcf','rect','rrcf','sinc','tri']
    pparms = []  for {'man','rect','tri'}
    pparms = [k, alpha] for {'rcf','rrcf'}
    pparms = [k, beta]
    for {'sinc'}
    k:"tail" truncation parameter for {'rcf','rrcf','sinc'}
    (truncates at -k*TB and k*TB)
    alpha:Rolloff parameter for {'rcf','rrcf'}, 0<=alpha<=1
    beta:Kaiser window parameter for {'sinc'}
    fcparms = [fc, thetac] for {'coh'}
    fcparms = [fc] for {'noncoh'}
    fc:carrier frequency in Hz
    thetac: carrier phase in deg (0: cos, -90: sin)
    """
    xtype = xtype.lower()
    ptype = ptype.lower()
    if xtype == 'coh':
        an = anthcn
        fc=fcparms[0]
        tt, st = pamfun.pam12(an, FB, Fs, ptype, pparms=[])
        st[where(st<0)] = 0
        thetac = fcparms[1]
        xt = st*cos(2*pi*fc*tt + thetac)
    elif xtype == 'noncoh':
        an = anthcn[0]
        fc = fcparms
        thetacn = anthcn[1]
        tt, sit = pamfun.pam12(an*cos(thetacn), FB, Fs, ptype, pparms=[])
        tt, sqt = pamfun.pam12(an*sin(thetacn), FB, Fs, ptype, pparms=[])
        st = sit + 1j*sqt
        xt = real(st*exp(1j*2*pi*fc*tt))
    else:
        print("xtype is incorrect")
    
    return tt, xt, st


from pylab import *
import pamfun
def askrcvr(tt,rt,rtype,fcparms,FBparms,ptype,pparms):
    """
    Amplitude Shift Keying (ASK) Receiver for
    Coherent ('coh') and Non-coherent ('noncoh') ASK Signals
    >>>>> bn,bt,wt,ixn = askrcvr(tt,rt,rtype,fcparms,FBparms,ptype,pparms) <<<<<
    where bn:received DT sequence b[n]
    bt:received 'CT' PAM signal b(t)
    wt = wit + 1j*wqt
    wit:in-phase component of b(t)
    wqt:quadrature component of b(t)
    ixn:sampling time indexes for b(t)->b[n], w(t)->w[n]
    tt:time axis for r(t)
    rt:received (noisy) ASK signal r(t)
    rtype:receiver type from list ['coh','noncoh']
    fcparms = [fc, thetac] for {'coh'}
    fcparms = [fc] for {'noncoh'}
    fc:carrier frequency in Hz
    thetac:carrier phase in deg (0: cos, -90: sin)
    FBparms = [FB, dly]
    FB:baud rate of PAM signal, TB=1/FB
    dly:sampling delay for b(t)->b[n], fraction of TB
    sampling times are t=n*TB+t0 where t0=dly*TB
    ptype:pulse type from list ['man','rcf','rect','rrcf','sinc','tri']
    pparms = [] for 'man','rect','tri'
    pparms = [k, alpha] for {'rcf','rrcf'}
    pparms = [k, beta] for {'sinc'}
    k:"tail" truncation parameter for {'rcf','rrcf','sinc'}
    (truncates at -k*TB and k*TB)
    alpha:Rolloff parameter for {'rcf','rrcf'}, 0<=alpha<=1
    beta:Kaiser window parameter for {'sinc'}
    """
    ptype = ptype.lower()
    rtype = rtype.lower()
    Fs = int(len(tt)/(tt[-1]-tt[0]))
    FBparms = FBparms
    pparms = pparms
    if rtype == 'coh':
        fc=fcparms[0]
        thetac = fcparms[1]
        rt = 2*rt*cos(2*pi*fc*tt + thetac)
        bn, bt, ixn = pamfun.pamrcvr10(tt, rt, FBparms, ptype, pparms)
        wt = bt
        bn[where(bn>0.0001)] = 1
        bn[where(bn<=0.0001)] = 0
    elif rtype == 'noncoh':
        an = anthcn[0]
        fc = fcparms
        thetacn = anthcn[1]
        vt = 2*rt*exp(-1j*2*pi*fc*tt)
        bni, wit, ixni, = pamfun.pamrcvr10(tt, real(vt), FBparms, ptype, pparms)
        bnq, wqt, ixnq, = pamfun.pamrcvr10(tt, imag(vt), FBparms, ptype, pparms)
        bt = (wit**2 + wqt**2)**0.5
        N = ceil(FBparms[0]*(tt[-1]-tt[0]))
        ixn = array(around((arange(N)+0.5+FBparms[1])*Fs/FBparms[0]),int)
        bn = bt[ixn]
        bn[where(bn>0.01)] = 1
        bn[where(bn<=0.01)] = 0
        wt = wit + 1j*wqt
    else:
        print("xtype is incorrect")
    bn = array(bn,int8)
    return bn, bt, wt, ixn
