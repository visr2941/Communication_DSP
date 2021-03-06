# writefile pam11.py
# File: pam11.py
# Functions for pulse amplitude modulation (PAM)
from pylab import *
def pam12(an, FB, Fs, ptype, pparms=[]):
    """
    Pulse amplitude modulation: a_n -> s(t), -TB/2<=t<(N-1/2)*TB,
    V1.0 for 'rect', 'sinc', and 'tri' pulse types.
    tt, st = pam10(an, FB, Fs, ptype, pparms)
    where an:
    N-symbol DT input sequence a_n, 0 <= n < N
    FB:
    Baud rate of a_n, TB=1/FB
    Fs:
    sampling rate of s(t)
    ptype: pulse type ('rect','sinc','tri')
    pparms not used for 'rect','tri'
    pparms = [k, beta] for 'sinc'
    pparms = [k, beta] for 'rcf'
    k: "tail" truncation parameter for 'sinc' and 'rcf'
    (truncates p(t) to -k*TB <= t < k*TB)
    beta: Kaiser window parameter for 'sinc'
    tt:
    time axis for s(t), starts at -TB/2
    st:
    CT output signal s(t), -TB/2<=t<(N-1/2)*TB,
    with sampling rate Fs
    """ 
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
    ptype = ptype.lower()    # Convert ptype to lowercase
    
    # Set left/right limits for p(t)
    if (ptype=='rect' or ptype=='man'):
        kL = -0.5; kR = -kL
    else:
        kL = -1.0; kR = -kL
    
    # Default left/right limits
    ixpL = ceil(Fs*kL*TB)    	# Left index for p(t) time axis
    ixpR = ceil(Fs*kR*TB)    	# Right index for p(t) time axis
    ttp = arange(ixpL,ixpR)/float(Fs)     # Time axis for p(t)
    pt = zeros(len(ttp))    	# Initialize pulse p(t)
    if (ptype=='rect'):    	# Rectangular p(t)
        ix = where(logical_and(ttp>=kL*TB, ttp<kR*TB))[0]
        pt[ix] = ones(len(ix))
    elif (ptype == 'tri'):
        pt = array([(1+i*1/TB) if i*1/TB+1 < 1.0 else (1-i*1/TB) for i in list(ttp)])
    elif (ptype=='sinc'):
        k=pparms[0]
        kL = kL*k; kR = -kL
        ixpL = ceil(Fs*kL*TB)		# Left index for p(t) time axis
        ixpR = ceil(Fs*kR*TB)		# Right index for p(t) time axis
        ttp = arange(ixpL,ixpR)/float(Fs)	 # Time axis for p(t)
        pt = zeros(len(ttp))
        beta=pparms[1]
        pt = array([sin(pi*t/TB)/(pi*t/TB) if t!= 0  else  1.0 for t in list(ttp)])
        pt=pt*kaiser(len(pt), beta)
    elif (ptype=='man'):
        ix = where(logical_and(ttp>=kL*TB, ttp<kR*TB))[0]
        pt[ix] = hstack((ones(int(len(ix)/2))-2, ones(len(pt)-int(len(pt)/2))))
    elif (ptype=='rcf'):
        k=pparms[0]
        alpha=pparms[1]
        kL = kL*k; kR = -kL
        ixpL = ceil(Fs*kL*TB)		# Left index for p(t) time axis
        ixpR = ceil(Fs*kR*TB)		# Right index for p(t) time axis
        ttp = arange(ixpL,ixpR)/float(Fs)	 # Time axis for p(t)
        pt = zeros(len(ttp))
        ix0= where(ttp==0)[0]
        pt[ix0] = array([1.0])
        if alpha != 0:
            ix0 = where(ttp==TB/(2*alpha))[0]
            pt[ix0] = array([0])
            ix0 = where(ttp==-TB/(2*alpha))[0]
            pt[ix0] = array([0])
            ix_rest = where(logical_and(logical_and(ttp!=0, ttp != TB/(2*alpha)), ttp != -TB/(2*alpha) ))[0]
            ttp = ttp[ix_rest]
        else:
            ix0 = where(ttp==0)[0]
            pt[ix0] = 1
            ix_rest =  where(ttp!=0)[0]
            ttp = ttp[ix_rest]
        pt[ix_rest] = (sin(pi*ttp/TB)/(pi*ttp/TB))*(cos(pi*alpha*ttp/TB)/(1-np.power(2*alpha*ttp/TB,2))) 
    elif ptype=='rrcf':
        k=pparms[0]
        alpha=pparms[1]
        kL = kL*k; kR = -kL
        ixpL = ceil(Fs*kL*TB)		# Left index for p(t) time axis
        ixpR = ceil(Fs*kR*TB)		# Right index for p(t) time axis
        ttp = arange(ixpL,ixpR)/float(Fs)	 # Time axis for p(t)
        pt = zeros(len(ttp))
        ix0= where(ttp==0)[0]
        pt[ix0] = 1 - alpha +(4*alpha/pi)
        ix0 = where(logical_or(ttp== -TB/(4*alpha), ttp==TB/(4*alpha)))[0]
        pt[ix0] = (alpha/2**0.5)*(((1+2/pi)*sin(pi/(4*alpha))) + ((1-2/pi)*cos(pi/(4*alpha))))
        ix0 = where(logical_and(logical_and(ttp != 0, ttp != TB/(4*alpha)),ttp != -TB/(4*alpha)))[0]
        t=ttp[ix0]
        p = pi*t/TB
        a = alpha*t/TB
        pt[ix0]= TB*(sin((1-alpha)*p) + 4*a*cos((1+alpha)*p))/(pi*t*(1-(4*a)**2))
    else:
        print("ptype '%s' is not recognized" % ptype)
    
    # ***** Filter with h(t) = p(t) *****
    
    st = convolve(ast,pt)/float(Fs)     # s(t) = a_s(t)*p(t)
    st = st[-int(ixpL):int(ixR-ixL-ixpL)]     	# Trim after convolution
    return tt, st

def pamrcvr10(tt, rt, FBparms, ptype, pparms=[]):
    """
    Pulse amplitude modulation receiver with matched filter:
    r(t) -> b(t) -> bn.
    V1.0 for 'man', 'rcf', 'rect', 'rrcf', 'sinc', and 'tri'
    pulse types.
    >>>>> bn, bt, ixn = pamrcvr10(tt, rt, FBparms, ptype, pparms) <<<<<
    where tt: time axis for r(t)
    rt: received (noisy) PAM signal r(t)
    FBparms: = [FB, dly]
    FB: Baud rate of PAM signal, TB=1/FB
    dly: sampling delay for b(t) -> b_n as a fraction of TB
    sampling times are t=n*TB+t0 where t0 = dly*TB
    ptype: pulse type from list ('man','rcf','rect','rrcf','sinc','tri')
    pparms not used for 'man','rect','tri'
    pparms = [k, alpha] for 'rcf','rrcf'
    pparms = [k, beta] for 'sinc'
    k: "tail" truncation parameter for 'rcf','rrcf','sinc'
    (truncates p(t) to -k*TB <= t < k*TB)
    alpha: rolloff parameter for ('rcf','rrcf'), 0<=alpha<=1
    beta: Kaiser window parameter for 'sinc'
    bn: received DT sequence after sampling at t=n*TB+t0
    bt: received PAM signal b(t) at output of matched filter
    ixn: indexes where b(t) is sampled to obtain b_n
    """
    
    FB = FBparms[0]
    t0 = FBparms[1]
    Fs = (len(tt)-1)/(tt[-1]-tt[0])

    # ***** Set up matched filter response h_R(t) *****
    TB = 1/float(FB)                                            # Time per symbol
    ptype = ptype.lower()                                       # Convert ptype to lowercase
     
    # Set left/right limits for p(t)
    
    if (ptype=='rect' or ptype=='man'):                                         # Rectangular or Manchester p(t)
        kL = -0.5; kR = -kL
    else:
        kL = -1.0; kR = -kL                                     # Default left/right limits
    
    ixpL = ceil(Fs*kL*TB)                                       # Left index for p(t) time axis
    ixpR = ceil(Fs*kR*TB)                                       # Right index for p(t) time axis
    ttp = arange(ixpL,ixpR)/float(Fs)                           # Time axis for p(t)
    pt = zeros(len(ttp))                                        # Initialize pulse p(t)
    if (ptype=='rect'):                                         # Rectangular p(t)
        ix = where(logical_and(ttp>=kL*TB, ttp<kR*TB))[0]
        pt[ix] = ones(len(ix))
    elif (ptype == 'tri'):
        pt = array([(1+i*1/TB) if i*1/TB+1 < 1.0 else (1-i*1/TB) for i in list(ttp)])
    elif (ptype=='sinc'):
        k=pparms[0]
        kL = kL*k; kR = -kL
        ixpL = ceil(Fs*kL*TB)		# Left index for p(t) time axis
        ixpR = ceil(Fs*kR*TB)		# Right index for p(t) time axis
        ttp = arange(ixpL,ixpR)/float(Fs)	 # Time axis for p(t)
        pt = zeros(len(ttp))
        beta=pparms[1]
        pt = array([sin(pi*t/TB)/(pi*t/TB) if t!= 0  else  1.0 for t in list(ttp)])
        pt=pt*kaiser(len(pt), beta)
    elif (ptype=='man'):
        ix = where(logical_and(ttp>=kL*TB, ttp<kR*TB))[0]
        pt[ix] = hstack((ones(int(len(ix)/2))-2, ones(len(pt)-int(len(pt)/2))))
    elif (ptype=='rcf'):
        k=pparms[0]
        alpha=pparms[1]
        kL = kL*k; kR = -kL
        ixpL = ceil(Fs*kL*TB)		# Left index for p(t) time axis
        ixpR = ceil(Fs*kR*TB)		# Right index for p(t) time axis
        ttp = arange(ixpL,ixpR)/float(Fs)	 # Time axis for p(t)
        pt = zeros(len(ttp))
        ix0= where(ttp==0)[0]
        pt[ix0] = array([1.0])
        if alpha != 0:
            ix0 = where(ttp==TB/(2*alpha))[0]
            pt[ix0] = array([0])
            ix0 = where(ttp==-TB/(2*alpha))[0]
            pt[ix0] = array([0])
            ix_rest = where(logical_and(logical_and(ttp!=0, ttp != TB/(2*alpha)), ttp != -TB/(2*alpha) ))[0]
            ttp = ttp[ix_rest]
        else:
            ix0 = where(ttp==0)[0]
            pt[ix0] = 1
            ix_rest =  where(ttp!=0)[0]
            ttp = ttp[ix_rest]
        pt[ix_rest] = (sin(pi*ttp/TB)/(pi*ttp/TB))*(cos(pi*alpha*ttp/TB)/(1-np.power(2*alpha*ttp/TB,2))) 
    elif ptype=='rrcf':
        k=pparms[0]
        alpha=pparms[1]
        kL = kL*k; kR = -kL
        ixpL = ceil(Fs*kL*TB)		# Left index for p(t) time axis
        ixpR = ceil(Fs*kR*TB)		# Right index for p(t) time axis
        ttp = arange(ixpL,ixpR)/float(Fs)	 # Time axis for p(t)
        pt = zeros(len(ttp))
        ix0= where(ttp==0)[0]
        pt[ix0] = 1 - alpha +(4*alpha/pi)
        ix0 = where(logical_or(ttp== -TB/(4*alpha), ttp==TB/(4*alpha)))[0]
        pt[ix0] = (alpha/2**0.5)*(((1+2/pi)*sin(pi/(4*alpha))) + ((1-2/pi)*cos(pi/(4*alpha))))
        ix0 = where(logical_and(logical_and(ttp != 0, ttp != TB/(4*alpha)),ttp != -TB/(4*alpha)))[0]
        t=ttp[ix0]
        p = pi*t/TB
        a = alpha*t/TB
        pt[ix0]= TB*(sin((1-alpha)*p) + 4*a*cos((1+alpha)*p))/(pi*t*(1-(4*a)**2))
    else:
        print("ptype '%s' is not recognized" % ptype)
    hRt = pt[::-1]                                              # h_R(t) = p(-t)
    hRt = Fs/sum(np.power(pt,2.0))*hRt                          # h_R(t) normalized
    
    # ***** Filter r(t) with matched filter h_R(t)
    bt = convolve(rt,hRt)/float(Fs)                             # Matched filter b(t)=r(t)*h_R(t)
    bt = bt[-ixpL:len(tt)-ixpL]                                 # Trim b(t)
    
    # ***** Sample b(t) at t=n*TB+t0 to obtain b_n *****
    N = ceil(FB*(tt[-1]-tt[0]))                                 # Number of symbols
    ixn = array(around((arange(N)+0.5+t0)*Fs/FB),int)           # Sampling indexes
    ix = where(logical_and(ixn>=0,ixn<len(tt)))[0]
    ixn = ixn[ix]                                               # Trim to existing indexes
    bn = bt[ixn]                                                # DT sequence sampled at t=n*TB+t0
    
    return bn, bt, ixn
